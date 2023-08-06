from typing import Dict, Union, List, Optional, Iterable

from sqlalchemy import Column, Integer, UniqueConstraint, ForeignKey, String, CheckConstraint, Text,\
    Enum as SqlalchemyEnum, Boolean, distinct
from sqlalchemy.orm import relationship, Query
from sqlalchemy.orm.collections import attribute_mapped_collection, column_mapped_collection

from ..common.electrical import Polarity, SimulationType, PinType
from ..core.dbbase import Base
from ..core.mixins import DefaultReprMixin, SerializeMixin
from ..validation.decorators import check_clean_session


class DiffPins(SerializeMixin, DefaultReprMixin, Base):
    """
        A group for differential pins.
        p for the differential positive Pin
        n for the differential negative Pin
    """
    __tablename__ = "diff_pins"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    p_id = Column(Integer, ForeignKey('pin.id'), nullable=False)
    _p = relationship('Pin', foreign_keys=[p_id], back_populates='_diff_p')

    n_id = Column(Integer, ForeignKey('pin.id'), nullable=False)
    _n = relationship('Pin', foreign_keys=[n_id], back_populates='_diff_n')

    part_id = Column(Integer, ForeignKey('part.id'), nullable=False)
    _part = relationship('Part', back_populates='diff_pins')

    __table_args__ = (UniqueConstraint('name', 'part_id', name='unique_diffpins_name',),
                      UniqueConstraint('p_id', 'part_id', name='unique_diffpins_p_id',),
                      UniqueConstraint('n_id', 'part_id', name='unique_diffpins_n_id',),
                      CheckConstraint('n_id != p_id')
                      )

    def __init__(self, p: 'Pin', n: 'Pin', name: Optional[str] = None):

        if p.part != n.part:
            raise ValueError('Positive and negative pin must be on the same part')
        super(DiffPins, self).__init__(_p=p, _n=n, _part=p.part, name=name)

    @property
    def p(self) -> 'Pin':
        return self._p

    @p.setter
    def p(self, p: 'Pin') -> 'Pin':
        if p.part != self._p.part:
            raise ValueError('Positive and negative pin must be on the same part')
        self._p = p

    @property
    def n(self) -> 'Pin':
        return self._n

    @n.setter
    def n(self, n: 'Pin') -> 'Pin':
        if n.part != self._n.part:
            raise ValueError('Positive and negative pin must be on the same part')
        self._n = n

    @property
    def part(self) -> 'Part':
        return self._part


class Pin(SerializeMixin, DefaultReprMixin, Base):
    """
        A pin defines a connection point of a part. The minimum it requires is a designator, also known as pin number.
        The name of the pin is a hint for it's function/usage.
    """
    __tablename__ = "pin"

    _serialization_ignore_keys = {'id', 'net_id', 'part_id', 'schpin', 'gates'}

    id = Column(Integer, primary_key=True)

    name = Column(String)
    designator = Column(String, nullable=False)

    part_id = Column(Integer, ForeignKey('part.id'))
    part = relationship('Part', back_populates='pins')

    net_id = Column(Integer, ForeignKey('net.id'))
    net = relationship('Net', back_populates='pins')

    net_paths = relationship('NetPath',
                             primaryjoin='or_(NetPath.pin1_id == Pin.id, NetPath.pin2_id == Pin.id)',
                             cascade="all, delete"
                             )

    sig_paths = relationship('SignalPath',
                             primaryjoin='or_(SignalPath.pin1_id == Pin.id, SignalPath.pin2_id == Pin.id)',
                             cascade="all, delete"
                             )

    _diff_p = relationship('DiffPins',
                           uselist=False,
                           back_populates='_p',
                           foreign_keys='DiffPins.p_id')

    _diff_n = relationship('DiffPins',
                           uselist=False,
                           back_populates='_n',
                           foreign_keys='DiffPins.n_id')

    # only for pads support, may be dropped
    swap_group = Column(Integer)

    electrical_type = Column(SqlalchemyEnum(PinType))

    __table_args__ = (UniqueConstraint('designator', 'part_id', name='unique_pin_designator'),)

    def __init__(self, designator: str, **kwargs):
        super(Pin, self).__init__(designator=designator, **kwargs)

    @property
    def diff_polarity(self) -> Optional[Polarity]:
        if self._diff_p:
            return Polarity.P
        elif self._diff_n:
            return Polarity.N
        else:
            return None

    @property
    def diff(self) -> Optional[DiffPins]:
        assert self._diff_p is None or self._diff_n is None
        if self._diff_p:
            return self._diff_p
        elif self._diff_n:
            return self._diff_n
        else:
            return None

    def copy(self) -> 'Pin':
        return Pin(name=self.name,
                   designator=self.designator,
                   swap_group=self.swap_group,
                   electrical_type=self.electrical_type)

    def schematic_repr(self) -> str:
        """
        returns a string of schematic representation.
        @return:
        """
        assert self.part.schematic
        return f'{self.part.designator}.{self.designator}'


