# DocuQuery — learning log

One line per day: what I did, what broke.

| Day | Date | Done | Broke / learned |
|---|---|---|---|
| 1 | 2026-09-19 | 5 scratch scripts: file I/O + `with`, comprehensions, dataclass, JSON + KeyError, httpx + raise_for_status | Forgot to save files, so scripts ran empty. Type hints are labels, not checks. Missing key raises KeyError (PHP gives null). |
| 2 | 2026-09-26 | Pydantic: Invoice + LineItem models, field validator (qty), model validator (total), 5 pytest tests passing | Validator written outside the class was silently ignored. `python` vs `uv run python`. Empty tests report green. |
| 3 | 2026-09-28 | scratch/08_async_fetch.py: sequential vs asyncio.gather vs blocking sleep vs asyncio.to_thread, all timed | Benchmark over httpbin was too noisy to show the to_thread win; isolating it gave 10.04s vs 1.01s. |
| 4 | 2026-10-04 | FastAPI app: /health, POST+GET /documents, HTTPException 404, InMemoryStore via Depends, 5 TestClient tests | `=` vs `==` chained assignment -> TypeError; added httpx2 (dev) to clear the Starlette warning. |
| 5 | 2026-10-04 | Multi-stage Dockerfile (non-root, 275MB), compose with Postgres 16, CI workflow (ruff + pytest), README, .env ignored | README.md missing inside the image; YAML indent errors twice; B008 false positive -> Annotated; .env was not git-ignored. |
