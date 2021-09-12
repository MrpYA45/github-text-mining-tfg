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
import Loading from "../Loading";
import getRepos from "../../services/getRepos";
import { REFRESH_DATA_INTERVAL } from "../../services/settings";
import checkIsEmptyArrayOrDict from "../../services/checkEmptyArrayOrDict"
import "./ListOfRepos.css";
import AnchorLink from "react-anchor-link-smooth-scroll";

export default function ListOfRepos() {
    const [loading, setLoading] = useState(false);
    const [repos, setRepos] = useState([]);
    const [searchQuery, setSearchQuery] = useState("");
    const [searchFilterAttributes] = useState(["repo_dir", "labels"]);

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
            if (!checkIsEmptyArrayOrDict(data)) {
                setRepos(data);
                setLoading(false);
            }
        })
        .catch((err) => console.error(err));
    }

    const applySearchFilter = () => {
        return repos.filter((repo) => {
            return searchFilterAttributes.some((key) => {
                const value = Array.isArray(repo[key]) ? repo[key].join(" ") : repo[key];
                return (
                    value
                        .toString()
                        .toLowerCase()
                        .indexOf(searchQuery.toLowerCase()) > -1
                );
            });
        });
    }

    if (loading) return <Loading />

    if (!repos.length)
        return (
            <article className="AppNoFound">
                <div className="AppNoFoundIcon">😢</div>
                <span>
                    No se han encontrado repositorios descargados.
                    <AnchorLink href="#FormAddRepo">¡Prueba añadiendo uno!</AnchorLink>
                </span>
            </article>
        );

    return (
        <section className="ListOfRepos">
            <form className="ListOfReposSearchForm">
                <label htmlFor="ListOfReposSearchForm">
                    <input
                        type="search"
                        name="ListOfReposSearchFormInput"
                        className="ListOfReposSearchFormInput"
                        placeholder="Prueba a buscar entre los repositorios disponibles..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                    />
                </label>
            </form>

            {applySearchFilter(repos).map(({ title, repo_dir, description, labels }) => (
                <Repo
                    key={repo_dir}
                    title={title}
                    repo_dir={repo_dir}
                    description={description}
                    labels={labels}
                />
            ))}
        </section>
    );
}
