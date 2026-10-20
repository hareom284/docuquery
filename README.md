# DocuQuery

RAG over a codebase and its docs, with citations and an eval table. Work in progress — built in public while following a 90-day AI-engineer plan.

**Stack:** Python 3.12 · FastAPI · Pydantic v2 · SQLAlchemy 2.0 + Alembic · Postgres 16 · Docker · GitHub Actions

## Status

| Day | Shipped |
|---|---|
| 1–3 | Python idioms, Pydantic models + validators, async benchmark (10 HTTP calls: 25.4s sequential → 4.2s with `asyncio.gather`) |
| 4 | FastAPI: `/health`, `POST /documents`, `GET /documents/{id}` with 404, dependency-injected store, 10 tests |
| 5 | Multi-stage Dockerfile (non-root, 275MB), compose with Postgres 16, CI running ruff + pytest |
| 6 | Postgres persistence (session-per-request), first Alembic migration, `GET /stream` over SSE, fake-store + rollback test fixtures |

Next: the retrieval pipeline — embeddings, pgvector, hybrid search, citations and evals.

## API

| Endpoint | Does |
|---|---|
| `GET /health` | liveness check |
| `POST /documents` | create a document — 201, or 422 when the body does not match the schema |
| `GET /documents/{id}` | fetch one — 404 when it does not exist |
| `GET /stream` | every document as server-sent events, one message at a time |

## Database

```bash
docker compose up -d db          # Postgres 16
uv run alembic upgrade head      # apply migrations
uv run alembic current           # which revision is applied
```

## Run it

```bash
# with Docker (API + Postgres)
docker compose up --build
curl http://localhost:8000/health        # {"status":"ok"}

# or locally
uv sync
uv run uvicorn docuquery.api:app --reload
```

Interactive API docs: <http://localhost:8000/docs>

## Develop

```bash
uv run pytest -q         # tests
uv run ruff check .      # lint — the same two commands CI runs
```

Copy `.env.example` to `.env` for local configuration. `.env` is git-ignored.
