import unittest
import math
from ..point import Point


class PointTestCase(unittest.TestCase):

    def assertPointAlmostEqual(self, test_point: Point, reference_point: Point):
        self.assertAlmostEqual(test_point.x, reference_point.x)
        self.assertAlmostEqual(test_point.y, reference_point.y)


class TestNewPoint(PointTestCase):

    def test_rotate(self):
        a = Point(0,1)
        ref = Point(1,1)

        c = a.rotate(ref, -math.pi/2)
        self.assertPointAlmostEqual(c, Point(1,2))

        a = Point(0, 1)
        c = a.rotate(ref, math.pi / 2)
        self.assertPointAlmostEqual(c, Point(1, 0))

    def test_distance(self):
        a = Point(0,0)
        b = Point(1,1)
        self.assertAlmostEqual(a.distance(b), math.sqrt(2))

    def test_move(self):
        a = Point(2,0)
        b = Point(1,1)
        self.assertPointAlmostEqual(a.move(b), Point(3,1))

    def test_angle(self):
        a = Point(1, 1)
        b = Point(2, 2)
        self.assertAlmostEqual(math.pi/4, a.angle(b))

    def test_x_mirror(self):
        a = Point(2, 1)
        ref = Point(1, -1)
        self.assertPointAlmostEqual(a.x_mirror(ref), Point(0, 1))

    def test_y_mirror(self):
        a = Point(2, 1)
        ref = Point(1, -1)
        self.assertPointAlmostEqual(a.y_mirror(ref), Point(2, -3))

    def test_x_y_mirror(self):
        a = Point(2, 1)
        ref = Point(1, -1)
        self.assertPointAlmostEqual(a.x_y_mirror(ref), Point(0, -3))


if __name__ == '__main__':
    unittest.main()
