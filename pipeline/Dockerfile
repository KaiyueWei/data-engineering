#base image
FROM python:3.13.10-slim

#multi-stage build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

#set working directory
WORKDIR /app

#add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

#copy dependency metadata first (layer caching)
COPY "pyproject.toml" "uv.lock" ".python-version" ./

#install dependencies using uv
RUN uv sync --locked

#copy application code
COPY pipepline.py pipepline.py

#set entrypoint
ENTRYPOINT [ "python", "pipeline.py" ]


