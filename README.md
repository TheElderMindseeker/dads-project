# Web Application

This is a simple web application created during Distributed and Decentralized Systems course by Daniil Botnarenku, Alexey Gospodchikov and Nick Gaivoronsky.

The deployed version of the project is available at https://dads-project.herokuapp.com

## Dependencies

This project uses Pipenv to track its dependencies. Pipenv file is situated in the root directory. If you want to know more about Pipenv, look [here](https://github.com/pypa/pipenv). Generally, to install all required dependencies use:

```bash
pipenv install
pipenv install --dev
```

You will only need the latter if you want to participate in the development of the project.

## Code Style and Quality Control

It is highly recommended to use the following tools to control code quality and make life easier working with this project:

* [Pylint](https://pylint.readthedocs.io/en/latest/)
* [Yapf](https://github.com/google/yapf)

Both utilities are locked in Pipenv dev-dependencies so it should not be a problem installing them. Pylint is a Python linter and Yapf is a code autoformatter. The `.style.yapf` file which you may find in the root of the directory is a code style declaration for it.

## Setup

Currently, the application will run only in the debug configuration. It will use a `test_db` Postgresql database.

To set up the application, the database must be created. To do so, set up the application with

    export FLASK_APP="livebook_run:create_app()"

Then, create the database:

    flask init-db

## Configuration

Currently, there are only two pieces of configuration you need to setup and both are environmental variables: `DADS_DATABASE_URI` and `DADS_TEST_DATABASE_URI`. The former points to the production database of the project and the latter to the testing.

## Running the Code

To simply run the code in order to make sure it works use the following command in the root directory:

```bash
pipenv run python livebook_run.py
```

## Testing

In order to test the project run the following command:

```bash
pipenv run pytest
```

Note that you need to install development dependencies for this command to work correctly.
