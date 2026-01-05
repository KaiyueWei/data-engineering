## Architecture

![Architecture](static/architecture.jpg)

## Workflow

1) Build the ingest image:
```bash
docker build -t taxi_ingest:v001 .
```

2) Start Postgres + pgAdmin:
```bash
docker compose up -d pgdatabase pgadmin
```

3) Run ingest (one-off job):
```bash
docker compose --profile ingest run --rm ingest
```

4) Connect from host:
```bash
uv run pgcli -h localhost -p 5432 -U root -d ny_taxi
```

5) Open pgAdmin: `http://localhost:8085` (login: `admin@admin.com` / `root`)

6) Shut down:
```bash
docker compose down
```
Data persists in Docker volumes; use `docker compose down -v` to delete volumes.

## Notes
- In Docker, `localhost` inside a container is the container itself; use a Docker network hostname (e.g. `pgdatabase`) or `host.docker.internal` (Docker Desktop on Mac/Windows) when connecting to services outside the container.
- Postgres 18+: mount the volume at `/var/lib/postgresql` (not `/var/lib/postgresql/data`).

## Python Environment Management with uv

### initialize a project
```bash
uv init --python 3.13
```

```bash
uv run python -V
Python 3.13.11
uv run which python
./.venv/bin/python
```

### add dependencies
```bash
uv add pandas pyarrow
```
we can check the dependecies in `./pyproject.toml`

### create Docker image with Dockerfile
```bash
docker build -t dataengineering:dev .
docker run --rm dataengineering:dev
```

### Pandas to process the data
#### pandas process data for schemaless csv files

### Ingest Data into Postgres
sqlalchemy psycopg2-binary

```python
from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
```


# Airflow Docker Setup

