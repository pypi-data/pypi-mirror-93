from typing import NamedTuple, Callable
from pathlib import Path as System_Path
from math import pi, ceil, isclose

from cairo import Context

from ..model.schmodel import PartSymbol
from .drawingmixins import ContainerMixin
from .boundaries import Boundaries
from .cairohelper import setup_cairo_font, PT_TO_MM
from ..drawing.textcolordefs import LineFormat
from ..drawing.drawingpieces import Text, Circle, Path, Rect, Point, Arc, Line
from .textcolordefs import MirrorState
from .helper import mirroring_from_mstate

DEG_90 = 1.5707963267948966


class Sheet(NamedTuple):
    width: float
    height: float
    convert_point:  Callable[[Point], Point]# (x: Point) -> Point
    transform_action: Callable
    scale: float


def set_context_from_line_format(context: Context, sheet: Sheet, line_format: LineFormat):
    """

    :param context:
    :param line_format:
    :return:
    """
    context.set_line_width(sheet.scale*line_format.width)
    context.set_source_rgba(line_format.color.r, line_format.color.g, line_format.color.b, line_format.opacity)
    # todo add linestyle


def draw_rect(context: Context, sheet: Sheet, rect: Rect):
    """

    :param context:
    :param sheet:
    :param rect:
    :return:
    """
    set_context_from_line_format(context, sheet, rect.line_format)
    # origin = sheet.convert_point(rect.origin)
    origin = rect.origin
    normed_angle = (rect.angle + pi/2) % pi -pi/2
    if isclose(normed_angle, 0.0):
        context.rectangle(*sheet.convert_point(Point(origin.x, origin.y)), sheet.scale*rect.width, -sheet.scale*rect.height)
        context.stroke_preserve()
        if rect.fill.opacity:
            context.set_source_rgba(rect.fill.color.r, rect.fill.color.g, rect.fill.color.b,rect.fill.opacity)
            context.fill()
    elif isclose(normed_angle, DEG_90):
        context.rectangle(*sheet.convert_point(Point(origin.x-rect.height, origin.y+rect.width)), sheet.scale*rect.height,
                          sheet.scale*rect.width)
        context.stroke_preserve()
        if rect.fill.opacity:
            context.set_source_rgba(rect.fill.color.r, rect.fill.color.g, rect.fill.color.b, rect.fill.opacity)
            context.fill() # todo reduce this redundancy
    else:
        raise NotImplementedError # Todo work with path


def draw_text(context: Context, sheet: Sheet, text: Text):
    """

    :param context:
    :param sheet:
    :param text:
    :return:
    """
    if text.visible:
        set_context_from_line_format(context, sheet, text.line_format)
        if text.line_format.opacity or text.fill.opacity:
            rect = text.bounding_box
            draw_rect(context, sheet, rect)
        context.set_source_rgb(*text.format.color)
        setup_cairo_font(context, text.format)
        if text.angle:
            font_matrix = context.get_font_matrix()
            font_matrix.rotate(-text.angle)
            context.set_font_matrix(font_matrix)
        context.move_to(*sheet.convert_point(text.fixed_origin))
        context.show_text(text.value)


def draw_line(context: Context, sheet: Sheet, line: Line):
    """

    :param context:
    :param sheet:
    :param line:
    :return:
    """
    set_context_from_line_format(context, sheet, line.line_format)
    context.move_to(*sheet.convert_point(line.a))
    context.line_to(*sheet.convert_point(line.b))
    context.stroke()


def draw_circle(context: Context, sheet: Sheet, circle: Circle):
    """

    :param context:
    :param sheet:
    :param circle:
    :return:
    """
    set_context_from_line_format(context, sheet, circle.line_format)
    context.move_to(*sheet.convert_point(Point(circle.origin.x + circle.radius, circle.origin.y)))
    context.arc(*sheet.convert_point(circle.origin), sheet.scale*circle.radius, 0, 2*pi)
    context.stroke_preserve()
    if circle.fill.opacity:
        context.set_source_rgba(*circle.fill.color, circle.fill.opacity)
        context.fill()

def convert_to_cairo_angles(angle_start: float, angle_end: float):
    start = convert_to_cairo_abs_angle(angle_start)
    end = convert_to_cairo_abs_angle(angle_end)
    return end, start

def convert_to_cairo_abs_angle(angle: float) -> float:
    """
    cairo arc uses angle clockwise direction, in this project angles are defined in counterclockwise direction
    :return:
    """
    # return 2*pi - angle if angle >=0 else -1 * angle
    return -1 * angle


