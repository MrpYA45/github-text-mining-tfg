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
import { toast } from "react-toastify";
import { useForm } from "react-hook-form";
import { API_URL } from "../../../services/settings";
import "../FormExperiment.css";
import "react-toastify/dist/ReactToastify.css";

export default function FormSUMM({ gh_user, gh_repo, issues }) {
    const [, setLocation] = useLocation();
    const { register, handleSubmit } = useForm();

    const apiURL = `${API_URL}/user/${gh_user}/repo/${gh_repo}/process/summ/`;

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

    return (
        <>
            <form
                className="FormExperiment"
                id="FormSUMM"
                onSubmit={handleSubmit(onSubmit, onError)}
            >
                <label
                    htmlFor="GitHubSUMMIssueId"
                    className="FormExperimentLabel"
                >
                    <span className="FormExperimentSpan">Seleccione una incidencia</span>
                    <select
                        className="FormExperimentDropdown FormExperimentInput"
                        id="GitHubSUMMIssueId"
                        name="issue_id"
                        defaultValue=""
                        {...register("issue_id", {
                            required: "Select an Issue",
                        })}
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
                    htmlFor="GitHubSUMMWithComments"
                    className="FormExperimentLabel"
                >
                    <span className="FormExperimentSpan">¿Utilizar comentarios?</span>
                    <div className="FormExperimentSwitch">
                        <input
                            type="checkbox"
                            className="FormExperimentSwitch-checkbox"
                            id="GitHubSUMMWithComments"
                            name="with_comments"
                            tabIndex="0"
                            {...register("with_comments")}
                        />
                        <label className="FormExperimentSwitch-label" htmlFor="GitHubSUMMWithComments">
                            <span className="FormExperimentSwitch-inner"></span>
                            <span className="FormExperimentSwitch-switch"></span>
                        </label>
                    </div>
                </label>
                <label
                    htmlFor="GitHubSUMMMinLength"
                    className="FormExperimentLabel"
                >
                    <span className="FormExperimentSpan">Longitud mínima de los fragmentos</span>
                    <input
                        type="number"
                        className="FormExperimentInput"
                        id="GitHubSUMMMinLength"
                        name="min_length"
                        defaultValue="20"
                        {...register("min_length")}
                    />
                </label>
                <label
                    htmlFor="GitHubSUMMMaxLength"
                    className="FormExperimentLabel"
                >
                    <span className="FormExperimentSpan">Longitud máxima de los fragmentos</span>
                    <input
                        type="number"
                        className="FormExperimentInput"
                        id="GitHubSUMMMaxLength"
                        name="max_length"
                        defaultValue="50"
                        {...register("max_length")}
                    />
                </label>
                <button
                    type="submit"
                    form="FormSUMM"
                    className="AppButton"
                    formMethod="post"
                    formAction={apiURL}
                >
                    Launch Summarization experiment
                </button>
            </form>
        </>
    );
}
