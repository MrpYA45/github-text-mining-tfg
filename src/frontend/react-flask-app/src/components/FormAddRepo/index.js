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

import React from 'react'
import {API_URL} from '../../services/settings'
import './FormAddRepo.css'

export default function FormAddRepo () {
    const apiURL = `${API_URL}/task/`
    return (
        <form className="FormAddRepo">
            <label for="GitHubUser" className="FormAddRepoLabel">
                {/*<span className="Add_Repo_Form_Label">GitHub Username:</span>*/}
                <input type="text" className="FormAddRepoInput" id="GitHubUser" name="gh_user" placeholder="Github Username" required></input>
            </label>
            <span>/</span>
            <label for="GitHubRepo" className="FormAddRepoLabel">
                {/*<span className="Add_Repo_Form_Label">GitHub Repository Name:</span>*/}
                <input type="text" className="FormAddRepoInput" id="GitHubRepo" name="gh_repo" placeholder="Github Repository" required></input>
            </label>
            <button type="submit" className="FormAddRepoButton" formmethod="post" formaction={apiURL}>Añadir Repositorio</button>
        </form>
    )
}
