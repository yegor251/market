import os
import json
from pathlib import Path


def manage_session(username, action="create", data=None):
    sessions_dir = Path(__file__).parent.parent / "sessions"
    file_path = sessions_dir / f"{username}.json"

    if action == "create" or action == "update":
        if data is None:
            data = create_session()
        sessions_dir.mkdir(exist_ok=True)
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    elif action == "read":
        if not file_path.exists():
            raise FileNotFoundError(f"No session file found for {username}")
        with open(file_path, "r") as file:
            return json.load(file)


def create_session():
    items_file = Path(__file__).parent.parent / "resources" / "items.json"

    items_data = {}
    if items_file.exists():
        with open(items_file, "r") as file:
            items_data = json.load(file)

    return {
        "money": 0,
        "bonus_timestamp": 0,
        "items": items_data
    }