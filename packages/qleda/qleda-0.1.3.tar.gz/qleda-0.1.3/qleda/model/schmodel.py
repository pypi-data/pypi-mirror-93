from typing import List, Optional, Dict
from enum import Enum, auto

from sqlalchemy import Column, Integer, UniqueConstraint, ForeignKey, Float, Boolean, String, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound

from ..core.dbbase import Base
from ..core.mixins import DefaultReprMixin
from ..core.point import Point
from ..drawing.dbdrawingcontainers import FlatContainer

from .basic import Pin


class SchPin(DefaultReprMixin, FlatContainer):
    """
        A schematic pin has name, designator and an optional symbol.
        It connects with wires on it's origin.
    """
    __tablename__ = 'sch_pin'

    id = Column(Integer, ForeignKey('flatcontainer.id'), primary_key=True)

    name = Column(String)
    designator = Column(String, nullable=False)

    part_symbol_id = Column(Integer, ForeignKey('part_symbol.id'))
    part_symbol = relationship('PartSymbol', backref='pins', foreign_keys=[part_symbol_id])

    pin_id = Column(Integer, ForeignKey('pin.id'))
    pin = relationship('Pin', backref='schpin', foreign_keys=[pin_id])

    __table_args__ = (UniqueConstraint('designator', 'part_symbol_id', name='unique_pin_designator'),)

    __mapper_args__ = {
        'polymorphic_identity': 'sch_pin',
    }

    def copy(self) -> 'SchPin':
        return SchPin(
            name=self.name,
            designator=self.designator,
            drawing_pieces=[dp.copy() for dp in self.drawing_pieces],
            labels={key: label.copy() for key, label in self.labels.items()}
        )

    def update_pin_attributes(self):
        """
        copies name and designator from pin link
        @return:
        """
        self.name = self.pin.name
        self.designator = self.pin.designator


class PartSymbol(DefaultReprMixin, FlatContainer):
    """
        A graphically representation of a sub part.
    """
    __tablename__ = 'part_symbol'

    id = Column(Integer, ForeignKey('flatcontainer.id'), primary_key=True)
    name = Column(String, nullable=False) # e.g. RES
    designator = Column(String, nullable=False, default='') # e.g. R200A

    # This seems to be more complicated then expected. Therefore used backref
    # pins = relationship('SchPin', back_populates='part_symbol', remote_side=[id])

    gate_id = Column(Integer, ForeignKey('gate.id'))
    gate = relationship('Gate', back_populates='part_symbols')

    library_id = Column(Integer, ForeignKey('symbol_library.id'))
    library = relationship('SymbolLibrary', back_populates='symbols')
    library_name = Column(String)

    __table_args__ = (UniqueConstraint('name', 'gate_id'),)

    __mapper_args__ = {
        'polymorphic_identity': 'part_symbol',
    }

    def get_all_points(self) -> List[Point]:
        if self.visible:
            return [
                *super().get_all_points(),
                *[p.move(pin.origin) for pin in self.pins for p in pin.get_all_points() if p]
            ]
        else:
            None

    def copy(self) -> 'PartSymbol':
        return PartSymbol(
            name=self.name,
            pins=[schpin.copy() for schpin in self.pins],
            drawing_pieces=[dp.copy() for dp in self.drawing_pieces],
            labels={key: label.copy() for key, label in self.labels.items()}
        )


class NetConnector(DefaultReprMixin, FlatContainer):
    """
        A graphical representation of a Net Connector
    """
    __tablename__ = 'netconnector'

    id = Column(Integer, ForeignKey('flatcontainer.id'), primary_key=True)

    name = Column(String, nullable=False) # e.g. PWR, GND, etc.
    pin_id = Column(Integer, ForeignKey('sch_pin.id'))
    pin = relationship('SchPin', backref='netconnector', foreign_keys=[pin_id])

    library_id = Column(Integer, ForeignKey('symbol_library.id'))
    library = relationship('SymbolLibrary', back_populates='netconnectors')
    library_name = Column(String)

    __table_args__ = (UniqueConstraint('name', 'library_id'),)

    __mapper_args__ = {
        'polymorphic_identity': 'netconnector',
    }


