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

""" Base Configuration class module.
"""

import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from gtmcore.data.config.err.configurationfilenotcreated import \
    ConfigurationFileNotCreated

ConfigValueType = Optional[Union[int, str, float, bool, Dict, List, Tuple]]


class BaseConfiguration(ABC):
    """ The class responsible for creating and loading a per service configuration.
    """

    def __init__(self) -> None:
        self.config_path: Path = Path(
            "config/" + self.get_config_module_str() + "/settings.json").absolute()
        self.__config: Dict[str, ConfigValueType] = {}
        if not self.check_config_file_exists():
            self.create_config_file()
            logging.info("[GTMCORE] The configuration file for module '%s' has been created.",
                         self.get_config_module_str())
        self.load_config()

    def check_config_file_exists(self) -> bool:
        """ Checks if there is an existing configuration file in the service config path.

        Returns:
            bool: If the config file has been found or not.
        """
        try:
            return self.config_path.is_file()
        except OSError:
            return False

    def create_config_file(self) -> None:
        """ Creates or recreates the configuration file with the default template.

        Raises:
            ConfigurationFileNotCreated: Thrown when the configuration file could not be created.
        """
        try:
            config_template: dict = self.get_config_template()
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with self.config_path.open("w+", encoding="utf-8") as config_file:
                json.dump(config_template, config_file, indent=4)
        except OSError as err:
            raise ConfigurationFileNotCreated(
                f"The configuration file for '{self.get_config_module_str()}'"
                " could not be created"
            ) from err

    def load_config(self):
        """ Loads the keys and values from the configuration file.
        """
        with self.config_path.open("r", encoding="utf-8") as config_file:
            self.__config = json.load(config_file)

    def get_config(self) -> Dict[str, ConfigValueType]:
        """ Gets the dictionary with all the configuration keys and values.

        Returns:
            Dict[str, ConfigValueType]: A dictionary with all the configuration keys and values.
        """
        return self.__config

    def get_value(self, key: str) -> Optional[ConfigValueType]:
        """ Gets the value associated with the key in the configuration file.

        Args:
            key (str): The key from the configuration file.

        Returns:
            Optional[ConfigValueType]: The value associated with the key or None if not found.
        """
        try:
            return self.__config.get(key)
        except KeyError:
            return None

    def set_value(self, key: str, value: ConfigValueType) -> None:
        """ Sets the value associated with the key in the configuration.

        Args:
            key (str): The key of the configuration paramether.
            value (ConfigValueType): The value of the configuration paramether.

        Raises:
            TypeError: Thrown when the configuration file could not be created.
        """
        try:
            self.__config[key] = value
        except TypeError as err:
            raise TypeError(
                f"Incorrect value detected for key '{key}'" +
                f"at configuration file for '{self.get_config_module_str()}'.") from err

    @abstractmethod
    def get_config_template(self) -> Dict[str, ConfigValueType]:
        """ Gets the template of the configuration file.

        Returns:
            Dict[str, ConfigValueType]: Dictionary with the configuration file format.
        """
        return {}

    @abstractmethod
    def get_config_module_str(self) -> str:
        """ Gets the configuration module name string.

        Returns:
            str: The configuration module name string.
        """
        return ""
