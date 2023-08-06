from collections.abc import Iterable
from typing import Union, List

from sqlalchemy import Column, Integer, UniqueConstraint, ForeignKey, Float, Boolean, String
from sqlalchemy.orm import composite, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from .dbdrawingpieces import DbDrawingPiece, DbPoint, DbArc, LabeledAttributeMixin
from .drawingpieces import Arc, Path as SimplePath
from .drawingmixins import ContainerMixin
from .textcolordefs import MirrorState, Color, Fill, LineFormat

from ..core.point import Point
from ..core.dbbase import Base


class DbSimplePathMember(Base):
    __tablename__ = 'simple_path_member'
    id = Column(Integer, primary_key=True)

    simple_path_id = Column(Integer, ForeignKey('simple_path.id'))
    simple_path = relationship("DbSimplePath", back_populates="members", foreign_keys=[simple_path_id])

    sequence = Column(Integer)

    dp_id = Column(Integer, ForeignKey('dp.id'), nullable=False)
    dp = relationship("DbDrawingPiece", foreign_keys=[dp_id])

    __table_args__ = (UniqueConstraint('sequence', 'simple_path_id', name='simple_path_member_uc_sequence'),
                      UniqueConstraint('dp_id', name='simple_path_member_uc_dp_id'))

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, sequence={self.sequence}, dp={self.dp})'

    def get_point_or_arc(self) -> Union[Point, Arc]:
        if isinstance(self.dp, DbArc):
            return self.dp.arc
        elif isinstance(self.dp, DbPoint):
            return self.dp.point
        else:
            raise ValueError


SimplePathMember = Union[DbPoint, DbArc, Arc, Point]


class DbSimplePath(ContainerMixin, DbDrawingPiece):
    """
        simple path, only points and arcs are allowed.

        A Path combines Point with Arc to one object.
        The connection between a point and an Arc is defined by the backwards_drawn attribute of the Arc.

        The bool closed defines if the path has to be closed or not.
    """
    __tablename__ = 'simple_path'

    id = Column(Integer, ForeignKey("dp.id"), primary_key=True)

    members = relationship("DbSimplePathMember", back_populates="simple_path", order_by=DbSimplePathMember.sequence)
    closed = Column(Boolean, nullable=False)

    # line_format
    line_format_style = Column(Integer, nullable=False)
    line_format_width = Column(Float, nullable=False)

    # line_format color
    line_format_color_r = Column(Integer, nullable=False)
    line_format_color_g = Column(Integer, nullable=False)
    line_format_color_b = Column(Integer, nullable=False)

    line_format_opacity = Column(Float, nullable=False)

    # fill

    # fill color
    fill_color_r = Column(Integer, nullable=False)
    fill_color_g = Column(Integer, nullable=False)
    fill_color_b = Column(Integer, nullable=False)

    fill_opacity = Column(Float, nullable=False)

    line_format_color = composite(Color, line_format_color_r, line_format_color_g, line_format_color_b)
    line_format = composite(LineFormat._generate_from_row, line_format_style, line_format_width, line_format_color_r,
                            line_format_color_g, line_format_color_b, line_format_opacity)
    fill_color = composite(Color, fill_color_r, fill_color_g, fill_color_b)
    fill = composite(Fill._generate_from_row, fill_color_r, fill_color_g, fill_color_b, fill_opacity)

    __mapper_args__ = {
        'polymorphic_identity': 'simple_path',
    }

    def __init__(self, **kwargs):
        if 'members' in kwargs:
            members = kwargs['members']
            if not isinstance(members, Iterable):
                raise TypeError('members need to be an Iterable')
            for index, arc_or_point in enumerate(members):
                self._create_simple_path_member(arc_or_point, index)
        del kwargs['members']
        super().__init__(**kwargs)

    def _create_simple_path_member(self, arc_or_point: SimplePathMember, index: int):
        if isinstance(arc_or_point, (DbPoint, DbArc)):
            DbSimplePathMember(simple_path=self, sequence=index, dp=arc_or_point)
        elif isinstance(arc_or_point, Arc):
            DbSimplePathMember(simple_path=self, sequence=index, dp=DbArc(arc=arc_or_point))
        elif isinstance(arc_or_point, Point):
            DbSimplePathMember(simple_path=self, sequence=index, dp=DbPoint(point=arc_or_point))
        else:
            raise TypeError('{} can only contain DbPoint, DbArc, Point or Arc objects. is {}'.format(self.__tablename__,
                                                                                                     arc_or_point))

    def append(self, arc_or_point: SimplePathMember):
        index = len(self.members)
        self._create_simple_path_member(arc_or_point, index)

    def insert(self, arc_or_point: SimplePathMember, index: int):
        if index > len(self.members):
            raise IndexError
        for i, m in enumerate(self.members[index:]):
            self.members[i+index].sequence = i + index + 1

        self._create_simple_path_member(arc_or_point, index)

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, closed={self.closed}, line_format={self.line_format},' \
               f' fill={self.fill}, members={self.members})'

    @property
    def simple_path(self) -> SimplePath:
        s = SimplePath(
            p_or_arc_tuple=tuple([x.get_point_or_arc() for x in self.members]),
            closed=self.closed,
            line_format=self.line_format,
            fill=self.fill)
        return self._member_apply_transformation(s)

    @staticmethod
    def create_by_simple_path(s: SimplePath) -> 'DbSimplePath':
        """
        create a DBSimplePath object from the given Path
        @param s:
        @return:
        """
        return DbSimplePath(
            origin=Point(0, 0),
            angle=0,
            mirror=MirrorState.no_mirror,
            members=s.p_or_arc_tuple,
            closed=s.closed,
            line_format=s.line_format,
            fill=s.fill
        )

    def tuple_repr(self):
        return self.simple_path

    def copy(self) -> 'DbSimplePath':
        return DbSimplePath.create_by_simple_path(self.simple_path)


