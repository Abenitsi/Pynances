# Python Skeleton

## Usage
1.  Fork this project
2.  Edit README.md, adding the necessary information. See [makeareadme.com](https://www.makeareadme.com)
3.  Edit pyproject.toml accordingly
    1. Change the project name (project/name)
    2. Change the python version if needed (project/requires-python)
    3. Add your core dependencies (project/dependencies)
    4. Add your optional dependencies (project.optional-dependencies)
    5. If needed, configure the bundled development tools
    6. Import linter should be either configured or removed, as it does not come with a base configuration
    7. If needed, configure your optional dependencies (the use of pyproject.toml is preferred over specific custom files)
4.  Run `make install` in order to install the required dependencies and pre-commit hooks
5.  Edit etc/Dockerfile, as it doesn't come with an entrypoint by default, or remove it if the project wont be using Docker
6.  Start developing your project!

## Bundled tools
-   [black](https://black.readthedocs.io/en/stable/)

    A code style linter and fixer. Will automatically fix all style issues on the codebase.

    Run it with `black src`.

-   [mypy](https://mypy.readthedocs.io/en/stable/)

    A type checker. Will point to missing type annotations, and mistreated types.

    Run it with `mypy src`.

-   [import-linter](https://import-linter.readthedocs.io/en/stable/readme.html)

    A tool to enforce architecture patterns. Will make sure the defined architecture rules are followed.

    Run it with `lint-imports`.

-   [pre-commit](https://pre-commit.com/index.html)

    A git hook configuration tool.

    Run it with `make pre-commit-run`.

    It will also run automatically when committing changes by default, but more stages can be configured (e.g. before pushing, after merging, etc).

    If, for some reason, a hook is causing trouble, it can be temporarily disabled by setting a $SKIP environment variable after committing:

    `$SKIP=black,mypy git commit -m "fix: some really messed up bug"`

-   [pytest](https://docs.pytest.org/en/7.3.x/)

    A unit testing framework. Will run all modules starting with test, all classes starting with Test and all functions starting with test.

    Run it with `pytest`.

-   [coverage.py](https://coverage.readthedocs.io/en/7.2.3/index.html)

    A tool to measure the code coverage.

    Run `coverage run` to gather the necessary data.

    Run `coverage report` to output the results on the command line.

    Run `coverage html` to generate an interactive HTML report.

## Make targets
The skeleton comes a Makefile to simplify installing the project and running some commands. It comes with the following targets:
-   `install`:

    Use it to install all the project dependencies and set up the git hooks.

-   `pre-commit run`:

    Run the pre-commit tool against all the project files.

-   `cq`:

    Run all the code quality commands. Use it to check your code while developing.

-   `test`:

    Run all the unit tests.

-   `coverage`:

    Get the current code coverage, outputted in the shell.

-   `coverage-html`:

    Generate an HTML report of the current code coverage, under the htmlcov directory.
