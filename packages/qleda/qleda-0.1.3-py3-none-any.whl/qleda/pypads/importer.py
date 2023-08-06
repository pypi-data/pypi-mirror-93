from pathlib import Path
from typing import List, Dict
from collections import deque
import logging
import shlex
from math import radians, sin, cos, sqrt
from copy import deepcopy
from typing import Union
from re import search as re_search

from ..core.point import Point
from ..model.basic import Pin, Part, PartLibrary, Schematic, Net
from ..model.schmodel import PartSymbol, SymbolLibrary, SchPin, NetConnector, SchRepresentation, Gate
from ..drawing.drawingpieces import Text, Arc, Circle
from ..drawing.dbdrawingpieces import DbText, DbCircle
from ..drawing.dbdrawingcontainers import DbSimplePath
from ..drawing.textcolordefs import JustVertical, JustHorziontal, LineStyle, Fill, NO_FILL, LineFormat, TextFormat, \
    NO_LINE, BLACK as C_BLACK
from ..drawing.collections import EMPTY_TEXT
from ..drawing.textcolordefs import MirrorState
from ..common.units import UnitOfLength, create_conversion_to_m

from .collection import PIN_DECALS, EMPTY_PIN_SYMBOL
from .padshelper import read_timestamp
from .filestructures import SchLibHeaderInformation, Mirror, PADS_TERMINAL_MIRROR_MAP, \
    PadsPieceEntryHeader, PartLibHeaderInformation, PadsPartType, PadsHeaderLine, PadsGateDecalLine, PADS_PINTYPE_MAP, \
    PinType, PART_ITEMS, SIGNAL, MISC
from .constants import PADS_FILE_ENCODING, PADS_DESIGNATOR_KEY,  PADS_NAME_KEY, VALID_PADS_PINDECAL, DEF_PIECE_ENTRY_TYPES

logger = logging.getLogger(__name__)

MILS_TO_POINT = 0.072


# TODO use Common/Units.py
def mils_to_m(length: float) -> float:
    """

    """
    return float(length) * 2.54e-5


def point_mils_to_m(p_mils: Point) -> Point:
    """

    """
    return Point(mils_to_m(p_mils.x), mils_to_m(p_mils.y))

_DEFAULT_TXT_HEIGHT = 90
_DEFAULT_LINE_WIDTH = 10

def _pads_font_info_to_text_format(text_height: str, text_line_width: str, text_font: str,
                                   just_hor: JustHorziontal = JustHorziontal.start,
                                   just_vert: JustVertical = JustVertical.bottom) -> TextFormat:
    """

    """
    text_height = float(text_height)
    if not (10 <= text_height <= 1000):
        logger.warning('text height has to be between 10 and 1000, was {}. Now set to {}'.format(text_height,
                                                                                                 _DEFAULT_TXT_HEIGHT))
        text_height = _DEFAULT_TXT_HEIGHT  # PADS is not that strict with this value
    fontsize = round(text_height * MILS_TO_POINT)

    text_line_width = float(text_line_width)
    if not (1 <= text_line_width <= 50):
        logger.warning('line width has to be between 1 and 50, was {}. Now set to {}'.format(text_line_width,
                                                                                             _DEFAULT_LINE_WIDTH))
        text_line_width = _DEFAULT_LINE_WIDTH

    designator_line_width = text_line_width * MILS_TO_POINT
    bold = True if float(fontsize) / designator_line_width > 1 / 6 else False
    return TextFormat(fontsize, text_font, just_hor, just_vert,
                      bold, False, False, False, C_BLACK)


def read_header_lines(first_four_lines: list, from_schematic: bool = False) -> SchLibHeaderInformation:
    """The schematic decal header consists of four lines.
        First line format:
        name x y pnhgt pnwid pnmhgt pnmwid labels pieces txt terminals vis (library)
        name x y pnhgt pnwid pnmhgt pnmwid labels pieces txt terminals vis ?? (schematic)


        Second line format:
        TIMESTAMP year.month.day.hour.minute.second

        Third line format:
        fontinfo

        Fourth line format:
        fontinfo

        Where:

        name: User-defined decal name Values can be up to 40 alphanumeric characters.

        x, y: Coordinates of the symbol origin Expressed in mils.

        pnhgt: Height of pin number text Values range from 10 to 1000.

        pnwid: Line width of pin number text Values range from 1 to 50.

        pnmhgt: Height of pin name text Values range from 10 to 1000.

        pnmwid: Line width of pin name text Values range from 1 to 50.

        labels: Number of attribute label locations defined for the decal

        pieces: Total number of drawing pieces that make up the symbol Values range from 0 to 4096.
                A definition follows each piece.

        txt: Number of free text strings within the decal

        terminals: Total number of terminals in the symbol that make up each decal Values range from 0 to 2048.

        vis: Visibility flag
            Variable value associated with the visibility of part text. The minimum value is
            0; the maximum value is 31. These values are determined in bits, and are as
            follows:
            For off-page symbols:
            BIT 0 = NETNAME INVISIBILITY
            For connector decals:
            BIT 0 = REF DES AND PIN NUMBER INVISIBILITY
            BIT 1 = PART TYPE INVISIBILITY
            For part decals:
            BIT 0 = REF DES INVISIBILITY
            BIT 1 = PART TYPE INVISIBILITY
            BIT 3 = PIN NAMES INVISIBILITY
            BIT 4 = PIN NUMBERS AND NAMES
            Note: A bit set indicates that the name is not visible.

        ?? no documentation found, but 0 for normal decal and 1 for Pin decals

        fontinfo: Font information for pin numbers (2 nd line)

        fontinfo: Font information for pin names (3 rd line)

        """
    first_line = first_four_lines[0].split()
    if not (len(first_line) == 12 and not from_schematic) and not (len(first_line) == 13 and from_schematic):
        raise ValueError("Invalid schematic decal header line.")

    pieces = int(first_line[8])
    if not (0 <= pieces < 4096):
        raise ValueError('Total number of drawing pieces has to be between 0 and 4096')

    pins = int(first_line[10])
    if not (0 <= pins < 2048):
        raise ValueError('Total number of terminals in the symbol has to be between 0 and 2048')

    vis = int(first_line[11])

    return SchLibHeaderInformation(
        name=first_line[0],
        pin_name_format=_pads_font_info_to_text_format(first_line[5], first_line[6],
                                                       first_four_lines[3].strip('"')),
        pin_designator_format=_pads_font_info_to_text_format(first_line[3], first_line[4],
                                                             first_four_lines[2].strip('"')),
        last_edit=read_timestamp(first_four_lines[1]),
        symbol_origin=point_mils_to_m(Point(float(first_line[1]), float(first_line[2]))),
        n_labels=int(first_line[7]),
        n_drawing_pieces=pieces,
        n_free_text=int(first_line[9]),
        n_pins=pins,
        designator_invisible=bool(0b1 & vis),
        name_invisible=bool(0b10 & vis),
        pin_names_invisible=bool(0b1000 & vis) or bool(0b10000 & vis),
        pin_designator_invisible=bool(0b10000 & vis)
    )


