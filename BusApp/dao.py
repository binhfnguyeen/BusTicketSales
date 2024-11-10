from flask import Flask, render_template, request
import os
import json
import hashlib
from BusApp import main
from BusApp.models import KhachHang, NhanVien
import BusApp


def read_user():
    with open(os.path.join(BusApp.app.root_path, "./data/user.json"), encoding="utf-8") as f:
        return json.load(f)

def write_user(data):
    with open(os.path.join(BusApp.app.root_path, "./data/user.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def validate_user(username=None, password=None):
    users = read_user()  # Đảm bảo rằng read_user() không trả về None
    password_hash = hashlib.md5(password.strip().encode("utf-8")).hexdigest()  # Sửa cách gọi hexdigest
    for user in users:
        if user["username"].strip() == username.strip() and user["password"] == password_hash:
            return user
    return None


def load_customers():
    page = request.args.get('page', 1, type=int)
    return KhachHang.query.paginate(page=page, per_page=6)

def total_customers():
    return KhachHang.query.count()

def load_employees():
    page = request.args.get('page', 1, type=int)
    return NhanVien.query.paginate(page=page, per_page=6)

def total_employees():
    return NhanVien.query.count()
