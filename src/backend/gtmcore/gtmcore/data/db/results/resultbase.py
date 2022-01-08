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

""" ResultBase class module.
"""

from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy import MetaData, Table  # type: ignore
from sqlalchemy.orm import mapper  # type: ignore


class ResultBase(ABC):
    """ Base class for all the database record classes.
    """

    @classmethod
    def map(cls: type, metadata: MetaData) -> None:
        """ Maps the database user records to instances of this class.

        Args:
            cls (type): This class.
            metadata (MetaData): The database schema metadata
                (used to gather the entities' definitions and mapping)
        """
        mapper(
            cls,
            cls._table_definition(metadata),  # type: ignore
            properties=cls._mapping_properties()  # type: ignore
        )

    @staticmethod
    @abstractmethod
    def _table_definition(metadata: MetaData) -> Table:
        """ Gets the table definition.

        Args:
            metadata(MetaData): The database schema metadata
                (used to gather the entities' definitions and mapping).

        Returns:
            Table: A Table object with the table definition.
        """

    @staticmethod
    def _mapping_properties() -> Dict:
        """ Gets the mapping properties dictionary.

        Returns:
            Dict: A dictionary with the mapping properties.
        """
        return {}
