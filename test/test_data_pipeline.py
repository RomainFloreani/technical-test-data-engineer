import pytest
import sqlite3
from src.data_pipeline import extract, transform, load
from src.moovitamix_fastapi.classes_out import TracksOut, UsersOut, ListenHistoryOut
from datetime import datetime

# ---------------------------
# Transform Tests
# ---------------------------
@pytest.mark.unit
def test_transform_tracks():
    fake_track = TracksOut.generate_fake().dict()
    raw_tracks = {"items": [fake_track]}
    result = transform.transform_tracks(raw_tracks)

    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    assert result[0]["name"] == fake_track["name"]

@pytest.mark.unit
def test_transform_users():
    fake_user = UsersOut.generate_fake().dict()
    raw_users = {"items": [fake_user]}
    result = transform.transform_users(raw_users)

    assert isinstance(result, list)
    assert result[0]["email"] == fake_user["email"]

@pytest.mark.unit
def test_transform_listen_history():
    fake_history = ListenHistoryOut(
        user_id=1,
        items=[101, 102],
        created_at="2025-04-19T10:00:00",
        updated_at="2025-04-19T10:00:00"
    ).dict()
    raw_history = {"items": [fake_history]}
    result = transform.transform_listen_history(raw_history)

    assert isinstance(result, list)
    assert len(result) == 2  # One row per track_id
    assert result[0]["user_id"] == 1
    assert result[0]["track_id"] in [101, 102]

# ---------------------------
# Load Tests
# ---------------------------

@pytest.mark.unit
def test_load_creates_tables(tmp_path):
    db_path = tmp_path / "test_music.db"
    conn = load.init_db(str(db_path))
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in cursor.fetchall()}

    assert "tracks" in tables
    assert "users" in tables
    assert "listen_history" in tables

# ---------------------------
# Extract Tests with Mocking
# ---------------------------

@pytest.mark.api
def test_fake_extract(requests_mock):
    from src.data_pipeline.extract import BASE_URL, ENDPOINTS
    for ep in ENDPOINTS:
        requests_mock.get(f"{BASE_URL}/{ep}", json={"items": []}, status_code=200)

    from src.data_pipeline.extract import test_endpoints
    test_endpoints()


@pytest.mark.api
def test_tracks_extract(requests_mock):
    track = TracksOut.generate_fake().dict()
    track["created_at"] = track["created_at"].isoformat()
    track["updated_at"] = track["updated_at"].isoformat()
    requests_mock.get("http://localhost:8000/tracks", json={"items": [track]}, status_code=200)
    response = extract.requests.get("http://localhost:8000/tracks")
    assert response.status_code == 200
    assert response.json()["items"][0]["name"] == track["name"]

@pytest.mark.api
def test_users_extract(requests_mock):
    user = UsersOut.generate_fake().dict()
    user["created_at"] = user["created_at"].isoformat()
    user["updated_at"] = user["updated_at"].isoformat()
    requests_mock.get("http://localhost:8000/users", json={"items": [user]}, status_code=200)
    response = extract.requests.get("http://localhost:8000/users")
    assert response.status_code == 200
    assert response.json()["items"][0]["email"] == user["email"]

@pytest.mark.api
def test_listens_extract(requests_mock):
    history = ListenHistoryOut(user_id=1, items=[1, 2],created_at=datetime.now(),updated_at=datetime.now()).dict()
    history["created_at"] = history["created_at"].isoformat()
    history["updated_at"] = history["updated_at"].isoformat()
    requests_mock.get("http://localhost:8000/listen_history", json={"items": [history]}, status_code=200)
    response = extract.requests.get("http://localhost:8000/listen_history")
    assert response.status_code == 200
    assert response.json()["items"][0]["user_id"] == history["user_id"]