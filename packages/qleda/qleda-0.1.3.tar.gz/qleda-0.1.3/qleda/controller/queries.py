from typing import Iterable, Optional
from enum import Enum
from sqlalchemy import and_, update, select, exists, or_, insert
from sqlalchemy.orm import aliased, Query
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import Select
from sqlalchemy import func

from ..model.basic import Part, PartProperty, Schematic, PartLibrary, Pin, DiffNet, Net


def query_missing_part_attributes(session: Session, schematic_id: int, library_id: int) -> Query:
    query_schematic_properties = session.query(
        Part.name.label('sch_part_name'),
        PartProperty.name.label('sch_prop_name')).select_from(PartProperty).join(Part)\
        .filter(Part.schematic_id == schematic_id) \
        .group_by('sch_part_name', 'sch_prop_name').cte('schematic_properties')
    query_library_properties = session.query(
        Part.name.label('lib_part_name'),
        PartProperty.name.label('lib_prop_name')).select_from(Part).join(PartProperty)\
        .join(PartLibrary) \
            .filter(PartLibrary.id == library_id)\
        .group_by('lib_part_name',
                                                                                           'lib_prop_name')
    query_library_properties = query_library_properties.cte('library_properties')
    result_query = session.query('lib_part_name', 'lib_prop_name').select_from(query_library_properties) \
        .outerjoin(query_schematic_properties,
                   and_(query_schematic_properties.c.sch_part_name == query_library_properties.c.lib_part_name,
                        query_schematic_properties.c.sch_prop_name == query_library_properties.c.lib_prop_name)) \
        .join(Part, Part.name == query_library_properties.c.lib_part_name) \
        .filter(Part.schematic_id != None) \
        .filter(query_schematic_properties.c.sch_prop_name == None)
    return result_query


def update_schematic_pins_from_libraries(session: Session, schematic_id: int, library_id: int):
    """

    @param session:
    @param schematic_id:
    @param library_id:
    @return:
    """
    pin_sch = aliased(Pin, name='pin_sch')
    pin_lib = aliased(Pin, name='pin_lib')
    part_sch = aliased(Part, name='part_sch')
    part_lib = aliased(Part, name='part_lib')
    u_table = session.query(pin_sch.id, pin_lib.name)\
        .select_from(pin_sch)\
        .join(part_sch, part_sch.id == pin_sch.part_id)\
        .join(part_lib, part_lib.name == part_sch.name)\
        .join(pin_lib, and_(pin_lib.part_id == part_lib.id, pin_lib.designator == pin_sch.designator))\
        .filter(part_sch.schematic_id == schematic_id)\
        .filter(part_lib.library_id == library_id)\
        .filter(pin_sch.name == None).cte('u_table')
    u_stmt = update(Pin.__table__).values(name=select([u_table.c.name]).where(u_table.c.id == Pin.id)).where(
        exists(select([u_table.c.name]).where(u_table.c.id == Pin.id))
    )
    session.execute(u_stmt)
    session.commit()


def schematic_build_nets_diff_pairs_from_net_names(session: Session, schematic_id: int) -> Query:
    """
    Builds diff Net's, if nets differs only in '_N' '_P' suffixes.
    @param session:
    @param schematic_id:
    @return:
    """
    nets_p = session.query(Net.id, func.REPLACE(Net.name, '_P', '').label('match_name'), Net.schematic_id.label('schematic_id')).filter(Net.schematic_id == schematic_id)\
        .filter(Net.name.like('%_P'))\
        .cte('nets_p')
    nets_n = session.query(Net.id, func.REPLACE(Net.name, '_N', '').label('match_name')).filter(Net.schematic_id == schematic_id)\
        .filter(Net.name.like('%_N')).cte('nets_n')
    return session.query(nets_p.c.id.label('p_id'), nets_p.c.match_name.label('name'), nets_n.c.id.label('n_id'),
                         nets_p.c.schematic_id.label('schematic_id')).select_from(nets_p)\
        .join(nets_n, nets_p.c.match_name == nets_n.c.match_name)\
        .join(DiffNet, or_(nets_p.c.id == DiffNet.p_id, nets_n.c.id == DiffNet.n_id), isouter=True)\
        .filter(DiffNet.id == None)


