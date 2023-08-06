import unittest
import math

from ...core.point import Point
from ...core.test.test_point import PointTestCase

from ..drawingpieces import Arc


class TestArc(PointTestCase):

    def test_functions(self):
        a = Arc(Point(1, 1), Point(0, 1), 0.5*math.pi, False)
        self.assertAlmostEqual(1.0, a.radius)
        self.assertAlmostEqual(math.pi, a.angle_start)
        self.assertAlmostEqual(-math.pi/2, a.angle_end)
        self.assertPointAlmostEqual(a.end_point, Point(1,0))

        a = a.rotate(Point(0,1), math.pi)
        self.assertPointAlmostEqual(a.origin, Point(-1, 1))
        self.assertPointAlmostEqual(a.start, Point(0, 1))
        self.assertPointAlmostEqual(a.end_point, Point(-1, 2))

        a = a.move(Point(1, 0))
        self.assertPointAlmostEqual(a.origin, Point(0, 1))
        self.assertPointAlmostEqual(a.start, Point(1, 1))
        self.assertPointAlmostEqual(a.end_point, Point(0, 2))
        self.assertAlmostEqual(a.angle, 0.5*math.pi)


if __name__ == '__main__':
    unittest.main()