class SchRepresentation(DefaultReprMixin, Base):
    """
        A Schematic representation can have one or several symbols for a part (e.g. resistor european or us style).
        But it can also have several symbols which in total represents the part in the schematic (e.g. opamp with
        multiple gates and power).

        Symbols representing the same pins but with different drawings are grouped together in a gate.

        The set of all the schematic PartSymbol's pins designators need to match with the parts pin designators.
    """
    __tablename__ = 'sch_rep'

    id = Column(Integer, primary_key=True)
    name = Column(String)   # optional description e.g. european, american, etc.

    gates = relationship('Gate', back_populates='sch_representation')

    part_id = Column(Integer, ForeignKey('part.id'))
    part = relationship('Part', backref='sch_representations')

    __table_args__ = (UniqueConstraint('name', 'part_id'),)




gate_pins_relation_table = Table('gate_pins_relation', Base.metadata,
    Column('gate_id', Integer, ForeignKey('gate.id')),
    Column('pin_id', Integer, ForeignKey('pin.id'))
)


class PinMatchingStrategy(Enum):
    Position = auto()       # PADS style, match symbol and Logic Pins by Index
    Designator = auto()


class PinMatchingError(Exception):
    pass


class Gate(DefaultReprMixin, Base):
    """

    """
    __tablename__ = 'gate'

    id = Column(Integer, primary_key=True)
    name = Column(String)  # optional description e.g. Power, MGTs etc.

    part_symbols = relationship('PartSymbol', back_populates='gate')

    sch_representation_id = Column(Integer, ForeignKey('sch_rep.id'))
    sch_representation = relationship('SchRepresentation', back_populates='gates')

    pins = relationship('Pin',
                        secondary=gate_pins_relation_table,
                        backref='gates')

    @staticmethod
    def _match_pins_by_dict(gate: 'Gate', pins: Dict[str, Pin], override_part_symbols_pins):
        for symbol in gate.part_symbols:
            symbol_pins = {pin.designator: pin for pin in symbol.pins}
            if set(symbol_pins.keys()) != set(pins.keys()):
                raise PinMatchingError
            else:
                for refdes, symbol_pin in symbol_pins.items():
                    symbol_pin.pin=pins[refdes]
                    if override_part_symbols_pins:
                        symbol_pin.update_pin_attributes()

    def connect_part_symbol_pins_with_part(self, strategy: PinMatchingStrategy,
                                           override_part_symbols_pins: bool = False):
        """
        connects the part symbols pin with the parts pin.
        assumes the Gates pins are already set.
        @param strategy:
        @param override_part_symbols_pins: True overrides the schpins name and designator. False: no override
        @return:
        @raise: PinMatchingError if pins of part can't be matched with the symbol.
                ValueError if illegal strategy was given.
        """
        if strategy == PinMatchingStrategy.Position:
            pins_to_match = {'#{}'.format(i): pin for i, pin in enumerate(self.pins)}
        elif strategy == PinMatchingStrategy.Designator:
            pins_to_match = {pin.designator: pin for pin in self.pins}
        else:
            raise ValueError('illegal Value for strategy')
        Gate._match_pins_by_dict(self, pins_to_match, override_part_symbols_pins)



class SymbolLibrary(DefaultReprMixin, Base):
    """
        A Symbol is nothing more then a stupid name with relationships to PartSymbol.
    """
    __tablename__ = "symbol_library"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False, unique=True)
    symbols = relationship('PartSymbol', back_populates='library')
    netconnectors = relationship('NetConnector', back_populates='library')


def get_unique_part_symbol(session, name: str, library_name: Optional[str]=None) -> PartSymbol:
    """
    queries session and returns a unique part symbol. warning, the entry library_name of PartSymbol is ignored
    @param name:
    @param library_name:
    @return:
    """
    try:
        if library_name is not None:
            return session.query(PartSymbol).join(SymbolLibrary).filter(SymbolLibrary.name==library_name)\
                .filter(PartSymbol.name==name).one()
        else:
            return session.query(PartSymbol).filter(PartSymbol.name==name).one()
    except NoResultFound:
        raise NoResultFound("{} wasn't found in library {}".format(name, library_name))