def _get_justification_attr_label(just: str, rot90deg=False) -> tuple:
    """
    justification:
                Justification of the attribute text string
                The value is a bit string as follows:
                Bit 0 = 0 Left justified or center (X direction) justified
                Bit 0 = 1 Right justified
                Bit 1 = 0 Bottom justified or middle (Y direction) justified
                Bit 1 = 1 Top justified
                Bit 2 = 0 Left or right justified
                Bit 2 = 1 Center justified
                Bit 3 = 0 Bottom or top justified
                Bit 3 = 1 Middle justified.

                When attribute text is rotated the definitions for bits 0 and 1 are interchanged.
                Allowed values for unrotated attribute text are as follows:
                bottom left = 0
                bottom right = 1
                bottom center = 4
                top left = 2
                top right = 3
                top center = 6
                middle left = 8
                middle right = 9
                middle center = 12

                Allowed values for rotated attribute text are as follows:
                bottom left = 0
                bottom right = 2
                bottom center = 4
                top left = 1
                top right = 3
                top center = 5
                middle left = 8
                middle right = 10
                middle center = 12

                Pads default value is center down
    :param just:
    :return: {'horizontal': hor, 'vertical': ver}
    """
    just = int(just)
    if not rot90deg:
        if just in [0, 2, 8]:
            hor = JustHorziontal.start
        elif just in [1, 3, 9]:
            hor = JustHorziontal.end
        elif just in [4, 6, 12]:
            hor = JustHorziontal.middle
        else:
            logger.warning('illegal value for justification in schematic decal')
            hor = JustHorziontal.middle
        if just in [0, 1, 4]:
            ver = JustVertical.bottom
        elif just in [2, 3, 6]:
            ver = JustVertical.top
        elif just in [8, 9, 12]:
            ver = JustVertical.middle
        else:
            logger.warning('illegal value for justification in schematic decal')
            ver = JustVertical.bottom
    else:
        if just in [0, 1, 8]:
            hor = JustHorziontal.start
        elif just in [2, 3, 10]:
            hor = JustHorziontal.end
        elif just in [4, 5, 12]:
            hor = JustHorziontal.middle
        else:
            logger.warning('illegal value for justification in schematic decal')
            hor = JustHorziontal.middle

        if just in [0, 2, 4]:
            ver = JustVertical.bottom
        elif just in [1, 3, 5]:
            ver = JustVertical.top
        elif just in [8, 10, 12]:
            ver = JustVertical.middle
        else:
            logger.warning('illegal value for justification in schematic decal')
            ver = JustVertical.bottom
    return hor, ver


def _get_justification_drafting_item(just: str) -> tuple:
    """
           just:   TextTuple string justification
                       Value is the decimal equivalent of a bit string as follows:
                       Bits 0 to 3 encode a four-bit value for horizontal justification with the following
                       values:
                       0 = Left justified
                       1 = Center justified
                       2 = Right justified
                       Bits 4 to 7 encode a four-bit value for vertical justification with the following
                       values:
                       0 = Bottom justified
                       1 = Middle justified
                       2 = Top justified.
                       Allowed values for justification are as follows:
                       Bottom left = 0
                       Bottom center = 1
                       Bottom right = 2
                       Middle left = 16
                       Middle center= 17
                       Middle right = 18
                       Top left = 32
                       Top center = 33
                       Top right = 34
           :param just:
           :return:
           """
    just = int(just)
    hor = just & 0b1111
    if hor == 0:
        hor = JustHorziontal.start
    elif hor == 1:
        hor = JustHorziontal.middle
    else:  # PADS is doing the same with illegal values
        hor = JustHorziontal.end

    ver = just >> 4
    if ver == 1:
        ver = JustVertical.middle
    elif ver == 2:
        ver = JustVertical.top
    else:
        ver = JustVertical.bottom  # PADS is doing the same with illegal values
    return hor, ver


def _read_attribute_label_line(line: str, label_visible: bool) -> Text:
    """ Each attribute label consists of two lines as follows:
        x y rotation justification height width fontinfo

        Where:
        x, y:   Coordinates of the text string location relative to the origin of the schematic

        rotation: Orientation of the text in degrees (listed as 0 for 0 degree rotation and 900 for 90
                    degree rotation)

        justification:
                Justification of the attribute text string
                The value is a bit string as follows:
                Bit 0 = 0 Left justified or center (X direction) justified
                Bit 0 = 1 Right justified
                Bit 1 = 0 Bottom justified or middle (Y direction) justified
                Bit 1 = 1 Top justified
                Bit 2 = 0 Left or right justified
                Bit 2 = 1 Center justified
                Bit 3 = 0 Bottom or top justified
                Bit 3 = 1 Middle justified.

                When attribute text is rotated the definitions for bits 0 and 1 are interchanged.
                Allowed values for unrotated attribute text are as follows:
                bottom left = 0
                bottom right = 1
                bottom center = 4
                top left = 2
                top right = 3
                top center = 6
                middle left = 8
                middle right = 9
                middle center = 12

                Allowed values for rotated attribute text are as follows:
                bottom left = 0
                bottom right = 2
                bottom center = 4
                top left = 1
                top right = 3
                top center = 5
                middle left = 8
                middle right = 10
                middle center = 12

        height: Height of text
                Values range from 10 to 1000 mils.

        width:  Width of text in mils
                Values range from 1 to 50 mils.

        fontinfo:
                Font information for attribute label text"""

    entries = shlex.split(line, posix=False)

    angle = radians(float(entries[2]) / 10)

    f = _pads_font_info_to_text_format(entries[4], entries[5], entries[6].strip('"'),
                                       *_get_justification_attr_label(entries[3], True if angle > 0 else False))

    return Text(
        origin=Point(*point_mils_to_m(Point(float(entries[0]), float(entries[1])))),
        value='',
        format=f,
        line_format=NO_LINE,
        fill=NO_FILL,
        angle=angle,
        visible=label_visible
    )


