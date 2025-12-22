### Python Environment Management with uv

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


### Postgres
```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \ 
  # mounts a named Docker volume to persist Postgres data across container restarts.
  -p 5432:5432 \ 
  # port mapping
  postgres:18
```

#### host access to postgres
uv add pgcli
uv run pgcli -h localhost -p 5432 -U root -d ny_taxi

#### Docker networking reminder (common gotcha)
- When `ingest_data.py` runs **inside a container**, `localhost` means **that container**, not your Mac and not the Postgres container.
- On Docker Desktop for **Mac**, use `host.docker.internal` to reach services published on your Mac (e.g. `-p 5432:5432`).

Example (ingest container -> Postgres via Mac published port):
```bash
docker run --rm taxi_ingest:v001 \
  --pg-host host.docker.internal \
  --pg-port 5432
```

Alternative (container-to-container via user-defined network + DNS):
```bash
docker network create pg-network

docker run -it --rm \
  --name pgdatabase \
  --network pg-network \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgressql/ \
  -p 5432:5432 \
  postgres:18

docker build -t taxi_ingest:v001 .

docker run -it --rm \
  --network pg-network \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips_2021_2 \
    --year=2021 \
    --month=2 \
    --chunksize=100000

uv run pgcli -h localhost -p 5432 -U root -d ny_taxi

docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

### Pandas to process the data
#### pandas process data for schemaless csv files

### Ingest Data into Postgres
sqlalchemy psycopg2-binary

```python
from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
```



