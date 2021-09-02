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

import React, { useEffect, useState, useRef } from "react";
import Repo from "../Repo";
import getRepos from "../../services/getRepos";
import { REFRESH_DATA_INTERVAL } from "../../services/settings";
import "./ListOfRepos.css";
import AnchorLink from "react-anchor-link-smooth-scroll";

export default function ListOfRepos() {
    const [loading, setLoading] = useState(false);
    const [repos, setRepos] = useState([]);

    const interval = useRef();

    useEffect(function () {
        setLoading(true);
        updateRepos();
        interval.current = setInterval(updateRepos, REFRESH_DATA_INTERVAL);
        return () => {
            clearInterval(interval.current);
        };
    }, []);

    const updateRepos = () => {
        getRepos()
        .then((data) => {
            if (data != null) {
                setRepos(data);
            }
            setLoading(false);
        })
        .catch((err) => console.error(err));
    }

    if (loading)
        return (
            <article className="loader">
                <div className="spinner"></div>
                <span>Loading</span>
            </article>
        );

    if (!repos.length)
        return (
            <article className="no-found">
                <div className="no-found-icon">😢</div>
                <span>
                    No repositories have been found.
                    <AnchorLink href="#FormAddRepo">Try adding one</AnchorLink>
                </span>
            </article>
        );

    return (
        <>
            {repos.map(({ title, repo_dir, description, labels }) => (
                <Repo
                    key={repo_dir}
                    title={title}
                    repo_dir={repo_dir}
                    description={description}
                    labels={labels}
                />
            ))}
        </>
    );
}
