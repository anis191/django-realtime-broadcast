FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy uv
COPY --from=ghcr.io/astral-sh/uv:0.10.10 /uv /uvx /bin/

# Prevent python from writing .pyc files & enable logs immediately
ENV UV_PYTHON_PREFERENCE=only-system
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /django-broadcast

COPY pyproject.toml /django-broadcast/
COPY uv.lock /django-broadcast/

RUN uv sync --locked

# Copy project files
COPY . /django-broadcast/