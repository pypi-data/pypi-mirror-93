from typing import Tuple, Union
from .drawingpieces import Text
from .textcolordefs import DEFAULT_TEXT_FORMAT, NO_FILL, LINE_FORMAT_DEFAULT

from ..core.point import Point

DEFAULT_TEXT = Text(
    origin=Point(0,0),
    value='',
    format=DEFAULT_TEXT_FORMAT,
    line_format=LINE_FORMAT_DEFAULT,
    fill=NO_FILL,
    angle=0,
    visible=False
)


def create_text_by_string_or_text(text: Union[str, Text]) -> Tuple[str, Text]:
    if type(text) == Text:
        return text.value, text
    return text, DEFAULT_TEXT._replace(value=text)


EMPTY_TEXT = Text(
            origin=Point(0, 0),
            value='',
            format=DEFAULT_TEXT_FORMAT,
            line_format=LINE_FORMAT_DEFAULT,
            fill=NO_FILL,
            angle=0,
            visible=False
    )