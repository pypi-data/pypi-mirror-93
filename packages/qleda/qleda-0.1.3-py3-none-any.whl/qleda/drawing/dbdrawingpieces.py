from typing import Union, Optional

from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey, Float, Boolean, Enum as SqlalchemyEnum, \
    CheckConstraint, inspect
from sqlalchemy.orm import composite, relationship

from ..core.dbbase import Base
from .drawingpieces import Rect, Line, Text, Circle, Arc

from ..drawing.textcolordefs import LineStyle, JustHorziontal, JustVertical, MirrorState
from .textcolordefs import Color, Fill, LineFormat, TextFormat
from ..core.point import Point


class DbDrawingPiece(Base):
    __tablename__ = 'dp'
    id = Column(Integer, primary_key=True)

    container_id = Column(Integer, ForeignKey('dc.id'))
    container = relationship('DrawingContainer', back_populates='drawing_pieces')

    flatcontainer_id = Column(Integer, ForeignKey('flatcontainer.id'))
    flatcontainer = relationship('FlatContainer', back_populates='drawing_pieces')

    type = Column(String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'dp',
        'polymorphic_on': type
    }

    def tuple_repr(self):
        """
        returns the tuple representation of the obj
        @return:
        """
        raise NotImplementedError('to be implemented by child class')

    def copy(self):
        raise NotImplementedError('to be implemented by child class')
# TODO may remove origin and angle and save those kind of action like movement, rotation etc. on parrent obj

class DbPoint(DbDrawingPiece):
    """
    Db class of Point. Attributes definition done by _print_DbClass
    """
    __tablename__ = "point"

    id = Column(Integer, ForeignKey("dp.id"), primary_key=True)

    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)

    # composite attributes
    point = composite(Point, x, y)

    __mapper_args__ = {
        'polymorphic_identity': 'point',
    }

    def __repr__(self):
        return "DbPoint(id={}, point={})".format(self.id, self.point)

    def tuple_repr(self):
        return self.point

    def copy(self) -> 'DbPoint':
        return DbPoint(x=self.x, y=self.y)


class DbRect(DbDrawingPiece):
    """
    Db class of Rect. Attributes definition done by _print_DbClass
    """
    __tablename__ = "rect"

    id = Column(Integer, ForeignKey("dp.id"), primary_key=True)

    # origin
    origin_x = Column(Float, nullable=False)
    origin_y = Column(Float, nullable=False)

    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    angle = Column(Float, nullable=False)

    # line_format
    line_format_style = Column(SqlalchemyEnum(LineStyle), nullable=False)
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

    # composite attributes
    origin = composite(Point, origin_x, origin_y)
    line_format_color = composite(Color, line_format_color_r, line_format_color_g, line_format_color_b)
    line_format = composite(LineFormat._generate_from_row, line_format_style, line_format_width, line_format_color_r,
                            line_format_color_g, line_format_color_b, line_format_opacity)
    fill_color = composite(Color, fill_color_r, fill_color_g, fill_color_b)
    fill = composite(Fill._generate_from_row, fill_color_r, fill_color_g, fill_color_b, fill_opacity)
    rect = composite(Rect._generate_from_row, origin_x, origin_y, width, height, angle, line_format_style,
                     line_format_width, line_format_color_r, line_format_color_g, line_format_color_b,
                     line_format_opacity, fill_color_r, fill_color_g, fill_color_b, fill_opacity)

    __mapper_args__ = {
        'polymorphic_identity': 'rect',
    }

    def __repr__(self):
        return "DbRect(id={}, rect={})".format(self.id, self.rect)

    def tuple_repr(self):
        return self.rect

    def copy(self) -> 'DbRect':
        return DbRect(rect=self.rect)


class DbLine(DbDrawingPiece):
    """
    Db class of Line. Attributes definition done by _print_DbClass
    """
    __tablename__ = "line"

    id = Column(Integer, ForeignKey("dp.id"), primary_key=True)

    # a
    a_x = Column(Float, nullable=False)
    a_y = Column(Float, nullable=False)

    # b
    b_x = Column(Float, nullable=False)
    b_y = Column(Float, nullable=False)

    # line_format
    line_format_style = Column(SqlalchemyEnum(LineStyle), nullable=False)
    line_format_width = Column(Float, nullable=False)

    # line_format color
    # TODO use color mixin or a Color table to easier create Constraint on it
    line_format_color_r = Column(Integer, CheckConstraint('line_format_color_r >= 0 and line_format_color_r <= 255'),
                                 nullable=False)
    line_format_color_g = Column(Integer, nullable=False)
    line_format_color_b = Column(Integer, nullable=False)

    line_format_opacity = Column(Float, nullable=False)

    # composite attributes
    a = composite(Point, a_x, a_y)
    b = composite(Point, b_x, b_y)
    line_format_color = composite(Color, line_format_color_r, line_format_color_g, line_format_color_b)
    line_format = composite(LineFormat._generate_from_row, line_format_style, line_format_width, line_format_color_r,
                            line_format_color_g, line_format_color_b, line_format_opacity)
    line = composite(Line._generate_from_row, a_x, a_y, b_x, b_y, line_format_style, line_format_width,
                     line_format_color_r, line_format_color_g, line_format_color_b, line_format_opacity)

    __mapper_args__ = {
        'polymorphic_identity': 'line',
    }

    def __repr__(self):
        return "DbLine(id={}, line={})".format(self.id, self.line)

    def tuple_repr(self):
        return self.line

    def copy(self) -> 'DbLine':
        return DbLine(line=self.line)

