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
import "./Home.css"

export default function Home() {

    const [, setLocation] = useLocation();

    return (
        <>
            <header className="AppHeader">
                <div className="AppWelcome">
                    <h1 className="AppTitle">GitHub Text Mining</h1>
                    <p className="AppDesc">Experimenta, juega con los parámetros y observa los resultados de la aplicación de técnicas de procesamiento del lenguaje natural a la gestión de tareas haciendo uso modelos preentrenados sobre repositorios GitHub de código abierto de manera fácil y sencilla.</p>
                    <button className="AppButton" onClick={() => setLocation("/repos")}>¡Empieza ya!</button>
                </div>
            </header>
            <main>

            </main>
        </>
    );
}
