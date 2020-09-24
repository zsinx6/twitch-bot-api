import os

import pytest
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from pytest_postgresql.factories import DatabaseJanitor

from bot_api import create_app

DB_CONN = os.environ.get("TEST_SQLALCHEMY_DATABASE_URI")
DB_OPTS = sa.engine.url.make_url(DB_CONN).translate_connect_args()

pytest_plugins = ["pytest-flask-sqlalchemy"]


@pytest.fixture(scope="session")
def database(request):
    """
    Create a Postgres database for the tests, and drop it when the tests are done.
    """
    pg_host = DB_OPTS.get("host")
    pg_port = DB_OPTS.get("port")
    pg_user = DB_OPTS.get("username")
    pg_db = DB_OPTS["database"]
    janitor = DatabaseJanitor(pg_user, pg_host, pg_port, pg_db, 12.4)
    janitor.init()

    @request.addfinalizer
    def drop_database():
        janitor.drop()


@pytest.fixture(scope="session")
def app(database):
    """
    Create a Flask app context for the tests.
    """
    app = create_app()

    app.config["SQLALCHEMY_DATABASE_URI"] = DB_CONN

    return app


@pytest.fixture(scope="session")
def _db(app):
    """
    Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy
    database connection.
    """
    db = SQLAlchemy(app=app)

    return db
