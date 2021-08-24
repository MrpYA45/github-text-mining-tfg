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

import React from 'react';
import ListOfRepos from '../../components/ListOfRepos';
import FormAddRepo from '../../components/FormAddRepo';

export default function Home() {
    return (
        <>
            <header className="App-header App-section">
                <h1>GitHub Text Mining</h1>
                <FormAddRepo />
            </header>
            <main>
                <section className="App-list-repos App-section">
                    <h2>Lista de Repositorios Disponibles</h2>
                    <ListOfRepos />
                </section>
            </main>
        </>
    )
}