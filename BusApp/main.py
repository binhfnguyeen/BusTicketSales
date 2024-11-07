from flask import Flask, render_template, request, redirect, url_for
from flask import Blueprint
import dao

login_blueprint = Blueprint("login", __name__)
app = Flask(__name__)

@login_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    err_msg = ""
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.validate_user(username=username, password=password)
        if user:
            return render_template("home.html")
        else:
            err_msg = "DANH NHAP THAT BAI"
    return render_template("dangnhap.html", err_msg=err_msg)

# @login_blueprint.route("/")
# def index():
#     return render_template("home.html")

