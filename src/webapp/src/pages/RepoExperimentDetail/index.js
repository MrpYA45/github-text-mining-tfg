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

import React, {useEffect, useState, useRef} from "react";
import ExperimentZSC from "../../components/experiments/ExperimentZSC";
import ExperimentSA from "../../components/experiments/ExperimentSA";
import ExperimentSUMM from "../../components/experiments/ExperimentSUMM";
import Loading from "../../components/Loading";
import getTask from "../../services/getTask"
import getRepoInfo from "../../services/getRepoInfo";
import getIssueInfo from "../../services/getIssueInfo";
import getOutcome from "../../services/getOutcome";
import updateData from "../../services/updateData"
import { REFRESH_DATA_INTERVAL } from "../../services/settings";

export default function RepoExperimentDetail({ gh_user, gh_repo, issue_id, task_id }) {

    const [ repoInfo, setRepoInfo ] = useState({});
    const [ loadingRepoInfo, setLoadingRepoInfo ] = useState(true);

    const [ taskData, setTaskData ] = useState({});
    const [ loadingTaskData, setLoadingTaskData ] = useState(true);

    const [ issueInfo, setIssueInfo ] = useState({});
    const [ loadingIssueInfo, setLoadingIssueInfo ] = useState(true);

    const [ outcome, setOutcome ] = useState({});
    const [ loadingOutcome, setLoadingOutcome ] = useState(true);

    const interval = useRef();

    useEffect(function () {
        updateData([gh_user, gh_repo], getRepoInfo, setRepoInfo, setLoadingRepoInfo);
        updateData([task_id], getTask, setTaskData, setLoadingTaskData);
        updateData([gh_user, gh_repo, issue_id], getIssueInfo, setIssueInfo, setLoadingIssueInfo);
        updateData([task_id], getOutcome, setOutcome, setLoadingOutcome);

        interval.current = setInterval(() => {
            updateData([gh_user, gh_repo], getRepoInfo, setRepoInfo, setLoadingRepoInfo);
            updateData([task_id], getTask, setTaskData, setLoadingTaskData);
            updateData([gh_user, gh_repo, issue_id], getIssueInfo, setIssueInfo, setLoadingIssueInfo);
            updateData([task_id], getOutcome, setOutcome, setLoadingOutcome);
            
            if (!loadingRepoInfo && !loadingTaskData && !loadingIssueInfo && !loadingOutcome) clearInterval(interval.current);

        }, REFRESH_DATA_INTERVAL);

        return () => {
            clearInterval(interval.current);
        };

    }, [gh_repo, gh_user, issue_id, loadingIssueInfo, loadingOutcome, loadingRepoInfo, loadingTaskData, task_id]);

    if (loadingRepoInfo || loadingTaskData || loadingOutcome || loadingIssueInfo) return <Loading />

    switch (taskData["params"]["model_type"]) {
        case "zsc":
            return <ExperimentZSC
                gh_user={gh_user}
                gh_repo={gh_repo}
                repo_info={repoInfo}
                task_data={taskData}
                issue_info={issueInfo}
                outcome={outcome}
            />
        case "sa":
            return <ExperimentSA
                gh_user={gh_user}
                gh_repo={gh_repo}
                repo_info={repoInfo}
                task_data={taskData}
                issue_info={issueInfo}
                outcome={outcome}
            />
        case "summ":
            return <ExperimentSUMM
                gh_user={gh_user}
                gh_repo={gh_repo}
                repo_info={repoInfo}
                task_data={taskData}
                issue_info={issueInfo}
                outcome={outcome}
            />
        default:
            return (
                <article className="AppUnknownModel">
                    <span className="AppUnknownModelIcon">⚠</span>
                    <span className="AppUnknownModelMsg">Los datos del experimento se encuentran dañados.</span>
                </article>
            )
    }
}
