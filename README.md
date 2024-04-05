# scrap_parc_relai
Projet demo pour tester python

## GIT

## INSTALLATION DU PROJET AVEC POETRY

### Init
poetry new scrap_parc_relai --name src

### ajout de depandances
poetry add pytest
poetry add requests
poetry add logging
poetry add pytest
poetry add pytest-cov --group dev

### mise à jour suite à l'ajout de dépendance
poetry install
poetry update


### analyse des depandance 
poetry show

### activation du vitual env
poetry config virtualenvs.create true --local
poetry config virtualenvs.in-project true --local
poetry config virtualenvs.prefer-active-python true --local

## Run
poetry run pytest -v --cov=src --cov-report=html 

## Tests
poetry run pytest -v --cov=src --cov-report=html 