from extract import fetch_all_data
from transform import (
    transform_tracks, transform_users, transform_listen_history
)
from load import load_to_db
import requests

BASE_URL = "http://localhost:8000"

def run_etl():
    print("Starting ETL...")

    data = fetch_all_data()
    tracks = transform_tracks(data['tracks'])
    users = transform_users(data["users"])
    history = transform_listen_history(data["listen_history"])

    load_to_db(tracks, users, history)

    print("✅ ETL complete!")

if __name__ == "__main__":
    run_etl()