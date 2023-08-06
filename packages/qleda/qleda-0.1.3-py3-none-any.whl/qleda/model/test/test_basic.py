import unittest
from copy import deepcopy

from sqlalchemy.exc import IntegrityError

from ...common.electrical import Polarity
from ...core.testing import DbTestCase

from ..basic import Part, Schematic, PartLibrary, Pin, Net, PartProperty, DiffPins, DiffNet, NetPath, SignalPath,\
    InvalidSignalPath


def build_resistor() -> Part:
    return Part(
        name='resistor',
        pins={
            '1': Pin(designator='1'),
            '2': Pin(designator='2'),
        }
    )


class TestModel(DbTestCase):

    # uncomment to debug with a database file. Warning unittest.main() won't work
    # _DEBUG = True

    def testConstraintsPart(self):
        # allowed since no library id (ex. in schematic)
        part1 = Part(name='part1', library_name='lib1')
        part2 = Part(name='part2', library_name='lib1')
        part3 = Part(name='part1', library_name='lib2')
        self.session.add_all([part1, part2, part3])
        part4 = Part(name='part1', library_name='lib2')
        self.session.add(part4)
        self.session.commit()

        # not allowed when library has a reference on it
        self.assertRaises(ValueError, PartLibrary, name='testlib', parts=[part1, part2, part3])

        part5 = Part(name='part5')
        part6 = Part(name='part5')
        self.session.add_all([part5, part6])

    def testInitNet(self):
        schema = Schematic(name='test_schema')
        gnd = Net(name='GND', schematic=schema)
        r1 = build_resistor()
        r2 = build_resistor()

        gnd.pins = [r1.pins['1'], *r2.pins.values()]
        self.session.add(gnd)
        self.session.commit()
        self.assertEqual(3, len(gnd.pins))

    def testInitNet2(self):
        schema = Schematic(name='test_schema')
        gnd = Net(name='GND', schematic=schema)
        r1 = build_resistor()

        gnd.pins = [r1.pins['1'], r1.pins['1']]
        self.session.add(gnd)
        self.session.commit()
        self.assertEqual(1, len(gnd.pins))

    def test_NoSchematicNet(self):
        self.session.add(Net(name='net'))
        self.assertRaises(IntegrityError, self.session.commit)

    def testNetConstraint(self):
        schema = Schematic(name='test_schema')
        gnd1 = Net(name='GND', schematic=schema)
        gnd2 = Net(name='GND', schematic=schema)
        self.session.add_all([gnd1, gnd2])
        self.assertRaises(IntegrityError, self.session.commit)

    def testRelationships(self):
        schematic_a = Schematic(name='schema_a')
        part_a = Part(name='part1', designator='Part1')
        pin_a = Pin(designator='1', name='VCC')
        part_a.pins = {pin_a.designator: pin_a}
        schematic_a.parts = {part_a.designator: part_a}
        self.session.add(schematic_a)
        self.session.commit()
        self.assertEqual(part_a.schematic_id, schematic_a.id)
        self.assertEqual(part_a.id, pin_a.part.id)
        pin_b = Pin(designator='2', name='VCCB')
        part_a.pins[pin_b.designator] = pin_b
        self.session.commit()

        # test cascade
        self.assertEqual([pin_a, pin_b], self.session.query(Pin).all())
        p1 = PartProperty(name='mpn', part=part_a)
        p2 = PartProperty(name='manufacturer', part=part_a)
        print(type(part_a.properties))
        self.session.commit()
        self.assertEqual([p1, p2], self.session.query(PartProperty).all())
        self.session.delete(part_a)
        self.session.commit()
        self.assertEqual([], self.session.query(PartProperty).all())
        self.assertEqual([], self.session.query(Pin).all())

    def testProperties(self):
        part_a = Part(name='part1')
        p1 = PartProperty(name='mpn', part=part_a)
        p2 = PartProperty(name='manufacturer', part=part_a)

        # Fixme this is a little risky, because it's not like expected
        part_a.properties['gugus'] = PartProperty(name= 'distre', value='Digi-Key')
        print(part_a.properties)
        self.session.add(part_a)
        self.session.commit()
        print(part_a.properties)

    def testCopy(self):
        r1 = build_resistor()
        r2 = deepcopy(r1)
        self.session.add_all([r1, r2])
        self.session.commit()
        print(r1)
        print(r2)
        r3 = deepcopy(r1)
        # Warning r3 will have same id like r1
        print(r3)

    def test_diffpins(self):
        part = Part(name='test', designator='test_part')
        pin1 = Pin(designator='1', name='_P', part=part)
        pin2 = Pin(designator='2', name='_N', part=part)
        diff_pin = DiffPins(p=pin1, n=pin2, name='bla')
        self.session.add_all([part, diff_pin])
        self.session.commit()
        self.assertEqual(pin1.diff, diff_pin)
        self.assertEqual(diff_pin.part, part)
        self.assertEqual(part.diff_pins[0], diff_pin)
        self.assertEqual(Polarity.P, pin1.diff_polarity)
        self.assertEqual(Polarity.N, pin2.diff_polarity)

    def test_diffConstraints(self):
        part = Part(name='test', designator='test_part')
        part2 = Part(name='test2', designator='test_part2')
        pin1 = Pin(designator='1', name='_P', part=part)
        pin2 = Pin(designator='2', name='_N', part=part2)
        self.assertRaises(ValueError, DiffPins, p=pin1, n=pin2)
        pin3 = Pin(designator='3', name='_N', part=part)
        diff_pin = DiffPins(p=pin1, n=pin3)
        self.session.add_all([diff_pin, pin2])
        self.session.commit()
        self.assertRaises(ValueError, diff_pin.__setattr__, 'n', pin2)

    def test_diffnets(self):
        schema = Schematic(name='schema')
        n1 = Net(name='n1_p', schematic=schema)
        n2 = Net(name='n2_n', schematic=schema)
        diffnet = DiffNet(n1, n2)
        self.session.add_all([diffnet])
        self.session.commit()
        self.assertEqual(n1.diff, diffnet)
        self.assertEqual(n2.diff, diffnet)
        self.assertEqual(diffnet.schematic, schema)
        self.assertEqual(schema.diff_nets[0], diffnet)
        self.assertEqual(Polarity.P, n1.diff_polarity)
        self.assertEqual(Polarity.N, n2.diff_polarity)


