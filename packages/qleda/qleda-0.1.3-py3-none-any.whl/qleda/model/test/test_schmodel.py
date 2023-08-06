import unittest

from ..basic import Part
from ..schmodel import PartSymbol, SchRepresentation, SchPin, SymbolLibrary, Gate
from ...core.testing import DbTestCase

from sqlalchemy.exc import IntegrityError


class TestSchModel(DbTestCase):

    def test_Relations(self):
        normalr = Part(name='normal_r', designator='normalr')
        usleless_pin = SchPin()
        sch_pina = SchPin(designator='1')
        sch_pinb = SchPin(designator='1')
        resa = PartSymbol(name='resa', pins=[sch_pina])
        resb = PartSymbol(name='resb', pins=[sch_pinb])

        liba = SymbolLibrary(name='liba')
        resa.library = liba

        gatea = Gate()
        repa = SchRepresentation(gates=[Gate(part_symbols=[resa])], part=normalr)
        repb = SchRepresentation(gates=[Gate(part_symbols=[resb])], part=normalr)
        self.session.add(normalr)
        self.session.add(liba)
        self.session.commit()
        print(sch_pina)
        print(resb)
        print(liba)
        print(resb.pins)
        print(normalr.sch_representations)

    def test_constraints(self):
        sch_pina = SchPin(designator='1')
        sch_pinb = SchPin(designator='1')
        resa = PartSymbol(name='resa', pins=[sch_pina, sch_pinb])

        self.session.add(resa)
        self.assertRaises(IntegrityError, self.session.commit)
        self.session.rollback()

        normalr = Part(name='normal_r')
        sch_pina = SchPin(designator='1')
        sch_pinb = SchPin(designator='1')
        resa = PartSymbol(name='resa', pins=[sch_pina])
        resb = PartSymbol(name='resb', pins=[sch_pinb])

        repa = SchRepresentation(name='rep', gates=[Gate(part_symbols=[resa])], part=normalr)
        repb = SchRepresentation(name='rep', gates=[Gate(part_symbols=[resb])], part=normalr)

        self.session.add(normalr)
        self.assertRaises(IntegrityError, self.session.commit)


if __name__ == '__main__':
    unittest.main()
