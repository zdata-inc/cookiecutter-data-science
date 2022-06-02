{{cookiecutter.project_name}}
==============================

[![Tests](https://github.com/{{cookiecutter.github_org_or_user}}/{{cookiecutter.repo_name}}/workflows/Tests/badge.svg)](https://github.com/{{cookiecutter.github_org_or_user}}/{{cookiecutter.repo_name}}/actions?workflow=Tests)

{{cookiecutter.description}}

Development guidelines
----------------------

This project template is intended to be open-ended and flexible without
overprescribing decisions about how the project development should proceed.
However it does make some nudges which are based on opinions on how development
should proceed. Some of the tools here could be replaced with other tools.
Poetry is not necessary, dvc is not necessary, etc. But a good workflow should
incorporate tooling and processes that offer similar functionality.

Some sources of inspiration for compiling this:
- personal experience
- [Hypermodern python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/). There actually is a hypermodern python cookiecutter template already, but we opt to create our own that is more data science focused. In particular, the use of data versioning and experiment setup is not handled in that document.  main additions are the use of DVC

The instructions in this README assume you have already instantiated a repo
from this template using

```
pip install cookiecutter # This can be in any environment
cookiecutter {{cookiecutter.repo_name}}
```

Note that cookiecutter can be installed in any environment. We'll be using
poetry to create a project-specific environment once the repository is set up.

Poetry for dependency and virtual environment management
--------------------------------------------------------

The top level directory contains a `pyproject.toml` file. This adheres to pep
517 and 518. This can be used by a tool such as poetry to manage a virtual
environment and its dependencies. I encourage the use of poetry or some other
comparable tool instead of adhoc management of a requirements.txt file.

Install the package with:
```
poetry install
```

Subsequent commands can be run in the virtual environment by calling
```
poetry shell
```

See poetry documentation for more details.

Worth noting is that the default `pyproject.toml` in this template includes a
number of development dependencies.

You should also try updating some of the included dev dependencies with `poetry update`.

## Data Versioning (with DVC)

Beyond using a git repository in the first place to track code changes, the
next most important component of machine learning reproducability is to track
changes to the data. A typical workflow on our projects would start by
recieving some small amount of data from a client for which we begin
experimenting. Along the way we might refine labels (or add them if they
weren't there to begin with). After this initial iteration we then might be
given more data from the client or we might hunt down our own in order to fill
in gaps in the representation of the training data. This process will repeat
and along the way we will be experimenting and gathering results. It is
essential to be able to keep track of the changes to all this data so that the
context that gave rise to a trained model.

There are a number of young tools for the job here. One solid option that
builds on top of git is [dvc](https://dvc.org/). The protocol that this project
template advocates for is to put all raw data in `data/raw/` and `dvc add` it
before git committing.  Any manual modifications made to the data should happen
to data in `data/raw/` and it should be `dvc add`ed and `git commit`ed again.
Any automated manipulations of the data as part of preprocessing should output
the final product in `data/processed`. The scripts to do this should be in
`src/data/` (for example `src/data/preprocess.py`). The command used to produce
that data should be in the `dvc.yaml` file in the root directory. The template
`dvc.yaml` file in this template offers some degree of support for incremental
processing. It just requires the list of files in `data/raw/` to be captured
in a YAML list in `params.yaml`. If the number of these files is too great to
manually be managed this could be automated with a script that
writes the contents of `data/raw/` to `params.yaml`, but we leave that to
future work.

In this case any change, however small, in the `data/raw` directory would
trigger re-running of the data pipeline. An alternative would be to store a
variable with a list of files in `data/raw/` and reference that variable in the
dependencies in that stage in the `dvc.yaml` file. But that is beyond the scope
of this README.md.

## Testing

### pytest

`tests/` is a directory that can be used to house tests written for pytest. A
practice I have found useful is to follow a loose interpretation of test-driven
development. In this approach it is not that unit tests need to be run are all
written before the program code, but that when _running_ the code a pytest test
case is used. This frees the programmer up to write code before tests, but
provides sufficient lean to create tests when wanting to run code. These tests
can be incrementally refined. The underlying philosophy is that it is better to
have some sort of habit of creating imperfect test cases rather than none at
all because true test-driven development was too hard.

### nox

[Nox](https://nox.thea.codes/en/stable/) is a tool for automating testing. The
`noxfile.py` that we have as default in this project template runs tests found
in `tests/` (reporting code coverage of those tests along the way) and
additionally runs the static analysis tools `flake8` and `mypy`. It's good to
run nox periodically though there is no enforcement to do it each commit via a
pre-commit hook (the tests would slow things down and discourage
small commits). A better place to run this is based on judgment after some
substantial change has been made. It could be run before merges into master,
though that may be best left for a CI tool like Github Actions. Update this: We
run nox in github actions. What we really want excluded are pytest.mark.slow
tests.

## Pre-commit hooks

`.pre-commit-config.yaml` includes some pre-commit hooks to use. `poetry run pre-commit install` to use them. They are mostly style checks. Decisions should be made about what makes it into a pre-commit hook versus what
is left simply for IDEs to check versus what gets checked by Github Actions
before merging into the trunk.

## CI Tests with Github Actions

To be done.


Differences to the default cookeicutter template.
-------------------------------------------------

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── preprocess.py
    │   │
    │   └── models         <- Scripts to train models and then use trained models to make
    │       │                 predictions
    │       ├── predict.py
    │       └── train.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
