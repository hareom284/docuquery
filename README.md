# DocuQuery

RAG over a codebase and its docs, with citations and an eval table. Work in progress — built in public while following a 90-day AI-engineer plan.

**Stack:** Python 3.12 · FastAPI · Pydantic v2 · Postgres 16 · Docker · GitHub Actions

## Status

| Day | Shipped |
|---|---|
| 1–3 | Python idioms, Pydantic models + validators, async benchmark (10 HTTP calls: 25.4s sequential → 4.2s with `asyncio.gather`) |
| 4 | FastAPI: `/health`, `POST /documents`, `GET /documents/{id}` with 404, dependency-injected store, 10 tests |
| 5 | Multi-stage Dockerfile (non-root, 275MB), compose with Postgres 16, CI running ruff + pytest |

Next: Postgres persistence and SSE streaming, then the retrieval pipeline.

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
