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

### Pandas to process the data
#### pandas process data for schemaless csv files

### Ingest Data into Postgres
sqlalchemy psycopg2-binary

```python
from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
```





