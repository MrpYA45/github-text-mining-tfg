// Copyright (C) 2021 Pablo Fernández Bravo
//
// This file is part of github-text-mining-tfg.
//
// github-text-mining-tfg is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// github-text-mining-tfg is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with github-text-mining-tfg.  If not, see <http://www.gnu.org/licenses/>.

import { API_URL } from "./settings";
import fetchData from "./fetchData"

const extractRepoIssueComments = (response) => {
    const { eqlts: comments = [] } = response;
    if (Array.isArray(comments)) {
        return comments;
    }
    return [];
};

export default function getComments(gh_user, gh_repo, issue_id) {
    let apiURL = `${API_URL}/user/${gh_user}/repo/${gh_repo}/issue/${issue_id}/comments`;
    return fetchData(apiURL, extractRepoIssueComments)
}