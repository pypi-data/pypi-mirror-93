from datetime import datetime
from typing import NamedTuple, Optional
from enum import Enum, auto

from ..common.units import UnitOfLength, create_conversion_to_m
from ..core.point import Point
from ..drawing.textcolordefs import LineStyle, Fill, NO_FILL, LineFormat, TextFormat, NO_LINE, BLACK as C_BLACK


class PinType(Enum):
    signal_source = auto()
    signal_load = auto()
    signal_bidirectional = auto()
    open_collector = auto()
    or_signal_source = auto()
    tristate = auto()
    terminator = auto()  # coming from pads, may drop support
    power_source = auto()
    power_load = auto()
    ground = auto()
    undefined = auto()


class SchLibHeaderInformation(NamedTuple):
    name: str
    pin_name_format: TextFormat
    pin_designator_format: TextFormat
    last_edit: datetime
    symbol_origin: Point
    n_labels: int
    n_drawing_pieces: int
    n_free_text: int
    n_pins: int
    designator_invisible: bool
    name_invisible: bool
    pin_names_invisible: bool
    pin_designator_invisible: bool


class PadsPartType(Enum):
    NormalPart = 0
    Connector = 1
    OffPageRef = 2
    GND = auto()
    PWR = auto()


class PadsHeaderLine(NamedTuple):
    type: PadsPartType
    n_decals: int
    n_pins: int
    gate_swap: int


class PadsGateDecalLine(NamedTuple):
    decalname: str
    pintype: Optional[PinType]

PADS_PINTYPE_MAP = {
    'S': PinType.signal_source,
    'B': PinType.signal_bidirectional,
    'C': PinType.open_collector,
    'O': PinType.or_signal_source,
    'T': PinType.tristate,
    'L': PinType.signal_load,
    'Z': PinType.terminator,
    'P': PinType.power_source,
    'G': PinType.ground,
    'U': PinType.undefined
}


class PartLibHeaderInformation(NamedTuple):
    name: str
    pcb_decals: str  # List of alternate PCB decal names, separated by colons name:name:…
    unit_type: UnitOfLength
    logic_family: str  #
    n_attrs: int  # number of defined attributes
    n_gates: int  # number of gates in the part
    n_sigpins: int  # Number of standard signals predefined in the part, which is typically,
    # but not exclusively, power and ground.
    n_pinmap: int  # Number of alphanumeric pins defined in the part pin mapping.
    part_type: PadsPartType


class PartInstanceHeader(NamedTuple):
    designator: str  # 0
    name: str        # 1
    origin: Point    # 2,3
    rotation: float    # 4 (0 or 90 deg)
    mirror_flag: int    # 5 0 = None, 1 = X Mirror (x = -x), 2 = y Mirror (y = -y), 3 = X&Y Mirror
    pin_name_format: TextFormat # 6=pinnumber height, 7 = pinnummber width
    pin_designator_format: TextFormat #8 = pinname height, 9 = pinname width
    n_labels: int    # 10
    n_attrs: int     # 11
    n_pins: int      # 12
    unknown: int     # 13 not sure what this is for, may n_sig
    symbol_index: int  # 14
    designator_invisible: bool
    name_invisible: bool
    pin_names_invisible: bool
    pin_designator_invisible: bool


class Mirror(Enum):
    no_mirror = 0
    x_mirror = 1
    y_mirror = 2
    x_and_y_mirror = 3


class PadsPieceEntryHeader(NamedTuple):
    type: str
    nummcoord: int
    line_width: float  # in meters
    layer_number: int
    line_style: LineStyle


# somehow pads documented something else, then the data is...
PADS_TERMINAL_MIRROR_MAP = {
    '0': Mirror.no_mirror,
    '2': Mirror.x_mirror,
    '3': Mirror.x_and_y_mirror,
    '4': Mirror.y_mirror,
    '6': Mirror.x_and_y_mirror
}

#  can be applied to OFFPAGE REFS and maybe a lot more
PADS_SCHEMATIC_MIRROR_MAP = {
    '0': Mirror.no_mirror,
    '1': Mirror.x_mirror,
    '2': Mirror.y_mirror,
    '3': Mirror.x_and_y_mirror
}

# A List of known section beginnings
PARTTYPE = '*PARTTYPE*'
PART_ITEMS = '*PART*'
SCH_DECAL = '*CAEDECAL*'
NET = '*NET*'
CONNECTION = '*CONNECTION*'
TIEDOTS = '*TIEDOTS*'
OFF_PAGE = '*OFFPAGE REFS*'
SIGNAL = '*SIGNAL*'
NETNAMES = '*NETNAMES*'
MISC = '*MISC*'