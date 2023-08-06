from typing import Optional
import unittest

from ...core.testing import DbTestCase
from ...model.basic import Part, PartLibrary, Pin

from ..functions import part_library_no_empty_pin_name
from ..exceptions import DirtySessionException, EmptyPinNames


class TestFunctions(DbTestCase):

    def setUp(self, debug: Optional[bool] = None) -> None:
        super(TestFunctions, self).setUp(debug)
        self.partlib = PartLibrary(name='test_lib',
                    parts=[
                        Part(
                            name='p1',
                            pins=[
                                Pin(name='vcc', designator='1'),
                                Pin(name='gnd', designator='2'),
                        ]),
                        Part(name='p2',
                             pins=[
                                 Pin(name='vcc', designator='1'),
                                 Pin(designator='2'),
                             ])
                    ])

    def test_part_library_no_empty_pin_name(self):
        self.session.add(self.partlib)
        self.session.commit()

        # Test dirty session
        self.partlib.parts['p2'].pins['1'].name = 'bla'
        self.assertRaises(DirtySessionException, part_library_no_empty_pin_name, self.session, self.partlib)

        # Test EmptyPinNames
        self.session.commit()
        self.assertRaises(EmptyPinNames, part_library_no_empty_pin_name, self.session, self.partlib)

        self.partlib.parts['p2'].pins['2'].name = 'bla2'
        self.session.commit()
        part_library_no_empty_pin_name(self.session, self.partlib)

        # Test unrelated Pins
        self.session.add(Part(name='unrelated',
                             pins=[
                                 Pin(name='vcc', designator='1'),
                                 Pin(designator='2'),
                             ]))
        self.session.commit()
        part_library_no_empty_pin_name(self.session, self.partlib)


if __name__ == '__main__':
    unittest.main()