MAP_JUST_HORIZONTAL = {
    Mirror.no_mirror: {
        JustHorziontal.start: JustHorziontal.start,
        JustHorziontal.middle: JustHorziontal.middle,
        JustHorziontal.end: JustHorziontal.end
    },
    Mirror.x_mirror: {
        JustHorziontal.start: JustHorziontal.start,
        JustHorziontal.middle: JustHorziontal.middle,
        JustHorziontal.end: JustHorziontal.end
    },
    Mirror.y_mirror: {
        JustHorziontal.start: JustHorziontal.end,
        JustHorziontal.middle: JustHorziontal.middle,
        JustHorziontal.end: JustHorziontal.start
    },
    Mirror.x_and_y_mirror: {
        JustHorziontal.start: JustHorziontal.end,
        JustHorziontal.middle: JustHorziontal.middle,
        JustHorziontal.end: JustHorziontal.start
    }
}
MAP_JUST_VERTICAL = {
    Mirror.no_mirror: {
        JustVertical.bottom: JustVertical.bottom,
        JustVertical.middle: JustVertical.middle,
        JustVertical.top: JustVertical.top
    },
    Mirror.x_mirror: {
        JustVertical.bottom: JustVertical.top,
        JustVertical.middle: JustVertical.middle,
        JustVertical.top: JustVertical.bottom
    },
    Mirror.y_mirror: {
        JustVertical.bottom: JustVertical.bottom,
        JustVertical.middle: JustVertical.middle,
        JustVertical.top: JustVertical.top
    },
    Mirror.x_and_y_mirror: {
        JustVertical.bottom: JustVertical.top,
        JustVertical.middle: JustVertical.middle,
        JustVertical.top: JustVertical.bottom
    }
}


def _create_text_from_text_item(txt_line: str, txt_name: str) -> Text:
    """
        Each text entry consists of two lines as follows:
        x y rotation layer height width mirror just drwnum field fontinfo
        textstring

        x, y:   Coordinates of the text string location relative to the origin of the schematic

        rotation:
                Orientation of the text in degrees

        layer:
                Numeric layer number for use in PADS Layout.
                Values range from 0 to 250. A layer value of zero means all layers. The layer
                number is ignored in PADS Logic.
        height:
                Height of text
                Values range from 0.01 to 1.0 inches, expressed in the selected units type.

        width:  Width of text in mils
                Values range from 0.001 to 0.050 inches, expressed in the selected units type.

        mirror: Flag indicating text mirroring in PADS Layout.
                0 = not mirrored, 1 = mirrored about the y-axis when viewed with zero
                orientation.

        just:   TextTuple string justification
                Value is the decimal equivalent of a bit string as follows:
                Bits 0 to 3 encode a four-bit value for horizontal justification with the following
                values:
                0 = Left justified
                1 = Center justified
                2 = Right justified
                Bits 4 to 7 encode a four-bit value for vertical justification with the following
                values:
                0 = Bottom justified
                1 = Middle justified
                2 = Top justified.
                Allowed values for justification are as follows:
                Bottom left = 0
                Bottom center = 1
                Bottom right = 2
                Middle left = 16
                Middle center= 17
                Middle right = 18
                Top left = 32
                Top center = 33
                Top right = 34

        drwnum:
                For auto-dimensioning text, this is the PCB drawing number. For other text, the
                value is zero.

        field:  A flag to indicate that the text item is a PADS Logic field label.
                fontinfo Font information string, as described in the Font Information Definition section.
    """
    entries = shlex.split(txt_line)

    just_hor, just_vert = _get_justification_drafting_item(entries[7])
    if entries[6] == '0':
        mirror = Mirror.no_mirror
    elif entries[6] == '1':
        mirror = Mirror.x_mirror
    else:
        raise ValueError('mirror entry has to be either 0 or 1')
    f = _pads_font_info_to_text_format(entries[4], entries[5], entries[10].strip('"'),
                                       MAP_JUST_HORIZONTAL[mirror][just_hor], MAP_JUST_VERTICAL[mirror][just_vert])
    return Text(
        origin=point_mils_to_m(Point(float(entries[0]), float(entries[1]))),
        value=txt_name,
        format=f,
        line_format=NO_LINE,
        fill=NO_FILL,
        angle=radians(float(entries[2]) / 10),
        visible=True)


SCH_JUST_MAP = {
    '0': {
        '0': (JustHorziontal.start, JustVertical.bottom),
        '1': (JustHorziontal.end, JustVertical.bottom),
        '2': (JustHorziontal.start, JustVertical.top),
        '3': (JustHorziontal.end, JustVertical.top),
        '4': (JustHorziontal.middle, JustVertical.bottom),
        '5': (JustHorziontal.middle, JustVertical.bottom),
        '6': (JustHorziontal.middle, JustVertical.top),
        '7': (JustHorziontal.middle, JustVertical.top),
        '8': (JustHorziontal.start, JustVertical.middle),
        '9': (JustHorziontal.end, JustVertical.middle),
        '10': (JustHorziontal.start, JustVertical.middle),
        '11': (JustHorziontal.end, JustVertical.middle),
        '12': (JustHorziontal.middle, JustVertical.middle),
        '16': (JustHorziontal.start, JustVertical.bottom),
    },
    '90': {
        '0': (JustHorziontal.start, JustVertical.bottom),
        '1': (JustHorziontal.start, JustVertical.top),
        '2': (JustHorziontal.end, JustVertical.bottom),
        '3': (JustHorziontal.end, JustVertical.top),
        '4': (JustHorziontal.middle, JustVertical.bottom),
        '5': (JustHorziontal.middle, JustVertical.top),
        '6': (JustHorziontal.middle, JustVertical.bottom),
        '7': (JustHorziontal.middle, JustVertical.top),
        '8': (JustHorziontal.start, JustVertical.middle),
        '9': (JustHorziontal.start, JustVertical.middle),
        '10': (JustHorziontal.end, JustVertical.middle),
        '11': (JustHorziontal.end, JustVertical.middle),
        '12': (JustHorziontal.middle, JustVertical.middle),
        '13': (JustHorziontal.middle, JustVertical.middle),
    }
}


def _pin_attributes_to_text(x: str, y: str, rotation: str,
                            justification: Union[str, bool], text_format: TextFormat, visible: bool, text: str = '',
                            from_schematic: bool = False) -> Text:
    """
        takes PADS pin text attributes and return a valid Text object
    @param x: x-location in mils
    @param y: y-location in mils
    @param rotation:rotation in degrees
                Valid value is 0 or 90.
    @param justification: Pin number justification
                          See justification definition for Free TextTuple items
    @param from_schematic: True: from schematic False from library

    """
    if from_schematic:
        just_hor, just_vert = SCH_JUST_MAP[rotation][justification]
    else:
        if justification:
            just_hor, just_vert = _get_justification_drafting_item(justification)
        else:
            just_hor = text_format.horizontal
            just_vert = text_format.vertical
    f = TextFormat(
        fontsize=text_format.fontsize,
        font=text_format.font,
        horizontal=just_hor,
        vertical=just_vert,
        bold=text_format.bold,
        italic=text_format.italic,
        underline=text_format.italic,
        strikethrough=text_format.strikethrough,
        color=text_format.color
    )
    return Text(
        origin=point_mils_to_m(Point(float(x), float(y))),
        value=text,
        format=f,
        line_format=NO_LINE,
        fill=NO_FILL,
        angle=radians(float(rotation)),
        visible=visible)


