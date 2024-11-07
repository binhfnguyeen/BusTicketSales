from flask import Flask, render_template, request
import os
import json
import main
import hashlib
def read_user():
    with open(os.path.join(main.app.root_path, "./data/user.json"), encoding="utf-8") as f:
        return json.load(f)

def write_user(data):
    with open(os.path.join(main.app.root_path, "./data/user.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def validate_user(username=None, password=None):
    users = read_user()  # Đảm bảo rằng read_user() không trả về None
    password_hash = hashlib.md5(password.strip().encode("utf-8")).hexdigest()  # Sửa cách gọi hexdigest
    for user in users:
        if user["username"].strip() == username.strip() and user["password"] == password_hash:
            return user
    return None
