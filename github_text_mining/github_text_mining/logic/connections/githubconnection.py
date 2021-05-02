import json
from datetime import datetime
from typing import List, Optional

import github as gh
from github import Github, Issue, Label, Repository
from github_text_mining.github_text_mining.logic.connections.config import \
    ConnConfiguration


class GitHubConnection():

    def __init__(self) -> None:
        self.__g = gh.Github(ConnConfiguration.get_github_token())

    def get_session(self) -> Github:
        return self.__g

    def get_rate_limit_reset(self) -> datetime:
        return self.__g.get_rate_limit().core.reset
