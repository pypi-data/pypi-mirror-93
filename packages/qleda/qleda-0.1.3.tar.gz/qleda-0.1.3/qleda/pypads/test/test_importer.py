import unittest
from json import dump, load
from datetime import datetime

from cairo import SVGSurface

from ...drawing.cairoexport import export_container
from ...core.testing import DbTestCase, TestDataWriter, TestDataReader
from ...controller.library import build_schematic_instance
from ...model.schmodel import PinMatchingStrategy, PartSymbol
from ...model.basic import Schematic

from ..importer import read_pads_lib_elements, import_pads_symbol_lib, import_pads_part_lib, import_pads_netlist

ILLEGAL_BEGINNING = ('$OSR_BI_LEFT', '$OSR_BI_RIGHT', 'GND', 'VCC')


class TestNewImporter(TestDataReader, DbTestCase):

    def test_read_sch_decals(self):
        decals = read_pads_lib_elements(self.build_input_path('res.c'))

    def test_import_pads_symbol_lib(self):
        symbol_lib = import_pads_symbol_lib(self.build_input_path('res.c'))
        self.session.add(symbol_lib)
        self.session.commit()


class TestPartImport(TestDataReader, DbTestCase):

    def test_full_import(self):

        try:
            part_library = import_pads_part_lib(self.build_input_path('res.p'), False)
        except Exception:
            self.fail("Importing Library raised an exception")
        self.session.add(part_library)
        self.session.commit()


class TestController(TestDataWriter, TestDataReader, DbTestCase):

    def test_build_schematic_instance(self):
        symbol_lib = import_pads_symbol_lib(self.build_input_path('res.c'))
        part_library = import_pads_part_lib(self.build_input_path('res.p'), False)
        self.session.add_all([part_library, symbol_lib])
        self.session.commit()
        copies = [build_schematic_instance(self.session, part, True, PinMatchingStrategy.Position, symbol_lib)
                  for part in part_library.parts.values()]
        self.session.add_all(copies)
        self.session.commit()


class TestNetlistImport(TestDataWriter, TestDataReader, DbTestCase):

    _DEBUG = True

    def test_import_pads_netlist(self):

        try:
            # TODO upate to new netlist.sch
            schematic = import_pads_netlist(self.build_input_path('netlist.asc'))
            self.session.add(schematic)
            self.session.commit()
            test_d = schematic.to_dict(nested=True, full_depth=True)
            with(open(self.build_output_path('test_export.json'), 'w')) as f:
                dump(test_d, f, indent=2)

        except Exception:
            self.fail("test_import_net_list_ascii raised an exception")

        self.assertEqual(schematic.parts['R2'].properties['VALUE'].value, '1k2')
        self.assertEqual(schematic.parts['R3'].properties['VALUE'].value, '1k')

    def test_from_dict(self):

        start_read_json = datetime.now()
        with(open(self.build_input_path('test_export.json'), 'r')) as f:
            schematic_d = load(f)
        start_transform_dict = datetime.now()
        schematic = Schematic.from_dict(schematic_d)
        end_transform_dict = datetime.now()
        self.session.add(schematic)
        self.session.commit()
        end_commit = datetime.now()
        time_read_json = start_transform_dict-start_read_json
        time_transform_dict = end_transform_dict-start_transform_dict
        time_commit = end_commit-end_transform_dict
        print(f'time_read_json = {time_read_json}')
        print(f'time_transform_dict = {time_transform_dict}')
        print(f'time_commit = {time_commit}')


def _fill_empty_attrs_and_refdes(symbol: PartSymbol):
    attrs = [k for k in symbol.labels.keys() if k not in {'name', 'designator'}]
    symbol.labels['name'].visible = True
    symbol.labels['designator'].visible = True
    if not symbol.designator:
        symbol.designator = 'Refdes'
    for attr in attrs:
        symbol.labels[attr].visible = True
        symbol.labels[attr].value = attr


class MyTestCase(TestDataWriter, TestDataReader, DbTestCase):

    def test_export_res(self):
        symbol_lib = import_pads_symbol_lib(self.build_input_path('res.c'))
        self.session.add(symbol_lib)
        self.session.commit()

        for schematicdecal in [*symbol_lib.netconnectors, *symbol_lib.symbols]:
            if isinstance(schematicdecal, PartSymbol):
                _fill_empty_attrs_and_refdes(schematicdecal)
            export_container(SVGSurface, schematicdecal, self.build_output_path('{}.svg'
                                 .format(schematicdecal.name)))

if __name__ == '__main__':
    unittest.main()