# TODO rename to DbLabel
class DbText(Base):
    """
        Db class of Text. Most of attributes definition were done by _print_DbClass

        if value is None, then the Text value is read from the container object.
    """
    __tablename__ = "text"

    id = Column(Integer, primary_key=True)

    key = Column(String)
    # Fixme not the best solution, we have redundant information with this bool
    attribute_label = Column(Boolean, default=False, nullable=False)

    container_id = Column(Integer, ForeignKey('dc.id'))
    container = relationship('DrawingContainer', back_populates='labels')

    flatcontainer_id = Column(Integer, ForeignKey('flatcontainer.id'))
    flatcontainer = relationship('FlatContainer', back_populates='labels')

    # DBTexts function mirror must be called before rendering
    mirror = Column(SqlalchemyEnum(MirrorState), nullable=False, default=MirrorState.no_mirror)

    # origin
    origin_x = Column(Float, nullable=False)
    origin_y = Column(Float, nullable=False)

    value = Column(String)

    # format
    format_fontsize = Column(Integer, nullable=False)
    format_font = Column(String, nullable=False)
    format_horizontal = Column(SqlalchemyEnum(JustHorziontal), nullable=False)
    format_vertical = Column(SqlalchemyEnum(JustVertical), nullable=False)
    format_bold = Column(Boolean, nullable=False)
    format_italic = Column(Boolean, nullable=False)
    format_underline = Column(Boolean, nullable=False)
    format_strikethrough = Column(Boolean, nullable=False)

    # format color
    format_color_r = Column(Integer, nullable=False)
    format_color_g = Column(Integer, nullable=False)
    format_color_b = Column(Integer, nullable=False)

    # line_format
    line_format_style = Column(SqlalchemyEnum(LineStyle), nullable=False)
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

    angle = Column(Float, nullable=False)
    visible = Column(Boolean, nullable=False)

    # composite attributes
    origin = composite(Point, origin_x, origin_y)
    format_color = composite(Color, format_color_r, format_color_g, format_color_b)
    format = composite(TextFormat._generate_from_row, format_fontsize, format_font, format_horizontal, format_vertical,
                       format_bold, format_italic, format_underline, format_strikethrough, format_color_r,
                       format_color_g, format_color_b)
    line_format_color = composite(Color, line_format_color_r, line_format_color_g, line_format_color_b)
    line_format = composite(LineFormat._generate_from_row, line_format_style, line_format_width, line_format_color_r,
                            line_format_color_g, line_format_color_b, line_format_opacity)
    fill_color = composite(Color, fill_color_r, fill_color_g, fill_color_b)
    fill = composite(Fill._generate_from_row, fill_color_r, fill_color_g, fill_color_b, fill_opacity)

    __table_args__ = (UniqueConstraint('key', 'container_id', name='unique_key_container_id'),)

    def _get_value(self) -> str:
        if self.attribute_label:
            if self.container:
                return str(self.container.__getattribute__(self.key))
            elif self.flatcontainer:
                return str(self.flatcontainer.__getattribute__(self.key))
            else:
                raise ValueError('Either container_id or flatcontainer_id')
        else:
            return self.value

    # --------- properties --------
    @property
    def label(self) -> Text:
        if self.key is None and self.value is None:
            raise ValueError
        return Text(origin=self.origin,
                    value=self._get_value(),
                    format=self.format,
                    line_format=self.line_format,
                    fill=self.fill,
                    angle=self.angle,
                    visible=self.visible)

    @label.setter
    def label(self, label: Text):
        v = None if self.attribute_label else label.value

        self.origin = label.origin
        self.value = v
        self.format = label.format
        self.line_format = label.line_format
        self.fill = label.fill
        self.angle = label.angle
        self.visible = label.visible

    def __repr__(self):
        return "DbText(id={}, text={})".format(self.id, self.label.__repr__())

    @staticmethod
    def create_by_label(label: Text, attribute_label: bool, key: Optional[str] = None):
        """
        creates a DBText from the given label. If a key is given, it is assumed the label shall be an attribute_label
        for a container or a flatcontainer
        @param label:
        @param key: optional key for a attribute
        @return:
        """
        if key is None and label.value is None:
            raise ValueError('either key or label.value must be set')
        db_text = DbText(
            attribute_label=attribute_label,
            key=key
        )
        db_text.label = label
        return db_text

    def tuple_repr(self):
        return self.label

    def copy(self, copy_attribute_label: bool = True) -> 'DbText':
        ret_label = DbText(attribute_label=self.attribute_label if copy_attribute_label else False, key=self.key)
        ret_label.label = self.label
        return ret_label


