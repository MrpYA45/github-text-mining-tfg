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

import React from "react";
import { useLocation } from "wouter";
import "./Repo.css";

export default function Repo({ title, repo_dir = "", description = "", labels =""}) {

  const [, setLocation] = useLocation();

  const [gh_user, gh_repo] = repo_dir.split('/');

    return (
        <article className="Repo" onClick={() => setLocation(`/user/${gh_user}/repo/${gh_repo}`)}>
            <h3 className="RepoTitle">{title}</h3>
            <p className="RepoDir">{repo_dir}</p>
            <p className="RepoDesc">{description}</p>
            <div className="RepoTags">
                {labels.map((label) => (
                    <span key={label}>#{label}</span>
                ))}
            </div>
        </article>
    );
}
