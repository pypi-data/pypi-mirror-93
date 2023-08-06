from sqlalchemy.orm.session import Session

from ..model.basic import PartLibrary, Part, Pin

from .decorators import req_clean_session
from .exceptions import EmptyPinNames


@req_clean_session
def part_library_no_empty_pin_name(session: Session, library: PartLibrary):
    assert library.id is not None
    r = session.query(Pin).join(Part).join(PartLibrary).filter(PartLibrary.id == library.id).filter(Pin.name == None)
    if r.count() > 0:
        raise EmptyPinNames(r)

