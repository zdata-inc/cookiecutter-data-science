import nox


@nox.session(python=["3.10"])
def tests(session):
    args = session.posargs or ["--cov=src"]
    session.run("poetry", "install", "--no-dev", external=True)
    session.run("pytest", *args, external=True)


@nox.session(python=["3.10"])
def lint(session):
    args = session.posargs or ['src', 'tests', 'noxfile.py']
    session.run("flake8", *args, external=True)
