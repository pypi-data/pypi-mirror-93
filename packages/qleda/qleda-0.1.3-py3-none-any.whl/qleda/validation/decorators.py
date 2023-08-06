from sqlalchemy.orm.session import Session
from typing import Callable

from .exceptions import DirtySessionException


def check_clean_session(session: Session) -> Session:
    if session.dirty:
        raise DirtySessionException('A clean session was expected')
    return session

def req_clean_session(func: Callable):
    """
        check if the session is in a clean state
    """
    def wrapper(session: Session, *args, **kwargs):
        check_clean_session(session)
        func(session, *args, **kwargs)

    return wrapper