class DbCircle(DbDrawingPiece):
    """
    Db class of Circle. Attributes definition done by _print_DbClass
    """
    __tablename__ = "circle"

    id = Column(Integer, ForeignKey("dp.id"), primary_key=True)

    # origin
    origin_x = Column(Float, nullable=False)
    origin_y = Column(Float, nullable=False)

    radius = Column(Float, nullable=False)

    # line_format
    line_format_style = Column(SqlalchemyEnum(LineStyle), nullable=False)
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

    # composite attributes
    origin = composite(Point, origin_x, origin_y)
    line_format_color = composite(Color, line_format_color_r, line_format_color_g, line_format_color_b)
    line_format = composite(LineFormat._generate_from_row, line_format_style, line_format_width, line_format_color_r,
                            line_format_color_g, line_format_color_b, line_format_opacity)
    fill_color = composite(Color, fill_color_r, fill_color_g, fill_color_b)
    fill = composite(Fill._generate_from_row, fill_color_r, fill_color_g, fill_color_b, fill_opacity)
    circle = composite(Circle._generate_from_row, origin_x, origin_y, radius, line_format_style, line_format_width,
                       line_format_color_r, line_format_color_g, line_format_color_b, line_format_opacity, fill_color_r,
                       fill_color_g, fill_color_b, fill_opacity)

    __mapper_args__ = {
        'polymorphic_identity': 'circle',
    }

    def __repr__(self):
        return "DbCircle(id={}, circle={})".format(self.id, self.circle)

    def tuple_repr(self):
        return self.circle

    def copy(self) -> 'DbCircle':
        return DbCircle(circle=self.circle)


class DbArc(DbDrawingPiece):
    """
    Db class of Arc. Attributes definition done by _print_DbClass
    """
    __tablename__ = "arc"

    id = Column(Integer, ForeignKey("dp.id"), primary_key=True)

    # origin
    origin_x = Column(Float, nullable=False)
    origin_y = Column(Float, nullable=False)

    # start
    start_x = Column(Float, nullable=False)
    start_y = Column(Float, nullable=False)

    angle = Column(Float, nullable=False)
    backwards_drawn = Column(Boolean, nullable=False)

    # composite attributes
    origin = composite(Point, origin_x, origin_y)
    start = composite(Point, start_x, start_y)
    arc = composite(Arc._generate_from_row, origin_x, origin_y, start_x, start_y, angle, backwards_drawn)

    __mapper_args__ = {
        'polymorphic_identity': 'arc',
    }

    def __repr__(self):
        return "DbArc(id={}, arc={})".format(self.id, self.arc)

    def tuple_repr(self):
        return self.arc

    def copy(self)-> 'DbArc':
        return DbArc(arc=self.arc)


class LabeledAttributeMixin:

    labels = None

    def _check_attr_name(self, attribute_name):
        if attribute_name.startswith('_'):
            raise ValueError('attributes beginning with a _ are system reserved and are not allowed to have a label')
        if not hasattr(self, attribute_name):
            raise AttributeError("given object has no attribute {}".format(attribute_name))
        attr = self.__getattribute__(attribute_name)
        if attr is not None and not isinstance(attr, (int, str, float)):
            raise TypeError('unsupported type to create a label')

        return attr

    def create_dblabel_for_attribute(self, attribute_name: str, label: Text) -> DbText:
        """
            creates or updates a label for the given existing internal attribute. A label can only be created for int,
            str and float objects
        @param attribute_name:
        @param label:
        @return:
        """
        self._check_attr_name(attribute_name)
        if isinstance(label, Text):
            if attribute_name in self.labels:
                rlabel = self.labels[attribute_name]
            else:
                rlabel = DbText(key=attribute_name)
            rlabel.attribute_label = True
            rlabel.label = label
        else:
            raise TypeError('only Text allowed')
        self.labels[attribute_name] = rlabel
        return rlabel

    def set_attribute_and_label(self, attribute_name: str, label: Text) -> DbText:
        """
            sets the attribute to the value saved in the given label and adds the attribute
        @param attribute_name:
        @param label:
        @return:
        """
        attr = self._check_attr_name(attribute_name)

        # Fixme not good enough we must know the Column type, but
        # using each time inspect would be really slow. Or it could be removed and checking is only done during
        # commit
        # https://stackoverflow.com/questions/45344384/how-to-inspect-custom-types-in-sqlalchemy
        if attr is not None and not isinstance(attr, str):
            raise TypeError('str attribute is expected')

        self.__setattr__(attribute_name, label.value)
        return self.create_dblabel_for_attribute(attribute_name, label)
