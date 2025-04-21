import sqlite3
from pathlib import Path

def init_db(db_path="music_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS tracks (
        id INTEGER PRIMARY KEY,
        name TEXT, artist TEXT, songwriters TEXT,
        duration TEXT, genres TEXT, album TEXT,
        created_at TEXT, updated_at TEXT
    );

    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        first_name TEXT, last_name TEXT, email TEXT,
        gender TEXT, favorite_genres TEXT,
        created_at TEXT, updated_at TEXT
    );

    CREATE TABLE IF NOT EXISTS listen_history (
        user_id INTEGER,
        track_id INTEGER,
        created_at TEXT,
        updated_at TEXT
    );
    """)
    conn.commit()
    return conn

def load_to_db(tracks, users, listen_history, db_path="music_data.db"):
    conn = init_db(db_path)
    cursor = conn.cursor()

    cursor.executemany("""
    INSERT OR REPLACE INTO tracks VALUES (
        :id, :name, :artist, :songwriters,
        :duration, :genres, :album,
        :created_at, :updated_at
    )
    """, tracks)

    cursor.executemany("""
    INSERT OR REPLACE INTO users VALUES (
        :id, :first_name, :last_name, :email,
        :gender, :favorite_genres,
        :created_at, :updated_at
    )
    """, users)

    cursor.executemany("""
    INSERT INTO listen_history VALUES (
        :user_id, :track_id, :created_at, :updated_at
    )
    """, listen_history)

    conn.commit()
    conn.close()
