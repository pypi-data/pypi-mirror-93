from typing import List

from sqlalchemy import Column, Float, Enum as SqlalchemyEnum, Boolean
from sqlalchemy.orm import composite
from sqlalchemy.ext.declarative import declared_attr

from ..core.point import Point
from ..core.dbnamedtuple import DbNamedTuple
from .textcolordefs import MirrorState
from .helper import mirroring_from_mstate


class ContainerMixin:

    # origin and angle are always relative to the parent object
    origin_x = Column(Float, nullable=False, default=0.0)
    origin_y = Column(Float, nullable=False, default=0.0)

    # angle and mirror are always relative to the origin
    angle = Column(Float, nullable=False, default=0.0)
    mirror = Column(SqlalchemyEnum(MirrorState), nullable=False, default=MirrorState.no_mirror)

    visible = Column(Boolean, nullable=False, default=True)


    # composite attributes
    @declared_attr
    def origin(cls):
        return composite(Point, cls.origin_x, cls.origin_y)

    # TODO all obj with functions rotate, mirror etc. should be in a mixin class, which then can be tested
    def _member_apply_transformation(self, member: DbNamedTuple):
        """
        Executes the Transformations: Mirroring, rotating and movement of the given element member,
        depending on the internal state.
        Returns the transfomred obj.
        @param member:
        @return:
        """
        if not issubclass(member.__class__, tuple):
            raise ValueError('invalid data type {}. DbNamedTuple expected'.format(type(member)))
        reference = Point(0, 0)
        return mirroring_from_mstate(member.rotate(reference, self.angle), self.mirror, reference).move(self.origin)

    def get_all_points(self) -> List[Point]:
        """
        returns all points of the container in a List
        @return:
        """
        raise NotImplementedError