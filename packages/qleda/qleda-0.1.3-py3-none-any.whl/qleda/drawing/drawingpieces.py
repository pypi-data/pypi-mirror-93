import math
from typing import NamedTuple, Tuple
from math import cos, sin, pi, isclose

from ..core.dbnamedtuple import DbNamedTuple

from ..core.point import Point
from .textcolordefs import LineStyle, JustHorziontal, JustVertical, Color, Fill, \
    LINE_STYLE_DEFAULT_COLOR, LineFormat, TextFormat
from .cairohelper import font_extents, text_extents, FontExtentsCairo, TextExtentsCairo

NO_LINE = LineFormat(LineStyle.no_line, 0, LINE_STYLE_DEFAULT_COLOR, 1)
DEFAULT_TEXT_BOUNDINGBOX_LINE = NO_LINE


class Path(DbNamedTuple):
    """
           A Path combines Point with Arc to one object.
           The connection between a point and an Arc is defined by the backwards_drawn attribute of the Arc.

           The bool closed defines if the path has to be closed or not.

       """
    p_or_arc_tuple: tuple # types only Arc and Point
    closed: bool
    line_format: LineFormat
    fill: Fill

    def move(self, vector: Point) -> 'Path':
        """
        returns the moved Path
        :param vector:
        :return:
        """
        return Path(tuple(p.move(vector) for p in self.p_or_arc_tuple), self.closed, self.line_format, self.fill)

    def rotate(self, reference_point: Point, angle: float) -> 'Path':
        """
        returns the rotated arc, arc is rotated around reference point
        :param reference_point:
        :param angle: angle in radians
        :return:
        """
        return Path(tuple(p.rotate(reference_point, angle) for p in self.p_or_arc_tuple), self.closed,
                    self.line_format, self.fill)

    def get_p(self) -> tuple:
        """
        function returns a tuple with all points of the object
        :return:
        """
        return tuple([p for point in self.p_or_arc_tuple for p in point.get_p()])

    # TODO add test
    def x_mirror(self, reference_point: Point) -> 'Path':
        """
        :param reference_point:
        :return:
        """
        return self._replace(p_or_arc_tuple=tuple([x.x_mirror(reference_point) for x in self.p_or_arc_tuple]))

    # TODO add test
    def y_mirror(self, reference_point: Point) -> 'Path':
        """
        :param reference_point:
        :return:
        """
        return self._replace(p_or_arc_tuple=tuple([x.y_mirror(reference_point) for x in self.p_or_arc_tuple]))

    # TODO add test
    def x_y_mirror(self, reference_point: Point) -> 'Path':
        """
        mirrors self on the reference point
        :param reference_point:
        :return:
        """
        return self._replace(p_or_arc_tuple=tuple([x.x_y_mirror(reference_point) for x in self.p_or_arc_tuple]))


class Rect(DbNamedTuple):
    """
        A rect has a width and a height.
        The origin of the rect is always at the bottom left of the rectangle.
        The points of the rectangle are numbered counterclockwise. index 0 is at origin, index 1 at bottom right ...
        The angle of the rect is defined between the first line and the x-axis.

        The Rect also has a line format and a fill. Those values can be None if not used.
    """
    origin: Point
    width: float
    height: float
    angle: float
    line_format: LineFormat
    fill: Fill

    def move(self, vector: Point):
        """
            returns a moved rect
            :param vector:
            :return:
        """
        return Rect(self.origin.move(vector), self.width, self.height, self.angle, self.line_format, self.fill)

    def rotate(self, reference_point: Point, angle: float, include_all_edges: bool = True):
        """
        returns a rotated rect
        :param reference_point:
        :param angle: angle in radians
        :param include_all_edges:   True all edges are rotated (angle is added to internal angle)
                                    False only origin gets rotated
        :return:
        """
        if include_all_edges:
            return Rect(self.origin.rotate(reference_point, angle), self.width, self.height, self.angle + angle,
                        self.line_format, self.fill)
        else:
            return Rect(self.origin.rotate(reference_point, angle), self.width, self.height, self.angle,
                        self.line_format, self.fill)

    @property
    def points(self):
        """

        :return: points tuple from 0:3 counterclockwise starting at origin. origin is always 0.
        """
        b = Point(self.origin.x + cos(self.angle) * self.width,
                  self.origin.y + sin(self.angle) * self.width)
        return (
            self.origin, b,
            Point(b.x + cos(self.angle + pi / 2) * self.height,
                  self.origin.y + sin(self.angle) * self.width),
            Point(self.origin.x + cos(self.angle + pi / 2) * self.height,
                  self.origin.y + sin(self.angle + pi / 2) * self.height)
        )

    def get_p(self) -> tuple:
        """
        function returns a list with all points of the object
        :return:
        """
        return self.points

    # TODO add test
    def x_mirror(self, reference_point: Point) -> 'Rect':
        """
        :param reference_point:
        :return:
        """
        return self._replace(origin=self.origin.x_mirror(reference_point), height=-self.height)

    # TODO add test
    def y_mirror(self, reference_point: Point) -> 'Rect':
        """
        :param reference_point:
        :return:
        """
        return self._replace(origin=self.origin.y_mirror(reference_point), width=-self.width)

    # TODO add test
    def x_y_mirror(self, reference_point: Point) -> 'Rect':
        """
        mirrors self on the reference point
        :param reference_point:
        :return:
        """
        return self._replace(origin=self.origin.x_y_mirror(reference_point), width=-self.width, height=-self.height)


