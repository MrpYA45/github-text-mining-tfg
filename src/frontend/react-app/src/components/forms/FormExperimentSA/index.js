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

import React, {useState} from "react";
import { useLocation } from "wouter";
import { toast } from "react-toastify";
import { useForm } from "react-hook-form";
import getRepoIssueComments from "../../../services/getRepoIssueComments";
import { API_URL } from "../../../services/settings";
import "../FormExperiment.css";
import "react-toastify/dist/ReactToastify.css";

export default function FormSA({ gh_user, gh_repo, issues }) {
    const [, setLocation] = useLocation();
    const { register, handleSubmit } = useForm();

    const [ selectedIssueId, setSelectedIssueId ] = useState("")
    const [ selectedIssueComments, setSelectedIssueComments ] = useState([])
    const [ selectedUser, setSelectedUser ] = useState("")

    const apiURL = `${API_URL}/user/${gh_user}/repo/${gh_repo}/process/sa/`;

    const onSubmit = (formData) => {
        const submitForm = fetch(apiURL, { method: "POST", headers: { "Content-Type": "application/json"}, body: JSON.stringify(formData) });
        toast.promise(
            submitForm,
            {
                pending: "Pending repository data extraction petition. Please wait ⌛",
                success: "Repository successfully queued. Extracted data will be available shortly 👌",
                error: "Repository data extraction petition rejected 🤔"
            }
        );
        submitForm.then((res) => {
            res.json().then((data) => {
                setLocation(`/user/${gh_user}/repo/${gh_repo}/issue/${formData["issue_id"]}/experiment/${data["task_id"]}`)
            })
        })
    };

    const onError = (errors) => {
        for (const error in errors) {
            toast.error(errors[error].message);
        }
    };

    const handleSelectIssue = (e) => {
        setSelectedIssueId(parseInt(e.target.value))
        getRepoIssueComments(gh_user, gh_repo, parseInt(e.target.value))
        .then(
            comments => setSelectedIssueComments(comments)
        )
    }

    const getUsersAtSelectedIssue = () => {
        if (selectedIssueId === "") return []
        const selectedIssue = issues.filter(issue => Object.values(issue).includes(selectedIssueId))
        const usersIssueComments = selectedIssueComments.map(({author}) => author)
        return [...new Set([selectedIssue[0]["author"], ...usersIssueComments])]
    }

    const checkSelectedUserIsAuthor = () => {
        if (selectedIssueId === "") return false
        const selectedIssue = issues.filter(issue => Object.values(issue).includes(selectedIssueId))
        return selectedIssue[0]["author"] === selectedUser
    }

    return (
        <>
            <form
                className="FormExperiment"
                id="FormSA"
                onSubmit={handleSubmit(onSubmit, onError)}
            >
                <label
                    htmlFor="GitHubSAIssueId"
                    className="FormExperimentLabel"
                >
                    <span className="FormExperimentSpan">Seleccione una incidencia</span>
                    <select
                        className="FormExperimentDropdown FormExperimentInput"
                        id="GitHubSAIssueId"
                        name="issue_id"
                        defaultValue=""
                        {...register("issue_id", {
                            required: "Select an Issue",
                        })}
                        onChange={(e) => handleSelectIssue(e)}
                    >
                        <option className="FormExperimentDropdownOption" value="" disabled hidden>
                            Seleccione una incidencia aquí...
                        </option>
                        {issues.map((issue) => {
                            return (
                                <option
                                    key={issue["issue_id"]}
                                    className="FormExperimentDropdownOption"
                                    value={issue["issue_id"]}
                                >
                                    {issue["title"].length > 85 ? issue["title"].substring(0, 85) + "..." : issue["title"]}
                                </option>
                            );
                        })}
                    </select>
                </label>
                <label
                    htmlFor="GitHubSAAuthor"
                    className="FormExperimentLabel"
                >
                    <span className="FormExperimentSpan">Seleccione una usuario</span>
                    <select
                        className="FormExperimentDropdown FormExperimentInput"
                        id="GitHubSAAuthor"
                        name="author"
                        defaultValue=""
                        {...register("author", { disabled: selectedIssueId === "" })}
                        onChange={(e) => setSelectedUser(e.target.value)}
                    >
                        <option className="FormExperimentDropdownOption" htmlFor="author" value="">
                            { selectedIssueId === "" ? "⚠ Seleccione una incidencia primero!" : "Todos los usuarios" }
                        </option>
                        {getUsersAtSelectedIssue().map((user) => {
                            return (
                                <option
                                    key={user}
                                    className="FormExperimentDropdownOption"
                                    htmlFor="author"
                                    value={user}
                                >
                                    {user}
                                </option>
                            );
                        })}
                    </select>
                </label>
                <label
                    htmlFor="GitHubSAWithComments"
                    className="FormExperimentLabel"
                >
                    <span className="FormExperimentSpan">¿Utilizar comentarios?</span>
                    <div className="FormExperimentSwitch">
                        <input
                            type="checkbox"
                            className="FormExperimentSwitch-checkbox"
                            id="GitHubSAWithComments"
                            name="with_comments"
                            checked={ checkSelectedUserIsAuthor() ? undefined : true }
                            tabIndex="0"
                            {...register("with_comments")}
                        />
                        <label className="FormExperimentSwitch-label" htmlFor="GitHubSAWithComments">
                            <span className="FormExperimentSwitch-inner"></span>
                            <span className="FormExperimentSwitch-switch"></span>
                        </label>
                    </div>
                </label>
                <button
                    type="submit"
                    form="FormSA"
                    className="AppButton"
                    formMethod="post"
                    formAction={apiURL}
                >
                    Launch Sentiment Analysis experiment
                </button>
            </form>
        </>
    );
}
