from flask import Flask, render_template, request
import os
import json
import hashlib
from BusTicketSales.BusApp import main
from BusTicketSales.BusApp.models import KhachHang, NhanVien, TuyenXe, Xe
from BusTicketSales import BusApp


def read_user():
    try:
        with open(os.path.join(BusApp.app.root_path, "./data/user.json"), encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict) and 'users' in data and isinstance(data['users'], list):
                return data['users']
            else:
                raise ValueError("The user data should be a list of dictionaries under the 'users' key")
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        raise ValueError("The user.json file is not a valid JSON format")

def write_user(data):
    with open(os.path.join(BusApp.app.root_path, "./data/user.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def validate_user(username=None, password=None):
    users = read_user()
    if not users:
        return None  # No users found or error reading users

    password_hash = hashlib.md5(password.strip().encode("utf-8")).hexdigest()
    for user in users:
        if user.get('username') == username and user.get('password') == password_hash:
            return user
    return None  # If no matching user is found

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

def load_tuyenXe():
    page = request.args.get('page', 1, type=int)
    return TuyenXe.query.paginate(page=page, per_page=6)

def total_tuyenXe():
    return TuyenXe.query.count()

def load_Xe():
    page = request.args.get('page', 1, type=int)
    return Xe.query.paginate(page=page, per_page=6)

def total_Xe():
    return Xe.query.count()