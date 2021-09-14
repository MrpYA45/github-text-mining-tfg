[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![Issues](https://img.shields.io/github/issues/MrpYA45/github-text-mining-tfg?color=blue)](https://github.com/MrpYA45/github-text-mining-tfg/issues)
[![pylint score](https://github.com/MrpYA45/github-text-mining-tfg/actions/workflows/stylechecking.yml/badge.svg?style=for-the-badge)](https://github.com/MrpYA45/github-text-mining-tfg/actions/workflows/stylechecking.yml)
[![mypy typechecking](https://github.com/MrpYA45/github-text-mining-tfg/actions/workflows/typechecking.yml/badge.svg)](https://github.com/MrpYA45/github-text-mining-tfg/actions/workflows/typechecking.yml)
[![codebeat badge](https://codebeat.co/badges/b88ca615-8ccc-4770-a607-79e83b14dac5)](https://codebeat.co/projects/github-com-mrpya45-github-text-mining-tfg-main)

# GitHub Text Mining (Bachelor's Degree Final Project)

This project has the objective of creating a microservices application which lets the user introduce the url of a Github repository and extract a series of information from it applying certain natural language processing models (NLP).

## Use
The first time you launch the application it will probably fail, don't worry. You will find a folder on each service called `config`. Inside you will find a `config.json` file. If you just want to try the project the only file you need to change is the one in the extraction service which asks for a `GitHub token`. If you need help getting the token, please refer to the official [GitHub Docs](https://docs.github.com/es/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token).

## Docker

The application was designed using Docker. In the repository you could find the required files to launch the application.

To build the application you can use the next command:

```
docker-compose -f docker/config/docker-compose.yml build
```

To run the application just use:

```
docker-compose -f docker/config/docker-compose.yml up -d
```
To stop the application and remove the containers use:
```
docker-compose -f docker/config/docker-compose.yml rm -sfv
```

## Authors and Acknowledgement

-   [Pablo Fernández](https://www.github.com/mrpya45) for development and design.
-   [Carlos López](https://www.github.com/clopezno) for tutorization.
-   [Jesús Alonso Abad](https://www.github.com/kencho) for tutorization.
