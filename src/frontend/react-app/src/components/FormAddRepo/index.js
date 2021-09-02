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

import React, {useRef} from "react";
import { useLocation } from "wouter";
import { toast } from "react-toastify";
import { useForm } from "react-hook-form";
import { API_URL } from "../../services/settings";
import "./FormAddRepo.css";
import "react-toastify/dist/ReactToastify.css";

export default function FormAddRepo() {
    const [, setLocation] = useLocation();
    const { register, handleSubmit } = useForm();

    const apiURL = `${API_URL}/extract/`;

    const onSubmit = (formData) => {
        const res = fetch(
            apiURL,
            { method: "POST", headers: { "Content-Type": "application/json"}, body: JSON.stringify(formData) })
/*             .then(res => {
                setLocation(`/user/${formData["gh_user"]}/repo/${formData["gh_repo"]}`)
                //if (res.ok) setLocation(`/user/${formData["gh_user"]}/repo/${formData["gh_repo"]}`)
            }) */
        toast.promise(
            res,
            {
                pending: "Pending repository data extraction petition. Please wait ⌛",
                success: "Repository successfully queued. Extracted data will be available shortly 👌",
                error: "Repository data extraction petition rejected 🤔"
            }
        );
        setLocation(`/user/${formData["gh_user"]}/repo/${formData["gh_repo"]}`)
    };

    const onError = (errors) => {
        for (const error in errors) {
            toast.error(errors[error].message);
        }
    };

    return (
        <>
            <form
                className="FormAddRepo"
                id="FormAddRepo"
                onSubmit={handleSubmit(onSubmit, onError)}
            >
                <label htmlFor="GitHubUser" className="FormAddRepoLabel">
                    <input
                        type="text"
                        className="FormAddRepoInput"
                        id="GitHubUser"
                        name="gh_user"
                        placeholder="Github Username"
                        {...register("gh_user", {
                            required: "GitHub Username required.",
                        })}
                    />
                </label>
                <label htmlFor="GitHubRepo" className="FormAddRepoLabel">
                    <input
                        type="text"
                        className="FormAddRepoInput"
                        id="GitHubRepo"
                        name="gh_repo"
                        placeholder="Github Repository"
                        {...register("gh_repo", {
                            required: "GitHub Repository required.",
                        })}
                    />
                </label>
                <button
                    type="submit"
                    form="FormAddRepo"
                    className="FormAddRepoButton"
                    formMethod="post"
                    formAction={apiURL}
                >
                    Añadir Repositorio
                </button>
            </form>
        </>
    );
}