class Line(DbNamedTuple):
    """
        A line has two points, we call them a and b.
        A line has also a LineFormat
    """

    a: Point
    b: Point
    line_format: LineFormat

    def move(self, vector: Point) -> 'Line':
        """
            returns a moved Line
            :param vector:
            :return: moved line
        """
        return Line(self.a.move(vector), self.b.move(vector), self.line_format)

    def rotate(self, reference_point: Point, angle: float) -> 'Line':
        """
        returns a rotated line
        :param reference_point:
        :param angle: angle in radians
        :return:
        """
        return Line(self.a.rotate(reference_point, angle), self.b.rotate(reference_point, angle),
                    self.line_format)

    @property
    def length(self) -> float:
        """
        :return: length of line
        """
        return self.a.distance(self.b)

    def get_p(self) -> tuple:
        """
        function returns a tuple with all points of the object
        :return:
        """
        return tuple([self.a, self.b])

    @property
    def angle(self):
        """
        angle between point a and b
        :return:
        """
        return self.a.angle(self.b)

    # TODO add test
    def x_mirror(self, reference_point: Point) -> 'Line':
        """
        :param reference_point:
        :return:
        """
        return self._replace(a=self.a.x_mirror(reference_point), b=self.b.x_mirror(reference_point))

    # TODO add test
    def y_mirror(self, reference_point: Point) -> 'Line':
        """
        :param reference_point:
        :return:
        """
        return self._replace(a=self.a.y_mirror(reference_point), b=self.b.y_mirror(reference_point))

    # TODO add test
    def x_y_mirror(self, reference_point: Point) -> 'Line':
        """
        mirrors self on the reference point
        :param reference_point:
        :return:
        """
        return self._replace(a=self.a.x_y_mirror(reference_point), b=self.b.x_y_mirror(reference_point))


class Circle(DbNamedTuple):
    """
        Circle has an origin and a radius.

        The Circle also has a line format and a fill. Those values can be None if not used.
    """
    origin: Point
    radius: float
    line_format: LineFormat
    fill: Fill

    def move(self, vector: Point) -> 'Circle':
        """
            returns a moved circle
            :param vector:
            :return:
        """
        return Circle(self.origin.move(vector), self.radius, self.line_format, self.fill)

    def rotate(self, reference_point: Point, angle: float) -> 'Circle':
        """
        returns a rotated circle
        :param reference_point:
        :param angle: angle in radians
        :return:
        """
        return Circle(self.origin.rotate(reference_point, angle), self.radius, self.line_format, self.fill)

    def get_p(self) -> tuple:
        """
        function returns a tuple with all points of the object
        :return:
        """
        return tuple([Point(self.origin.x-self.radius, self.origin.y-self.radius),
                      Point(self.origin.x+self.radius, self.origin.y+self.radius)])

    # TODO add test
    def x_mirror(self, reference_point: Point) -> 'Circle':
        """
        :param reference_point:
        :return:
        """
        return self._replace(origin=self.origin.x_mirror(reference_point))

    # TODO add test
    def y_mirror(self, reference_point: Point) -> 'Circle':
        """
        :param reference_point:
        :return:
        """
        return self._replace(origin=self.origin.y_mirror(reference_point))

        # TODO add test
    def x_y_mirror(self, reference_point: Point) -> 'Circle':
        """
        mirrors self on the reference point
        :param reference_point:
        :return:
        """
        return self._replace(origin=self.origin.x_y_mirror(reference_point))


