from extract import test_endpoints
from transform import (
    transform_tracks, transform_users, transform_listen_history
)
from load import load_to_db
import requests

BASE_URL = "http://localhost:8000"

def run_etl():
    print("Starting ETL...")

    tracks_raw = requests.get(f"{BASE_URL}/tracks").json()
    users_raw = requests.get(f"{BASE_URL}/users").json()
    history_raw = requests.get(f"{BASE_URL}/listen_history").json()

    tracks = transform_tracks(tracks_raw)
    users = transform_users(users_raw)
    history = transform_listen_history(history_raw)

    load_to_db(tracks, users, history)

    print("✅ ETL complete!")

if __name__ == "__main__":
    run_etl()