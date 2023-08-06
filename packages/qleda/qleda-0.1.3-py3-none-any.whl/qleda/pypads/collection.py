from ..common.units import create_conversion_to_m, UnitOfLength
from ..drawing.drawingpieces import Line, Text
from ..core.point import Point
from ..drawing.textcolordefs import LineStyle, JustHorziontal, \
    JustVertical, BLACK as C_BLACK, NO_FILL, LineFormat, TextFormat, \
    LINE_FORMAT_DEFAULT
from ..model.schmodel import SchPin
from ..drawing.dbdrawingpieces import DbText, DbLine

EMPTY_PIN_SYMBOL = 'PINEMPTY'

PADS_HEIGHT_TO_POINT = 4058
mils_to_mm = create_conversion_to_m(UnitOfLength.mil)

_NAME_LABEL = Text(
    origin=Point(mils_to_mm(140), mils_to_mm(10)),
    value='',
    format=TextFormat(
        fontsize=round(10 * PADS_HEIGHT_TO_POINT),
        font="Regular Segoe UI",
        horizontal=JustHorziontal.start,
        vertical=JustVertical.middle,
        bold=False,
        italic=False,
        underline=False,
        strikethrough=False,
        color=C_BLACK
    ),
    line_format=LINE_FORMAT_DEFAULT,
    fill=NO_FILL,
    angle=0,
    visible=True
)
_DESIGNATOR_LABEL = Text(
    origin=Point(mils_to_mm(60), mils_to_mm(20)),
    value='',
    format=TextFormat(
        fontsize=round(10 * PADS_HEIGHT_TO_POINT),
        font="Regular Segoe UI",
        horizontal=JustHorziontal.end,
        vertical=JustVertical.bottom,
        bold=False,
        italic=False,
        underline=False,
        strikethrough=False,
        color=C_BLACK
    ),
    line_format=LINE_FORMAT_DEFAULT,
    fill=NO_FILL,
    angle=0,
    visible=True
)
_NET_NAME_LABEL = Text(
    origin=Point(mils_to_mm(-70), mils_to_mm(10)),
    value='',
    format=TextFormat(
        fontsize=round(10 * PADS_HEIGHT_TO_POINT),
        font="Regular Segoe UI",
        horizontal=JustHorziontal.end,
        vertical=JustVertical.bottom,
        bold=False,
        italic=False,
        underline=False,
        strikethrough=False,
        color=C_BLACK
    ),
    line_format=LINE_FORMAT_DEFAULT,
    fill=NO_FILL,
    angle=0,
    visible=True
)


def _create_pin_short() -> SchPin:

    p = SchPin(drawing_pieces=[DbLine(
        line=Line(Point(0, 0), Point(mils_to_mm(100), 0), LineFormat(LineStyle.solid, mils_to_mm(10), C_BLACK, 1.0)))])
    p.set_attribute_and_label('designator', _DESIGNATOR_LABEL)
    p.set_attribute_and_label('name', _NAME_LABEL)
    p.labels['net_name'] = DbText.create_by_label(_NET_NAME_LABEL, False, key='net_name')
    return p


def _create_pin_empty() -> SchPin:
    p = SchPin()
    p.set_attribute_and_label('designator', _DESIGNATOR_LABEL)
    p.set_attribute_and_label('name', _NAME_LABEL)
    p.labels['net_name'] = DbText.create_by_label(_NET_NAME_LABEL, False, key='net_name')

    return p

PIN_DECALS = {
    'PINSHORT': _create_pin_short(),
    EMPTY_PIN_SYMBOL: _create_pin_empty()
}