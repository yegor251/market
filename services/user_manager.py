from datetime import datetime, timedelta
from .session_manager import manage_session

class UserManager:
    def __init__(self):
        self.users = {}

    def get_current_time(self):
        return datetime.now()

    def can_gen_bonus(self, username: str):
        session = self.users[username]
        current_time = self.get_current_time()
        if current_time - datetime.fromtimestamp(session["bonus_timestamp"]) >= timedelta(minutes=1):
            return True, 0
        time_left = (datetime.fromtimestamp(session["bonus_timestamp"]) - current_time + timedelta(minutes=1)).total_seconds()
        return False, int(time_left)

    def read_user(self, username: str):
        self.users[username] = manage_session(username, "read")
        return self.users[username]

    def get_user(self, username: str):
        return self.users[username]

    def get_bonus(self, username: str, money: int):
        self.users[username]["money"] += money
        self.users[username]["bonus_timestamp"] = int(self.get_current_time().timestamp())

    def get_balance(self, username: str):
        session = self.users[username]
        return session["money"]

    def save_user(self, username: str):
        session = self.users[username]
        del self.users[username]
        manage_session(username, "update", session)

    def buy_item(self, item_id, username: str):
        session = self.users[username]
        if item_id not in session["items"]:
            return False
        if session["items"][item_id]["status"] == 1:
            return False
        if session["items"][item_id]["price"] <= session["money"]:
            session["money"] -= session["items"][item_id]["price"]
            session["items"][item_id]["status"] = 1
            return True
        return False

user_manager = UserManager()