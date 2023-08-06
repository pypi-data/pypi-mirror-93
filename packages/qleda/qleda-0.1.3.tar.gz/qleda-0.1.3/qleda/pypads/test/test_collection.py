import unittest

from ...core.testing import DbTestCase
from ..collection import _create_pin_short


class TestSchPin(DbTestCase):

    def test_create_pin_short(self):
        p = _create_pin_short()
        self.session.add(p)
        self.session.commit()
        print(p)
        print(p.labels)
        p.designator = '2'
        print(p)
        print(p.labels)


if __name__ == '__main__':
    unittest.main()
