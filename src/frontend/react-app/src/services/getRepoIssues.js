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

const extractRepoIssuesInfo = (response) => {
    const { eqlts = [] } = response;
    if (Array.isArray(eqlts)) {
        const issues = eqlts.map((issue) => {
            const {
                repo_dir,
                issue_id,
                author,
                title,
                description,
                labels,
                is_pull_request,
            } = issue;
            return {
                repo_dir,
                issue_id,
                author,
                title,
                description,
                labels,
                is_pull_request,
            };
        });
        return issues;
    }
    return [];
};

export default function getRepoIssues(gh_user, gh_repo) {
    const apiURL = `${API_URL}/user/${gh_user}/repo/${gh_repo}/issues`;
    return fetch(apiURL)
        .then((res) => res.json())
        .then(extractRepoIssuesInfo)
        .catch((err) => console.error(err));
}
