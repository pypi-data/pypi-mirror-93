import unittest

from ...core.testing import DbTestCase
from ...core.point import Point

from ..textcolordefs import Color, NO_FILL
from ..dbdrawingpieces import DbRect, DbPoint, DbText, DbLine
from ..drawingpieces import Rect, Line
from ..collections import DEFAULT_TEXT, LINE_FORMAT_DEFAULT

# needed to fix sqlalchemy.exc.NoReferencedTableError
from ..dbdrawingcontainers import FlatContainer

class TestDbDrawingPieces(DbTestCase):

    def test_initRect(self):
        r = DbRect(origin=Point(0, 0),
                 width=2,
                 height=10,
                 angle=0,
                 line_format=LINE_FORMAT_DEFAULT,
                 fill=NO_FILL)
        r2 = DbRect(rect=Rect(origin=Point(0, 0),
                 width=2,
                 height=10,
                 angle=0,
                 line_format=LINE_FORMAT_DEFAULT,
                 fill=NO_FILL))
        self.session.add(r)
        self.session.commit()
        print(r)
        print(r.rect)

    def test_initDbPoint(self):
        p = DbPoint(point=Point(0, 0))

        self.session.add(p)
        self.session.commit()
        print(p)
        print(p.point)

    def test_initDbText(self) -> None:
        t = DEFAULT_TEXT
        label = DbText(label=t)
        self.session.add(label)
        self.session.commit()
        print(label)

    def test_DbLine(self):
        line = Line(a=Point(0, 0), b=Point(1, 1), line_format=LINE_FORMAT_DEFAULT)
        dbline = DbLine(line=line)
        self.session.add(dbline)
        self.session.commit()

    def test_CheckConstraint(self):
        line = Line(a=Point(0, 0), b=Point(1, 1), line_format=LINE_FORMAT_DEFAULT._replace(color=Color(255, -1, 0)))
        dbline = DbLine(line=line)
        self.session.add(dbline)
        self.session.commit()


if __name__ == '__main__':
    unittest.main()

