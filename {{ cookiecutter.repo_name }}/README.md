{{cookiecutter.project_name}}
==============================

[![Tests](https://github.com/{{cookiecutter.github_org_or_user}}/{{cookiecutter.repo_name}}/workflows/Tests/badge.svg)](https://github.com/{{cookiecutter.github_org_or_user}}/{{cookiecutter.repo_name}}/actions?workflow=Tests)

{{cookiecutter.description}}

Steps after having cookiecutter cloned this repo:

- Set up a python virtual environment and automate its use when in this directory. E.g., with
 pyenv-virtualenv: ``pyenv virtualenv {{ cookiecutter.min_python_version }} <proj-name>`` then `echo <proj-name> > .python-version`
- Initialize git repo with `git init`.
- Initialize DVC with `dvc init`.
- Set up a [dvc remote](https://dvc.org/doc/command-reference/remote).
- Set up [DVC merge driver](https://dvc.org/doc/user-guide/how-to/resolve-merge-conflicts#directories)
- Set up pre-commit hooks `pre-commit install --hook-type pre-push --hook-type post-checkout --hook-type pre-commit`
- Set up DVC pre-commit hooks: `dvc install --use-pre-commit-tool`
- Go through and delete files we don't want.
- Run nox

Questions to ask the client:
- Create this list.

Project Organization
------------

```
├── LICENSE
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── dvc.yaml           <- DVC file that specifies a pipeline's directed acyclic graph (DAG)
│
├── .github/workflows/tests.yaml  <- Github Actions configuration file.
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── noxfile.py         <- Test managmenet configuration
│
├── params.yaml        <- Parameters for experiments managed by DVC.
│
├── .pre-commit-config.yaml  <- Configuration for pre-commit hooks.
│
├── pyproject.toml     <- Houses project metadata and dependencies. Used by Poetry.
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
└── src                <- Source code for use in this project.
    ├── __init__.py    <- Makes src a Python module
    │
    ├── data           <- Scripts to download or generate data
    │   └── make_dataset.py
    │
    ├── models         <- Scripts to train models and then use trained models to make
    │   │                 predictions
    │   ├── predict_model.py
```

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
