# Stanford CS 168: Modern Algorithmic Toolbox

Class assignments with support code for http://web.stanford.edu/class/cs168/index.html. All of the assignments are under [`cs168/notebooks/`](./cs168/notebooks/).

The notebooks sometimes refer to data stored in the `materials/` submodule, but that repo cannot be made public due to copyright (if you email me I can give you personal access). The materials are all still available on the internet in other locations.

## My goals for the course

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

For now, all of the formatting, linting, etc. can be run only from the pre-commit hook:

    poetry run pre-commit run -v --hook-stage commit --all-files

I know it's dumb... I may look into it sometime.

A VSCode settings file is included which contains configurations for all of the linting and formatting tools installed.

## Developing Notebooks

After installing `poetry` and the dependencies:

    poetry shell
    cd cs168/notebooks
    jupyter lab

## License

Apache 2.0; some material from mini project 6 is copyright DINDIN Meryll, also released under Apache 2.0.