def insert_diff_net_by_query(session: Session, query: Query):
    q = query.cte('bla')
    i_stmt = DiffNet.__table__.insert() \
        .from_select([q.c.name, q.c.p_id, q.c.n_id, q.c.schematic_id], select([q.c.name, q.c.p_id, q.c.n_id,
                                                                               q.c.schematic_id]))
    session.execute(i_stmt)
    session.commit()


class NSerieParts(Enum):
    zero = 0
    one = 1


def query_signal_paths(session: Session, schematic_id: int, start_designator: str, end_designators: Iterable[str],
                       max_series_part: NSerieParts, max_nodes_each_net: int,
                       illegal_net_ids: Optional[Iterable[int]] = None) -> Select:
    """
        Important start and end nets name must much with the following query:
            <start_net_name> like <end_net_name> + '%' or  <end_net_name> like <start_net_name> + '%'
        or there is a serial part

    @param session:
    @param schematic_id: 
    @param start_designator: 
    @param end_designators:
    @param max_series_part: 
    @param max_nodes_each_net:
    @param illegal_net_ids:

    @return: 
    """
    possible_nets = session.query(Net.id, Net.name).join(Pin).\
                    filter(Net.schematic_id == schematic_id)\
                    .group_by(Net.id).having(func.count(Pin.id) <= max_nodes_each_net)
    if illegal_net_ids:
        possible_nets = possible_nets.filter(~Net.id.in_(illegal_net_ids)).cte('possible_nets')
    else:
        possible_nets = possible_nets.cte('possible_nets')

    serial_parts = session.query(Part.id).join(Pin)\
        .filter(Part.schematic_id == schematic_id)\
        .group_by(Part.id)\
        .having(func.count(Pin.id) == 2).cte('serial_parts')
    start = session.query(
        Pin.id.label('pin_id'),
        Pin.designator.label('pin_designator'),
        Net.id.label('net_id'),
        Net.name.label('net_name'),
        Part.designator.label('part_designator'),
        Part.id.label('part_id'))\
        .select_from(Net)\
        .join(Pin)\
        .join(possible_nets, possible_nets.c.id == Net.id)\
        .join(Part, Part.id == Pin.part_id).cte('s')

    end = aliased(start, name='e')

    if max_series_part == NSerieParts.zero:
        stmt = select([
            start.c.part_id,
            start.c.pin_id,
            start.c.pin_designator,
            start.c.net_name,
            start.c.net_id,
            end.c.pin_id,
            end.c.pin_designator,
            end.c.net_name,
            end.c.part_id,
        ]).select_from(
            start.join(end, end.c.net_id == start.c.net_id)
        ).apply_labels()\
            .where(start.c.part_designator == start_designator)\
            .where(end.c.part_designator.in_(end_designators))
        return stmt

    left = aliased(start, name='l')
    right = aliased(start, name='r')
    if max_series_part == NSerieParts.one:
        stmt = select([
            start.c.part_id,
            start.c.pin_id,
            start.c.pin_designator,
            start.c.net_name,
            start.c.net_id,
            left.c.net_name,
            left.c.pin_designator,
            left.c.pin_id,
            left.c.part_designator,
            left.c.part_id,
            right.c.pin_id,
            right.c.pin_designator,
            right.c.net_name,
            end.c.net_name,
            end.c.pin_id,
            end.c.pin_designator,
            end.c.part_id,
        ]).select_from(
            start.join(left, and_(left.c.net_id == start.c.net_id, start.c.part_id != left.c.part_id))\
                .join(right, and_(right.c.part_id == left.c.part_id, left.c.net_id != right.c.net_id))\
                .join(end, and_(right.c.net_id == end.c.net_id, right.c.part_id != end.c.part_id))
        ).apply_labels()\
            .where(end.c.net_id != start.c.net_id)\
            .where(or_(end.c.net_name.like(start.c.net_name + '%'),
                       start.c.net_name.like(end.c.net_name + '%'),
                       left.c.part_id.in_(serial_parts)
                       ))\
            .where(start.c.part_designator == start_designator)\
            .where(end.c.part_designator.in_(end_designators))
        return stmt
    else:
        raise NotImplementedError
