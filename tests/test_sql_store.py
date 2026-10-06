"""The one test that really talks to Postgres.

Everything else uses the fake store. This proves the SQL works:
the row goes in, comes back with the database-generated created_at,
and an unknown id returns None.

The db_session fixture rolls back at the end, so nothing is left behind.
"""

import pytest

from docuquery.api import DocumentIn, SqlStore


@pytest.mark.db
def test_sql_store_roundtrip(db_session):
    store = SqlStore(db_session)

    created = store.add(DocumentIn(title="Real", body="in postgres"))

    assert created.id
    assert created.title == "Real"
    assert created.created_at is not None  # filled in by the database, not by Python

    fetched = store.get(created.id)
    assert fetched is not None
    assert fetched.title == "Real"

    assert store.get("no-such-id") is None
