import unittest
from math import pi

from ...core.point import Point
from ..drawingpieces import Path, Arc
from .test_drawingpieces import TestPath


class MyTestCase(TestPath):

    def test_functions(self):
        p1 = Path(tuple([Point(1, 0),
                         Arc(Point(1, 1), Point(1, 0), 3*pi/2, False),
                         Point(0, 2),
                         Point(1, 0)]), False, None, None)
        p2 = Path(tuple([
            Point(0, 0),
            Point(-1, 1),
            Point(0, 2),
            Point(1, 1)
        ]), False, None, None)
        p3 = Path(tuple([
            Point(0, -3),
            Point(-1, -3)
        ]), False, None, None)


if __name__ == '__main__':
    unittest.main()
