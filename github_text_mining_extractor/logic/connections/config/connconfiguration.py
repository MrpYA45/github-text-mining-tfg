"""Connections Configuration class module.
"""
import os
import json


class ConnConfiguration():

    def __init__(self) -> None:
        file_path: str = "./config/config.json"
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=False)
            config_template: dict = self.get_config_template()
            with open(file_path, "w") as config_file:
                json.dump(config_template, config_file, indent=4)
        except OSError:
            pass

    @staticmethod
    def get_github_token() -> str:
        with open("./config/config.json") as config_file:
            config = json.load(config_file)
        return config["GITHUB_TOKEN"]

    @staticmethod
    def get_config_template() -> dict:
        config_template = {}
        config_template["GITHUB_TOKEN"] = ""
        return config_template


if __name__ == "__main__":
    config = ConnConfiguration()