class TestSchematic(DbTestCase):

    _DEBUG = False

    @staticmethod
    def build_schematic() -> Schematic:
        return Schematic(
            name='schema_a',
            parts=[
                Part('R_0402_0R',
                     designator='R1',
                     pins=[
                         Pin('1'),
                         Pin('2'),
                     ],
                     properties=[
                         PartProperty('Value', '10k'),
                         PartProperty('Tolerance', '±1%'),
                     ]),
                Part('R_0402_0R',
                     designator='R2',
                     pins=[
                         Pin('1'),
                         Pin('2'),
                     ]),
                Part('R_0402_2R',
                     designator='R3',
                     pins=[
                         Pin('1'),
                         Pin('2'),
                     ]),
                Part('SPLIT',
                     designator='U1',
                     pins=[
                         Pin('1', name='single'),
                         Pin('2', name='DIFF_P'),
                         Pin('3', name='DIFF_N'),
                     ]),
                Part('SPLIT',
                     designator='U2',
                     pins=[
                         Pin('1', name='single'),
                         Pin('2', name='DIFF_P'),
                         Pin('3', name='DIFF_N'),
                     ]),
            ]
        )

    def test_replace_part(self):
        schema_a = self.build_schematic()
        r1_to_r2 = Net('r1_to_r2', pins=[schema_a.parts['R1'].pins['2'], schema_a.parts['R2'].pins['1']])
        r2_to_r3 = Net('r2_to_r3', pins=[schema_a.parts['R2'].pins['2'], schema_a.parts['R3'].pins['1']])
        r3_to_split = Net('r3_to_split', pins=[schema_a.parts['R3'].pins['2'], schema_a.parts['U1'].pins['1']])
        u1_to_u2_p = Net('U1_TO_U2_P', pins=[schema_a.parts['U1'].pins['2'], schema_a.parts['U2'].pins['2']])
        u1_to_u2_n = Net('U1_TO_U2_N', pins=[schema_a.parts['U1'].pins['3'], schema_a.parts['U2'].pins['3']])
        u2_open_end = Net('u2_open_end', pins=[schema_a.parts['U2'].pins['1']])
        diff_net = DiffNet(p=u1_to_u2_p, n=u1_to_u2_n, name=u1_to_u2_p.name[:-2])
        self.session.add_all([schema_a, diff_net])
        self.session.commit()
        self.assertEqual(schema_a.diff_nets[0], diff_net)
        schema_b = schema_a.copy('schema_b')
        self.session.add(schema_b)
        self.session.commit()
        parts_count = self.session.query(Part).count()
        schema_b.replace_part('R3',
                              Part('R_0402_22R',
                                   pins=[
                                       Pin('1'),
                                       Pin('2'),
                                   ])
                              )
        self.session.commit()
        self.assertEqual(parts_count, (parts_count := self.session.query(Part).count()))
        schema_c = schema_a.copy('schema_c')
        schema_c.replace_part('R3',
                      Part('R_0402_220R',
                           pins=[
                               Pin('1'),
                               Pin('2'),
                           ])
                      )
        self.session.add(schema_c)
        self.session.commit()
        self.assertEqual(parts_count + len(schema_c.parts), self.session.query(Part).count())


        # test delete_part
        backup_diff_net_count = self.session.query(DiffNet).count()
        backup_net_count = self.session.query(Net).count()
        backup_part_count = self.session.query(Part).count()
        schema_b.delete_part('U2')
        self.session.commit()

        self.assertEqual(backup_diff_net_count, self.session.query(DiffNet).count())
        self.assertEqual(backup_net_count, self.session.query(Net).count() + 1)  # only the net u2_open_end was removed
        self.assertEqual(backup_part_count, self.session.query(Part).count() + 1)

        backup_diff_net_count = self.session.query(DiffNet).count()
        backup_net_count = self.session.query(Net).count()
        backup_part_count = self.session.query(Part).count()
        schema_b.delete_part('U1')
        self.session.commit()

        self.assertEqual(backup_diff_net_count, self.session.query(DiffNet).count() + 1)
        self.assertEqual(backup_net_count, self.session.query(Net).count() + 2)
        self.assertEqual(backup_part_count, self.session.query(Part).count() + 1)

        # test delete_part3
        backup_diff_net_count = self.session.query(DiffNet).count()
        backup_net_count = self.session.query(Net).count()
        backup_part_count = self.session.query(Part).count()
        schema_d = schema_a.copy('schema_d')
        schema_d.delete_part('U2')
        schema_d.delete_part('U1')
        self.session.add(schema_d)
        self.session.commit()

        self.assertEqual(backup_diff_net_count, self.session.query(DiffNet).count())
        self.assertEqual(backup_net_count + 3, self.session.query(Net).count())
        self.assertEqual(backup_part_count + 3, self.session.query(Part).count())

    def test_net_path_signal_path_exception(self):
        schema = self.build_schematic()
        r1_to_r2 = Net('r1_to_r2', pins=[schema.parts['R1'].pins['2'], schema.parts['R2'].pins['1']])
        r2_to_r3 = Net('r2_to_r3', pins=[schema.parts['R2'].pins['2'], schema.parts['R3'].pins['1']])
        r3_to_split = Net('r3_to_split', pins=[schema.parts['R3'].pins['2'], schema.parts['U1'].pins['1'],
                                               schema.parts['U1'].pins['2']])

        net_path1 = NetPath(schema.parts['R1'].pins['2'], schema.parts['R2'].pins['1'])
        net_path2 = NetPath(schema.parts['R2'].pins['2'], schema.parts['R3'].pins['1'])
        net_path3 = NetPath(schema.parts['R3'].pins['2'], schema.parts['U1'].pins['1'])
        net_path4 = NetPath(schema.parts['R3'].pins['2'], schema.parts['U1'].pins['2'])
        net_paths = [net_path1, net_path2, net_path3, net_path4]

        self.assertRaises(InvalidSignalPath, SignalPath, net_paths)

    def test_net_path_signal_path(self):
        schema = self.build_schematic()
        r1_to_r2 = Net('r1_to_r2', pins=[schema.parts['R1'].pins['2'], schema.parts['R2'].pins['1']])
        r2_to_r3 = Net('r2_to_r3', pins=[schema.parts['R2'].pins['2'], schema.parts['R3'].pins['1']])
        r3_to_split = Net('r3_to_split', pins=[schema.parts['R3'].pins['2'], schema.parts['U1'].pins['1'],
                                               schema.parts['U1'].pins['2']])

        net_path1 = NetPath(schema.parts['R1'].pins['2'], schema.parts['R2'].pins['1'])
        net_path2 = NetPath(schema.parts['R2'].pins['2'], schema.parts['R3'].pins['1'])
        net_path3 = NetPath(schema.parts['R3'].pins['2'], schema.parts['U1'].pins['1'])

        valid_path = SignalPath([net_path1, net_path2, net_path3])
        self.session.add(valid_path)
        self.session.commit()

        valid_path2 = SignalPath([
            NetPath(schema.parts['U1'].pins['2'].id, schema.parts['U2'].pins['2'].id),
        ],ignore_validation=True)
        self.session.add(valid_path2)
        self.session.commit()



if __name__ == '__main__':
    unittest.main()
