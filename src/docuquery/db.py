"""Day 6 — engine and session-per-request.

THE SHAPE
  engine   = the connection pool. ONE for the whole app, created at import.
  Session  = one unit of work. ONE PER REQUEST, opened and closed by the dependency.

Mixing those up is the classic bug: a session shared between requests leaks one
user's uncommitted data into another's.

LARAVEL MAP
  get_session()  ~ the DB connection resolved per request out of the container.
  The `yield` is why it closes cleanly — see below.

TASK
  Fill in TODO 1 and TODO 2.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from docuquery.settings import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_session() -> Generator[Session, None, None]:
    """A dependency that hands out one Session and always closes it.

    `yield` makes this a generator dependency: FastAPI runs the code up to the
    yield before the endpoint, hands over the session, then runs the `finally`
    after the response is sent — exactly the `with` guarantee from Day 1.
    """
    # TODO 1: open a session, yield it, and close it in a finally block
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
    # rais  e NotImplementedError