def _create_schpin_from_pads_logic_lines(schdecal_header: SchLibHeaderInformation, terminal_line: str,
                                         terminal_property_line: str, pin_decals: dict, pin_nr: int,
                                         from_schematic: bool = False) -> SchPin:
    """
    terminal_line:
                Tx y rtn xym pnx pny pnrtn pnjust pnmx pnmy pnmrtn pnmjust pindecal

                x, y:
                    Coordinates of the terminal location relative to the decal origin

                rtn:
                    Terminal rotation in degrees
                    Value is 0 or 90.

                xym:
                    Terminal mirror flags
                    Values are:
                    0 = no mirror
                    1 = X mirror
                    2 = Y mirror
                    3 = X and Y mirror

                pnx, pny:
                    X Y location of the pin number relative to the terminal

                pnrtn:
                    Pin number rotation in degrees
                    Valid value is 0 or 90.

                pnjust:
                    Pin number justification
                    See justification definition for Free TextTuple items.

                pnmx, pnmy:
                    X Y location of the pin name relative to the terminal

                pnmrtn:
                    Pin name rotation in degrees
                    Valid value is 0 or 90.

                pnmjust:
                    Pin name justification

                pindecal Name of the pin decal

    terminal_property_line:
                Pplx ply plrtn pljust nlx nly nlrtn nljust pflags


                plx, ply:
                        X Y location of the pin properties label relative to the terminal

                plrtn:
                        Pin properties label rotation in degrees
                        Valid value is 0 or 90.

                pljust:
                        Pin properties label justification
                        See justification definition for Free TextTuple items.

                nlx, nly:
                        X Y location of the netname label relative to the terminal

                nlrtn:
                        Netname label rotation in degrees
                        Valid value is 0 or 90.

                nljust:
                        Netname label justification
                        See justification definition for Free TextTuple items.

                pflags:
                        Defines whether the pin properties or netname label positions are valid for this
                        terminal. If not valid, the positions are taken from the corresponding label
                        positions in the pin decal associated with the terminal.
                        A clear flag indicates the label is valid, a set flag indicates the label position in
                        the terminal is to be ignored. The flags are:
                        Bit 6 Pin properties label position invalid
                        Bit 7 Netname label position invalid
    """

    entries = terminal_line.split()

    origin = Point(0, 0)

    # somehow in schematic the pin mirror flag is always shifted one to the right
    def convert_mirror_entry(mirror_entry):
        if from_schematic:
            return str(int(mirror_entry) << 1)
        else:
            return mirror_entry

    pin_mirror = PADS_TERMINAL_MIRROR_MAP[convert_mirror_entry(entries[3])]
    pin_decal_name = entries[12] if len(entries) >= 13 else 'illegal'
    pin_origin = point_mils_to_m(Point(float(entries[0].lstrip('T')), float(entries[1])))
    angle_deg = float(entries[2])

    if pin_decal_name not in VALID_PADS_PINDECAL:
        raise ValueError('illegal pads pindecal')
    else:
        try:
            pin_decal = pin_decals[pin_decal_name]
        except KeyError:
            logger.debug("WARNING no valid pindecal was found. Will use PINSHORT definiton")
            pin_decal = pin_decals['PINSHORT']

    # TODO optimize
    schpin = deepcopy(pin_decal)

    argument_list_designator = [entries[4], entries[5], entries[6], entries[7],
                                schdecal_header.pin_designator_format, not schdecal_header.pin_designator_invisible]
    argument_list_name = [entries[8], entries[9], entries[10], entries[11],
                          schdecal_header.pin_name_format, not schdecal_header.pin_names_invisible]
    entries = terminal_property_line.split()

    argument_list_net_label = [entries[4], entries[5], entries[6], entries[7],
                               schdecal_header.pin_name_format, not schdecal_header.pin_names_invisible]

    designator = _pin_attributes_to_text(*argument_list_designator, from_schematic=from_schematic)
    designator = designator._replace(value='#{}'.format(pin_nr))
    name = _pin_attributes_to_text(*argument_list_name, from_schematic=from_schematic)

    if int(entries[8]) & (1 << 7):  # given net label is invalid
        net_name = pin_decal.labels['net_name'].label

    else:  # given attributes are valid
        net_name = _pin_attributes_to_text(*argument_list_net_label, from_schematic=from_schematic)

    if angle_deg:
        angle_rad = radians(angle_deg)
        schpin.angle = angle_rad

        result = []
        for label in [name, designator, net_name]:
            if label.angle:
                label = label.rotate(origin, angle_rad)._replace(angle=0)
                label = label.x_y_mirror(label.origin)
                result.append(label)
            else:
                result.append(label.rotate(origin, angle_rad))
        name, designator, net_name = result

    if pin_mirror == Mirror.x_mirror:
        schpin.mirror = MirrorState.v_mirror
    elif pin_mirror == Mirror.y_mirror:
        schpin.mirror = MirrorState.h_mirror
    elif pin_mirror == Mirror.x_and_y_mirror:
        schpin.mirror = MirrorState.hv_mirror

    schpin.set_attribute_and_label('name', name)
    schpin.set_attribute_and_label('designator', designator)
    schpin.labels['net_name'] = DbText.create_by_label(net_name, False, key='net_name')
    schpin.origin = pin_origin

    return schpin


_LINE_STYLES_MAPPING = {
    1: LineStyle.solid,
    0: LineStyle.dotted,
    -1: LineStyle.solid,
    -2: LineStyle.dashed,
    -3: LineStyle.dotted,
    -4: LineStyle.dash_dotted,
    -5: LineStyle.dash_double_dotted
}


