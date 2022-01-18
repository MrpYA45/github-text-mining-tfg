// Copyright (C) 2022 Pablo Fernández Bravo
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
import "./About.css"

export default function About() {

    return (
        <>
            <section className="AppSection AppAboutSection">
                <h2 className="AppAboutTitle AppAboutH2">Introducción</h2>
                
                <p className="AppAboutP">Este proyecto ha sido realizado por Pablo Fernández Bravo como Trabajo de Fin de Grado para la obtención del título de Graduado en Ingeniería Informática por la Universidad de Burgos. Su desarrollo con la colaboración de Dr. Carlos López Nozal y D. Jesús Alonso Abad en calidad de tutores del proyecto. </p>
            </section>
            
            <section className="AppSection AppAboutSection">
                <h2 className="AppAboutTitle AppAboutH2">Instrucciones de uso</h2>

                <h3 className="AppAboutTitle">Añadir repositorios</h3>
                <p className="AppAboutP">Para acceder al formulario que permite añadir nuevos repositorios el usuario deberá hacer clic sobre el apartado <a className="AppAboutLink" href="/repos">Repositorios</a>. En esta sección se podrá observar un listado de los repositorios disponibles debido a que hayan sido cargados previamente por el usuario, así como un formulario en una sección inferior que permite incorporar nuevos repositorios al sistema. El procedimiento para incorporar nuevos repositorios requiere de la introducción de una combinación válida de usuario y repositorio de GitHub. Una vez se introduzcan los datos y se pulse sobre el botón de añadir repositorio se encolará dicha petición, siempre y cuando el back-end de la aplicación se encuentre debidamente desplegado. El usuario recibirá una notificación indicando si la petición ha podido ser encolada satisfactoriamente o no. Tenga en cuenta que la introducción de una combinación incorrecta no producirá un error debido a que la notificación solo indica la recepción del trabajo por parte del back-end, no su resultado. En caso de que esta combinación resulte incorrecta la tarea quedará rechazada por el backend y el proceso no continuará. Una vez completado el formulario el usuario será redirigido a una nueva pestaña mientras se produce la extracción de los datos. En caso de que se le notifique que el proceso no ha podido continuar, regrese a la pestaña anterior. La detección de una combinación incorrecta no dispone de indicativos visuales, si detecta largos tiempos de espera incoherentes con el tamaño de su repositorio (calculado en función del número de incidencias y sus comentarios), por favor regrese a la sección de Repositorios. </p>

                <h3>Lanzar experimentos</h3>

                <p className="AppAboutP">Una vez la descarga de la información del repositorio se haya completado satisfactoriamente el usuario deberá ser capaz de poder visualizar a una nueva sección de la aplicación. Esta vista presenta una introducción con los datos principales del repositorio y una serie de formularios de acuerdo con los experimentos disponibles. </p>

                <h4 className="AppAboutTitle">Zero-Shot Classification</h4>

                <p className="AppAboutP">Este formulario permite al usuario la aplicación de un modelo de clasificación Zero-Shot sobre las incidencias del repositorio. El objetivo de este experimento consiste en, partiendo de una incidencia y de una serie de etiquetas, asignar una puntuación entre 0 y 1 a cada etiqueta de acuerdo con la probabilidad de que su temática se corresponda con la temática de la incidencia. Por defecto, las únicas etiquetas utilizadas son aquellas definidas por el repositorio para su clasificación manual. Los parámetros disponibles son los siguientes: </p>

                <ul className="AppAboutUl">
                    <li className="AppAboutLi">Selección de incidencia Este parámetro permite seleccionar mediante un desplegable las incidencias del repositorio de acuerdo con su título. Es posible que observe más incidencias que las disponibles en su sección homónima en su repositorio de GitHub. Esto se debe a que GitHub trata internamente las "pull request", o solicitudes de incorporación de cambios, como una extensión vitaminada de las incidencias. Como estas también incluyen un apartado de discusión, también es posible trabajar con ellas durante los experimentos. </li>
                    <li className="AppAboutLi">Precisión El slider de la precisión permite al usuario indicar un umbral a partir del cual las etiquetas que se encuentren por debajo de este no serán mostradas como resultado válido. </li>
                    <li className="AppAboutLi">Utilizar descripción Este parámetro permite otorgar un mayor contexto al modelo incluyendo la información correspondiente con la descripción de la incidencia en la realización de sus operaciones. Por defecto el modelo sólo utiliza la información deducida a partir de su título. </li>
                    <li className="AppAboutLi">Etiquetas extra Este parámetro permite añadir etiquetas fuera de aquellas declaradas por el propio repositorio en GitHub. Las etiquetas deberán introducirse en el cuadro de texto separadas haciendo uso del carácter punto y coma entre ellas. </li>
                </ul>

                <p className="AppAboutP">Los resultados del experimento se presentan en forma de de un gráfico circular que contiene aquellas etiquetas que sobrepasan el umbral establecido en los parámetros. El tamaño de las secciones representa la probabilidad de pertenencia a cada una de las temáticas propuestas. </p>

                <h4 className="AppAboutTitle">Sentiment Analysis</h4>

                <p className="AppAboutP">Este formulario permite al usuario la aplicación de un modelo de análisis de sentimientos sobre las incidencias del repositorio. La finalidad de este experimento radica en la obtención de una puntuación que defina la actitud de los usuarios participantes en la discusión generada por una incidencia. La puntuación obtenida se calcula por cada fragmento y puede variar entre 0 y 1, siendo cero la representación de una expresión de sentimientos muy negativos, y uno la representación de una expresión de sentimientos muy positivos. Los parámetros disponibles son los siguientes: </p>

                <ul className="AppAboutUl">
                    <li className="AppAboutLi">Selección de incidencia Este parámetro permite seleccionar mediante un desplegable las incidencias del repositorio de acuerdo con su título. </li>
                    <li className="AppAboutLi">Selección de usuario Este parámetro permite filtrar los comentarios de la incidencia que van a ser tomados como entrada del modelo a aquellos realizados exclusivamente por dicho usuario.</li>
                    <li className="AppAboutLi"> Utilizar comentarios. Este parámetro tiene como finalidad permitir la realización del análisis de sentimientos de la entrada inicial de la incidencia, excluyendo sus comentarios tanto del autor como del resto de participantes en la conversación. </li>
                </ul>

                <p className="AppAboutP">Los resultados del experimento se presentan haciendo uso de un gráfico de barras verticales. Cada barra azul representa la puntuación otorgada a un comentario, siendo la línea horizontal roja el indicador de la puntuación media obtenida de acuerdo con los parámetros introducidos. </p>

                <h4 className="AppAboutTitle">Summarization</h4>

                <p className="AppAboutP">Este formulario permite al usuario el lanzamiento de un experimento de generación de resúmenes abstractivos sobre las incidencias del repositorio. La finalidad de este experimento consiste en generar un fragmento de texto que resuma el contenido tratado por la incidencia. El modelo se aplica de manera individual a cada comentario y posteriormente se procede a la concatenación de los resultados para obtener un resumen general del tema tratado en la discusión de la incidencia. Este experimento cuenta con limitaciones lingüísticas debido a que el modelo utilizado que solo ofrece soporte a textos escritos en inglés. Los parámetros disponibles son los siguientes: </p>

                <ul className="AppAboutUl">
                    <li className="AppAboutLi">Selección de incidencia Este parámetro permite seleccionar mediante un desplegable las incidencias del repositorio de acuerdo con su título. </li>
                    <li className="AppAboutLi">Utilizar descripción Este parámetro permite otorgar un mayor contexto al modelo incluyendo la información correspondiente con la descripción de la incidencia en la realización de sus operaciones. Por defecto el modelo sólo utiliza la información deducida a partir de su título. </li>
                    <li className="AppAboutLi">Longitud mínima de los fragmentos Este parámetro permite establecer una longitud mínima de los resúmenes parciales que compondrán el resumen final. Es importante destacar el aspecto de los fragmentos, ya que los fragmentos de las entradas se introducen en el modelo de forma individual, por lo tanto el resumen final se elabora a partir de su concatenación. También se ha de destacar que esta longitud no se corresponde directamente con el número de caracteres debido a las consideraciones tomadas por el tokenizador utilizado por los modelos. </li>
                    <li className="AppAboutLi">Longitud máxima de los fragmentos Este parámetro permite establecer una longitud máxima de los resúmenes parciales que compondrán el resumen final. </li>
                </ul>

                <p className="AppAboutP">Los resultados del experimento proveen al usuario del resumen generado en función del contenido de la incidencia y los parámetros de longitud establecidos para cada fragmento. </p>
            </section>

            <section className="AppSection AppAboutSection">
                <h2 className="AppAboutTitle AppAboutH2">Créditos</h2>

                <ul className="AppAboutUl">
                    <li className="AppAboutCreditsLi">Modelo de Zero-Shot Classification creado por Facebook disponible en <a className="AppAboutLink" href="https://huggingface.co/facebook/bart-large-mnli">HuggingFace</a>. </li>
                    <li className="AppAboutCreditsLi">Modelo de Sentiment Analysis creado por nlptown disponible en <a className="AppAboutLink" href="https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment">HuggingFace</a>. </li>
                    <li className="AppAboutCreditsLi">Modelo de Summarization creado por Sshleifer disponible en <a className="AppAboutLink" href="https://huggingface.co/sshleifer/distilbart-cnn-12-6">HuggingFace</a>. </li>
                    <li className="AppAboutCreditsLi">El código fuente de este proyecto se encuentra disponible en <a className="AppAboutLink" href="https://github.com/MrpYA45/github-text-mining-tfg/">GitHub</a>. </li>
                </ul>
            </section>
        </>
    );
}
