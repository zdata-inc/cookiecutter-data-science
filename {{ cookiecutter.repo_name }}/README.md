{{cookiecutter.project_name}}
==============================

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
- 


The instructions in this README assume you have already instantiated a repo
from this template using

```
pip install cookiecutter
cookiecutter {{cookiecutter.repo_name}}
```

Note that cookiecutter can be installed in any environment. We'll be using
poetry to create a project-specific environment once the repository is set up.

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

You should also try updating some of the included dev dependencies with `poetry update`.


Salient things to discuss:
- pyproject.toml. 
- 


- It includes a pyproject.toml. Poetry is a package manager that can work with
    this <insert poetry commands to get set up with poetry>. Why poetry?
- It includes a test directory that can be used with pytest and nox. poetry add --dev
    pytest. Do test-driven coding. Why test-driven? At the very least use some
    pytest tests.
- It includes some dvc.yaml preconfigured to do some preprocessing. Add some
    dvc commands in here. Why dvc?
- pre-commit hooks. What should we leave to nox versus pre-commit hooks versus
    just having in an IDE.


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
