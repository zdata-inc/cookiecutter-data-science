import nox


@nox.session(python=["{{ cookiecutter.min_python_version }}"])
def tests(session):
    """Running tests."""
    args = session.posargs or ["--cov=src", "-m", "not slow"]
    session.run("pip", "install", ".[dev]")
    session.run("pytest", *args)


@nox.session(python=["{{ cookiecutter.min_python_version }}"])
def lint(session):
    """Linting."""
    args = session.posargs or ['src', 'tests', 'noxfile.py']
    session.run("pip", "install", ".[dev]")
    session.run("flake8", *args)
    session.run('mypy', '--install-types', '--non-interactive', 'src')