class DiffNet(SerializeMixin, DefaultReprMixin, Base):
    """
        A group for differential nets.
        p for the differential positive Net
        n for the differential negative Net
    """
    __tablename__ = "diff_net"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    p_id = Column(Integer, ForeignKey('net.id'), nullable=False)
    _p = relationship('Net', foreign_keys=[p_id], back_populates='_diff_p')

    n_id = Column(Integer, ForeignKey('net.id'), nullable=False)
    _n = relationship('Net', foreign_keys=[n_id], back_populates='_diff_n')

    schematic_id = Column(Integer, ForeignKey('schematic.id'), nullable=False)
    _schematic = relationship('Schematic', back_populates='diff_nets')

    __table_args__ = (UniqueConstraint('name', 'schematic_id', name='unique_diffnets_name',),
                      UniqueConstraint('p_id', 'schematic_id', name='unique_diffnets_p_id',),
                      UniqueConstraint('n_id', 'schematic_id', name='unique_diffnets_n_id',),
                      CheckConstraint('n_id != p_id')
                      )

    def __init__(self, p: 'Net', n: 'Net', name: Optional[str] = None):
        assert p.schematic == n.schematic
        super(DiffNet, self).__init__(_p=p, _n=n, _schematic=p.schematic, name=name)

    @property
    def p(self) -> 'Net':
        return self._p

    @p.setter
    def p(self, p: 'Net') -> 'Net':
        assert p.schematic == self._p.schematic
        self._p = p

    @property
    def n(self) -> 'Pin':
        return self._n

    @n.setter
    def n(self, n: 'Pin') -> 'Pin':
        assert n.schematic == self._n.schematic
        self._n = n

    @property
    def schematic(self) -> 'Schematic':
        return self._schematic

    def clear_schematic(self):
        self._schematic = None


class Net(SerializeMixin, DefaultReprMixin, Base):
    """
        A net can connects pins electrically together. It has a unique name in a schematic and it has a set of pins.
    """
    __tablename__ = "net"

    _serialization_ignore_keys = {'schematic_id'}

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    pins = relationship('Pin', back_populates='net')

    schematic_id = Column(Integer, ForeignKey('schematic.id'), nullable=False)
    schematic = relationship('Schematic', back_populates='nets')

    simulation_gnd = Column(Boolean, default=False)

    _diff_p = relationship('DiffNet',
                           uselist=False,
                           back_populates='_p',
                           foreign_keys='DiffNet.p_id')

    _diff_n = relationship('DiffNet',
                           uselist=False,
                           back_populates='_n',
                           foreign_keys='DiffNet.n_id')

    __table_args__ = (UniqueConstraint('name', 'schematic_id', name='name'),)

    def __init__(self, name: str, pins: Optional[List[Pin]] = None, schematic: Optional['Schematic'] = None, **kwargs):
        sch = schematic
        ps = [] if pins is None else pins
        if ps:
            schematic_set = {pin.part.schematic for pin in ps if pin.part and pin.part.schematic}
            assert len(schematic_set) <= 1
            if schematic_set:
                pins_schematic = schematic_set.pop()
                if schematic is None:
                    sch = pins_schematic
                else:
                    assert sch == ps[0].part.schematic
        super(Net, self).__init__(name=name, pins=ps, schematic=sch, **kwargs)

    @property
    def diff_polarity(self) -> Optional[Polarity]:
        if self._diff_p:
            return Polarity.P
        elif self._diff_n:
            return Polarity.N
        else:
            return None

    @property
    def diff(self) -> Optional[DiffPins]:
        assert self._diff_p is None or self._diff_n is None
        if self._diff_p:
            return self._diff_p
        elif self._diff_n:
            return self._diff_n
        else:
            return None


class PartProperty(SerializeMixin, DefaultReprMixin, Base):
    """
        Every part can have named string properties.
    """
    __tablename__ = "part_property"

    _serialization_ignore_keys = {'schematic_id'}

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    value = Column(String, nullable=False, default='')

    part_id = Column(Integer, ForeignKey('part.id'), nullable=False)
    part = relationship('Part', back_populates='properties')

    __table_args__ = (UniqueConstraint('name', 'part_id', name='unique_part_property'),)

    def __init__(self, name: str, value: str = '', **kwargs) -> None:
        super(PartProperty, self).__init__(name=name, value=value, **kwargs)

    def copy(self) -> 'PartProperty':
        return PartProperty(
            name=self.name,
            value=self.value
        )


