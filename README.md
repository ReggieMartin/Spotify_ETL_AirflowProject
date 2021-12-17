# Spotify_ETL_AirflowProject
Extracts recently played songs via Spotify API and transforms the data to place it in a SQLite database one a day via Airflow scheduler

INSTRUCTIONS: <br />
-Go to https://developer.spotify.com/console/get-recently-played/ and get a token for recently played songs.  <br />
-Paste the value into recent_songs.py (token ="") <br />
-Place spotify_dag.py in your dags folder ("export AIRFLOW_HOME=~/airflow" or wherever you installed airflow) <br />
-"airflow db init" <br />
-"airflow users create --username person --firstname Xxxx --Lastname Yyyy --role Admin --email z@example.com --password pass" <br />
-"airflow webserver --port 8080" <br />
-"airflow scheduler" (in a separate terminal) <br />