def read_drafting_piece_entry_header(header: str, from_schematic: bool = False) -> PadsPieceEntryHeader:
    """
        Each piece entry consists of a header line followed by a list of line segment or arc segment
        coordinates.

        type numcoord width layer linestyle

        type:   Type of piece
                Valid values are OPEN, CLOSED, CIRCLE, COPOPN, COPCLS,
                COPCIR, BRDCUT, BRDCCO, KPTCLS, KPTCIR, or TAG.
                (The TAG piece is used to combine coppers and copper cutouts inside
                the part decal into one item. It does not contain any coordinates and is
                used as either opening or close bracket. TAGs are also used to combine
                dimension pieces into a dimension drawing.)

        numcoord:
                Number of coordinates defining the item
                For open items, this is the number of corners. For closed line items, it is
                the number of corners plus one (to return to the starting corner). Circles
                have two corners that define opposite ends of any diameter. For TAGs,
                0 (zero).

        width:  Line width of all segments in the piece
                Values range from 0 to 0.25 inches, expressed in the selected units of
                the item.
                For TAGs, 0 (zero).

        layer:  Numeric layer number for use in PADS Layout.
                Values range from 0 to 250. A layer value of zero means all layers. The
                layer number is ignored in PADS Logic.
                For TAGs, the layer value specifies the TAG “type”:
                • 1 means an “opening bracket”, that is, start of the group.
                • 0 means a “closing bracket,”, that is, end of the group.

        linestyle:
                System flag for type of line or keepout restrictions
                A value of 1 indicates a solid line; a value of 0 indicates an old Logic
                style dotted line. Negative values indicate line styles introduced in
                PADS 9.4 (for piece types OPEN, CLOSED, CIRCLE only):
                -1 — solid
                -2 — dashed
                -3 — dotted
                -4 — dash dotted
                -5 — dash double-dotted
                Positive values indicate Keepout Restrictions (for piece types
                KPTCLS, KPTCIR only):
                Bit 0: (0x01) Placement
                Bit 1: (0x02) Trace and Copper
                Bit 2: (0x04) Copper Pour and Plane Area
                Bit 3: (0x08) Via and Jumper
                Bit 4: (0x10) Test Point
                Bit 5 : (0x20) Component Drill
                Bit 6: (0x40) Accordion
                Since TAGs have no graphics, the linestyle value for TAGs (typically
                -1) is non-significant.
    """
    entries = header.split()
    if len(entries) != 5 and not from_schematic or len(entries) != 4 and from_schematic:
        raise ValueError('invlalid piece entry header line')
    p_type = entries[0]
    if p_type not in DEF_PIECE_ENTRY_TYPES:
        raise ValueError('invlaid piece entry type')

    tag = True if p_type == 'TAG' else False
    keepout = True if p_type in ['KPTCLS', 'KPTCIR'] else False
    neg_linestyle_allowed = True if p_type in ['OPEN', 'CLOSED', 'CIRCLE', 'COPOPN', 'COPCLS', 'CIRCUT',
                                               'COPCIR'] else False  # COPOPN, COPCLS, CIRCUT, COPCIR not documented ...

    numcoord = int(entries[1])
    if tag and numcoord != 0:
        logger.debug('Warning: A tag should have numcoord 0')
    width = mils_to_m(float(entries[2]))

    if tag and width != 0:
        logger.debug('Warning: piece entry width should be 0 for a TAG')

    # TODO add a check that widht is in 0-0.25 inches
    if not from_schematic:
        layer = int(entries[3])
        if (not (-2 <= layer <= 250)):
            raise ValueError('illegal layer {}'.format(layer))
        if tag:
            raise NotImplemented
    else:
        layer = 0

    # pads was to stupid to use a signed char in pads logic, instead of -1 it saves 255
    line_style = int(entries[4]) if not from_schematic else int(entries[3])
    if line_style > 250:
        if line_style > 255:
            raise ValueError('invalid line style arguemnt {}'.format(line_style))
        else:
            line_style = 256 - line_style

    if keepout:
        raise NotImplemented
    else:
        if line_style < 0 and not neg_linestyle_allowed:
            raise ValueError('negativ linestyle is only allowed for piece types OPEN, CLOSED, CIRCLE')
        if line_style not in _LINE_STYLES_MAPPING:
            logger.debug("WARNING line {} has an unknown linestyle {} will use default".format(header, line_style))
            line_style = 0
        line_style = _LINE_STYLES_MAPPING[line_style]

    return PadsPieceEntryHeader(
        type=p_type,
        nummcoord=numcoord,
        line_width=width,
        layer_number=layer,
        line_style=line_style
    )


def read_pads_arc_line(values: list, input_unit: UnitOfLength) -> Arc:
    """
    reads a pads arc line and returns an Arc

    x y ab aa ax1 ay1 ax2 ay2 (format for arcs)

    format for arcs

    x, y:   Beginning of arc

    ab:     Beginning angle of the arc in tenths of a degree

    aa:     Angle swept by the arc from the start to the end (in tenths
            of a degree)

    ax1, ay1:
            Lower left point of rectangle around circle of arc

    ax2, ay2:
            Upper right point of rectangle around circle of arc
            The points of the rectangle define the circle radius
            describing the arc and the location of the center point of
            the circle relative to the origin of the line item.

    ax2 – ax1 = ay2 – ay1:
            Diameter of the circle of the arc

    (ax1 + ax2)/2, (ay1 +ay2)/2:
            Coordinates of the arc center
    @param values:
    @param input_unit:
    @return:
    """
    convert = create_conversion_to_m(input_unit)
    new_values = [convert(float(x)) if i not in [2, 3] else float(x) / 10.0 for i, x in enumerate(values)]
    p1 = Point(new_values[0], new_values[1])
    o = Point((new_values[4] + new_values[6]) / 2.0, (new_values[5] + new_values[7]) / 2.0)
    r = (new_values[6] - new_values[4]) / 2  # ax2 – ax1
    angle = radians(new_values[3])
    start_angle = radians(new_values[2])
    start = Point(o.x + r * cos(start_angle), o.y + r * sin(start_angle))
    end = start.rotate(o, angle)
    if p1.distance(start) < p1.distance(end):
        start = p1
        backwards_drawn = False
    else:
        backwards_drawn = True

    if angle < 0:
        start = end

    return Arc(
        origin=o,
        start=start,
        angle=angle,
        backwards_drawn=backwards_drawn
    )


def pads_piece_entry_to_eda_drawing(piece_entry_header: PadsPieceEntryHeader,
                                    lines: list, input_unit: UnitOfLength) -> Union[DbCircle, DbSimplePath]:
    """

    @param piece_entry_header:
    @param lines:
    @param input_unit:
    @return:
    """
    convert = create_conversion_to_m(input_unit)
    line_format = LineFormat(
        piece_entry_header.line_style,
        piece_entry_header.line_width,
        C_BLACK,
        1.0
    )
    if piece_entry_header.type == 'CIRCLE':
        if len(lines) != 2:
            raise ValueError('Invalid Circle definition\n{}'.format('\n'.join(lines)))
        a = Point(*[convert(float(x)) for x in lines[0].split()])
        b = Point(*[convert(float(x)) for x in lines[1].split()])
        dx = b.x - a.x
        dy = b.y - a.y
        r = sqrt(dx ** 2 + dy ** 2) / 2.0
        x = a.x + dx / 2
        y = a.y + dy / 2
        return DbCircle(circle=Circle(Point(x, y), r, line_format, NO_FILL))

    if piece_entry_header.type not in ('CLOSED', 'OPEN', 'COPCLS'):
        raise ValueError('unsupported type {}'.format(piece_entry_header.type))

    path = []
    for line in lines:
        values = line.split()
        n = len(values)
        if n == 8:
            path.append(read_pads_arc_line(values, input_unit))
        elif n == 2:
            path.append(Point(*[convert(float(x)) for x in values]))
        else:
            raise ValueError('illegal piece entry {}'.format(line))
    if piece_entry_header.type == 'OPEN':
        return DbSimplePath(members=tuple(path), closed=False, line_format=line_format, fill=NO_FILL)
    elif piece_entry_header.type == 'CLOSED':
        return DbSimplePath(members=tuple(path), closed=True, line_format=line_format, fill=NO_FILL)
    else:  # COPCLS
        return DbSimplePath(members=tuple(path), closed=True, line_format=line_format, fill=Fill(C_BLACK, 1.0))


