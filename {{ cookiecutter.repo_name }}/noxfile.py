# noxfile.py
import nox


@nox.session(python=["{{ cookiecutter.min_python_version }}"])
def tests(session):
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", "--no-dev", external=True)
    session.run("pytest", *args)

LOCATIONS = "src", "tests", "noxfile.py"

@nox.session(python=["3.8", "3.7"])
def lint(session):
    args = session.posargs or LOCATIONS
    session.install("flake8")
    session.run("flake8", *args)
