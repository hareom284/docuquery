"""Day 4 — FastAPI core.

TASK — build a tiny API with four pieces:

  1. GET  /health              -> {"status": "ok"}
  2. POST /documents           -> takes a DocumentIn body, returns DocumentOut (201)
  3. GET  /documents/{doc_id}  -> returns DocumentOut, or 404 via HTTPException
  4. an in-memory store injected with Depends()

LARAVEL MAP
  @app.get("/x")          ~ Route::get('/x', ...)
  DocumentIn body         ~ a FormRequest: FastAPI validates it with Pydantic first
  response_model=         ~ an API Resource: decides what goes OUT
  Depends(get_store)      ~ the service container: FastAPI builds it and hands it in
  HTTPException(404)      ~ abort(404)

WHAT TO NOTICE
  You never write validation code in the endpoint. If the body is wrong,
  FastAPI answers 422 with the Pydantic errors before your function runs.

DONE WHEN
  uv run uvicorn docuquery.api:app --reload
  ...then open http://127.0.0.1:8000/docs and try all three endpoints.

Run the tests with:  uv run pytest -q
"""

from datetime import UTC, datetime
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="DocuQuery", version="0.1.0")


# ---------------------------------------------------------------- models
class DocumentIn(BaseModel):
    """What the client is allowed to send."""

    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1)


class DocumentOut(DocumentIn):
    """What we send back: the input plus the fields the server owns."""

    id: str
    created_at: datetime


# ---------------------------------------------------------------- store
class InMemoryStore:
    """Stands in for a database until Day 6."""

    def __init__(self) -> None:
        self._documents: dict[str, DocumentOut] = {}

    def add(self, document: DocumentIn) -> DocumentOut:
        # TODO: build a DocumentOut with a new id (str(uuid4())) and
        #       created_at=datetime.now(timezone.utc), save it in self._documents,
        #       and return it.
        created_at = datetime.now(UTC)
        doc_id = str(uuid4())
        document_out = DocumentOut(id=doc_id, created_at=created_at, **document.model_dump())
        self._documents[doc_id] = document_out
        return document_out

    def get(self, doc_id: str) -> DocumentOut | None:
        # TODO: return the document, or None when the id is unknown.
        #       Remember Day 1: d[key] raises KeyError, d.get(key) returns None.
        return self._documents.get(doc_id)


_store = InMemoryStore()


def get_store() -> InMemoryStore:
    """The dependency. Tests swap this out with app.dependency_overrides."""
    return _store


# ---------------------------------------------------------------- routes
@app.get("/health")
def health() -> dict[str, str]:
    # TODO: return {"status": "ok"}
    return {"status": "ok"}


@app.post("/documents", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
def create_document(payload: DocumentIn, store: InMemoryStore = Depends(get_store)) -> DocumentOut:
    # TODO: return store.add(payload)
    return store.add(payload)


@app.get("/documents/{doc_id}", response_model=DocumentOut)
def read_document(doc_id: str, store: InMemoryStore = Depends(get_store)) -> DocumentOut:
    # TODO: document = store.get(doc_id)
    document = store.get(doc_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document
