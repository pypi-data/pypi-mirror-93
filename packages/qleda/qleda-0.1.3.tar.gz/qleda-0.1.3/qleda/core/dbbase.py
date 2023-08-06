from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session

from ..validation.decorators import check_clean_session


class _Base(object):

    @property
    def clean_session(self) -> Session:
        session = inspect(self).session
        return check_clean_session(session)

    @property
    def session(self) -> Session:
        return inspect(self).session


Base = declarative_base(cls=_Base)
