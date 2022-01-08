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
import Chart from "react-google-charts"
import Repo from "../../../components/Repo"
import "../Experiments.css";

export default function ExperimentZSC({gh_user, gh_repo, repo_info, task_data, issue_info, outcome}) {

    const { repo_dir, title, description, labels: repo_labels } = repo_info
    
    const { state, timestamp, params = {} } = task_data;
    const { accuracy, extra_labels = [], use_desc } = params;

    const { outcome_data, exec_time } = outcome;
    const { labels: rating_labels, ratings } = outcome_data;

    const pie_data = rating_labels.map((r_label, i) => {
        return [ r_label, ratings[i] ]
    })

    const [, setLocation] = useLocation();

    if (state === 3) return (
        <article className="AppError">
            <div className="AppErrorIcon">⚠</div>
            <p>
                Se ha producido un error al llevar a cabo la ejecución del experimento.
            </p>
            <button className="AppButton" onClick={() => setLocation(`/user/${gh_user}/repo/${gh_repo}`)}>Volver</button>
        </article>
    );

    return (
        <section className="ExperimentCard AppSection">
            <h2 className="ExperimentTitle">Experimento de Clasificación Zero-Shot</h2>
            <Repo title={title} repo_dir={repo_dir} description={description} labels={repo_labels}/>
            <article className="ExperimentSection">
                <h3>Parametros Introduccidos</h3>
                <div className="ExperimentParamsContainer">
                    <span className="ExperimentParam">Incidencia: {issue_info["title"]}</span>
                    <span className="ExperimentParam">Utilizar descripción: { use_desc ? "Activado" : "Desactivado" }</span>
                    <span className="ExperimentParam">Precisión: {accuracy}</span>
                    <span className="ExperimentParam">Etiquetas Extra:
                        <div className="ExperimentTagsContainer">
                            {extra_labels.length === 0 ? "No" : ""}
                            {extra_labels.map((label) => (
                                <span key={label} className="ExperimentTag">#{label}</span>
                            ))}
                        </div>
                    </span>
                </div>
            </article>
            <article className="ExperimentSection">
                <h3>Resultados del Experimento</h3>
                <Chart
                    width={'70%'}
                    height={'40rem'}
                    chartType="PieChart"
                    loader={<div>Cargando gráfico...</div>}
                    data={[["Etiqueta", "Precisión"], ...pie_data]}
                    options={{
                        backgroundColor: 'transparent',
                        legend: { position: 'bottom', alignment: 'start', maxLines: 2},
                        chartArea: {
                            height: '100%',
                            width: '100%',
                            top: 16,
                            left: 16,
                            right: 16,
                            bottom: 48
                        },
                        enableInteractivity: true,
                    }}
                />
            </article>
            <article className="ExperimentSection">
                <div className="ExperimentParamsContainer">
                    <span className="ExperimentParam">Fecha lanzamiento: {timestamp}</span>
                    <span className="ExperimentParam">Tiempo de ejecución: {exec_time.toFixed(2)} segundos</span>
                </div>
            </article>
        </section>
    );
}
