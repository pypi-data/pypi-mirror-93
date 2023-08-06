import unittest
from typing import NamedTuple
from ..dbnamedtuple import DbNamedTuple

class TestBla(NamedTuple):
    a: str
    b: str

class TestDbNamedTuple0(DbNamedTuple):
    a: str
    b: str


class TestDbNamedTuple1(DbNamedTuple):
    a: str
    b: str
    c: int


class TestNested(DbNamedTuple):
    bla: str
    test_db_named_tuple_0: TestDbNamedTuple0


class TestNested2(DbNamedTuple):
    a: TestNested
    my_str: str
    b: TestNested


def ret_tuple():
    return 'a', 'b'


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        # self.test = TestNamedTuple('a', 'b')
        self.inst_a = TestDbNamedTuple0('inst_a: a', 'inst_a: b')
        self.inst_b = TestDbNamedTuple0('inst_b: a', 'inst_b: b')
        self.inst_c = TestDbNamedTuple1('inst_c: a', 'inst_c: b', 2)
        self.nested = TestNested('bla', TestDbNamedTuple0('n_a', 'n_b'))
        self.nested2 = TestNested2(TestNested('bla', TestDbNamedTuple0('n_a', 'n_b')),
                                   'hihi',
                                   TestNested('blu', TestDbNamedTuple0('n_a', 'n_b')))

    def test_DbNamedTuple(self):
        self.assertEqual(self.inst_a.__composite_values__(), ('inst_a: a', 'inst_a: b'))
        self.assertEqual(self.inst_b.__composite_values__(), ('inst_b: a', 'inst_b: b'))
        self.assertEqual(self.inst_c.__composite_values__(), ('inst_c: a', 'inst_c: b', 2))
        self.assertEqual(self.nested.__composite_values__(), ('bla', 'n_a', 'n_b'))
        self.assertEqual(self.nested, TestNested._generate_from_row('bla', 'n_a', 'n_b'))
        self.assertEqual(self.nested2, TestNested2._generate_from_row('bla', 'n_a', 'n_b', 'hihi', 'blu', 'n_a', 'n_b'))


if __name__ == '__main__':
    unittest.main()
