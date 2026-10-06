"""Shared test setup.

conftest.py is pytest's magic filename: anything defined here is available to
every test in this folder without importing it.

TWO KINDS OF TEST
  1. Default: the API tests get a FAKE store, so they need no database.
     Fast, isolated, and CI stays green without Postgres.
  2. Marked `@pytest.mark.db`: a real Session against real Postgres, wrapped in a
     transaction that is ROLLED BACK afterwards, so the database is left untouched.
     Skipped automatically when no database is reachable.
"""

import pytest
from sqlalchemy import text

from docuquery.api import InMemoryStore, app, get_store
from docuquery.db import SessionLocal, engine


@pytest.fixture(autouse=True)
def fake_store():
    """Every test gets a fresh in-memory store unless it asks for the real one.

    autouse=True means it applies without any test naming it.
    """
    store = InMemoryStore()
    app.dependency_overrides[get_store] = lambda: store
    yield store
    app.dependency_overrides.clear()


@pytest.fixture
def db_session():
    """A real Session inside a transaction that is always rolled back.

    The test sees its own writes; the database never keeps them.
    """
    try:
        connection = engine.connect()
    except Exception as exc:  # no Postgres running
        pytest.skip(f"database not reachable: {exc}")

    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()  # undo everything this test did
        connection.close()


def pytest_configure(config):
    config.addinivalue_line("markers", "db: test that needs a real database")


__all__ = ["fake_store", "db_session", "text"]
