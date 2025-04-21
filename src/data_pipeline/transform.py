import json

def transform_tracks(raw_data):
    return raw_data["items"]

def transform_users(raw_data):
    return raw_data["items"]

def transform_listen_history(raw_data):
    history = []
    for row in raw_data["items"]:
        for track_id in row["items"]:
            history.append({
                "user_id": row["user_id"],
                "track_id": track_id,
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            })
    return history