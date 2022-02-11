# Stanford CS 168: Modern Algorithmic Toolbox

Class assignments for http://web.stanford.edu/class/cs168/index.html

## Goals

- Understand all of the lecture documents
- Do all of the assignments
- Maybe learn some interesting tech along the way

## Building

The simplest thing that will work for most developers:

    cd Stanford_CS_168
    pip3 install .

## Developing

The project is managed using [Poetry](https://python-poetry.org/docs/):

    pip3 install --user poetry

Install dependencies:

    poetry install --no-root

Install the pre-commit hooks:

    poetry run pre-commit install

If you _have_ to commit or push right now and don't have time to fix a failing test, use one of the following:

    git commit --no-verify
    git push --no-verify

For now, all of the tests, formatting, etc. can be run only from the pre-commit hook:

    poetry run pre-commit run --hook-stage commit --all-files

I know it's dumb... I'm looking into it.

A VSCode settings file is included which contains configurations for all of the linting and formatting tools installed.

## Developing Notebooks

    poetry shell
    cd cs168/notebooks
    jupyter lab
