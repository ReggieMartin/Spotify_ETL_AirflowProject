import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime as dt
import datetime
import sqlite3

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
USER_ID = "KetoKult"
TOKEN = "BQDVRa8LJzh038UcsgTyhWlqFPwYhAm9HobABc-VPhhyTc7Zk3CRNWTiadlqaGhDg1jj_8a-ISSC0KDQhBKLgR7rYL22D3xxE6WolUSM9UNFqW7TQ9oOjZI98EvChPibTnDck9KGEBMt_nKX0ReVjMq2d3FW4X2-kayX"

def is_data_valid(df):
    if df.empty:
        print("No songs found for this period.")
        return False
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Error: Duplicate Primary Key value")
    if df.isnull().values.any():
        raise Exception("Null value(s) found")
    """
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    timestamps = df["timestamp"].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, "%Y-%m-%d") != yesterday:
            raise Exception("Error: Found song(s) which didnt come from the last 24 hours")
    """
    return True


if __name__ == "__main__":
    headers = {
        "Accept" : "application/json",
        "Content-Type": "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }

    today = dt.now() #datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=10)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers=headers)

    data = r.json()

    song_names, artist_names, played_at_list, timestamps = [], [], [], []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps
    }

    song_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"])
    #print(data)
    print(song_df)
    
    if is_data_valid(song_df):
        print("Received data is valid.")

    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    create_query = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    cursor.execute(create_query)
    print("Database opened...")

    try:
        song_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except:
        print("Data already inside databse when attempting to add via to_sql method.")

    conn.close()
    print("Connection closed.")