def ascii_to_part_symbol(pads_ascii: str, pin_decals: dict, from_schematic: bool = False) \
        -> PartSymbol:
    """
    a schematic decal in pads consists of the following parts:
            - Schematic decal header lines
            - Attribute label locations
            - Piece definitions
            - TextTuple definitions
            - Terminal definitions

    to have a unique designator the pins get's a desgintor from #0 to#n-1
    """
    lines = deque(pads_ascii.split('\n'))
    header = read_header_lines([lines.popleft() for x in range(4)], from_schematic)

    attributes = {}
    name = EMPTY_TEXT._replace(value=header.name)
    designator = False
    partsymbol = PartSymbol()

    free_text = 0

    pins = []
    pin_nr = 0
    while len(lines):
        line = lines.popleft()
        n_entries = len(shlex.split(line, posix=False))

        if n_entries == 7 and line.endswith('"'):  # attribute label
            attr_label_line = line
            attribute_key = lines.popleft()
            if attribute_key == PADS_NAME_KEY:
                name = _read_attribute_label_line(attr_label_line, not header.name_invisible)
                name = name._replace(value=header.name)
            elif attribute_key == PADS_DESIGNATOR_KEY:
                designator = _read_attribute_label_line(attr_label_line, not header.designator_invisible)
            else:
                if attribute_key in attributes:
                    attribute_key = '{}_1'.format(attribute_key)
                attributes[attribute_key] = _read_attribute_label_line(attr_label_line, True)
        elif n_entries == 11 and line.endswith('"'):  # Free TextTuple
            free_text += 1
            text_line = line
            text_str = lines.popleft()
            ft = _create_text_from_text_item(text_line, text_str)
            dbft = DbText(key='_freetext{}'.format(free_text), label=ft)
            partsymbol.labels[dbft.key] = dbft
        elif n_entries == 13 and line.startswith('T'):  # Terminal entry
            terminal_line = line
            terminal_property_line = lines.popleft()
            pins.append(_create_schpin_from_pads_logic_lines(header, terminal_line, terminal_property_line,
                                                             pin_decals, pin_nr, from_schematic=from_schematic))
            pin_nr = pin_nr + 1
        elif n_entries == 5 and not from_schematic or n_entries == 4 and from_schematic:  # piece entry
            piece_header = read_drafting_piece_entry_header(line, from_schematic)
            pads_piece_entry = pads_piece_entry_to_eda_drawing(piece_header, [lines.popleft() for x in
                                                                              range(piece_header.nummcoord)],
                                                               UnitOfLength.mil)
            partsymbol.drawing_pieces.append(pads_piece_entry)
        else:
            raise ValueError('invalid pads ascii line\n{}\n'.format(line))

    if designator is False:
        raise ValueError(
            'ERROR at {}. PADS Logic definitions needs to have a {} attribute'.format(header.name,
                                                                                      PADS_DESIGNATOR_KEY))

    # TODO check header
    partsymbol.set_attribute_and_label('name', name)
    partsymbol.set_attribute_and_label('designator', designator)
    for k, attr in attributes.items():
        partsymbol.labels[k] = DbText.create_by_label(attr, False, key=k)
    partsymbol.origin = header.symbol_origin
    partsymbol.pins = pins

    return partsymbol


def read_pads_lib_elements(path: Path) -> List[str]:
    """
    reads a pads ascii file and returns a list of strings
    @param path:
    @return:
    """
    with open(path, 'r', encoding=PADS_FILE_ENCODING) as f:
        library = f.read()
        elements = [x.strip('\n') for x in library.split('\n\n')]
        # filter start, end and illegal definitions
        return list(filter(lambda x: not (x.count('\n') < 2), elements))


NET_CONNECTOR_NAMES = ('$OSR_BI_LEFT', '$OSR_BI_RIGHT', 'GND', 'GNDC', 'GNDE', 'GNDT', 'VCC', 'VCC-')
PART_NET_CONNECTOR_BEGINNING = ('$GND_SYMS', '$OSR_SYMS', '$PWR_SYMS')
PIN_DECALS_NAME = ('PIN', 'PINB', 'PCLK', 'PCLKB', 'PINIEB', 'PINORB', 'PINSHORT', 'PINVRTS')


def ascii_to_sch_pin(ascii: str, from_schematic: bool = False) -> SchPin:
    """

    @param ascii: pads ascii
        e.g.:
            PINSHORT         34000 34000 97 10 97 10 4 1 0 0 0 (in library)
            PINSHORT         34000 34000 97 10 97 10 4 1 0 0 0 1
            TIMESTAMP 2015.05.20.15.09.23
            "Regular Segoe UI"
            "Regular Segoe UI"
            60    20    0 1 100 10 "Regular Segoe UI"
            REF-DES
            140   10    0 8 100 10 "Regular Segoe UI"
            PART-TYPE
            -530  10    0 1 100 10 "Regular Segoe UI"
            *
            -70   10    0 1 100 10 "Regular Segoe UI"
            *
            OPEN   2 10 0 -1
            0     0
            100   0
    """
    sch_decal = ascii_to_part_symbol(ascii, PIN_DECALS, from_schematic)
    spin = SchPin(angle=0.0)
    spin.set_attribute_and_label('designator', sch_decal.labels['designator'].label)
    spin.set_attribute_and_label('name', sch_decal.labels['name'].label)
    spin.labels['net_name'] = DbText.create_by_label(sch_decal.labels['*_1'].label, False, key='net_name')
    spin.drawing_pieces = sch_decal.drawing_pieces
    return spin


