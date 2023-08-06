import typing

# every class which should be able to be an composite Value need to have the functions __composite_values__,
# __eq__ and __ne__. NamedTuple already has two of them, so only __composite_values__ needs to be added
# By inheritance of this can be achieved

# function __composite_values__ must return all fields in one tuple (in correct order). nested Tuples must be unpacked
# Nested Tuple additionaly need a generate function. We name it here _generate_from_row

_f_name_composite_values = '__composite_values__'
_f_name_generate_from_row = '_generate_from_row'
_attr_nested_structure = '_nested_structure'


class DbNamedTupleMeta(typing.NamedTupleMeta):

    def __new__(cls, typename, bases, ns):
        assert len(bases) < 2
        if bases:
            bases = (typing._NamedTuple, *bases)
            named_tuple_cls = super().__new__(cls, typename, bases, ns)
        else:
            return super(typing.NamedTupleMeta, cls).__new__(cls, typename, bases, ns)

        fields = named_tuple_cls._fields

        def composite_values(self):
            r = []
            for f in fields:
                attr = self.__getattribute__(f)
                if isinstance(attr, tuple):
                    r.extend(attr.__composite_values__())
                else:
                    r.append(attr)
            return tuple(r)
        setattr(named_tuple_cls, _f_name_composite_values, composite_values)
        nested_structure = tuple([(c, sum([x[1] if type(x) == tuple else 1
                                           for x in c._nested_structure])) if hasattr(c, _attr_nested_structure)
                                  else c for c in named_tuple_cls.__annotations__.values()])
        setattr(named_tuple_cls, _attr_nested_structure, nested_structure)

        # could be investigated if this can be done faster
        def generate_from_row(cls, *args):
            t = []
            counter = 0
            for i, a in enumerate(cls._nested_structure):
                if type(a) == tuple:
                    t.append(a[0]._generate_from_row(*args[counter:counter+a[1]]))
                    counter += a[1]
                else:
                    t.append(args[counter])
                    counter += 1
            return cls.__new__(cls, *t)
        setattr(named_tuple_cls, _f_name_generate_from_row, classmethod(generate_from_row))

        return named_tuple_cls


class DbNamedTuple(metaclass=DbNamedTupleMeta):

    def _nested_structure(self) -> tuple:
        raise NotImplementedError('added in DbNamedTupleMeta __new__ function')

    def __composite_values__(self) -> tuple:
        raise NotImplementedError('added in DbNamedTupleMeta __new__ function')

    def _generate_from_row(self) -> tuple:
        raise NotImplementedError('added in DbNamedTupleMeta __new__ function')
