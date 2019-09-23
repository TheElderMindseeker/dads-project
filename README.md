# Web Application

This is a simple web application created during Distributed and Decentralized Systems course by Daniil Botnarenku, Alexey Gospodchikov and Nick Gaivoronsky.

## Dependencies

This project uses Pipenv to track its dependencies. Pipenv file is situated in the root directory. If you want to know more about Pipenv, look [here](https://github.com/pypa/pipenv).

## Code Style and Quality Control

It is highly recommended to use the following tools to control code quality and make life easier working with this project:

* [Pylint](https://pylint.readthedocs.io/en/latest/)
* [Yapf](https://github.com/google/yapf)

Both utilities are locked in Pipenv dev-dependencies so it should not be a problem installing them. Pylint is a Python linter and Yapf is a code autoformatter. The `.style.yapf` file which you may find in the root of the directory is a code style declaration for it.

## Running the Code

To simply run the code in order to make sure it works use the following command in the root directory:

```bash
pipenv run python app.py
```
