import json
import hashlib
import os

class UserManager:

    def __init__(self):
        self.users = {}
        self.load_users()

    def login(self, username, password):
        user = self.users.get(username)
        if not user:
            return None
        if (
            user["password"]
            ==
            self.hash_password(password)
        ):
            return user["role"]
        return None
    
    def load_users(self):
        if not os.path.exists(
            "users.json"
        ):
            self.users = {
                "admin": {
                    "password": "1234",
                    "role": "Admin"
                }
            }
            self.save_users()
            return
        with open(
            "users.json",
            "r",
            encoding="utf-8"
        ) as f:
            self.users = json.load(f)
    
    def save_users(self):
        with open(
            "users.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                self.users,
                f,
                indent=4
            )
    
    def add_user(
        self,
        username,
        password,
        role
    ):
        if username in self.users:
            return False
        self.users[username] = {"password": self.hash_password(password),"role": role}
        self.save_users()
        return True
    
    def delete_user(
        self,
        username
    ):
        if username not in self.users:
            return False
        if username == "admin":
            return False
        del self.users[username]
        self.save_users()
        return True
    
    def change_password(
        self,
        username,
        new_password
    ):
        if username not in self.users:
            return False
        self.users[username]["password"] = (self.hash_password(new_password))
        self.save_users()
        return True
    
    def hash_password(self, password):
        return hashlib.sha256(
            password.encode()
        ).hexdigest()