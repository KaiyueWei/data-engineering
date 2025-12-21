# base image
FROM python:3.13-slim

# multi-stage: copy uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# copy dependency metadata first (layer caching)
COPY pyproject.toml uv.lock .python-version ./

# install dependencies using uv
RUN uv sync --locked --no-dev

# copy application code
COPY pipeline/ ./pipeline/

# set entrypoint
ENTRYPOINT ["python", "./pipeline/pipeline.py"]


