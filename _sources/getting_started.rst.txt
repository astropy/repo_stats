Getting started
===============

Repo file structure
-------------------
| The `py_template` repo has a basic file structure:
| 1) `.github` has two subfolders:
|   * `ISSUE_TEMPLATE` has files that are templates users can select from when opening an issue in the repo on GitHub
|   * `workflows` implements continuous integration (CI) through GitHub 'actions' that are automatically run according to a chosen trigger. These are currently:
|        - `docs.yml` builds and deploys this docs site when a push is made to `main`.
|        - `format_lint.yml` lints and formats the code on each push using *ruff*.
|        - `package.yml` releases the package to PyPI on each *release* (create a release from the repo's main GitHub page). This makes the latest release version of the package *pip*-installable. For a guide on how to first reserve a name for your project on PyPI (necessary for this workflow), see the `Python packaging guide <https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/>`_.
|        - `tests.yml` runs tests with *pytest* on each push.
|        - `type_check.yml` runs type checking with *mypy* on each push. The CI continues even if the type checker finds errors.
| 2) `docs` has the files used to build the docs with *Sphinx*, with the site content in `index.rst` and `py_API.rst`.
| 3) `py_template` is the source code folder, with the necessary `__init__.py` and example code file, `example_module.py`.
| 4) `test` has the unit tests, with example tests for the source code file in `test_example_module.py`. When you add new test files, they should start with `test_` so *pytest* recognizes them.
| 5) `.gitignore` is a list of file types that are ignored when you push to the remote repo.
| 6) `HISTORY.rst` is the change log that you should update as you implement the packaged version.
| 7) `LICENSE.rst` has the package's license.
| 8) `MANIFEST.in` has instructions for how to pre-process the package (which files to exclude) when preparing to release it to PyPI (the Python Package Index). Packages uploaded to PyPI can be installed by users with *pip*. 
| 9) `README.md` is the file you're reading! It has badges that use the CI to display if the unit tests are passing, what percentage of the code is covered by the tests, and if the docs build and deploy is passing.
| 10) `pyproject.toml` is the configuration file for packaging the software. See the `Python docs <https://packaging.python.org/en/latest/guides/writing-pyproject-toml/>`_ for a description of its contents. See also the `example_setup_files` directory for an example minimal `pyproject.toml` and the analogous `setup.py`.

Making a new Python repo using `py_template`
--------------------------------------------
| 1) Click the 'Use this template' button at the top-right of the GitHub page. 
| 2) In your new repo, rename (search and replace) all instances of "py_template" with the name for your package. 
| 3a) If you create a public repo, to set up your docs deployment CI: from your repo page, go to 'Settings' then 'Pages', then set 'Source' as 'Deploy from a branch' and set 'Branch' as 'gh-pages'. Your docs will now deploy according to the trigger in `.github/workflows/docs.yml`
| 3b) If you create a private repo, the docs build will fail because private repos can't have a public docs page. You can disable the docs build and deploy workflow in `.github/workflows/docs.yml`
| 4) Update the `authors` field in `pyproject.toml`, `docs/conf.py` and `LICENSE.rst` (the template is partially based on the `OpenAstronomy packaging guide <https://github.com/OpenAstronomy/packaging-guide>`_, so please retain that aspect of the license).

Interacting with your new code
------------------------------
| After cloning your repo to your computer, from the project's root directory, you can:
| 1) Install your package with all optional dependencies: 
| `pip install -e ".[dev]"`
| 2) Run your tests:
| `pytest .`
| 3) Run linting and formatting to see their effects:
| `ruff check .`
| 4) Run type checking using mypy:
| `mypy --strict .`
| 5) Build your docs locally:
| `cd docs; make html`
| After building the docs, view them with 
| `open docs/_build/html/index.html`

Developing your package
-----------------------
| 1) Add new unit tests in `test/test_*.py` for new functions and classes. Test not just whether the new code runs, but also if it gives a sensible result.
| 2) Update the docs, including the main page (`docs/index.rst`), adding pages, and updating the API (`docs/py_API.rst`) when you add new functions and classes.
| 3) Optionally change the CI triggers for each of the actions in `.github/workflows`.
| 4) Update the changelog in `HISTORY.rst` when you're ready to release your first version of the code!