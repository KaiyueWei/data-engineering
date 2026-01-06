from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import pandas as pd

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"


def ingest_green_taxi(execution_date, **context):
    year = execution_date.year
    month = f"{execution_date.month:02d}"

    filename = f"green_tripdata_{year}-{month}.parquet"
    url = f"{BASE_URL}/{year}/{filename}"

    print(f"Downloading {url}")
    df = pd.read_parquet(url)

    pg_hook = PostgresHook(postgres_conn_id="postgres_ny_taxi")
    engine = pg_hook.get_sqlalchemy_engine()

    df.to_sql(
        name="green_tripdata",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=100_000,
        method="multi",
    )

    print(f"Loaded {len(df)} rows")


with DAG(
    dag_id="nyc_green_taxi_to_postgres",
    start_date=datetime(2019, 1, 1),
    schedule_interval="0 9 * * *",
    catchup=True,
    tags=["airflow", "postgres", "nyc-tlc"],
) as dag:

    ingest = PythonOperator(
        task_id="ingest_green_taxi",
        python_callable=ingest_green_taxi,
    )