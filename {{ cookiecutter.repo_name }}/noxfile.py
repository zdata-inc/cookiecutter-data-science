import nox


@nox.session(python=["{{ cookiecutter.min_python_version }}"])
def tests(session):
    """Running tests."""
    args = session.posargs or ["--cov=src", "-m", "not slow"]
{% if cookiecutter.build_system == 'poetry' %}
    session.run("poetry", "install", "--no-dev", external=True)
    session.run("pytest", *args, external=True)
{% elif cookiecutter.build_system == 'setuptools' %}
    session.run("pip", "install", ".[dev]")
    session.run("pytest", *args){% endif %}


@nox.session(python=["{{ cookiecutter.min_python_version }}"])
def lint(session):
    """Linting."""
    args = session.posargs or ['src', 'tests', 'noxfile.py']
{% if cookiecutter.build_system == 'poetry' %}
    session.run("flake8", *args, external=True)
    session.run('mypy', 'src', external=True)
{% elif cookiecutter.build_system == 'setuptools' %}
    session.run("pip", "install", ".[dev]")
    session.run("flake8", *args)
    session.run('mypy', '--install-types', '--non-interactive', 'src'){% endif %}
