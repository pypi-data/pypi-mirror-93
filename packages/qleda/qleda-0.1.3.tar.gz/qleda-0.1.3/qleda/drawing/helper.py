"""
    should only be a temporary file. Use when it's unclear where to move functions or if they are used during
    development but they can be deleted later.
"""

from .textcolordefs import MirrorState
from ..core.point import Point


def mirroring_from_mstate(obj_to_mirror, mirror_state_to_apply: MirrorState, reference: Point):
    if mirror_state_to_apply == MirrorState.no_mirror:
        return obj_to_mirror
    elif mirror_state_to_apply == MirrorState.v_mirror:
        return obj_to_mirror.x_mirror(reference)
    elif mirror_state_to_apply == MirrorState.h_mirror:
        return obj_to_mirror.y_mirror(reference)
    elif mirror_state_to_apply == MirrorState.hv_mirror:
        return obj_to_mirror.x_y_mirror(reference)