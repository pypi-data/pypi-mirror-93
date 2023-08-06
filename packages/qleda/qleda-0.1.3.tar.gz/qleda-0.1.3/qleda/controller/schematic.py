from typing import Optional, Union, List, NamedTuple, Callable, Iterable, Tuple
from abc import ABC
from pathlib import Path
from inspect import getfile
from sqlalchemy.orm.session import Session
from sqlalchemy.engine import Engine

from ..model.basic import Schematic, PartLibrary, Part, SignalPath, NetPath
from ..core.dbsetup import init_db
from ..constants import DIR_DATA, DIR_SCHEMATIC, DIR_LIBRARIES, DIR_JSON_DUMPS
from ..pypads.importer import import_pads_netlist, import_pads_part_lib, import_pads_symbol_lib
from ..validation.decorators import check_clean_session

from .queries import query_missing_part_attributes, update_schematic_pins_from_libraries, insert_diff_net_by_query,\
    schematic_build_nets_diff_pairs_from_net_names, query_signal_paths, NSerieParts


class SupportedFiles(NamedTuple):
    description: str
    loader: Callable
    updater: Optional[Callable]
    additional_loader_args: tuple
    additional_updater_args: tuple


FILE_SUFFIXES = {
    '.asc': 'PADS Logic Netlist export',
    '.p': 'Menthor Graphics PADS Part Library',
    '.c': 'Menthor Graphics PADS Logic Symbol Library'
}


class ProcessingWarnings(NamedTuple):
    process_name: str
    warnings: List[str]


