# Day 5 — multi-stage image.
#
# STAGE 1 "builder" installs dependencies into /app/.venv
# STAGE 2 "runtime" copies only that .venv plus the source — no uv, no build tools,
#         no cache. Smaller image, smaller attack surface.
#
# THE CACHING RULE
#   Copy pyproject.toml + uv.lock and install FIRST, then copy src/.
#   Editing a .py file then only invalidates the last layers, not the install.
#
# Build and run:
#   docker build -t docuquery .
#   docker run --rm -p 8000:8000 docuquery
#   curl http://localhost:8000/health

# ---------------------------------------------------------------- stage 1
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# TODO 1: copy ONLY the dependency files first (this is the caching rule)
    COPY pyproject.toml uv.lock README.md ./


# TODO 2: install dependencies, no dev group, without installing the project itself yet
  RUN uv sync --locked --no-dev --no-install-project

# TODO 3: now copy the source, then sync again so the project itself is installed
   COPY src/ ./src/
   RUN uv sync --locked --no-dev

# ---------------------------------------------------------------- stage 2
FROM python:3.12-slim-bookworm AS runtime

# a non-root user: if the app is ever exploited, it is not root inside the container
RUN useradd --create-home --uid 1000 appuser

WORKDIR /app

# TODO 4: copy the built virtualenv and the source from the builder stage
   COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv
   COPY --from=builder --chown=appuser:appuser /app/src /app/src

# put the venv first on PATH so `uvicorn` resolves to ours
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

USER appuser

EXPOSE 8000

# 0.0.0.0, not 127.0.0.1 — inside a container, localhost means "this container only",
# so the port mapping would never reach it.
CMD ["uvicorn", "docuquery.api:app", "--host", "0.0.0.0", "--port", "8000"]
