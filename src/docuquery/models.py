"""Day 6 — the Document table, SQLAlchemy 2.0 style.

LARAVEL MAP
  Base            ~ Eloquent's Model base class
  __tablename__   ~ protected $table
  Mapped[str]     ~ a typed column; SQLAlchemy reads the annotation like Pydantic does
  Base.metadata   ~ the schema Alembic compares against to generate migrations

NOTE
  This is the DATABASE model. DocumentIn/DocumentOut in api.py are the API models.
  Keeping them separate means a column rename does not silently change your API.

TASK
  Fill in the three TODO columns.
"""

from datetime import UTC, datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)

    # TODO 1: title — a String(200), NOT NULL
    title: Mapped[str] = mapped_column(String(200), nullable=False)

    # TODO 2: body — Text (no length limit), NOT NULL
    body: Mapped[str] = mapped_column(Text, nullable=False)

    # TODO 3: created_at — timezone-aware timestamp, NOT NULL,
    #         defaulted by the DATABASE so every row gets one even outside the app
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    def __repr__(self) -> str:  # handy in the shell and in test failures
        return f"Document(id={self.id!r}, title={self.title!r})"
