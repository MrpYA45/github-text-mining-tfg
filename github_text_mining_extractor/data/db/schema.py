""" Schema class module.
"""

from sqlalchemy import create_engine, event  # type: ignore
from sqlalchemy.engine import Engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from .results import Issue, Repository, Task
from ..config import DBConfiguration


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):  # pylint: disable=unused-argument
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.close()


class Schema():

    def __init__(self):
        self.__declarative_base = declarative_base()

        self.__engine = create_engine(
            DBConfiguration.get_engine_str(), echo=True)
        self.__session_maker = sessionmaker(bind=self.__engine)

        Issue.map(self.__declarative_base.metadata)
        Repository.map(self.__declarative_base.metadata)
        Task.map(self.__declarative_base.metadata)
        self.__declarative_base.metadata.create_all(self.__engine)

    def new_session(self) -> Session:
        return self.__session_maker()
