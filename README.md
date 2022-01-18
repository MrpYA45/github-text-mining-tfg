[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![Issues](https://img.shields.io/github/issues/MrpYA45/github-text-mining-tfg?color=blue)](https://github.com/MrpYA45/github-text-mining-tfg/issues)
[![pylint score](https://github.com/MrpYA45/github-text-mining-tfg/actions/workflows/stylechecking.yml/badge.svg?style=for-the-badge)](https://github.com/MrpYA45/github-text-mining-tfg/actions/workflows/stylechecking.yml)
[![codebeat badge](https://codebeat.co/badges/b88ca615-8ccc-4770-a607-79e83b14dac5)](https://codebeat.co/projects/github-com-mrpya45-github-text-mining-tfg-main)

# GitHub Text Mining (Bachelor's Degree Final Project)

This project has the objective of creating a microservices application which lets the user introduce the url of a Github repository and extract a series of information from it applying certain natural language processing models (NLP).

Instalación y ejecución del proyecto
====================================

En el siguiente apartado se presentan las instrucciones a través de las
cuales establecer un entorno de desarrollo que disponga del código
fuente, utilidades, complementos y ejecutables requeridos para la puesta
en marcha del proyecto.

Prerrequisitos
--------------

El código fuente del proyecto se ha implementado haciendo uso de los
lenguajes de programación **Python** y **JavaScript**. En el caso de
Python este se requiere para las implementaciones llevadas a cabo en el
apartado del front-end. El uso de JavaScript se debe al desarrollo de la
aplicación web, implementada sobre el entorno de ejecución **NodeJS**. A
continuación se incluyen las versiones requeridas por la aplicación para
asegurar su correcto funcionamiento:

-   **Python 3.9.6** o superior.

-   **NodeJS 14.17.4** o superior.

-   **Docker 20.10.12** o superior.

-   **Docker Compose 1.29.2** o superior.

Se recomienda el uso del editor de texto **Visual Studio Code** debido a
la versatilidad que ofrece a la hora de trabajar con diversos lenguajes
de manera simultánea y el uso de extensiones que facilitan múltiples
aspectos en el proceso de desarrollo.

Obtención el proyecto
---------------------

Para proceder con la obtención de una copia local de los ficheros del 
proyecto se recurrirá a un software de control de versiones que ofrezca
soporte a repositorios de GitHub como **Git** o **GitHub Desktop**. 
También es posible la descarga directa de los ficheros a través esta misma web.

En caso de que se haya decidido escoger el popular software de control
de versiones Git el comando requerido para la obtención de los archivos
es el siguiente:

`git clone https://github.com/MrpYA45/github-text-mining-tfg`

![Obtención del repositorio mediante
Git.](docs/img/git_gtm.png)

Preparación de un entorno virtual
---------------------------------

Los entornos virtuales de Python permiten mantener varios desarrollos en
el mismo equipo de manera que las configuraciones y dependencias de un
entorno se mantengan aisladas del resto de entornos virtuales. No es un
requisito obligatorio su uso pero sí recomendable para evitar conflictos
entre posibles múltiples versiones de las dependencias utilizadas entre
proyectos, manteniendo solo aquellas estrictamente necesarias para el
desarrollo.

Para crear un entorno virtual se deberá situar la terminal en el
directorio raíz del proyecto y ejecutar el comando dispuesto a
continuación:

**MacOS/Linux:** `python3 -m venv env`

**Windows:** `python -m venv env`

![Creación de un entorno virtual para
Python.](docs/img/creating_venv.png)

Una vez se disponga de un entorno virtual deberemos activarlo, para la
cual el comando a utilizar dependerá del sistema operativo que se vaya a
utilizar.

**MacOS/Linux:** `source venv/bin/activate`

**Windows:** `venv\Scripts\activate`

Instalación de las dependencias del back-end
--------------------------------------------

Seguidamente se realizará la instalación de las dependencias de Python
utilizadas en el proyecto de acuerdo con el listado de paquetes que se
proporciona en el directorio raíz del proyecto mediante el fichero
`requirements.txt`. La instalación se realizará a través del gestor de
paquetes **PIP**, el cual se distribuye junto con Python desde la
versión 3.4.

**MacOS/Linux:** `pip3 install -r requirements.txt`

**Windows:** `pip install -r requirements.txt`

Instalación de las dependencias de la aplicación web
----------------------------------------------------

A continuación, se procederá con la instalación de las dependencias de
la aplicación web. Esta se encuentra construida sobre el entorno de
ejecución NodeJS basado en JavaScript. La aplicación web también ha sido
desarrollada haciendo uso de módulos que simplifican la programación de
ciertos aspectos de la web.

Para proceder a la instalación de estas dependencias se deberá situar la
terminal en la carpeta `src/webapp`. El fichero `package.json` es el
encargado de almacenar el listado con las dependencias necesarias para
poder proceder con la instalación, así como los *scripts* que permiten
lanzar la aplicación. Para proceder con la instalación de los ficheros
necesarios se deberá recurrir al siguiente comando:

**Windows/MacOS/Linux:** `npm install`

Lanzamiento de los servicios del back-end
-----------------------------------------

El lanzamiento de los servicios del back-end se realizará por medio del
uso de las herramientas **Docker** y **Docker Compose**, para las cuales
se ha diseñado una configuración que permite mantener cada uno de los
servicios y la base de datos en contenedores independientes.

El primer paso consistirá en la obtención de las imágenes que se
ejecutarán en el interior de los contenedores. Para ello, situándonos en
la directorio raíz del proyecto, se deberá ejecutar el comando de
construcción que se incluye a continuación. Se ha de tener en cuenta que
la primera ejecución del comando requiere de la descarga de numerosos
archivos pesados, por ello por lo que el proceso puede alargarse durante
varios minutos.

**Windows/MacOS/Linux:**

`docker-compose -f docker/config/docker-compose.yml build`

Una vez se ha completado el proceso de generación de las imágenes se
deberá proseguir con el levantamiento de los contenedores que contendrán
dichas imágenes. En una primera instancia este proceso requiere de un
extenso tiempo de espera durante el cual se procede a la descarga e
instalación de las dependencias requeridas por los servicios en el
interior de los propios contenedores.

**Windows/MacOS/Linux:**

`docker-compose -f docker/config/docker-compose.yml up`

El servicio con un mayor tiempo de despliegue inicial resulta ser el
servicio de procesamiento denominado *gtmprocessing*, el cual puede
llegar a requerir de entre 10 y 15 minutos en su arranque. Ante la pobre
vivacidad que se presenta en el proceso de obtención de los modelos se
recomienda realizar comprobaciones periódicas a través del siguiente
comando.

**Windows/MacOS/Linux:** `docker logs gtmprocessing -t`

Esta orden permite obtener un visualizar la actividad que se está
produciendo en el interior del contenedor. A través de esta salida se
podrá comprobar el estado de la descarga de los modelos.

### Configuración inicial de los servicios

Una vez finalizado el proceso de configuración inicial se deberá
verificar que se han generado correctamente los ficheros de
configuración. Estos ficheros se encuentran en el interior de cada uno
de los servicios en la ruta `/src/backend/%service_name%/config`.

Verificada la existencia de estos ficheros se deberán detener los
contenedores para poder proceder a su pertinente configuración.

**Windows/MacOS/Linux:**

`docker-compose -f docker/config/docker-compose.yml stop`

Cada servicio dispone de una carpeta *gtmcore* en su configuración que
permite alterar los parámetros de conexión con la base de datos. Por
defecto, estos ficheros se generan con una configuración básica de
acuerdo con la configuración de la base de datos establecida en el
fichero de variables de entorno de Docker localizado en la siguiente
ruta `docker/services/.env`. Se recomienda encarecidamente modificar
estos valores en caso de lanzar la aplicación en algún entorno de
producción.

Finalmente, el servicio de extracción dispone de una segunda carpeta de
configuración denominada *gtmprocessing*. En su interior se encuentra un
fichero de configuración que se requiere completar para lograr la
extracción de la información de los repositorios. Este fichero solicita
un token de acceso personal de GitHub.

Una vez se haya completado la configuración de los servicios se deberá
volver a levantar los contenedores con el comando señalado
anteriormente. En el momento en que los servicios se encuentren
completamente desplegados será posible acceder a la API REST de la
aplicación por medio de consultas a la dirección
<http://localhost:6060/>.

### Obtención de un token de acceso personal de GitHub

La obtención de un token de acceso personal de GitHub requiere de
encontrarnos registrados en la plataforma. Una vez en ella se puede
solicitar el token desde el apartado de *Settings*, *Developer
Settings*, y seleccionar el apartado [*Personal Access
Tokens*](https://github.com/settings/tokens).

La generación de un token requiere del establecimiento de un periodo de
caducidad y de la selección de una serie de permisos básicos para poder
realizar ciertas acciones. El uso básico de las peticiones que se
realizan por parte de la aplicación implica que solo se requiere del
permiso de acceso a repositorios públicos.

![Generación del Token de Acceso Personal en
GitHub.](docs/img/gen_github_access_tokens.png)

Lanzamiento de la aplicación web mediante NodeJS
------------------------------------------------

El lanzamiento de aplicación web solamente requiere de la situación de
la terminal en la ruta donde se localiza los ficheros de la aplicación
web (`src/webapp`) y la introducción del siguiente comando.

**Windows/MacOS/Linux:** `npm start gtm-webapp`

Tras su ejecución se producirá el despliegue de la aplicación en un
servidor de NodeJS y la apertura automática de una ventana en el
navegador web presentando al usuario la web. En caso de que esto no
suceda por algún motivo desconocido, la aplicación web se encuentra
accesible desde la siguiente dirección <http://localhost:3000/>.

Manual del usuario
==================

El manual de usuario tiene como finalidad ilustrar el uso de la interfaz
web de la aplicación.

Selección y obtención de repositorios
-------------------------------------

El primer paso requerido para explotar las funcionalidades de la
aplicación consiste en incorporar los datos de los repositorios a la
aplicación. Para ello, el usuario deberá hacer clic sobre el apartado
"**Repositorios**" de la web. En esta sección se podrá observar un
listado de los repositorios disponibles debido a que hayan sido cargados
previamente por el usuario, así como un formulario en una sección
inferior que permite incorporar nuevos repositorios al sistema (véase ).

![Sección "**Repositorios**" de la aplicación
web.](docs/img/webapp_list_and_get_repo.png)

El procedimiento para incorporar nuevos repositorios requiere de la
introducción de una combinación válida de usuario y repositorio de
**GitHub**. Una vez se introduzcan los datos y se pulse sobre el botón
de añadir repositorio se encolará dicha petición, siempre y cuando el
*back-end* de la aplicación se encuentre debidamente desplegado. El
usuario recibirá una notificación indicando si la petición ha podido ser
encolada satisfactoriamente o no.

Tenga en cuenta que la introducción de una combinación incorrecta no
producirá un error debido a que la notificación solo indica la recepción
del trabajo por parte del *back-end*, no su resultado. En caso de que
esta combinación resulte incorrecta la tarea quedará rechazada por el
*backend* y el proceso no continuará.

Una vez completado el formulario el usuario será redirigido a una nueva
pestaña mientras se produce la extracción de los datos. En caso de que
se le notifique que el proceso no ha podido continuar, regrese a la
pestaña anterior. La detección de una combinación incorrecta no dispone
de indicativos visuales, si detecta largos tiempos de espera
incoherentes con el tamaño de su repositorio (calculado en función del
número de incidencias y sus comentarios), por favor regrese a la sección
de Repositorios.

Lanzar experimentos
-------------------

Una vez la descarga de la información del repositorio se haya completado
satisfactoriamente el usuario deberá ser capaz de poder visualizar a una
nueva sección de la aplicación. Esta vista presenta una introducción con
los datos principales del repositorio y una serie de formularios de
acuerdo con los experimentos disponibles.

### Zero-Shot Classification

Este formulario permite al usuario la aplicación de un modelo de
clasificación Zero-Shot sobre las incidencias del repositorio (véase ).
El objetivo de este experimento consiste en, partiendo de una incidencia
y de una serie de etiquetas, asignar una puntuación entre 0 y 1 a cada
etiqueta de acuerdo con la probabilidad de que su temática se
corresponda con la temática de la incidencia. Por defecto, las únicas
etiquetas utilizadas son aquellas definidas por el repositorio para su
clasificación manual.

![Formulario de lanzamiento de experimento de Zero-Shot
Classification.](docs/img/webapp_zsc_form.png)

Los parámetros disponibles son los siguientes:

-   **Selección de incidencia**. Este parámetro permite seleccionar
    mediante un desplegable las incidencias del repositorio de acuerdo
    con su título. Es posible que observe más incidencias que las
    disponibles en su sección homónima en su repositorio de GitHub. Esto
    se debe a que GitHub trata internamente las "*pull request*", o
    solicitudes de incorporación de cambios, como una extensión
    vitaminada de las incidencias. Como estas también incluyen un
    apartado de discusión, también es posible trabajar con ellas durante
    los experimentos.

-   **Precisión**. El *slider* de la precisión permite al usuario
    indicar un umbral a partir del cual las etiquetas que se encuentren
    por debajo de este no serán mostradas como resultado válido.

-   **Utilizar descripción**. Este parámetro permite otorgar un mayor
    contexto al modelo incluyendo la información correspondiente con la
    descripción de la incidencia en la realización de sus operaciones.
    Por defecto el modelo sólo utiliza la información deducida a partir
    de su título.

-   **Etiquetas extra**. Este parámetro permite añadir etiquetas fuera
    de aquellas declaradas por el propio repositorio en GitHub. Las
    etiquetas deberán introducirse en el cuadro de texto separadas
    haciendo uso del carácter punto y coma entre ellas.

Los resultados del experimento se presentan en forma de de un gráfico
circular que contiene aquellas etiquetas que sobrepasan el umbral
establecido en los parámetros. El tamaño de las secciones representa la
probabilidad de pertenencia a cada una de las temáticas propuestas
(véase ).

![Resultados obtenidos en un experimento de Zero-Shot
Classification.](docs/img/webapp_zsc_output.png)

### Sentiment Analysis

Este formulario permite al usuario la aplicación de un modelo de
análisis de sentimientos sobre las incidencias del repositorio (véase ).
La finalidad de este experimento radica en la obtención de una
puntuación que defina la actitud de los usuarios participantes en la
discusión generada por una incidencia. La puntuación obtenida se calcula
por cada fragmento y puede variar entre 0 y 1, siendo cero la
representación de una expresión de sentimientos muy negativos, y uno la
representación de una expresión de sentimientos muy positivos.

![Formulario de lanzamiento de experimento de Sentiment
Analysis.](docs/img/webapp_sa_form.png)

Los parámetros disponibles son los siguientes:

-   **Selección de incidencia**. Este parámetro permite seleccionar
    mediante un desplegable las incidencias del repositorio de acuerdo
    con su título.

-   **Selección de usuario**. Este parámetro permite filtrar los
    comentarios de la incidencia que van a ser tomados como entrada del
    modelo a aquellos realizados exclusivamente por dicho usuario.

-   Utilizar comentarios. Este parámetro tiene como finalidad permitir
    la realización del análisis de sentimientos de la entrada inicial de
    la incidencia, excluyendo sus comentarios tanto del autor como del
    resto de participantes en la conversación.

Los resultados del experimento se presentan haciendo uso de un gráfico
de barras verticales. Cada barra azul representa la puntuación otorgada
a un comentario, siendo la línea horizontal roja el indicador de la
puntuación media obtenida de acuerdo con los parámetros introducidos
(véase ).

![Resultados obtenidos en un experimento de Sentiment
Analysis.](docs/img/webapp_sa_output.png)

### Summarization

Este formulario permite al usuario el lanzamiento de un experimento de
generación de resúmenes abstractivos sobre las incidencias del
repositorio (véase ). La finalidad de este experimento consiste en
generar un fragmento de texto que resuma el contenido tratado por la
incidencia. El modelo se aplica de manera individual a cada comentario y
posteriormente se procede a la concatenación de los resultados para
obtener un resumen general del tema tratado en la discusión de la
incidencia. Este experimento cuenta con limitaciones lingüísticas debido
a que el modelo utilizado que solo ofrece soporte a textos escritos en
inglés.

Los parámetros disponibles son los siguientes:

![Formulario de lanzamiento de experimento de
Summarization.](docs/img/webapp_summ_form.png)

-   **Selección de incidencia**. Este parámetro permite seleccionar
    mediante un desplegable las incidencias del repositorio de acuerdo
    con su título.

-   **Utilizar descripción**. Este parámetro permite otorgar un mayor
    contexto al modelo incluyendo la información correspondiente con la
    descripción de la incidencia en la realización de sus operaciones.
    Por defecto el modelo sólo utiliza la información deducida a partir
    de su título.

-   **Longitud mínima de los fragmentos**. Este parámetro permite
    establecer una longitud mínima de los resúmenes parciales que
    compondrán el resumen final. Es importante destacar el aspecto de
    los fragmentos, ya que los fragmentos de las entradas se introducen
    en el modelo de forma individual, por lo tanto el resumen final se
    elabora a partir de su concatenación. También se ha de destacar que
    esta longitud no se corresponde directamente con el número de
    caracteres debido a las consideraciones tomadas por el *tokenizador*
    utilizado por los modelos.

-   **Longitud máxima de los fragmentos**. Este parámetro permite
    establecer una longitud máxima de los resúmenes parciales que
    compondrán el resumen final.

Los resultados del experimento proveen al usuario del resumen generado
en función del contenido de la incidencia y los parámetros de longitud
establecidos para cada fragmento (véase ).

![Resultados obtenidos en un experimento de
Summarization.](docs/img/webapp_summ_output.png)

Uso de la API REST
------------------

En la siguiente sección se incluye un listado de los endpoint
proporcionados por la API junto con los parámetros necesarios para

### GET - Obtener estado

-   **Respuestas**

    -   **200 OK**. La aplicación se está ejecutando.

### GET - Obtener listado de las tareas

-   **Ruta**

    -   `/tasks/`

-   **Respuestas**

    -   **200 OK**. Se obtiene un objeto JSON con un único atributo
        *eqlts* que contiene un listado de objetos tarea.

        -   **Content-Type**: `application/json/`.

        -   **Body**:

            -   **task\_id**: Number

            -   **state**: Number

            -   **timestamp**: String

            -   **repo\_dir**: String

            -   **task\_type**: Number

            -   **params**: Object

    -   **500 Internal Server error**. Se ha producido un error interno
        en la aplicación.

### GET - Obtener listado de los repositorios

-   **Ruta**

    -   `/repos/`

-   **Respuestas**

    -   **200 OK**. Se obtiene un objeto JSON con un único atributo
        *eqlts* que contiene un listado de objetos respositorio.

        -   **Content-Type**: `application/json/`.

        -   **Body**:

            -   **repo\_dir**: String

            -   **title**: String

            -   **description**: String

            -   **labels**: List

    -   **500 Internal Server error**. Se ha producido un error interno
        en la aplicación.

### GET - Obtener listado de las incidencias

-   **Ruta**

    -   `/issues/`

-   **Respuestas**

    -   **200 OK**. Se obtiene un objeto JSON con un único atributo
        *eqlts* que contiene un listado de objetos incidencia.

        -   **Content-Type**: `application/json/`.

        -   **Body**:

            -   **repo\_dir**: String

            -   **issue\_id**: Number

            -   **author**: String

            -   **title**: String

            -   **description**: String

            -   **labels**: List

            -   **is\_pull\_request**: Boolean

    -   **500 Internal Server error**. Se ha producido un error interno
        en la aplicación.

### GET - Obtener listado de los comentarios

-   **Ruta**

    -   `/comments/`

-   **Respuestas**

    -   **200 OK**. Se obtiene un objeto JSON con un único atributo
        *eqlts* que contiene un listado de objetos comentario.

        -   **Content-Type**: `application/json/`.

        -   **Body**:

            -   **repo\_dir**: String

            -   **issue\_id**: Number

            -   **comment\_id**: Number

            -   **author**: String

            -   **body**: String

    -   **500 Internal Server error**. Se ha producido un error interno
        en la aplicación.

### GET - Obtener listado de los resultados de las ejecuciones

-   **Ruta**

    -   `/outcomes/`

-   **Respuestas**

    -   **200 OK**. Se obtiene un objeto JSON con un único atributo
        *eqlts* que contiene un listado de objetos resultado.

        -   **Content-Type**: `application/json/`.

        -   **Body**:

            -   **task\_id**: Number

            -   **repo\_dir**: String

            -   **model\_type**: String

            -   **outcome\_data**: JSON

            -   **exec\_time**: Number

    -   **500 Internal Server error**. Se ha producido un error interno
        en la aplicación.

### POST - Extraer la información de un repositorio

-   **Ruta**

    -   `/extract/`

-   **Parámetros**

    -   **Content-Type**: `application/json/`.

    -   **Body**:

        -   **gh\_user**: String

        -   **gh\_repo**: String

-   **Respuestas**

    -   **200 OK**. Se obtiene un objeto JSON con un indicador de que la
        tarea ha sido encolada correctamente y su identificador único.

        -   **Content-Type**: `application/json/`.

        -   **Body**:

            -   **Added**: \[Body\] Boolean

            -   **task\_id**: \[Body\] Number

    -   **400 Bad Request**. Los parámetros introducidos son
        incorrectos.

    -   **500 Internal Server error**. Se ha producido un error interno
        en la aplicación.

### GET - Obtener la información de un repositorio

-   **Ruta**

    -   `/user/<string:gh_user>/repo/<string:gh_repo>`

-   **Parámetros**

    -   **gh\_user**: \[Path\] String

    -   **gh\_repo**: \[Path\] String

-   **Respuestas**

    -   **200 OK**. Se obtiene un objeto JSON con la información del
        repositorio.

        -   **Content-Type**: `application/json/`.

        -   **Body**:

            -   **repo\_dir**: String

            -   **title**: String

            -   **description**: String

            -   **labels**: List

    -   **202 Accepted**. La petición es correcta pero la información
        solicitada aún no se encuentra disponible.

    -   **404 Not Found**. No se encuentra ningún repositorio de acuerdo
        con los parámetros introducidos.

    -   **424 Failed Dependency**. La extracción de los datos del
        repositorio falló.

    -   **500 Internal Server error**. Se ha producido un error interno
        en la aplicación.

### GET - Obtener la información de una incidencia de un repositorio

-   **Ruta**

    -   `/user/<string:gh_user>/repo/<string:gh_repo>/issue/<int:issue_id>`

-   **Parámetros**

    -   **gh\_user**: \[Path\] String

    -   **gh\_repo**: \[Path\] String

    -   **issue\_id**: \[Path\] Number

-   **Respuestas**

    -   **200 OK**. Se obtiene un objeto JSON con la información de la
        incidencia.

        -   **Content-Type**: `application/json/`.

        -   **Body**:

            -   **repo\_dir**: String

            -   **issue\_id**: Number

            -   **author**: String

            -   **title**: String

            -   **description**: String

            -   **labels**: List

            -   **is\_pull\_request**: Boolean

    -   **400 Bad Request**. Los parámetros introducidos son
        incorrectos.

    -   **404 Not Found**. No se encuentra ninguna incidencia de acuerdo
        con los parámetros introducidos.

    -   **500 Internal Server error**. Se ha producido un error interno
        en la aplicación.

### GET - Obtener las incidencias de un repositorio

-   **Ruta**

    -   `/user/<string:gh_user>/repo/<string:gh_repo>/issues`

-   **Parámetros**

    -   **gh\_user**: \[Path\] String

    -   **gh\_repo**: \[Path\] String

-   **Respuestas**

    -   **200 OK**. Se obtiene un objeto JSON con una lista incidencias
        del repositorio.

        -   **Content-Type**: `application/json/`.

        -   **Body**:

            -   **repo\_dir**: String

            -   **issue\_id**: Number

            -   **author**: String

            -   **title**: String

            -   **description**: String

            -   **labels**: List

            -   **is\_pull\_request**: Boolean

    -   **202 Accepted**. La petición es correcta pero la información
        solicitada aún no se encuentra disponible.

    -   **404 Not Found**. No se encuentra ningún repositorio de acuerdo
        con los parámetros introducidos.

    -   **424 Failed Dependency**. La extracción de los datos del
        repositorio falló.

    -   **500 Internal Server error**. Se ha producido un error interno
        en la aplicación.

### GET - Obtener los comentarios de una incidencia

-   **Ruta**

    -   `/user/<string:gh_user>/repo/<string:gh_repo>/issue/<int:issue_id>/comments`

-   **Parámetros**

    -   **gh\_user**: \[Path\] String

    -   **gh\_repo**: \[Path\] String

    -   **issue\_id**: \[Path\] Number

-   **Respuestas**

    -   **200 OK**. Se obtiene un objeto JSON con una lista comentarios
        de la incidencia.

        -   **Content-Type**: `application/json/`.

        -   **Body**:

            -   **repo\_dir**: String

            -   **issue\_id**: Number

            -   **author**: String

            -   **title**: String

            -   **description**: String

            -   **labels**: List

            -   **is\_pull\_request**: Boolean

    -   **202 Accepted**. La petición es correcta pero la información
        solicitada aún no se encuentra disponible.

    -   **404 Not Found**. No se encuentra ningún repositorio de acuerdo
        con los parámetros introducidos.

    -   **424 Failed Dependency**. La extracción de los datos del
        repositorio falló.

    -   **500 Internal Server error**. Se ha producido un error interno
        en la aplicación.

### GET - Obtener las operaciones realizadas sobre un repositorio

-   **Ruta**

    -   `/user/<string:gh_user>/repo/<string:gh_repo>/tasks`

-   **Parámetros**

    -   **gh\_user**: \[Path\] String

    -   **gh\_repo**: \[Path\] String

-   **Respuestas**

    -   **200 OK**. Se obtiene un objeto JSON con la lista de las
        operaciones realizadas sobre el repositorio.

        -   **Content-Type**: `application/json/`.

        -   **Body**:

            -   **task\_id**: Number

            -   **state**: Number

            -   **timestamp**: String

            -   **repo\_dir**: String

            -   **task\_type**: Number

            -   **params**: Object

    -   **204 No Content**. No se localizan registros de repositorios
        que concuerden con los parámetros introducidos.

    -   **500 Internal Server error**. Se ha producido un error interno
        en la aplicación.

### GET - Obtener los experimentos lanzados sobre un repositorio

-   **Ruta**

    -   `/user/<string:gh_user>/repo/<string:gh_repo>/experiments`

-   **Parámetros**

    -   **gh\_user**: \[Path\] String

    -   **gh\_repo**: \[Path\] String

-   **Respuestas**

    -   **200 OK**. Se obtiene un objeto JSON con la lista de los
        resultados de los experimentos lanzados sobre el repositorio.

        -   **Content-Type**: `application/json/`.

        -   **Body**:

            -   **task\_id**: Number

            -   **repo\_dir**: String

            -   **model\_type**: String

            -   **outcome\_data**: JSON

            -   **exec\_time**: Number

    -   **204 No Content**. No se localizan registros de repositorios
        que concuerden con los parámetros introducidos.

    -   **500 Internal Server error**. Se ha producido un error interno
        en la aplicación.

### POST - Lanzar un experimento de Zero-Shot Classification sobre un repositorio

-   **Ruta**

    -   `/user/<string:gh_user>/repo/<string:gh_repo>/process/zsc/`

-   **Content-Type**: `application/json/`.

-   **Parámetros**

    -   **gh\_user**: \[Path\] String

    -   **gh\_repo**: \[Path\] String

    -   **issue\_id**: \[Body\] Number

    -   **accuracy**: \[Body\] Float. Entre 0 y 1.

    -   **use\_desc**: \[Body\] Boolean

    -   **extra\_labels**: \[Body\] String. Cada término deberá estar
        separado por un punto y coma.

-   **Respuestas**

    -   **200 OK**. Se obtiene un objeto JSON con un indicador de que el
        experimento ha sido encolado correctamente y su identificador
        único.

        -   **Content-Type**: `application/json/`.

        -   **Body**:

            -   **Added**: \[Body\] Boolean

            -   **task\_id**: \[Body\] Number

    -   **400 Bad Request**. Los parámetros introducidos son
        incorrectos.

    -   **406 Not Acceptable**. Los parámetros introducidos no se
        corresponden con ninguno de los repositorios disponibles.

    -   **500 Internal Server error**. Se ha producido un error interno
        en la aplicación.

    -   **503 Service Unavailable**. En estos momentos no es posible
        lanzar el experimento sobre el repositorio solicitado.

### POST - Lanzar un experimento de Sentiment Analysis sobre un repositorio

-   **Ruta**

    -   `/user/<string:gh_user>/repo/<string:gh_repo>/process/sa/`

-   **Content-Type**: `application/json/`.

-   **Parámetros**

    -   **gh\_user**: \[Path\] String

    -   **gh\_repo**: \[Path\] String

    -   **issue\_id**: \[Body\] Integer

    -   **author**: \[Body\] String.

    -   **with\_comments**: \[Body\] Boolean

-   **Respuestas**

    -   **200 OK**. Se obtiene un objeto JSON con un indicador de que el
        experimento ha sido encolado correctamente y su identificador
        único.

        -   **Content-Type**: `application/json/`.

        -   **Body**:

            -   **Added**: \[Body\] Boolean

            -   **task\_id**: \[Body\] Number

    -   **400 Bad Request**. Los parámetros introducidos son
        incorrectos.

    -   **406 Not Acceptable**. Los parámetros introducidos no se
        corresponden con ninguno de los repositorios disponibles.

    -   **500 Internal Server error**. Se ha producido un error interno
        en la aplicación.

    -   **503 Service Unavailable**. En estos momentos no es posible
        lanzar el experimento sobre el repositorio solicitado.

### POST - Lanzar un experimento de Summarization sobre un repositorio

-   **Ruta**

    -   `/user/<string:gh_user>/repo/<string:gh_repo>/process/summ/`

-   **Content-Type**: `application/json/`.

-   **Parámetros**

    -   **gh\_user**: \[Path\] String

    -   **gh\_repo**: \[Path\] String

    -   **max\_length**: \[Body\] Integer

    -   **min\_length**: \[Body\] Integer

    -   **with\_comments**: \[Body\] Boolean

-   **Respuestas**

    -   **200 OK**. Se obtiene un objeto JSON con un indicador de que el
        experimento ha sido encolado correctamente y su identificador
        único.

        -   **Content-Type**: `application/json/`.

        -   **Body**:

            -   **Added**: \[Body\] Boolean

            -   **task\_id**: \[Body\] Number

    -   **400 Bad Request**. Los parámetros introducidos son
        incorrectos.

    -   **406 Not Acceptable**. Los parámetros introducidos no se
        corresponden con ninguno de los repositorios disponibles.

    -   **500 Internal Server error**. Se ha producido un error interno
        en la aplicación.

    -   **503 Service Unavailable**. En estos momentos no es posible
        lanzar el experimento sobre el repositorio solicitado.


## Authors and Acknowledgement

-   [Pablo Fernández](https://www.github.com/mrpya45) for development and design.
-   [Carlos López](https://www.github.com/clopezno) for tutorization.
-   [Jesús Alonso Abad](https://www.github.com/kencho) for tutorization.
