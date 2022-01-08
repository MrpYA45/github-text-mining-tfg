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