def ascii_to_net_connector(ascii_str: str, from_schematic: bool = False) -> NetConnector:
    """

    @param ascii_str:
    @param from_schematic:
    """
    # add a pseudo pin_decal to satisfy pADS_Ascii_to_Schematic_Decal function
    header = read_header_lines(ascii_str.split('\n')[0:4], from_schematic)
    n_breaks = ascii_str.count('\n')
    new_ascii = '\n'.join(
        [x + ' {}'.format(EMPTY_PIN_SYMBOL) if x.startswith('T') and i > (n_breaks - header.n_pins * 2)
         else x for i, x in enumerate(ascii_str.split('\n'))])
    sch_decal = ascii_to_part_symbol(new_ascii, PIN_DECALS, from_schematic)
    net_connetor = NetConnector()
    net_connetor.set_attribute_and_label('name', sch_decal.labels['name'].label)
    if len(sch_decal.pins) != 1:
        raise ValueError('Net Connector {} doesnt have 1 pins. {} instead'.format(sch_decal.name, len(sch_decal.pins)))
    net_connetor.pin = sch_decal.pins[0]
    net_connetor.drawing_pieces = sch_decal.drawing_pieces

    return net_connetor


def import_pads_symbol_lib(path: Path, from_schematic: bool = False) -> SymbolLibrary:
    """
        Imports a pads ascii symbol library.
    @param path:
    @return:
    """
    elements = read_pads_lib_elements(path)
    sch_decals = []
    net_conns_symbols = []

    pin_decal_ascii = [decal for decal in elements if decal[0:decal.index(' ')] in PIN_DECALS_NAME]
    pin_decals = deepcopy(PIN_DECALS)
    for decal in pin_decal_ascii:
        d = ascii_to_sch_pin(decal, from_schematic)
        if d.name is None:
            raise ValueError('pin must have a name')
        pin_decals[d.name] = d

    for decal in elements:
        name = decal[0:decal.index(' ')]
        if name in NET_CONNECTOR_NAMES:
            d = ascii_to_net_connector(decal, from_schematic)
            net_conns_symbols.append(d)
        elif name in PIN_DECALS_NAME:
            # already handled above
            pass
        else:
            d = ascii_to_part_symbol(decal, pin_decals, from_schematic)
            sch_decals.append(d)
    return SymbolLibrary(name=path.stem, symbols=sch_decals, netconnectors=net_conns_symbols)


def read_pads_part_gate_header(gate_header_line: str) -> PadsHeaderLine:
    """

    @param gate_header_line:
    @return:
    """
    entries = shlex.split(gate_header_line, posix=False)
    gswap = 0
    pins = 1
    if entries[0] == 'GATE':
        gtype = PadsPartType.NormalPart
        gswap = int(entries[3])
        pins = int(entries[2])
    elif entries[0] == 'CONN':
        gtype = PadsPartType.Connector
        pins = int(entries[2])
    elif entries[0] == 'OFF':
        gtype = PadsPartType.OffPageRef
    elif entries[0] == 'GND':
        gtype = PadsPartType.GND
    elif entries[0] == 'PWR':
        gtype = PadsPartType.PWR
    return PadsHeaderLine(
        type=gtype,
        n_decals=int(entries[1]),
        n_pins=pins,
        gate_swap=gswap
    )

def read_pads_part_gate_decal_line(gate_type: PadsPartType, line: str) -> PadsGateDecalLine:
    """
    The format for gates of normal parts:
        GATE decals pins gateswap
        decalname
        pinnumber pinswap pintype pinname

    For connector part types:
        CONN decals pins
        decalname pintype
        pinnumber pinswap
    For Off-page symbol part type:
        OFF decals
        decalname pintype
    For Ground symbol part type:
        GND decals
        decalname pintype netname
    @param line:
    @return:
    """
    entries = shlex.split(line, posix=False)
    if len(entries) == 2 and gate_type == PadsPartType.NormalPart:
        raise ValueError('Normal Parts are not allowed to have a pintype defined on gate level')
    decalname = entries[0]
    if gate_type == PadsPartType.NormalPart:
        pintype = None
    else:
        pintype = PADS_PINTYPE_MAP[entries[1]]
    return PadsGateDecalLine(decalname, pintype)


def read_pads_part_header(header_line: str, from_schematic: bool = False) -> PartLibHeaderInformation:
    """

    @param header_line:
    @return: PartLibHeaderInformation
    """
    entries = shlex.split(header_line, posix=False)
    u = entries[2] if not from_schematic else 'I'

    if u not in ['I', 'M']:
        raise ValueError('Only I or M are allowed for coordinate types in pads')
    return PartLibHeaderInformation(
        name=entries[0],
        pcb_decals=entries[1] if not from_schematic else '',
        # List of alternate PCB decal names, separated by colons name:name:…
        unit_type=UnitOfLength.mm if u == 'M' else UnitOfLength.mil,
        logic_family=entries[3] if not from_schematic else entries[1],
        n_attrs=int(entries[4]) if not from_schematic else 0,
        n_gates=int(entries[5]) if not from_schematic else int(entries[2]),

        # Number of standard signals predefined in the part, which is typically,
        # but not exclusively, power and ground.
        n_sigpins=int(entries[6]) if not from_schematic else int(entries[3]),

        # Number of alphanumeric pins defined in the part pin mapping.
        n_pinmap=int(entries[7]) if not from_schematic else int(entries[4]),
        part_type=PadsPartType(int(entries[8])) if not from_schematic else PadsPartType(int(entries[5]))
    )


def read_pads_part_logic_pin_line(gate_type: PadsPartType, line: str, pintype: PinType = None) -> Pin:
    """

    @param line:
    @return:
    """
    entries = shlex.split(line, posix=False)
    if gate_type == PadsPartType.NormalPart:
        if len(entries) < 3:
            raise ValueError('Invalid pin Line for a normal part')
        if len(entries) == 3:
            entries.append('')
        return Pin(name=entries[3], designator=entries[0], swap_group=entries[1])
                        # pin_type=PADS_PINTYPE_MAP[entries[2]])
    elif gate_type == PadsPartType.Connector:
        if len(entries) != 2:
            raise ValueError('Invalid pin Line for a connector part')
        if pintype is None:
            raise ValueError('For gate_type == Connector pintype needs to be defined')
        return Pin(name='', designator=entries[0], swap_group=entries[1])
                        # , pin_type=pintype)