class SchematicController(ABC):
    """
        A controller controls the building/validation process of a schematic or an output.
        Every step requires some input, either a file a db state or some previous steps.
        The controller handles this dependencies.
    """
    # interal attributes
    _libraries_path: List[Path]
    _schematic_path: Path
    _engine: Engine
    _session: Session
    _json_dump: bool

    _main_schematic: Optional[Schematic]
    _assembly_schematics: List[Schematic]
    _part_library: Optional[PartLibrary]

    _warnings: List[ProcessingWarnings]

    @classmethod
    def setup_directories(cls):
        cls.build_schematic_base_dir()
        cls.build_libraries_base_dir()

    @classmethod
    def get_project_root(cls) -> Path:
        return Path(getfile(cls)).parent

    @classmethod
    def get_db_base_dir(cls) -> Path:
        return cls.get_project_root() / DIR_DATA

    @classmethod
    def build_db_location(cls, name: str) -> Path:
        p = cls.get_db_base_dir() / f'{name}.db'
        SchematicController._build_path(p.parent)
        return p

    @staticmethod
    def _build_path(p: Path):
        if not p.exists():
            p.mkdir(parents=True)
        return p

    @classmethod
    def build_schematic_base_dir(cls) -> Path:
        return SchematicController._build_path(cls.get_project_root() / DIR_DATA / DIR_SCHEMATIC)

    @classmethod
    def build_libraries_base_dir(cls) -> Path:
        return SchematicController._build_path(cls.get_project_root() / DIR_DATA / DIR_LIBRARIES)

    @classmethod
    def build_libraries_json_dump_dir(cls) -> Path:
        return SchematicController._build_path(cls.get_project_root() / DIR_DATA / DIR_JSON_DUMPS)

    @classmethod
    def clean_json_dumps(cls):
        for file in [f for f in cls.build_libraries_json_dump_dir().iterdir() if f.suffix == '.json']:
            file.unlink()

    @classmethod
    def clean_db_files(cls):
        for file in [f for f in cls.get_db_base_dir().iterdir() if f.suffix == '.db']:
            file.unlink()

    @classmethod
    def clean(self):
        """
        clean any output files that could have been created.
        :return:
        """
        self.clean_db_files()
        self.clean_json_dumps()

    def _setup_session(self, session: Optional[Session], schematic_name: str, in_memoy_db: bool, override_db: bool):
        """
         part of __init__ function. Created function to structure code.
        @param session:
        @param schematic_name:
        @param in_memoy_db:
        @param override_db:
        @return: engine, session
        """
        if session is None:
            if in_memoy_db:
                _engine, _session = init_db()
            else:
                db_path = False if in_memoy_db else self.build_db_location(schematic_name)
                _engine, _session = init_db(db_path, override=override_db)
        else:
            _session = session
            _engine = None
        return _engine, _session

    def supported_libraries(self) -> set:
        return {'.p', '.c'}

    def supported_schematics(self) -> set:
        return {'.asc'}

    def _setup_libraries_path(self, libraries: Optional[List[Union[str, Path]]]):
        if libraries is None:
            lib_dir = self.build_libraries_base_dir()
            possible_files = [f for f in lib_dir.iterdir() if f.is_file() and f.suffix in self.supported_libraries()]
            if len(possible_files) == 0:
                raise FileNotFoundError("Couldn't find a supported file in {}\n".format(lib_dir) +
                                        'The following schematic file types are supported: {}'.format(
                                            ' '.join(self.supported_libraries())))
            else:
                return possible_files
        elif isinstance(libraries, bool) and libraries is False:
            return []
        elif isinstance(libraries, list):
            lib_paths = []
            for lib in libraries:
                if isinstance(lib, str):
                    lib_paths.append(self.build_schematic_base_dir() / lib)
                elif isinstance(lib, Path):
                    lib_paths.append(lib)
                else:
                    raise TypeError(f'Unexpected type {type(lib)} for argument libraries')
            return lib_paths
        else:
            if isinstance(libraries, bool):
                raise ValueError(f'libraries = {libraries} is an illegal state')
            raise TypeError(f'Unexpected type {type(libraries)} for argument libraries')

    def _setup_schematic_path(self, schematic: Optional[Union[str, Path]]) -> Path:
        if isinstance(schematic, str):
            return self.build_schematic_base_dir() / schematic
        elif isinstance(schematic, Path):
            return schematic
        elif schematic is None:
            sch_dir = self.build_schematic_base_dir()
            possible_files = [f for f in sch_dir.iterdir() if f.is_file() and f.suffix in self.supported_schematics()]
            if len(possible_files) > 1:
                raise ValueError('There were several possible schematic files in {}\n'.format(sch_dir) +
                                 'Please specify one by the argument schematic_name')
            elif len(possible_files) == 0:
                raise FileNotFoundError("Couldn't find a supported file in {}\n".format(sch_dir) +
                                        'The following schematic file types are supported: {}'.format(
                                            ' '.join(self.supported_schematics())))
            else:   # len(possible_files) == 1
                return possible_files[0]
        else:
            raise TypeError(f'Unexpected type {type(schematic)} for argument schematic')

    def __init__(self, session: Optional[Session] = None, schematic: Optional[Union[str, Path]] = None,
                 libraries: Optional[Union[List[Union[str, Path]], bool]] = None, json_dump: bool = True,
                 in_memoy_db: bool = False, override_db: bool = False):
        """

        @param session: A Sqlalchemy Session object. If parameter is None, a new db is created. By default the db
                        is written to the file storage. Thi behaviour can be changed by the parameter in_memory_db
        @param schematic:  The name of the schematic that shall be processed.
                                If the schematic_name is a str obj the controller will look for the schematic
                                content in the following order:
                                    1. given session (if there is one).
                                    2. In the database with the same name given (if override db is on false)
                                    3. json dump folder
                                    4. schematic data files (at the time of writing PADS Netlist files)

                                If schematic_name is a Path Controller will do the same like above with the file's name
                                except for point 3. There it takes the path.
                                If

        @param libraries:   A list of library files. For each the same process as above is done.
                            if libraries has the bool value False, no libraries are loaded.
        @param json_dump:       True: Json dumps are created.
                                False: No Json dumps are created
        @param in_memory_db:    Only considered if session is None.
                                True: The new session is created in memory.
                                False: DB is written to the file storage
        @param override_db:     True: existing dbs are will be deleted.
                                False: controller will load the existing db (same name as schematic).

        """
        self._schematic_path = self._setup_schematic_path(schematic)
        self._libraries_path = self._setup_libraries_path(libraries)
        self._engine, self._session = self._setup_session(session, self._schematic_path.stem, in_memoy_db, override_db)
        self._json_dump = json_dump
        self._assembly_schematics = []
        self._warnings = []
        self._part_library = None
        self._main_schematic = None

    def load_libraries_if_needed(self):
        """
        checks if existing session already has a reasonable library. otherwise it loads it from file
        @return:
        """
        if self._part_library is None:
            if (n_lib := self._session.query(PartLibrary).count()) > 1:
                self._part_library = self._session.query(PartLibrary).filter(PartLibrary.name.in_(
                    [p.stem for p in self._libraries_path]
                )).one()
            elif n_lib == 1:
                self._part_library = self._session.query(PartLibrary).one()
            else:
                self.load_libraries_from_file()
            return
        else:
            if len(self._part_library.parts) < 1:
                raise ValueError('library loaded ')

    def load_schematic_if_needed(self):
        """
        checks if existing session already has a reasonable schematic. otherwise it loads it from file
        @return:
        """
        if self._main_schematic is None:
            if (n_schematic := self._session.query(Schematic).count()) > 1:
                self._main_schematic = self._session.query(Schematic).filter(Schematic.name == self._schematic_path.stem).one()
            elif n_schematic == 1:
                self._main_schematic = self._session.query(Schematic).one()
            else:
                self.load_schematic_from_file()
            return
        else:
            if len(self._part_library.parts) < 1:
                raise ValueError('library loaded ')

    def load_libraries_from_file(self):
        for lib in self._libraries_path:
            if lib.suffix == '.p':
                self._part_library = imported_lib = import_pads_part_lib(lib, from_schematic=False)
            elif lib.suffix == '.c':
                imported_lib = import_pads_symbol_lib(lib, from_schematic=False)
            else:
                raise TypeError('Unsupported File format {} for libraries'.format(lib.suffix))
            self._session.add(imported_lib)
            self._session.commit()

    def load_schematic_from_file(self):
        if self._schematic_path.suffix == '.asc':
            imported_schematic = import_pads_netlist(self._schematic_path)
        else:
            raise TypeError('Unsupported File format {} for libraries'.format(self._schematic_path.suffix))
        self._session.add(imported_schematic)
        self._session.commit()

    def read_data_files_if_needed(self):
        self.load_libraries_if_needed()
        self.load_schematic_if_needed()

    def schematic_add_missing_parts_attributes_from_library(self):
        session = self.clean_session
        schematic = self.main_schematic
        library = self.part_library

        #  [(part_name, prop_name),... ]
        missing_part_attributes = query_missing_part_attributes(self.clean_session, schematic.id, library.id)
        all_missing = missing_part_attributes.all()
        parts_to_update = [part for part in session.query(Part).filter(Part.schematic_id == schematic.id).filter(Part.name.in_( [
            r[0] for r in all_missing
        ])).all()]
        missing_attr_map = {part_name: [prop for pa, prop in all_missing if pa == part_name] for part_name in
                            set([x[0] for x in all_missing])}
        for part in parts_to_update:
            for attr in missing_attr_map[part.name]:
                if attr not in part.properties and attr in library.parts[part.name].properties:
                    part.properties[attr] = library.parts[part.name].properties[attr]
        session.commit()

    @property
    def clean_session(self):
        if self._session is None:
            raise ValueError
        else:
            return check_clean_session(self._session)

    @property
    def main_schematic(self) -> Schematic:
        if self._main_schematic is None:
            self._main_schematic = self.clean_session.query(Schematic)\
                .filter(Schematic.name == self._schematic_path.stem).one()
        return self._main_schematic

    @property
    def part_library(self):
        if self._part_library is None:
            library_name = self._libraries_path[0].stem if self._libraries_path and len(self._libraries_path) > 1 else None
            if library_name is None:
                libraries = self.clean_session.query(PartLibrary).all()
                if len(libraries) != 1:
                    raise ValueError('Found several libraries. Please specify name')
                self._part_library = libraries[0]
            else:
                self._part_library = self.clean_session.query(PartLibrary).filter(PartLibrary.name == library_name)
        return self._part_library

    def run(self):
        self.read_data_files_if_needed()
        self.combine_existing_data()
        self.build_diff_pairs_from_rules()

    def combine_existing_data(self):
        self.schematic_add_missing_parts_attributes_from_library()
        update_schematic_pins_from_libraries(self.clean_session, self.main_schematic.id, self.part_library.id)

    def build_diff_pairs_from_rules(self):
        insert_diff_net_by_query(self.clean_session,
                                 schematic_build_nets_diff_pairs_from_net_names(self.clean_session,
                                                                                self.main_schematic.id))


