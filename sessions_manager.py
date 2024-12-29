import os
import json

def manage_session(username, action="create", data=None):
    file_path = os.path.join(os.getcwd(), "sessions", f"{username}.json")

    if action == "create" or action == "update":
        if data is None:
            data = create_session()
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    elif action == "read":
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No session file found for {username}")
        with open(file_path, "r") as file:
            return json.load(file)


def create_session():
    items_file_path = os.path.join(os.getcwd(), "resources", "items.json")

    if os.path.exists(items_file_path):
        with open(items_file_path, "r") as file:
            items_data = json.load(file)
    else:
        items_data = {}

    session = {
        "money": 0,
        "bonus_timestamp": 0,
        "items": items_data
    }
    return session


