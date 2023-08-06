import unittest
import math

from sqlalchemy.exc import IntegrityError


from ...core.testing import DbTestCase
from ...core.point import Point


from ..textcolordefs import NO_FILL, LINE_FORMAT_DEFAULT
from ..dbdrawingcontainers import DbSimplePath, DbSimplePathMember, DrawingContainer
from ..collections import EMPTY_TEXT
from ..dbdrawingpieces import DbPoint, DbDrawingPiece, DbText
from ..drawingpieces import Arc, Path as SimplePath


class TestDbSimplePathMember(DbTestCase):

    def test_init(self) -> None:
        p1 = Point(-1, -1)
        simple_path_member = DbSimplePathMember(
            dp=DbPoint(point=p1)
        )
        self.session.add(simple_path_member)
        self.session.commit()


def _build_simple_path() -> DbSimplePath:
    members = [Point(-1, -1),
               Point(-4, 0),
               Arc(Point(-3, 0), Point(-3, 1), math.pi / 2, False),
               Point(0, 0),
               Point(-1, -1)]
    simple_path = DbSimplePath(
        members=members,
        closed=False,
        line_format=LINE_FORMAT_DEFAULT,
        fill=NO_FILL,
    )
    return simple_path


def _build_simple_path2() -> DbSimplePath:
    s = SimplePath(tuple([Point(-1, -1),
                          Point(-4, 0),
                          Arc(Point(-3, 0), Point(-3, 1), math.pi / 2, False),
                          Point(0, 0),
                          Point(-1, -1)]),
                   closed=False,
                   line_format=LINE_FORMAT_DEFAULT,
                   fill=NO_FILL,
                   )
    return DbSimplePath.create_by_simple_path(s)


class TestDbSimplePath(DbTestCase):

    def test_init(self) -> None:
        p = _build_simple_path()
        p2 = _build_simple_path2()
        self.session.add_all([p, p2])
        self.session.commit()
        print(p)


class TestDrawingContainer(DbTestCase):

    def test_init(self) -> None:
        c1 = DrawingContainer(drawing_pieces=[_build_simple_path2(), _build_simple_path2()])
        c2 = DrawingContainer(children=[c1])
        test_origin = DrawingContainer(origin=Point(1, 1))
        self.session.add(c2)
        self.session.add(test_origin)
        self.session.commit()
        print(c2)
        print(test_origin)

    def test_unique_key_labels(self) -> None:
        dp1 = DbDrawingPiece()
        dp2 = DbDrawingPiece()
        c1 = DrawingContainer(drawing_pieces=[dp1, dp2])

        self.session.add_all([dp1, dp2])
        self.session.commit()

        dp3 = DbText(key='dp3', label=EMPTY_TEXT)
        dp4 = DbText(key='dp4', label=EMPTY_TEXT)
        c1.labels = {l.key: l for l in [dp3, dp4]}
        self.session.commit()

        dp5 = DbText(key='dp5', label=EMPTY_TEXT, container=c1)
        dp_fake_5 = DbText(key='dp5', label=EMPTY_TEXT, container=c1)
        self.assertRaises(IntegrityError, self.session.commit)

    def test_create_label_for_attribute(self) -> None:
        c1 = DrawingContainer(angle=10)
        c1.create_dblabel_for_attribute('angle', EMPTY_TEXT)
        self.session.add(c1)
        self.session.commit()
        dblabel = c1.labels['angle']
        self.assertEqual(str(c1.angle), dblabel.label.value)
        print(dblabel)
        self.assertEqual(c1, dblabel.container)
        self.assertRaises(KeyError, c1.labels.__getitem__, 'bla')


    def test_set_attribute_and_label(self) -> None:
        c1 = DrawingContainer(angle=10)
        self.assertRaises(TypeError, c1.set_attribute_and_label, EMPTY_TEXT._replace(value='20'))


if __name__ == '__main__':
    unittest.main()

