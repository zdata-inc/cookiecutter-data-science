import nox


@nox.session(python=["{{ cookiecutter.min_python_version }}"])
def tests(session):
    args = session.posargs or ["--cov=src", "-m", '"not slow"']
    session.run("poetry", "install", "--no-dev", external=True)
    session.run("pytest", *args, external=True)


@nox.session(python=["{{ cookiecutter.min_python_version }}"])
def lint(session):
    args = session.posargs or ['src', 'tests', 'noxfile.py']
    session.run("flake8", *args, external=True)
    session.run('mypy', 'src', external=True)