class Part(SerializeMixin, DefaultReprMixin, Base):
    """
        A Part is an electronic component with at least some Pins.
        It can be used in a Library, in a schematic or on a pcb.
    """
    __tablename__ = "part"

    _serialization_ignore_keys = {'schematic_id', 'library_id'}

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)   # alternative reference in library
    designator = Column(String)             # alternative reference in schematic

    schematic_id = Column(Integer, ForeignKey('schematic.id'))
    schematic = relationship('Schematic', back_populates='parts')

    library_id = Column(Integer, ForeignKey('part_library.id'))
    library = relationship('PartLibrary', back_populates='parts')
    library_name = Column(String)

    footprint_name = Column(String)

    spice_model = Column(Text)

    simulation_type = Column(SqlalchemyEnum(SimulationType))

    properties = relationship('PartProperty',
                              back_populates='part',
                              collection_class=column_mapped_collection(PartProperty.__table__.c.name),
                              cascade="all, delete")

    pins = relationship('Pin',
                        back_populates='part',
                        collection_class=column_mapped_collection(Pin.__table__.c.designator),
                        cascade="all, delete")

    diff_pins = relationship('DiffPins', back_populates='_part')

    __table_args__ = (UniqueConstraint('name', 'library_id', name='part_unique_name_library'),
                      UniqueConstraint('designator', 'schematic_id', name='part_unique_schematic_designator'))

    def __init__(self, name: str, pins: Optional[Union[Dict[str, Pin], List[Pin]]] = None,
                 properties: Optional[Union[Dict[str, PartProperty], List[PartProperty]]] = None, **kwargs):
        if isinstance(pins, list):
            pins_d = {pin.designator: pin for pin in pins}
            if len(pins_d) != len(pins):
                raise ValueError('given pins designator have duplications')
            pins = pins_d
        elif pins is None:
            pins = {}

        if isinstance(properties, List):
            prop_d = {prop.value: prop for prop in properties}
            if len(prop_d) != len(properties):
                raise ValueError('given properties values have duplications')
            properties = prop_d
        elif properties is None:
            properties = {}
        super(Part, self).__init__(name=name, pins=pins, properties=properties, **kwargs)

    def __repr__(self):
        return f'{self.__class__.__name__}({self._default_cols_repr()}, pins = {self.pins})'

    def add_property(self, name: str, value: str):
        if name in self.properties:
            raise KeyError('Property already exists')
        else:
            self.properties[name] = PartProperty(name=name, value=value)

    def add_pin(self, pin: Pin):
        if pin.designator in self.pins:
            raise KeyError('Pin Designator already exists')
        elif pin.part is not None:
            raise ValueError('Pin already has a part assigned')
        else:
            self.pins[pin.designator] = pin

    def copy(self) -> 'Part':
        part = Part(
            name=self.name,
            designator=self.designator,
            library_name=self.library_name,
            footprint_name=self.footprint_name,
            spice_model=self.spice_model,
            simulation_type=self.simulation_type,
            properties={key: prop.copy() for key, prop in self.properties.items()},
            pins={p.designator: p.copy() for p in self.pins.values()},
        )
        part.diff_pins = [
            DiffPins(p=part.pins[diff_pin.p.designator],
                     n=part.pins[diff_pin.n.designator],
                     name=diff_pin.name)
            for diff_pin in self.diff_pins
        ]
        return part


