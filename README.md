# A Cookiecutter Data Science Template With Data Versioning and Experiment Management

This project template is intended to be open-ended and flexible without
overprescribing decisions about how the project development should proceed and
hopefully without overwhelming the developer with excessive tooling.  However,
it does make some nudges which are based on opinions on effective ways
development should proceed on new data science projects. Some of the tools here
could be replaced with other tools. Poetry could be used instead of setuptools; DVC is not
necessary; etc.  But a good workflow is likely to incorporate tooling and
processes that offer similar functionality.

The tooling in this template is designed to address the most important issues
in a data science workflow:
- Data versioning (DVC)
- Experiment management (DVC)
- Dependency and virtual environment management

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

The remainder of this document steps through typical usage of this template and,
where appropriate, offers some guidance on the use of the relevant tools.

The following instructions in this README assume you have already instantiated
a repo from this template using:
```
pip install cookiecutter # This can be in any environment
cookiecutter https://github.com/zdata-inc/cookiecutter-data-science
```
Note that cookiecutter can be installed in any environment.

## Modern dependency and virtual environment management with setuptools

The top level directory contains a `pyproject.toml` file. This adheres to PEP
517 and 518. This can be used by setuptools and other tools such as Poetry to manage a virtual
environment and its dependencies. I encourage the use of a `pyproject.toml` instead of adhoc management of a `requirements.txt` file.
`requirements.txt` files has the crucial shortcoming that they track only the state
of installed packages, not the dependencies between packages. As a result,
conflicts between dependencies can lead the programmer into a confusing and
sorry state of affairs. Furthermore, since the requirements.txt contains the
state of all installed packages, there is limited human interpretability: which
of those packages is a direct dependency of the code, and which are merely
dependencies of dependencies?

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
that processed data should be in the `dvc.yaml` file in the root directory. The `dvc.yaml` file
serves both as documentation of how the different scripts work together to make a data pipeline, and
also enables running `dvc repro` to run that pipeline.
(Note: In typical use any change, however small, in the `data/raw` directory would
trigger re-running of the data pipeline.  the template `dvc.yaml` file in this template offers some degree of
support for incremental processing, whereby adding a single file to `data/raw`
should result in additional preprocessing only for that file, and not
re-running the whole pipeline. It just requires the list of files in
`data/raw/` to be captured in a YAML list in `params.yaml`. If the number of
these files is too great to be managed manually then this could be automated with a
script that writes the contents of `data/raw/` to `params.yaml`, but we leave
that to future work.)

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

I will admit I've never had complete success using `DVC`s experiment management, but I haven't tried
too hard. One issue is managing the metrics file output. You actually need to code the metrics
output, and sometimes that might not be relevant (say if you're using AutoML) or the metric of
interest might be changing a lot. I don't think it's a huge issue, but I've often just defaulted
back to using a google sheet spreadsheet to track salient experiments: put the commit hash in one
column, quantitative metrics in another, and a plain text description in a comment field. For me
this has never been a show-stopper, but if hyperparameter tuning is extensive then it can start to
become unwieldly.

## Testing

Testing is good software engineering practice and can help catch bugs and
prevent the introduction of new ones. Testing is an art, and guidance on the actual engineering of
tests is beyond the scope of this README. That said, it's worth making some remarks about testing in
the context of the machine learning projects we tend to work on at zData, since that has an effect
on the nature of testing.

The objective of testing is to ensure software works as intended and is robust to a wide variety of
inputs. Tests can be categorized by the granularity or level of abstraction at which they operate.
At one end there are unit tests that test specific functions, and at the other end there are
end-to-end tests that test the whole softare system in entirety. Finding the right balance is
important (see [Grug on Testing](https://grugbrain.dev/#grug-on-testing)).

This can be difficult in machine learning, because running the actual learning code can be very
computationally demanding and not something that can be feasibly done on a commit hook or as part of
a continuous integration system. The good news though is that by its very nature, machine learning
projects involve a subsantial amount of implicit testing. A well-run machine learning project will
involve scoping diverse data inputs and doing substantial error analysis to understand fail modes of
the model. Along the way quantitative metrics of performance will be gathered. So in a certain
sense, simply adhering to good machine learning practices gives you a well tested model.

But there's a couple crucial details to get right:
1. The code that computes metrics must be correct.
2. Examples from the train set can't leak into validation or test.

To address (1), it's best to use existing off-the-shelf approaches to calculate metrics. Sometimes
this can't be done. For instance, we often use a multi-label version of seqeval which was developed
in-house. If making your own code for metrics, you must test it.

To address (2), it's not strictly necessary to use actual test functions, but there should be
liberal use of assertions in the code to ensure the train, validation and test sets are disjoint.

Beyond that, the value of testing is to ensure your code is actually doing what you want it to do.
For example, you might be reporting metrics correctly and have seen first hand how your model can do on
inputs not seen in training. However, you believed you were implementing architecture X when in fact you
implemented architecture Y. And maybe getting the archicture X implementation correct will give a
performance boost. To ensure you're getting your implementation correct, you should test.

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

`.pre-commit-config.yaml` includes some pre-commit hooks to use. They are
mostly style checks. Decisions should be made about what makes it into a
pre-commit hook versus what is left simply for IDEs to check versus what gets
checked by Github Actions before merging into the trunk.

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
├── pyproject.toml     <- Houses project metadata and dependencies. Used by
setuptools.
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
        │                 predictions
        ├── predict_model.py
        └── train_model.py
 ```
