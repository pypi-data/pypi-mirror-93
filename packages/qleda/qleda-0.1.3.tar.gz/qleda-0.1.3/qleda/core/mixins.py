from collections import Iterable

from sqlalchemy import inspect
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import RelationshipProperty, ColumnProperty
from sqlalchemy.orm.collections import MappedCollection
from sqlalchemy.util import symbol

from .dbbase import Base
from ..common.electrical import Polarity, SimulationType, PinType


class classproperty(object):
    """
    @property for @classmethod
    taken from http://stackoverflow.com/a/13624858
    """

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class DefaultReprMixin:

    def _default_cols_repr(self):
        return', '.join(['{}={}'.format(c.name, getattr(self, c.name).__repr__()) for c in self.__table__.columns])

    def __repr__(self):
        return f'{self.__class__.__name__}({self._default_cols_repr()})'


# copied from https://github.com/absent1706/sqlalchemy-mixins/blob/master/sqlalchemy_mixins/inspection.py
class InspectionMixin(Base):
    __abstract__ = True

    @classproperty
    def columns(cls):
        return inspect(cls).columns.keys()

    @classproperty
    def primary_keys_full(cls):
        """Get primary key properties for a SQLAlchemy cls.
        Taken from marshmallow_sqlalchemy
        """
        mapper = cls.__mapper__
        return [
            mapper.get_property_by_column(column)
            for column in mapper.primary_key
        ]

    @classproperty
    def primary_keys(cls):
        return [pk.key for pk in cls.primary_keys_full]

    @classproperty
    def relations(cls):
        """Return a `list` of relationship names or the given model
        """
        return [c.key for c in cls.__mapper__.iterate_properties
                if isinstance(c, RelationshipProperty)]

    @classproperty
    def settable_relations(cls):
        """Return a `list` of relationship names or the given model
        """
        return [r for r in cls.relations
                if getattr(cls, r).property.viewonly is False]

    @classproperty
    def hybrid_properties(cls):
        items = inspect(cls).all_orm_descriptors
        return [item.__name__ for item in items
                if type(item) == hybrid_property]

    @classproperty
    def hybrid_methods_full(cls):
        items = inspect(cls).all_orm_descriptors
        return {item.func.__name__: item
                for item in items if type(item) == hybrid_method}

    @classproperty
    def hybrid_methods(cls):
        return list(cls.hybrid_methods_full.keys())


SERIALIZE_SUPPORTED_ENUM = {Polarity, SimulationType, PinType}
_ENUM_SERIALIZE_MAP = {
    enum_t: {enum_entry: enum_entry.name for enum_entry in enum_t}
    for enum_t in SERIALIZE_SUPPORTED_ENUM
}

_ENUM_DESERIALIZE_MAP = {
    enum_t: {enum_entry.name: enum_entry for enum_entry in enum_t}
    for enum_t in SERIALIZE_SUPPORTED_ENUM
}


# starting point copied from https://github.com/absent1706/sqlalchemy-mixins/blob/master/sqlalchemy_mixins/serialize.py
class SerializeMixin(InspectionMixin):
    """Mixin to make model serializable."""

    __abstract__ = True

    _serialization_ignore_keys = {}
    _serialization_ignore_backref = True

    def to_dict(self, nested: bool = False, hybrid_attributes: bool = False, full_depth: bool = False):
        """Return dict object with model's data.
        :@param nested: flag to return nested relationships' data if true
        :@param hybrid_attributes: flag to include hybrid attributes if true
        :@param full_depth: True go into full depth of all objects
        :@return: dict
        """
        result = dict()
        for key in self.columns:
            if key not in self._serialization_ignore_keys:
                if (attr := getattr(self, key)) is not None:
                    if (t_attr := type(attr)) in _ENUM_SERIALIZE_MAP:
                        result[key] = _ENUM_SERIALIZE_MAP[t_attr][attr]
                    else:
                        result[key] = attr

        if hybrid_attributes:
            for key in self.hybrid_properties:
                result[key] = getattr(self, key)

        # [c.key for c in cls.__mapper__.iterate_properties
        #                 if isinstance(c, RelationshipProperty)]
        if nested or full_depth:
            r_properties = [c for c in self.__class__.__mapper__.iterate_properties
                        if isinstance(c, RelationshipProperty) and c.direction not in {symbol('MANYTOONE')}]
            for r_property in r_properties:
                key = r_property.key
                obj = getattr(self, key)

                if isinstance(obj, SerializeMixin) and obj is not None:
                    result[key] = obj.to_dict(hybrid_attributes=hybrid_attributes, full_depth=full_depth)
                elif isinstance(obj, MappedCollection) and obj:
                    result[key] = {k: o.to_dict(hybrid_attributes=hybrid_attributes, full_depth=full_depth) for k, o in obj.items()}
                elif isinstance(obj, Iterable) and obj:
                    result[key] = [o.to_dict(hybrid_attributes=hybrid_attributes, full_depth=full_depth) for o in obj]

        return result

    @classmethod
    def from_dict(cls, d: dict):
        """
        reads from dict
        @param d:
        @return: cls object
        """
        prop_d = {p.key: p for p in cls.__mapper__.iterate_properties}
        init_args = {}
        for k, v in d.items():
            prop = prop_d[k]
            if isinstance(prop, ColumnProperty):
                if (t_attr := cls.__table__.c[k].type.python_type) in SERIALIZE_SUPPORTED_ENUM:
                    init_args[k] = _ENUM_DESERIALIZE_MAP[t_attr][v]
                else:
                    init_args[k] = v
            elif isinstance(prop, RelationshipProperty):
                if issubclass(prop.entity.class_, SerializeMixin):
                    if prop.direction == symbol('ONETOMANY'):
                        if isinstance(v, dict):
                            init_args[k] = {v_key: prop.entity.class_.from_dict(v_value) for v_key, v_value in v.items()}
                        elif isinstance(v, list):
                            init_args[k] = [prop.entity.class_.from_dict(v_value) for v_value in v]
                        else:
                            raise ValueError
                    else:
                        raise NotImplementedError('At the moment only ONETOMANY realtions are supported')
            else:
                ValueError('Only ColumnProperty or RelationshipProperty are supported')
        return cls(**init_args)