class Schematic(SerializeMixin, DefaultReprMixin, Base):
    """
        A Schematic is a container for Parts and it's connections.
        Additionally it's the connection point to the graphical world, since it can contain Drawing Pages.
    """
    __tablename__ = "schematic"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False, unique=True)

    parts = relationship('Part',
                         back_populates='schematic',
                         collection_class=attribute_mapped_collection('designator'),
                         cascade="all, delete"
                         )
    nets = relationship('Net',
                        back_populates='schematic',
                        collection_class=attribute_mapped_collection('name'),
                        cascade="all, delete"
                        )

    diff_nets = relationship('DiffNet', back_populates='_schematic')

    def __init__(self, name: str, parts: Optional[Union[Dict[str, Part], List[Part]]] = None, **kwargs):
        if isinstance(parts, list):
            parts_d = {part.designator: part for part in parts}
            if len(parts_d) != len(parts):
                raise ValueError('given parts have duplicated designator')
            parts = parts_d
        elif parts is None:
            parts = {}
        super(Schematic, self).__init__(name=name, parts=parts, **kwargs)

    def get_distinct_part_names_session(self) -> List[str]:
        return [r[0] for r in self.clean_session.query(distinct(Part.name)).filter(Part.schematic_id == self.id).all()]

    def copy(self, new_name: str) -> 'Schematic':
        s = Schematic(
            name=new_name,
            parts={designator: p.copy() for designator, p in self.parts.items()}

        )
        s.nets = {name: Net(
            name=name,
            pins=[
                s.parts[pin_ref.part.designator].pins[pin_ref.designator]
                for pin_ref in net.pins],
            simulation_gnd=net.simulation_gnd)
            for name, net in self.nets.items()}
        s.diff_nets=[
            DiffNet(
                p=s.nets[diff_net.p.name],
                n=s.nets[diff_net.n.name],
                name=diff_net.name
            )
            for diff_net in self.diff_nets
        ]
        return s

    def replace_part(self, designator: str, new_part: Part, ignore_new_pins: bool = False):
        """

        @param designator:  schematic designator of the part which will be replaced.
        @param new_part:    new part instance to replace the one  in the schematic.
                            Warning new_part must already be a copy, replace_part doesn't duplicate given instance.
        @param ignore_new_pins: True: new_part can have more pins then the part in schematic (needed for netlist import)
                                False: new_part pins designators must match the old part
        @return:
        """
        assert new_part.schematic is None
        assert new_part.library is None
        part_to_replace = self.parts[designator]
        assert new_part.footprint_name == part_to_replace.footprint_name
        if ignore_new_pins:
            assert set(part_to_replace.pins.keys()).issubset(set(new_part.pins.keys()))
        else:
            assert new_part.pins.keys() == part_to_replace.pins.keys()
        new_part.designator = designator

        for pin_designator, pin in part_to_replace.pins.items():
            new_part.pins[pin_designator].net = pin.net
            pin.net = None

        del self.parts[designator]
        if self.session:
            self.session.delete(part_to_replace)
        self.parts[designator] = new_part

    def delete_unconnected_nets(self):
        nets_to_delete = [net for net in self.nets.values() if not net.pins]
        diff_nets = [n.diff for n in nets_to_delete if n.diff]
        for net_to_delete in nets_to_delete:
            del self.nets[net_to_delete.name]
            if self.session:
                self.session.delete(net_to_delete)
        for diff_net in diff_nets:
            diff_net.clear_schematic()
            if self.session:
                self.session.delete(diff_net)

    def delete_part(self, designator: str):
        part_to_delete = self.parts[designator]
        del self.parts[designator]
        if self.session:
            self.session.delete(part_to_delete)
        else:
            for pin in part_to_delete.pins.values():
                pin.net = None
        self.delete_unconnected_nets()


class PartLibrary(SerializeMixin, DefaultReprMixin, Base):
    """
        A PartLibrary is nothing more then a stupid name with relationships to parts.
    """
    __tablename__ = "part_library"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False, unique=True)
    parts = relationship('Part',
                         back_populates='library',
                         collection_class=column_mapped_collection(Part.__table__.c.name),
                         cascade="all, delete"
                         )

    def __init__(self, name: str, parts: Union[Dict[str, Part], List[Part]]):
        if isinstance(parts, list):
            parts_d = {part.name: part for part in parts}
            if len(parts_d) != len(parts):
                raise ValueError('given parts name have duplicated names')
            parts = parts_d
        elif parts is None:
            parts = {}
        super(PartLibrary, self).__init__(name=name, parts=parts)

    def query_part_by_unique_property(self, property_name: str, property_value: str,
                                    footrpint_name: Optional[str] = None) -> Query:
        q = self.session.query(Part) \
            .join(PartProperty) \
            .filter(PartProperty.name == property_name, PartProperty.value == property_value) \
            .filter(Part.library_id == self.id)
        if footrpint_name:
            q = q.filter(Part.footprint_name == footrpint_name)
        return q


