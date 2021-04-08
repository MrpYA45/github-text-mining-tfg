from datetime import datetime
import json
import github as gh
from typing import List, Optional
from github import Repository, Issue, Label, Github


class GitHubConnection():

    def __init__(self, token: str = "") -> None:
        # self.load_config()
        pass

    def load_config(self):
        with open('../config/config.json') as config_file:
            config = json.load(config_file)
            self.create_session(config['GITHUB_TOKEN'])

    def create_session(self, token: str = "") -> None:
        self.__g = gh.Github(token)

    def get_session(self) -> Github:
        return self.__g

    def get_rate_limit_reset(self) -> datetime:
        return self.__g.get_rate_limit().core.reset
