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
import { API_URL } from "../../services/settings";
import "./FormExperimentSA.css";
import "react-toastify/dist/ReactToastify.css";

export default function FormExperimentSA({ gh_user, gh_repo, issues }) {
    const [, setLocation] = useLocation();
    const { register, handleSubmit } = useForm();

    const apiURL = `${API_URL}/user/${gh_user}/repo/${gh_repo}/process/sa/`;

    const onSubmit = (formData) => {
        const res = fetch(apiURL, { method: "POST", headers: { "Content-Type": "application/json"}, body: JSON.stringify(formData) });
        toast.promise(
            res,
            {
                pending: "Pending repository data extraction petition. Please wait ⌛",
                success: "Repository successfully queued. Extracted data will be available shortly 👌",
                error: "Repository data extraction petition rejected 🤔"
            }
        );
        //setLocation(`/user/${formData["gh_user"]}/repo/${formData["gh_repo"]}`);
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
                id="FormExperimentSA"
                onSubmit={handleSubmit(onSubmit, onError)}
            >
                <label
                    htmlFor="GitHubIssueId"
                    className="FormExperimentLabel"
                >
                    <span className="FormExperimentSpan">Select an issue</span>
                    <select
                        className="FormExperimentDropdown FormExperimentInput"
                        id="GitHubIssueId"
                        name="issue_id"
                        defaultValue=""
                        {...register("issue_id", {
                            required: "Select an Issue",
                        })}
                    >
                        <option className="FormExperimentDropdownOption" htmlFor="issue_id" value="" disabled hidden>
                            Choose an issue here
                        </option>
                        {issues.map((issue) => {
                            return (
                                <option
                                    key={issue["issue_id"]}
                                    className="FormExperimentDropdownOption"
                                    htmlFor="issue_id"
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
                    <span className="FormExperimentSpan">Author (not-required)</span>
                    <input
                        className="FormExperimentInput"
                        id="GitHubSAAuthor"
                        name="author"
                        {...register("author")}
                    />
                </label>
                <label
                    htmlFor="GitHubSAWithComments"
                    className="FormExperimentLabel"
                >
                    <span className="FormExperimentSpan">Use comments</span>
                    <input
                        type="checkbox"
                        className="FormExperimentCheckBox FormExperimentInput"
                        id="GitHubSAWithComments"
                        name="with_comments"
                        {...register("with_comments")}
                    />
                </label>
                <button
                    type="submit"
                    form="FormExperimentSA"
                    className="FormExperimentButton"
                    formMethod="post"
                    formAction={apiURL}
                >
                    Launch Sentiment Analysis experiment
                </button>
            </form>
        </>
    );
}
