# File contains enums for units
from enum import IntEnum


class UnitOfLength(IntEnum):
    m = 1
    cm = 2
    mm = 3
    mil = 4


CONVERSION_MAP = {
    UnitOfLength.m: 1.0,
    UnitOfLength.cm: 1e-2,
    UnitOfLength.mm: 1e-3,
    UnitOfLength.mil: 2.54e-5
}


def create_conversion_to_m(unit: UnitOfLength):
    """
    converts the given length to meters
    @param unit:
    @return: returns a function whichs converts the given UnitOfLength to meters
    """
    return lambda x: CONVERSION_MAP[unit] * x
