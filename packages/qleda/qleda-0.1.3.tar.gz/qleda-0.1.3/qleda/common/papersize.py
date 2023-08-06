from typing import NamedTuple
from .units import create_conversion_to_m, UnitOfLength


class PaperSize(NamedTuple):
    height: float       # in m
    width: float        # in m


_mm2m = create_conversion_to_m(UnitOfLength.mm)


A0 = PaperSize(_mm2m(841), _mm2m(1189))
A1 = PaperSize(_mm2m(594), _mm2m(841))
A2 = PaperSize(_mm2m(420), _mm2m(594))
A3 = PaperSize(_mm2m(297), _mm2m(420))
A4 = PaperSize(_mm2m(210), _mm2m(297))
A5 = PaperSize(_mm2m(148), _mm2m(210))