def pads_ascii_to_part(ascii_text: str, from_schematic: bool = False) -> Part:
    """
          a part in pads consists of the following parts:
                - Part header lines
                - Attributes Values
                - Piece definitions
                - TextTuple definitions
                - Terminal definitions

        to have a unique designator the pins get's a desgintor from #0 to#n-1
    @param ascii_text:
    @param from_schematic:
    @return:
    """
    lines = deque(ascii_text.split('\n'))
    header = read_pads_part_header(lines.popleft(), from_schematic)

    pcb_decal_references = header.pcb_decals.split(':')
    if len(pcb_decal_references) > 1:
        raise ValueError('At the moment only one footprint for each part is supported')

    part = Part(
        name=header.name,
        footprint_name=pcb_decal_references[0]
    )
    sch_representation = SchRepresentation(part=part)
    gates = []
    all_pins = []
    while len(lines):
        line = lines.popleft()

        if line.startswith('"'):  # attribute
            line = line.lstrip('"')
            k = line.split('"')[0]
            v = ''.join(line.split('"')[1:])
            v = v.strip()
            if k not in part.properties:
                part.add_property(k, v)
            else:
                raise KeyError("Duplicated Attribute Key {}".format(k))
        elif line.startswith('GATE') or line.startswith('CONN') or line.startswith('OFF'):
            gate_header = read_pads_part_gate_header(line)
            gate_decals = []
            if gate_header.n_decals != 0:
                gates_decals_info = [read_pads_part_gate_decal_line(gate_header.type,
                                                                    lines.popleft()) for x in
                                     range(0, gate_header.n_decals)]
                if [x for x in gates_decals_info if x.pintype != gates_decals_info[0].pintype]:
                    raise ValueError('All pintypes for the gates need to have the same value')
                # TODO pintype

                for i, g in enumerate(gates_decals_info):
                    g_decal = PartSymbol(name=g.decalname)
                    gate_decals.append(g_decal)
                pintype = gates_decals_info[0].pintype
            else:
                pintype = None

            logic_pins = [read_pads_part_logic_pin_line(gate_header.type, lines.popleft(), pintype)
                          for x in range(0, gate_header.n_pins)]
            if lines and not lines[0].startswith('GATE'):
                raise ValueError('Invalid Gate definition, number of Gates_decal or/and number of pins may be wrong')

            if gate_header.n_decals != 0:
                gate = Gate(sch_representation=sch_representation, part_symbols=gate_decals)
                gates.append(gate)
                if logic_pins:
                    gate.pins = logic_pins
            else:
                gates.append(None)

            if logic_pins:
                all_pins.extend(logic_pins)

        elif line.startswith('TIMESTAMP'):
            part.last_edit = read_timestamp(line)
        else:
            raise ValueError("line {} doesn't match a pattern".format(line))

    # Data consistency checks
    if len(gates) != header.n_gates:
        raise ValueError('Number of gates is incorrect')

    if len(part.properties) != header.n_attrs:
        raise ValueError('Number of attributes is incorrect')
    if None in part.pins:
        raise ValueError('illegal pin.designator')
    part.pins = {pin.designator: pin for pin in all_pins}
    return part


def import_pads_part_lib(path: Path, from_schematic: bool = False) -> PartLibrary:
    """
        Imports a pads ascii part library.
    @param path:
    @return:
    """
    elements = read_pads_lib_elements(path)
    parts = []
    for part_ascii in elements:
        if part_ascii.startswith('$'):
            # ignore net connectors
            pass
        else:
            part = pads_ascii_to_part(part_ascii, from_schematic)
            parts.append(part)
    return PartLibrary(name=path.stem, parts=parts)


def _process_part_items_netlist_info(part_itmes_lines: List[str], parts: Dict[str, Part]) -> Dict[str, Part]:
    """

    @param part_itmes_lines: Pads part item from netlist info e.g.:
            J200    HIROSE_FX10A-168P-SV@J_HIROSE_FX10A-168P-SV
            R900    R_0402_0R_1%_JUMPER1@R_0402_JUMPER1

    @param parts:   already existing parts in the design (normally empty)

    """
    for line in part_itmes_lines:
        designator, part_name_fp = line.split()

        if designator in parts:
            raise ValueError('Duplicated designator {} found'.format(designator))
        part_name, pcbdecal = part_name_fp.split('@')
        p = Part(name=part_name, designator=designator, footprint_name=pcbdecal)
        parts[designator] = p

    return parts


def _process_signal_netlist_info(header_line: str, signal_lines: List[str], parts: Dict[str, Part],
                                 nets):
    """

    @param header_line: Signal header line : e.g. *SIGNAL* GND
    @param parts:
    @param signal_lines: Pads Signal lines from netlist  e.g.
                            J200.167 J200.143 J200.139 J200.135 J200.125
    @param nets: already existing nets
    """
    if SIGNAL not in header_line:
        raise ValueError('illegal header line {} for a signal'.format(header_line))
    signal_name = header_line.replace(SIGNAL, '').strip()
    net = Net(name=signal_name)
    nets[signal_name] = net
    for line in signal_lines:
        for connection_point in line.split():
            part_designator, pin_designator = connection_point.split('.')
            parts[part_designator].add_pin(Pin(designator=pin_designator, net=net))


def _process_misc_netlist_info(signal_lines: List[str], parts: Dict[str, Part]):
    """
    super dirty and hacky. But at the moment I don't have the motivation to solve this properly
    @param signal_lines:
    @param parts:
    @return:
    """
    start_line = 'ATTRIBUTE VALUES'
    lines = deque(signal_lines)
    while lines and lines[0] != start_line:
        lines.popleft()
    part = None
    while lines:
        if lines[0].startswith('"'):
            line = lines[0].lstrip('"')
            k = line.split('"')[0]
            v = ''.join(line.split('"')[1:])
            v = v.strip()
            if part is None:
                raise ValueError
            part.add_property(k, v)
        elif lines[0].startswith('PART '):
            part_designator = shlex.split(lines[0], posix=False)[1]
            part = parts[part_designator]
        lines.popleft()


def import_pads_netlist(path: Path) -> Schematic:
    """
    imports a PADS ascii netlist and returns a schematic with the given information.
    Additional information about parts etc, can be loaded by differen functions like tbd.

    @param path: path to Netlist file
    @return: Schematic
    """
    with open(path, encoding=PADS_FILE_ENCODING) as f:
        lines = deque([l for l in f.read().split('\n')])

    parts = {}  # type: Dict[str, Part]
    nets = {}  # type: Dict[str, Signal]
    while lines:
        line = lines.popleft()
        if line.startswith('*'):  # and re.search(r'\*[A-Z]+\*',line):
            key = re_search(r'\*[A-Z]+\*', line)
            if key:
                section_lines = []
                while lines and not lines[0].startswith('*'):
                    section_lines.append(lines.popleft())
                if key[0] == PART_ITEMS:
                    _process_part_items_netlist_info(section_lines, parts)
                elif key[0] == SIGNAL:
                    _process_signal_netlist_info(line, section_lines, parts, nets)
                elif key[0] == MISC:
                    _process_misc_netlist_info(section_lines, parts)

    return Schematic(name=path.stem, parts=parts, nets=nets)
