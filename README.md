# Spotify_ETL_AirflowProject
Extracts recently played songs via Spotify API and transforms the data to place it in a SQLite database one a day via Airflow scheduler

INSTRUCTIONS:
-Place spotify_dag.py in your dags folder ("export AIRFLOW_HOME=~/airflow" or wherever you installed airflow)
-"airflow db init"
-"airflow users create --username person --firstname Xxxx --Lastname Yyyy --role Admin --email z@example.com --password pass"
-"airflow webserver --port 8080"
-"airflow scheduler" (in a separate terminal)
