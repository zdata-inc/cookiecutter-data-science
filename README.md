# A Cookiecutter Data Science Template With Data Versioning and Experiment Management

This project template is intended to be open-ended and flexible without
overprescribing decisions about how the project development should proceed and
hopefully without overwhelming the developer with excessive tooling.  However
it does make some nudges which are based on opinions on effective ways
development should proceed on new data science projects. Some of the tools here
could be replaced with other tools.  Poetry is not necessary; DVC is not
necessary; etc.  But a good workflow is likely to incorporate tooling and
processes that offer similar functionality.

The tooling in this template is designed to address the most important issues
in a data science workflow:
- Data versioning (we use DVC)
- Experiment management (we use DVC)
- Dependency and virtual environment management (we use Poetry)

Subordinate to the above main focuses is to have the template encourage testing
and simple but effective continuous integration practices. Here we use pytest, some
static analysis tools such as flake8 and mypy, nox, and Github Actions.

Some sources of inspiration for compiling this:
- Personal experience
- [Hypermodern python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/).
  There actually is a [cookiecutter hypermodern
  python](https://github.com/cjolowicz/cookiecutter-hypermodern-python)
  template already, but we opt to create our own that is more data science
  focused. In particular data versioning and experiment management is not
  handled in that template, but there is a lot more other tooling going on.  The
  main distinction here is that this template is:
    1. More lightweight than the cookiecutter hypermodern
       python template.
    2. Includes some DVC-related files to encourage lean towards data
       versioning and rigorous experiment management.

The remainder of this document steps through typical usage of this template and
where appropriate offers some guidance on the use of the relevant tools.

The following instructions in this README assume you have already instantiated
a repo from this template using:
```
pip install cookiecutter # This can be in any environment
cookiecutter {{cookiecutter.repo_name}}
```
Note that cookiecutter can be installed in any environment. We'll be using
poetry to create a project-specific environment once the repository is set up.

## Dependency and virtual environment management with Poetry

The top level directory contains a `pyproject.toml` file. This adheres to PEP
517 and 518. This can be used by a tool such as Poetry to manage a virtual
environment and its dependencies. I encourage the use of Poetry or some other
comparable tool instead of adhoc management of a `requirements.txt` file.
`requirements.txt` files has the crucial shortcoming that they track only the state
of installed packages, not the dependencies between packages. As a result,
conflicts between dependencies can lead the programmer into a confusing and
sorry state of affairs. Furthermore, since the requirements.txt contains the
state of all installed packages, there is limited human interpretability: which
of those packages is a direct dependency of the code, and which are merely
dependencies of dependencies?

[Install Poetry](https://python-poetry.org/docs/#installation). Then install the projects `src/` package with:
```
poetry install
```

Poetry creates a virtual environment for you. Subsequent commands can be run in
the virtual environment by calling
```
poetry shell
```

Packages can be added to the virtual environment using
```
poetry add <package>
```

See [Poetry documentation](https://python-poetry.org/docs/) for more
information.

It is worth noting that the default `pyproject.toml` in this template includes a
number of development dependencies. These are not dependencies of the code
itself, but aid in the development of the package itself. You may want to
update some of the included dev dependencies with `poetry update` since there
may be newer versions available.

## Data Versioning (with DVC)

Beyond using a git repository to track code changes, the
next most important component of machine learning reproducibility is to track
changes to the data. A typical workflow on our projects starts by
receiving some small amount of data from a client with which we begin
exploring and experimenting. Along the way we might refine labels or add them if they
weren't there to begin with. After this initial iteration we then might be
given more data from the client or we might hunt down our own in order to fill
in gaps in the representation of the training data. This process will repeat
and along the way we will be experimenting and gathering results. It is
essential to be able to keep track of the changes to all this data so that the
context that gave rise to a trained model can be reproduced.

There are a number of young tools for the job here. One solid option that
builds on top of git is [DVC](https://dvc.org/). The protocol that this project
template advocates for is to put all raw data in `data/raw/` and `dvc add` it
before `git commit`ing.  Any manual modifications made to the data should happen
to data in `data/raw/` and it should be `dvc add`ed and `git commit`ed again.
Any automated manipulations of the data as part of preprocessing should output
the final product in `data/processed`. The scripts to do this should be in
`src/data/` (for example `src/data/preprocess.py`). The command used to produce
that processed data should be in the `dvc.yaml` file in the root directory.
(Note: the template `dvc.yaml` file in this template offers some degree of
support for incremental processing, whereby adding a single file to `data/raw`
should result in additional preprocessing only for that file, and not
re-running the whole pipeline. It just requires the list of files in
`data/raw/` to be captured in a YAML list in `params.yaml`. If the number of
these files is too great to manually be managed this could be automated with a
script that writes the contents of `data/raw/` to `params.yaml`, but we leave
that to future work.)

In this case any change, however small, in the `data/raw` directory would
trigger re-running of the data pipeline. An alternative would be to store a
variable with a list of files in `data/raw/` and reference that variable in the
dependencies in that stage in the `dvc.yaml` file. But that is beyond the scope
of this README.md.

## Experiment management (with DVC)

For effective experiment management in DVC there are two main requirements
beyond keeping track of the data:
  1. Keeping track of model hyperparameters that were used in training the
     model
  2. Keeping track of the quantitative performance of the model.

Here is a very brief overview:
- Model hyperparameters should be stored in `params.yaml`. The included
  `params.yaml` file in this template shows some example parameters.
- The training script should output a `metrics.json` file containing any
    metrics we want to track.
- The `dvc.yaml` file should include a training stage that references these
    parameters and the output metrics.json file. See the template's example
    `dvc.yaml` file as a starting point.

Using `dvc exp run` training experiments can be run and the results tracked. No
explicit git committing is required; each experiment will be associated with
its own git ref, so you don't need to make a bunch of different branches for
different experiments. You can simply change the parameter and run `dvc exp
run` and it will be all tracked. There exists various functionality to do
things such as visually compare experimental runs and convert an experiment
into a new branch. See the
[docs](https://dvc.org/doc/user-guide/experiment-management) for more info.

## Testing

Testing is good software engineering practice and can help catch bugs and
prevent the introduction of new ones.

### pytest

`tests/` is a directory that can be used to house tests written for pytest. A
practice I have found useful is to follow a loose interpretation of test-driven
development. In this approach it is not that unit tests are all
written before the program code, but that when _running_ the code a pytest test
case is used. This frees the programmer up to write code before tests, but
provides sufficient lean to create tests when wanting to run code. After being
created - even if all the test case does is run a script's `main()` function -
these tests can be incrementally refined and their mere existence gives some
mental inertia to encourage writing proper tests. The underlying philosophy is
that it is better to have some sort of habit of creating imperfect test cases
rather than none at all because true test-driven development was too much of a
mental hurdle to overcome.

### nox

[Nox](https://nox.thea.codes/en/stable/) is a tool for automating testing. The
`noxfile.py` that we have as default in this project template runs tests found
in `tests/` (reporting code coverage of those tests along the way) and
additionally runs the static analysis tools `flake8` and `mypy`. It's good to
run nox periodically though there is no enforcement to do it each commit via a
pre-commit hook (the tests would slow things down and discourage
small commits). A better place to run this is based on judgment after some
substantial change has been made, or before merging feature branches into a
main branch.

## Pre-commit hooks

`.pre-commit-config.yaml` includes some pre-commit hooks to use. `poetry run
pre-commit install` to use them. They are mostly style checks. Decisions should
be made about what makes it into a pre-commit hook versus what is left simply
for IDEs to check versus what gets checked by Github Actions before merging
into the trunk.

## CI Tests with Github Actions

Github Actions can automatically spin up tests when commits are pushed to a
Github remote. `.github/workflow/tests.yaml` is the configuration file for
this. It used nox to run what is in `noxfile.py` when commits are pushed. nox
will run all the pytest test cases that aren't marked with the
`@pytest.mark.slow` decorator. Slow test cases that shouldn't be run when each
commit is pushed should receive this mark.


## The resulting directory structure

The directory structure of your new project looks like this: 

```
├── LICENSE
├── Makefile           <- Makefile with commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default Sphinx project; see sphinx-doc.org for details
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
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
└── src                <- Source code for use in this project.
    ├── __init__.py    <- Makes src a Python module
    │
    ├── data           <- Scripts to download or generate data
    │   └── make_dataset.py
    │
    ├── features       <- Scripts to turn raw data into features for modeling
    │   └── build_features.py
    │
    ├── models         <- Scripts to train models and then use trained models to make
    │   │                 predictions
    │   ├── predict_model.py
    │   └── train_model.py
    │
    └── visualization  <- Scripts to create exploratory and results oriented visualizations
        └── visualize.py
 ```
