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

""" Database Configuration class module.
"""


from typing import Dict
from gtmcore.data.config.baseconfiguration import (BaseConfiguration,
                                                   ConfigValueType)


class DBConfiguration(BaseConfiguration):
    """ Definition of database configuration aspects.
    """

    def get_config_template(self) -> Dict[str, ConfigValueType]:
        """ Gets the template of the configuration file.

        Returns:
            Dict[str, ConfigValueType]: Dictionary with the configuration file format.
        """
        config_template: Dict[str, ConfigValueType] = {}
        config_template["MARIADB_USER"] = "root"
        config_template["MARIADB_PASSWORD"] = "rootpassword"
        config_template["MARIADB_HOST"] = "172.16.0.10"
        config_template["MARIADB_PORT"] = 3306
        config_template["DATABASE_NAME"] = "gtm_database"
        config_template["DEBUG"] = False
        return config_template

    def get_username(self) -> str:
        """ Gets the database username.

        Returns:
            str: The username.
        """
        return str(self.get_value("MARIADB_USER"))

    def get_password(self) -> str:
        """ Gets the database password.

        Returns:
            str: The password.
        """
        return str(self.get_value("MARIADB_PASSWORD"))

    def get_host(self) -> str:
        """ Gets the database host.

        Returns:
            str: The host.
        """
        return str(self.get_value("MARIADB_HOST"))

    def get_port(self) -> int:
        """ Gets the database port.

        Returns:
            int: The port.
        """
        return int(str(self.get_value("MARIADB_PORT")))

    def get_dbname(self) -> str:
        """ Gets the database name.

        Returns:
            str: The database name.
        """
        return str(self.get_value("DATABASE_NAME"))

    def get_debug_state(self) -> bool:
        """ Gets the debug state.

        Returns:
            bool: The debug state.
        """
        return bool(self.get_value("DEBUG"))

    def get_config_module_str(self) -> str:
        """ Gets the configuration module name string.

        Returns:
            str: The configuration module name string.
        """
        return "gtmcore"


if __name__ == "__main__":
    config: DBConfiguration = DBConfiguration()
