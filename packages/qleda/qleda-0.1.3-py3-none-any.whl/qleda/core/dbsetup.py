from typing import NamedTuple
from pathlib import Path
from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.engine import Engine

from .dbbase import Base


class DbVariables(NamedTuple):
    engine: Engine
    session: Session


def init_db(path: Union[bool, Path] = False, echo: bool = False, override: bool = False) -> DbVariables:
    """

    @param path: False: in memory
                 otherwise path to DB (SQLite)
    @param echo: use SQL logging or not
    @param override: True: delete old Sqlite database
    @return:
    """
    if path and not path.parent.exists():
        path.parent.mkdir(parents=True)
    p = 'sqlite:///:memory:' if path is False else 'sqlite:///{}'.format(path.absolute())
    if override and path and path.is_file():
        path.unlink()
    engine = create_engine(p, echo=echo)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DbVariables(engine, DBSession())
