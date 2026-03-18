from airflow import DAG
from airflow.operators.python import PythonOperator # Simplified import for Airflow 3
from datetime import datetime, timedelta
import subprocess
import os

# Define the path to your virtual environment's python
VENV_PYTHON = "/home/latitude/internet-pulse-platform/venv/bin/python3"

def run_news_collector():
    # check=True will ensure the Airflow task fails if the script fails
    subprocess.run([VENV_PYTHON, "/home/latitude/internet-pulse-platform/data_ingestion/news_collector.py"], check=True)

def run_spark_processing():
    subprocess.run([VENV_PYTHON, "/home/latitude/internet-pulse-platform/spark_processing/process_news.py"], check=True)

with DAG(
    dag_id="news_pipeline",
    start_date=datetime(2026, 3, 14),
    schedule="@hourly",   # Changed to hourly
    catchup=False,
    max_active_runs=1,        # CRITICAL: Prevents 5-min runs from overlapping
    tags=["news", "spark"],
) as dag:

    task1 = PythonOperator(
        task_id="news_collector",
        python_callable=run_news_collector,
        retries=1,
        retry_delay=timedelta(seconds=30)
    )

    task2 = PythonOperator(
        task_id="spark_processing",
        python_callable=run_spark_processing
    )

    task1 >> task2