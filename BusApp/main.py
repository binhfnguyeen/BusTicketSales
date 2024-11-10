import hashlib
from flask import Flask, render_template, request, redirect, url_for, session
from flask import Blueprint
import dao

login_blueprint = Blueprint("login", __name__)
app = Flask(__name__)

app.secret_key = 'nhom5attt'

@login_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    err_msg = ""
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.validate_user(username=username, password=password)
        if user:
            session['username'] = username
            return render_template("home.html")
        else:
            err_msg = "DANH NHAP THAT BAI"
    return render_template("dangnhap.html", err_msg=err_msg)


@login_blueprint.route('/dangky')
def register():
    err_msg = ""
    return render_template('dangky.html', err_msg=err_msg)
