"""Connections Configuration class module.
"""


from typing import Dict

from gtmcore.data.config.baseconfiguration import (BaseConfiguration,
                                                   ConfigValueType)


class ConnConfiguration(BaseConfiguration):
    """ Definition of github connection configuration aspects.
    """

    def __init__(self) -> None:
        BaseConfiguration.__init__(self)

    def get_config_template(self) -> Dict[str, ConfigValueType]:
        """ Gets the template of the configuration file.

        Returns:
            Dict[str, ConfigValueType]: Dictionary with the configuration file format.
        """
        config_template: Dict[str, ConfigValueType] = {}
        config_template["GITHUB_TOKEN"] = ""
        return config_template

    def get_github_token(self) -> str:
        """ Gets the github token string.

        Returns:
            str: The github token string.
        """
        return str(self.get_value("GITHUB_TOKEN"))

    def get_config_module_str(self) -> str:
        """ Gets the configuration module name string.

        Returns:
            str: The configuration module name string.
        """
        return "gtmcore_configuration"


if __name__ == "__main__":
    config: BaseConfiguration = ConnConfiguration()