class DrawingContainer(LabeledAttributeMixin, ContainerMixin, Base):
    __tablename__ = 'dc'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    drawing_pieces = relationship("DbDrawingPiece", back_populates='container')

    parent_id = Column(Integer, ForeignKey('dc.id'))
    parent = relationship('DrawingContainer', back_populates='children', foreign_keys=[parent_id], remote_side=[id])

    labels = relationship('DbText',
                              back_populates='container',
                              collection_class=attribute_mapped_collection('key'),
                              cascade="all, delete")

    children = relationship('DrawingContainer', back_populates='parent')

    __mapper_args__ = {
        'polymorphic_identity': 'dc',
        'polymorphic_on': type
    }

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, origin={self.origin}, angle={self.angle}, ' \
               f'drawing_pieces={self.drawing_pieces}, children={self.children})'

    def get_all_points(self) -> List[Point]:
        if self.visible:
            ps = [
                *[p for dp in self.drawing_pieces for p in dp.tuple_repr().get_p() if p],
                *[p for label in self.labels for p in label.tuple_repr().get_p() if label.visible and p]
            ]
            for child in self.children:
                ps.extend([p.move(self.origin) for p in child.get_all_points()])
            return ps
        else:
            None


class FlatContainer(LabeledAttributeMixin, ContainerMixin, Base):
    """
        FlatContainer only allow one level of drawing pieces.
        Should be used for inheritance.
    """
    __tablename__ = 'flatcontainer'
    id = Column(Integer, primary_key=True)
    type = Column(String)

    drawing_pieces = relationship('DbDrawingPiece', back_populates='flatcontainer')

    labels = relationship('DbText',
                              back_populates='flatcontainer',
                              collection_class=attribute_mapped_collection('key'),
                              cascade="all, delete")

    __mapper_args__ = {
        'polymorphic_identity': 'flatcontainer',
        'polymorphic_on': type
    }

    def get_all_points(self) -> List[Point]:
        if self.visible:
            return [
                *[p for dp in self.drawing_pieces for p in dp.tuple_repr().get_p() if p],
                *[p for label in self.labels.values() for p in label.tuple_repr().get_p() if label.visible and p]
            ]
        else:
            None