# TODO rename to Label
class Text(DbNamedTuple):
    """
        A Text has a text (string) a format, and an origin.
        The origin depends on the Justification.
        Ideas were taken from: http://www.tortall.net/mu/wiki/CairoTutorial#line-width

        Justification Horizontal:
            start:  the x coordinate of the origin is on the start of the first letter
            middle: the x coordinate is in the middle of the text.
            end:    the x coordinate is at the end of the last character.

        Justification Vertical:
            top:    the y coordinate is at the top of the highest character
            middle: the y coordinate is in the middle (from ascent to baseline)

    """
    origin: Point
    value: str
    format: TextFormat
    line_format: LineFormat
    fill: Fill
    angle: float  # angle to the x-Axis of the origin in radians
    visible: bool

    def move(self, vector: Point) -> 'Text':
        """
        returns the moved Text
        :param vector:
        :return:
        """
        return Text(self.origin.move(vector), self.value, self.format, self.line_format, self.fill, self.angle,
                    self.visible)

    def rotate(self, reference_point: Point, angle: float, include_text_direction: bool = True) -> 'Text':
        """
        returns the rotated Text, Text is rotated around reference point
        :param reference_point:
        :param angle: angle in radians
        :param include_text_direction: True: texts direction is also rotated. False: only the origin is rotated
        :return: rotated Text
        """
        return Text(self.origin.rotate(reference_point, angle), self.value, self.format, self.line_format, self.fill,
                    self.angle + angle if include_text_direction else self.angle, self.visible)

    @property
    def fixed_origin(self):
        """
        the fixed_origin is always at Bottom left on the center line (like in cairo)
        the origin attributes depends on the justification
        :return: internal_origin used for other tools
        """
        fontextends = font_extents(self.format)  # type: FontExtentsCairo
        textenxtends = text_extents(self.value, self.format)  # type: TextExtentsCairo
        if self.format.horizontal == JustHorziontal.start:
            x = self.origin.x
        elif self.format.horizontal == JustHorziontal.middle:
            x = self.origin.x - textenxtends.width / 2
        elif self.format.horizontal == JustHorziontal.end:
            x = self.origin.x - textenxtends.width
        else:
            raise ValueError
        if self.format.vertical == JustVertical.bottom:
            y = self.origin.y
        elif self.format.vertical == JustVertical.middle:
            y = self.origin.y - fontextends.fascent / 2
        elif self.format.vertical == JustVertical.top:
            y = self.origin.y - fontextends.fascent
        else:
            raise ValueError
        return Point(x, y).rotate(self.origin, self.angle)

    @property
    def bounding_box(self):
        """

        :return: rect surrounding of text
        """
        textenxtends = text_extents(self.value, self.format)  # type: TextExtentsCairo
        fo = self.fixed_origin
        return Rect(Point(fo.x + textenxtends.xbearing, fo.y - textenxtends.height - textenxtends.ybearing),
                    textenxtends.width,
                    textenxtends.height,
                    self.angle,
                    self.line_format,
                    self.fill)

    def get_p(self) -> tuple:
        """
        function returns a tuple with all points of the object
        :return:
        """
        return self.bounding_box.get_p()

    def rename(self, text) -> 'Text':
        """

        @param text:
        @return:
        """
        return Text(self.origin, text, self.format, self.line_format, self.fill, self.angle, self.visible)

    def _justification_mirroring(self, x: bool, y: bool)-> Tuple[JustHorziontal, JustVertical]:
        hor = self.format.horizontal
        ver = self.format.vertical
        if isclose(self.angle, pi/2):
            x = not x
            y = not y
        if x:
            if hor == JustHorziontal.start:
                hor = JustHorziontal.end
            elif hor == JustHorziontal.end:
                hor = JustHorziontal.start

        if y:
            if ver == JustVertical.bottom:
                ver = JustVertical.top
            elif ver == JustVertical.top:
                ver = JustVertical.bottom
        return hor, ver

    # TODO add test
    def x_mirror(self, reference_point: Point, x_mirror_justification: bool = True, y_mirror_justification: bool = False) -> 'Text':
        """
        The text itself is not mirrored. May supported in future.
        :param reference_point:
        :param x_mirror_justification:
        :return:Text
        """

        hor, ver = self._justification_mirroring(x_mirror_justification, y_mirror_justification)
        return self._replace(origin=self.origin.x_mirror(reference_point), format=self.format._replace(horizontal=hor, vertical=ver))

    # TODO add test
    def y_mirror(self, reference_point: Point, x_mirror_justification: bool = False,
                 y_mirror_justification: bool = True) -> 'Text':
        """
        The text itself is not mirrored. May supported in future.
        :param reference_point:
        :param y_mirror_justification:
        :return:
        """
        hor, ver = self._justification_mirroring(x_mirror_justification, y_mirror_justification)
        return self._replace(origin=self.origin.y_mirror(reference_point),
                             format=self.format._replace(horizontal=hor, vertical=ver))

        # TODO add test
    def x_y_mirror(self, reference_point: Point, x_mirror_justification: bool = True,
                 y_mirror_justification: bool = True) -> 'Text':
        """
        mirrors self on the reference point
        The text itself is not mirrored. May supported in future.
        :param reference_point:
        :param mirror_justification:
        :return:
        """
        hor, ver = self._justification_mirroring(x_mirror_justification, y_mirror_justification)
        return self._replace(origin=self.origin.x_y_mirror(reference_point),
                             format=self.format._replace(horizontal=hor, vertical=ver))

    def __str__(self) -> str:
        return self.value