def create_signal_paths_direct_connected(session: Session, schematic_id: int, start_designator: str,
                                         end_designators: Iterable[str]) -> Tuple[List[SignalPath], Iterable[int]]:
    """

    @param session:
    @param schematic_id:
    @param start_designator:
    @param end_designators:
    @return:
    """
    sig_paths = session.execute(
        query_signal_paths(session, schematic_id, start_designator, end_designators, NSerieParts.zero, 3))
    ret_paths = []
    net_ids = []
    for row in sig_paths:
        ret_paths.append(SignalPath(
            net_paths=[
                NetPath(row.s_pin_id, row.e_pin_id, name=row.s_net_name)
            ],
            name=row.s_net_name, ignore_validation=True))
        net_ids.append(row.s_net_id)
    return ret_paths, net_ids


def create_signal_paths_one_serial_part(session: Session, schematic_id: int, start_designator: str,
                                        end_designators: Iterable[str], illegal_net_ids: Optional[Iterable[int]] = None) -> List[SignalPath]:
    """

    @param session:
    @param schematic_id:
    @param start_designator:
    @param end_designators:
    @return:
    """
    sig_paths = session.execute(
        query_signal_paths(session, schematic_id, start_designator, end_designators, NSerieParts.one, 3,
                           illegal_net_ids))
    ret_paths = []
    for row in sig_paths:
        ret_paths.append(SignalPath(
            net_paths=[
                NetPath(row.s_pin_id, row.l_pin_id, name=row.s_net_name),
                NetPath(row.r_pin_id, row.e_pin_id, name=row.e_net_name),
            ],
            name=min([row.s_net_name, row.e_net_name], key=lambda x: len(x)),
            ignore_validation=True))
    return ret_paths