def draw_path(context: Context, sheet: Sheet, path: Path):
    """

    :param context:
    :param sheet:
    :param path:
    :return:
    """
    set_context_from_line_format(context, sheet, path.line_format)

    if isinstance(path.p_or_arc_tuple[0], Arc):
        if path.p_or_arc_tuple[0].backwards_drawn:
            context.move_to(*sheet.convert_point(path.p_or_arc_tuple[0].end_point))
        else:
            context.move_to(*sheet.convert_point(path.p_or_arc_tuple[0].start))
    else:
        new_point = sheet.convert_point(path.p_or_arc_tuple[0])
        context.move_to(*new_point)

    for p in path.p_or_arc_tuple:
        if isinstance(p, Arc):
            if not p.backwards_drawn:
                start = sheet.convert_point(p.start)
                context.line_to(*start)
                end = sheet.convert_point(p.end_point)
            else:
                start = sheet.convert_point(p.end_point)
                context.line_to(*start)
                end = sheet.convert_point(p.start)
            context.move_to(*sheet.convert_point(p.end_point))
            # warning in cairo the drawn angle is between first angle and second angle argument, but the angle is
            # counter clockwise
            cairo_start, cairo_end = convert_to_cairo_angles(p.angle_start, p.angle_end)
            context.arc(*sheet.convert_point(p.origin), sheet.scale*p.radius, cairo_start,
                        cairo_end
                        )
            context.move_to(*end)
        elif isinstance(p, Point):
            context.line_to(*sheet.convert_point(p))
        else:
            raise TypeError('Only Arc and Point are supported in a path')

    if path.closed:
        context.close_path()

    if path.fill.opacity:
        context.set_source_rgba(*path.fill.color, path.fill.opacity)
        context.fill_preserve()
    context.stroke()

DRAW_FUNCTION_MAP = {
    Text: draw_text,
    Circle: draw_circle,
    Path: draw_path,
    Rect: draw_rect,
    Line: draw_line
}


def _convert_transform_action(mirror: MirrorState, rotation: float, old_transform_function) -> Callable:
    def new_transform_function(obj):
        reference = Point(0.0, 0.0)
        obj = old_transform_function(obj)
        obj = obj.rotate(reference, rotation)
        obj = mirroring_from_mstate(obj, mirror, reference)
        return obj
    return new_transform_function


def draw_container(context: Context, sheet: Sheet, container: ContainerMixin):
    """

    :param context:
    :param sheet:
    :param container:
    :return:
    """
    new_sheet = sheet._replace(convert_point=lambda x: sheet.convert_point(x.move(container.origin)),
                               transform_action=_convert_transform_action(container.mirror, container.angle,
                                                                          sheet.transform_action))
    if container.visible:
        for label in container.labels.values():
            if label.visible:
                tuple_dp = new_sheet.transform_action(label.tuple_repr())
                draw_text(context, new_sheet, tuple_dp)
        for dp in container.drawing_pieces:
            tuple_dp = new_sheet.transform_action(dp.tuple_repr())
            DRAW_FUNCTION_MAP[type(tuple_dp)](context, new_sheet, tuple_dp)
        if isinstance(container, PartSymbol):
            for pin in container.pins:
                draw_container(context, new_sheet, pin)
        if hasattr(container, 'children'):
            for child in container.children:
                draw_container(context, new_sheet, child)


def export_container(surface_class, container: ContainerMixin, output_path: System_Path):
    """

    @param surface_class: e.g. PDFSurface, SVGSurface
    @param container:
    @param output_path:
    @return:
    """
    ps = list(container.get_all_points())
    xs = [p.x for p in ps if p is not None]
    ys = [p.y for p in ps if p is not None]
    try:
        b = Boundaries(min(xs), min(ys), max(xs), max(ys))
    except ValueError as e:
        raise e

    scale = 1000 / PT_TO_MM
    v = Point(scale * -b.min_x, scale * -b.min_y)

    def convert_point(point: Point) -> Point:
        return Point(scale * point.x, scale * (b.max_y - (point.y - b.min_y))).move(v)

    def transform_action(obj):
        return obj
    width = ceil(scale*(b.max_x - b.min_x))
    height = ceil(scale*(b.max_y - b.min_y))

    sheet = Sheet(width,
                  height,
                  convert_point,
                  transform_action,
                  scale)

    surface = surface_class(System_Path(output_path).absolute(),
                            width, height)
    cr = Context(surface)
    backup_origin = container.origin
    container.origin = Point(0, 0)
    draw_container(cr, sheet, container)
    container.origin = backup_origin