def fix_angle(angle):
    """
    takes angle and gives an output in range -pi to pi
    :param angle:
    :return:
    """
    a = angle % (2 * math.pi)
    return a if a <= math.pi else a - 2 * math.pi


class Arc(DbNamedTuple):
    """
        An Arc is defined by its origin, the start point and the angle.
        The angle is defined counterclockwise from the starting point to the origin.
        The backwards_drawn attributes defines in which direction the arc is drawn.
            True: the Arc is drawn from end_point() to start
            False: the Arc is drawn from start to end_point()
    """
    origin: Point
    start: Point
    angle: float
    backwards_drawn: bool

    def move(self, vector: Point) -> 'Arc':
        """
        returns the moved Arc
        :param vector:
        :return:
        """
        return Arc(self.origin.move(vector), self.start.move(vector), self.angle, self.backwards_drawn)

    def rotate(self, reference_point: Point, angle: float) -> 'Arc':
        """
        returns the rotated arc, arc is rotated around reference point
        :param reference_point:
        :param angle: angle in radians
        :return:
        """
        return Arc(self.origin.rotate(reference_point, angle), self.start.rotate(reference_point, angle), self.angle,
                   self.backwards_drawn)

    @property
    def radius(self) -> float:
        """
        returns radius of the given arc
        :return: radius
        """
        return self.origin.distance(self.start)

    @property
    def angle_start(self) -> float:
        """
        returns the angle of the start point relative to x-axis
        :return: angle to x-axis
        """
        return fix_angle(self.origin.angle(self.start))

    @property
    def angle_end(self) -> float:
        """
        returns the angle of the end point relative to x-axis
        :return: angle to x-axis
        """
        return fix_angle(self.angle_start + self.angle)

    @property
    def end_point(self) -> Point:
        """
        returns the Arcs end Point
        :return:
        """
        a_end = self.angle_end
        r = self.radius
        return self.origin.move(Point(math.cos(a_end)*r, math.sin(a_end)*r))

    def get_p(self) -> tuple:
        """
        function returns a tuple with all points of the object
        :return:
        """
        r = self.radius
        return tuple([Point(self.origin.x - r, self.origin.y - r),
                      Point(self.origin.x + r, self.origin.y + r)])

    # TODO add test
    def x_mirror(self, reference_point: Point) -> 'Arc':
        """
        :param reference_point:
        :return:
        """
        return self._replace(origin=self.origin.x_mirror(reference_point), start=self.start.x_mirror(reference_point),
                             angle=fix_angle(-self.angle))

    # TODO add test
    def y_mirror(self, reference_point: Point) -> 'Arc':
        """
        :param reference_point:
        :return:
        """
        return self._replace(origin=self.origin.y_mirror(reference_point), start=self.start.y_mirror(reference_point),
                             angle=fix_angle(-self.angle))

    # TODO add test
    def x_y_mirror(self, reference_point: Point) -> 'Arc':
        """
        mirrors self on the reference point
        :param reference_point:
        :return:
        """
        return self._replace(origin=self.origin.y_mirror(reference_point), start=self.start.y_mirror(reference_point))