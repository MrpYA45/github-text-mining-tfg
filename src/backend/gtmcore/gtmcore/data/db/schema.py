# Copyright (C) 2021 Pablo Fernández Bravo
#
# This file is part of github-text-mining-tfg.
#
# github-text-mining-tfg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# github-text-mining-tfg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with github-text-mining-tfg.  If not, see <http://www.gnu.org/licenses/>.

""" Schema class module.
"""

from gtmcore.data.config.dbconfiguration import DBConfiguration
from gtmcore.data.db.results import Comment, Issue, Outcome, Repository, Task
from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore


class Schema():
    """ Database Schema.
    """

    def __init__(self):
        self.__declarative_base = declarative_base()

        self.__db_config: DBConfiguration = DBConfiguration()

        self.__engine = create_engine(
            self.get_engine_str(), pool_pre_ping=True,
            echo=self.__db_config.get_value("DEBUG"), max_overflow=-1)

        self.__session_maker = sessionmaker(
            bind=self.__engine, autoflush=True, autocommit=False)

        Issue.map(self.__declarative_base.metadata)
        Repository.map(self.__declarative_base.metadata)
        Task.map(self.__declarative_base.metadata)
        Comment.map(self.__declarative_base.metadata)
        Outcome.map(self.__declarative_base.metadata)
        self.__declarative_base.metadata.create_all(self.__engine)

    def new_session(self) -> Session:
        """ Creates a new database session.

        Returns:
            Session: The database session.
        """
        session: Session = self.__session_maker()
        session.expire_on_commit = False
        return session

    def dispose_engine(self) -> None:
        """ Closes all current database connections.
        """
        self.__engine.dispose()

    def get_engine_str(self) -> str:
        """ Gets the engine connection string.

        Returns:
            str: The engine connection string.
        """
        mdb_user: str = self.__db_config.get_username()
        mdb_pd: str = self.__db_config.get_password()
        mdb_host: str = self.__db_config.get_host()
        mdb_port: str = str(self.__db_config.get_port())
        db_name: str = self.__db_config.get_dbname()
        return f"mariadb+mariadbconnector://{mdb_user}:{mdb_pd}@{mdb_host}:{mdb_port}/{db_name}"
