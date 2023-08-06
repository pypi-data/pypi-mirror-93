import unittest
import math

from ..drawingpieces import Path, Circle, Arc
from ..textcolordefs import LINE_FORMAT_DEFAULT

from ...core.point import Point
from ...core.test.test_point import PointTestCase


class TestRect(unittest.TestCase):
# TODO
    pass


class TestPath(PointTestCase):

    def assertPathAlmostEqual(self, test_l_or_arc_combo: Path, reference: Path):
        for i, p in enumerate(test_l_or_arc_combo.p_or_arc_tuple):
            for j, f in enumerate(p):
                self.assertAlmostEqual(f, reference.p_or_arc_tuple[i][j])

    def test_functions(self):
        c2 = Path((
            Arc(origin=Point(1, 1), start=Point(1, 0), angle= math.pi*3/2, backwards_drawn=False),
            Point(0, 2),
            Point(1, 0)
        ), False, LINE_FORMAT_DEFAULT, None)

        c2 = c2.rotate(Point(1, 0), -math.pi / 2)
        self.assertPointAlmostEqual(c2.p_or_arc_tuple[0].start, Point(1, 0))
        self.assertPointAlmostEqual(c2.p_or_arc_tuple[0].end_point, Point(2, 1))
        self.assertPointAlmostEqual(c2.p_or_arc_tuple[1], Point(3, 1))
        self.assertPointAlmostEqual(c2.p_or_arc_tuple[2], Point(1, 0))

        c1 = Path((
            Point(-1, -1),
            Point(-4, 0),
            Arc(Point(-3, 0), Point(-3, 1), math.pi/2, False),
            Point(0, 0),
            Point(-1, -1)
        ), False, LINE_FORMAT_DEFAULT, None)

        c2 = Path(tuple((
            Arc(origin=Point(1, 1), start=Point(1, 0), angle=math.pi * 3 / 2, backwards_drawn=False),
            Point(0, 2),
            Point(1, 0)
        )), False, LINE_FORMAT_DEFAULT, None).move(Point(1, 1))
        self.assertPathAlmostEqual(c2, Path((
            Arc(origin=Point(2, 2), start=Point(2, 1), angle=math.pi * 3 / 2, backwards_drawn=False),
            Point(1, 3),
            Point(2, 1)
        ), False, c2.line_format, None))

        c1.get_p()


class TestCircle(PointTestCase):

    def test_functions(self):
        c = Circle(Point(1, 2), 1.2, None, None)
        c = c.rotate(Point(0, 0), -math.pi / 2)
        self.assertPointAlmostEqual(c.origin, Point(2, -1))
        c = c.move(Point(1, 2.2))
        self.assertPointAlmostEqual(c.origin, Point(3, 1.2))

# TODO write test for text


if __name__ == '__main__':
    unittest.main()
