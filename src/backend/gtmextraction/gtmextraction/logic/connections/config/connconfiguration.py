"""Connections Configuration class module.
"""
import json
import os


class ConnConfiguration():
    """[summary]
    """

    file_path: str = "app/backend/config/config.json"

    def __init__(self) -> None:
        """[summary]
        """
        try:
            os.makedirs(os.path.dirname(
                ConnConfiguration.file_path), exist_ok=False)
            config_template: dict = self.get_config_template()
            with open(ConnConfiguration.file_path, "w") as config_file:
                json.dump(config_template, config_file, indent=4)
        except OSError:
            pass

    @ staticmethod
    def get_github_token() -> str:
        with open(ConnConfiguration.file_path) as config_file:
            loaded_config = json.load(config_file)
        return loaded_config["GITHUB_TOKEN"]

    @ staticmethod
    def get_config_template() -> dict:
        config_template = {}
        config_template["GITHUB_TOKEN"] = ""
        return config_template


if __name__ == "__main__":
    config = ConnConfiguration()
