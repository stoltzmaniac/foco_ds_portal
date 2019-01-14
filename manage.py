# manage.py


import unittest
import os

import coverage

from flask.cli import FlaskGroup

from project.server import create_app, db
from project.server.models import User
import subprocess
import sys

app = create_app()
cli = FlaskGroup(create_app=create_app)

# code coverage
COV = coverage.coverage(
    branch=True,
    include="project/*",
    omit=[
        "project/tests/*",
        "project/server/config.py",
        "project/server/*/__init__.py",
    ],
)
COV.start()


@cli.command()
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@cli.command()
def create_admin():
    """Creates the admin user."""
    db.session.add(User(username='happyad123', email="happyad123@happyad.com", password="happyad321", admin=True))
    db.session.commit()


@cli.command()
def create_data():
    """Creates sample data."""
    pass


@cli.command()
def test():
    """Runs the pytest without test coverage."""
    import pytest
    rv = pytest.main(["project/tests_pytest", "--verbose"])
    exit(rv)


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    import pytest
    rv = pytest.main(["project/tests_pytest", "--cov"])
    exit(rv)


@cli.command()
def flake():
    """Runs flake8 on the project."""
    subprocess.run(["flake8", "project"])


if __name__ == "__main__":
    cli()
