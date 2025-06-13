# Stage 1: Build with uv and dependencies installed
FROM ghcr.io/astral-sh/uv:python3.10-alpine AS uv

WORKDIR /app

# Enable bytecode compilation and copy mode
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy pyproject.toml and README.md to generate uv.lock
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=README.md,target=README.md \
    uv lock

# Copy all source files
ADD . .

# Install dependencies from lockfile with caching
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project --no-dev --no-editable

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-dev --no-editable

# Cleanup .venv caches to reduce size
RUN find /app/.venv -name '__pycache__' -type d -exec rm -rf {} + && \
    find /app/.venv -name '*.pyc' -delete && \
    find /app/.venv -name '*.pyo' -delete && \
    echo "Cleaned up .venv"

# Stage 2: Runtime image with minimal Alpine and non-root user
FROM python:3.10-alpine

# Create non-root user 'appuser'
RUN adduser -D -h /home/appuser -s /bin/sh appuser

WORKDIR /app
USER appuser

# Copy virtual environment and source from builder stage
COPY --from=uv --chown=appuser:appuser /app/.venv /app/.venv
COPY --from=uv --chown=appuser:appuser /app /app

# Ensure virtualenv executables are in PATH
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

# Expose MCP server port (adjust if needed)
EXPOSE 8080

# Run your MCP server main module
CMD ["python", "main.py"]
