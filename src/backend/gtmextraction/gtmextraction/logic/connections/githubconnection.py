""" GitHub Connection class module.
"""


from datetime import datetime

import github as gh
from github import Github
from gtmextraction.logic.connections.config.connconfiguration import \
    ConnConfiguration


class GitHubConnection():
    """ Definition of github connection.
    """

    def __init__(self) -> None:
        self.__conn_config: ConnConfiguration = ConnConfiguration()
        self.__token: str = self.__conn_config.get_github_token()
        self.__g = gh.Github(self.__token)

    def get_session(self) -> Github:
        """ Gets a GitHub session to access the Github API.

        Returns:
            Github: The GitHub session.
        """
        return self.__g

    def get_rate_limit_reset(self) -> datetime:
        """ Gets the time when the rate limit of the GitHub connection resets.

        Returns:
            datetime: The reset time.
        """
        return self.__g.get_rate_limit().core.reset