class NetPath(SerializeMixin, DefaultReprMixin, Base):
    """
        A NetPath contains only two pins from the same net.
        It represents a path from one Part to another.

        This object should only be created.
    """
    __tablename__ = "net_path"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    pin1_id = Column(Integer, ForeignKey('pin.id'), nullable=False)
    _pin1 = relationship('Pin', back_populates='net_paths', foreign_keys=[pin1_id])

    pin2_id = Column(Integer, ForeignKey('pin.id'), nullable=False)
    _pin2 = relationship('Pin', back_populates='net_paths', foreign_keys=[pin2_id])

    signal_path_id = Column(Integer, ForeignKey('signal_path.id'), nullable=False)
    _signal_path = relationship('SignalPath', back_populates='_net_paths')

    sig_path_sequence = Column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint('sig_path_sequence', 'signal_path_id', name='unique_sig_path_sequence'),)

    def __init__(self, pin1: Union[Pin, int], pin2: Union[Pin, int], name: str = None):
        assert type(pin1) == type(pin2)
        if isinstance(pin1, Pin):
            if pin1.net != pin2.net:
                raise ValueError(f'{pin1.schematic_repr()} is connected to {pin1.net.name} and {pin2.schematic_repr()} '
                                 f'to {pin2.net.name}.')
            if pin1.net is None:
                raise ValueError(f'{pin1.schematic_repr()} net is None')
            super(NetPath, self).__init__(_pin1=pin1, _pin2=pin2, name=name)
        elif isinstance(pin1, int):
            super(NetPath, self).__init__(pin1_id=pin1, pin2_id=pin2, name=name)
        else:
            raise TypeError

    @property
    def pin1(self) -> Pin:
        return self._pin1

    @property
    def pin2(self) -> Pin:
        return self._pin2

    @property
    def signal_path(self) -> 'SignalPath':
        return self._signal_path


class InvalidSignalPath(Exception):
    pass


class SignalPath(SerializeMixin, DefaultReprMixin, Base):
    """
        A SignalPath describes a Path a signal can take in the schematic.
        E.g. from a connector, through a resistor, a capacitor or/and a level shifter to an phy.
        It the paths should not depend on the states of the devices.

        This object should only be created.
    """
    __tablename__ = "signal_path"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    pin1_id = Column(Integer, ForeignKey('pin.id'), nullable=False)
    _pin1 = relationship('Pin', back_populates='sig_paths', foreign_keys=[pin1_id])

    pin2_id = Column(Integer, ForeignKey('pin.id'), nullable=False)
    _pin2 = relationship('Pin', back_populates='sig_paths', foreign_keys=[pin2_id])

    _net_paths = relationship('NetPath',
                              back_populates='_signal_path',
                              order_by='NetPath.sig_path_sequence')

    @staticmethod
    def validate_net_paths(net_paths: List[NetPath]):
        """
        Validates if the net paths List is valid.
        It is expected, that the net_paths together build a chain, from one part to another.

        The first element represent the start, the last the destination. Therfore the part of element 0 pin1 and the
        part of pin2 of the last element need to be unique.

        @param net_paths:
        @return:
        @raise: InvalidSignalPath
        """
        if len(net_paths) < 1:
            raise InvalidSignalPath('A Signal Path must contain at least 1 net_paths.')
        start_part = net_paths[0].pin1.part
        end_part = net_paths[-1].pin2.part
        assert start_part and end_part
        if start_part == end_part:
            raise InvalidSignalPath('Start and End must be different.')
        history = {start_part, end_part}

        for i, net_path in enumerate(net_paths[:-1]):
            if (part := net_path.pin2.part) != net_paths[i+1].pin1.part:
                raise InvalidSignalPath('net_path.pin2.part != net_paths[i+1].pin1.part')
            if net_path.pin2 == net_paths[i+1].pin1:
                raise InvalidSignalPath('net_path.pin2 == net_paths[i+1].pin1')
            if part in history:
                raise InvalidSignalPath('{} is duplicated in the net_paths.'.format(part.designator))
            history.add(net_path.pin2.part)

    def __init__(self, net_paths: List[NetPath], name: Optional[str] = None, ignore_validation: bool = False):
        if not ignore_validation:
            self.validate_net_paths(net_paths)

        for i, netpath in enumerate(net_paths):
            netpath.sig_path_sequence = i

        if net_paths[0].pin1:
            assert net_paths[-1].pin2 is not None
            kwargs = {'_pin1': net_paths[0].pin1, '_pin2': net_paths[-1].pin2 }
        else:
            assert net_paths[0].pin1_id and net_paths[-1].pin2_id
            kwargs = {'pin1_id': net_paths[0].pin1_id, 'pin2_id': net_paths[-1].pin2_id}
        super(SignalPath, self).__init__(_net_paths=net_paths, name=name, **kwargs)

    @property
    def net_paths(self) -> List[NetPath]:
        return self._net_paths

    @property
    def pin1(self) -> Pin:
        return self._pin1

    @property
    def pin2(self) -> Pin:
        return self._pin2
