""" Schema class module.
"""

from github_text_mining.github_text_mining.data.config.dbconfiguration import \
    DBConfiguration
from github_text_mining.github_text_mining.data.db.results import (Issue,
                                                                   Repository,
                                                                   Task)
from sqlalchemy import create_engine, event  # type: ignore
from sqlalchemy.engine import Engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):  # pylint: disable=unused-argument
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.close()


class Schema():

    def __init__(self):
        self.__declarative_base = declarative_base()

        self.__engine = create_engine(
            DBConfiguration.get_engine_str(), echo=False)
        self.__session_maker = sessionmaker(bind=self.__engine)

        Issue.map(self.__declarative_base.metadata)
        Repository.map(self.__declarative_base.metadata)
        Task.map(self.__declarative_base.metadata)
        self.__declarative_base.metadata.create_all(self.__engine)

    def new_session(self) -> Session:
        return self.__session_maker()
