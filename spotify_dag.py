from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(0,0,0,0,0),
    'email': ['someone@fakeemail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'spotify_dag',
    default_args = default_args,
    description = 'Spotify recent songs ETL dag',
    schedule_interval = timedelta(days=1)
)

def test_function():
    print("***Test function***")

run_etl = PythonOperator(
    task_id = 'whole_spotify_etl',
    python_callable = test_function,
    dag = dag
)

run_etl