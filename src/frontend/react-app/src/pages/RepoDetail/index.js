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
import FormExperimentZSC from "../../components/forms/FormExperimentZSC";
import FormExperimentSA from "../../components/forms/FormExperimentSA";
import FormExperimentSUMM from "../../components/forms/FormExperimentSUMM";
import Repo from "../../components/Repo";
import Loading from "../../components/Loading";
import getRepoIssues from "../../services/getRepoIssues";
import getRepoInfo from "../../services/getRepoInfo";
import { REFRESH_DATA_INTERVAL } from "../../services/settings";
import checkIsEmptyArrayOrDict from "../../services/checkEmptyArrayOrDict"

export default function RepoDetail({ gh_user, gh_repo }) {
    const [loading, setLoading] = useState(true);
    const [repoInfo, setRepoInfo] = useState({});
    const [repoIssues, setRepoIssues] = useState([]);

    const interval = useRef();

    useEffect(function () {
        updateData(gh_user, gh_repo, getRepoInfo, setRepoInfo);
        updateData(gh_user, gh_repo, getRepoIssues, setRepoIssues);
        interval.current = setInterval(() => {
            updateData(gh_user, gh_repo, getRepoInfo, setRepoInfo);
            updateData(gh_user, gh_repo, getRepoIssues, setRepoIssues);
        }, REFRESH_DATA_INTERVAL);
        return () => {
            clearInterval(interval.current);
        };
    }, [gh_repo, gh_user]);

    const updateData = (gh_user, gh_repo, getData, setData) => {
        getData(gh_user, gh_repo)
        .then((data) => {
            if (!checkIsEmptyArrayOrDict(data)) {
                setData(data);
                setLoading(false);
            }
        })
        .catch((err) => console.error(err));
    }

    if (loading) return <Loading />
    
    return (
        <>
            <header className="AppSection">
                <Repo
                    key={repoInfo["repo_dir"]}
                    title={repoInfo["title"]}
                    repo_dir={repoInfo["repo_dir"]}
                    description={repoInfo["description"]}
                    labels={repoInfo["labels"] || []}
                />
            </header>
            <main>
                <section className="AppFormZSC AppSection">
                    <h2>Zero-Shot Classification</h2>
                    <FormExperimentZSC
                        gh_user={gh_user}
                        gh_repo={gh_repo}
                        issues={repoIssues}
                    />
                </section>
                <section className="AppFormZSC AppSection">
                    <h2>Sentiment Analysis</h2>
                    <FormExperimentSA
                        gh_user={gh_user}
                        gh_repo={gh_repo}
                        issues={repoIssues}
                    />
                </section>
                <section className="AppFormZSC AppSection">
                    <h2>Summarization</h2>
                    <FormExperimentSUMM
                        gh_user={gh_user}
                        gh_repo={gh_repo}
                        issues={repoIssues}
                    />
                </section>
            </main>
        </>
    );
}
