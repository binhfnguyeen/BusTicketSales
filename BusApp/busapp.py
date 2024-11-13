from enum import verify
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from flask import url_for, render_template, redirect, request, flash, make_response, session, jsonify
from BusApp.main import login_blueprint
from BusApp.datve import datve_blueprints
import sqlite3
import os
import json
import dao

from BusApp import app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

app.register_blueprint(datve_blueprints)
app.register_blueprint(login_blueprint)


@app.route('/thanhtoan')
def thanh_toan():
    return render_template("thanhtoan.html")


@app.route('/')
def trang_chu():
    with sqlite3.connect('data/database.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM provinces ")
        provinces = c.fetchall()
    conn.close()
    return render_template("home.html", provinces=provinces)


@app.route('/TuyenXe')
def tuyenXe_admin():
    tx = dao.load_tuyenXe()
    total = dao.total_tuyenXe()
    return render_template("tuyenXe.html", tuyenXe=tx, sum=total)


@app.route('/Xe')
def xe_admin():
    x = dao.load_Xe()
    total = dao.total_Xe()
    return render_template("xe.html", Xe=x, sum=total)


@app.route('/HomeAdmin')
def home_admin():
    return render_template("homeAd_new.html")


@app.route('/UserAdmin/NhanVien')
def user_admin_NV():
    kw = request.args.get('kw')
    em = dao.load_employees(kw=kw)
    total = dao.total_employees()
    return render_template("userAd_NV.html", employees=em, sum=total)

@app.route('/ThemNhanVien', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        # Xử lý dữ liệu từ form
        hoNV = request.form['hoKhach']
        tenNV = request.form['tenKhach']
        soDienThoai = request.form['soDienThoai']
        gioiTinh = request.form['gioiTinh']
        email = request.form['email']
        ngaySinh = request.form['ngaySinh']
        nganHang = request.form['nganHang']
        soTaiKhoan = request.form['soTaiKhoan']

        # Kết nối và thêm dữ liệu vào database
        connection = sqlite3.connect('./data/database.db')
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO NhanVien (hoNV, tenNV, soDienThoai, gioiTinh, email, ngaySinh, nganHang, soTaiKhoan) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (hoNV, tenNV, soDienThoai, gioiTinh, email, ngaySinh, nganHang, soTaiKhoan))
        connection.commit()
        connection.close()

        # Chuyển hướng về trang chính sau khi thêm thành công
        return redirect('/HomeAdmin')

    # Nếu là GET, hiển thị trang thêm khách hàng
    return render_template('them_NV.html')

@app.route('/xoa_NV/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        # Giả sử bạn có một hàm để kết nối và xóa dữ liệu từ database
        dao.delete_customer_from_db(employee_id)  # X óa nhan vien theo ID
        return jsonify({"success": True}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False}), 500

@app.route('/chinhSua_NV/<int:id>')
def edit_employee(id):
    conn = get_db_connection()
    employee = conn.execute('SELECT * FROM NhanVien WHERE idNhanVien = ?', (id,)).fetchone()
    conn.close()
    if employee:
        return render_template('capNhat_NV.html', employee=employee)
    return "Customer not found", 404

# Route để cập nhật thông tin khách hàng
@app.route('/capNhat_NV/<int:id>', methods=['POST'])
def update_employee(id):
    hoNV = request.form['hoNV']
    tenNV = request.form['tenNV']
    soDienThoai = request.form['soDienThoai']
    gioiTinh = request.form['gioiTinh']
    email = request.form['email']
    ngaySinh = request.form['ngaySinh']
    nganHang = request.form['nganHang']
    soTaiKhoan = request.form['soTaiKhoan']

    conn = get_db_connection()
    conn.execute('''UPDATE NhanVien SET hoNV = ?, tenNV = ?, soDienThoai = ?, gioiTinh = ?, 
                    email = ?, ngaySinh = ?, nganHang = ?, soTaiKhoan = ? WHERE idNhanVien = ?''',
                 (hoNV, tenNV, soDienThoai, gioiTinh, email, ngaySinh, nganHang, soTaiKhoan, id))
    conn.commit()
    conn.close()
    return redirect(url_for('home_admin'))  # Chuyển hướng về trang chủ sau khi cập nhật thành công

@app.route('/UserAdmin/KhachHang')
def user_admin_KH():
    kw = request.args.get('kw')
    cus = dao.load_customers(kw=kw)
    total = dao.total_customers()
    return render_template("userAd_KH.html", customers=cus, sum=total)

@app.route('/ThemKhachHang', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        # Xử lý dữ liệu từ form
        hoKhach = request.form['hoKhach']
        tenKhach = request.form['tenKhach']
        soDienThoai = request.form['soDienThoai']
        gioiTinh = request.form['gioiTinh']
        email = request.form['email']
        ngaySinh = request.form['ngaySinh']
        nganHang = request.form['nganHang']
        soTaiKhoan = request.form['soTaiKhoan']

        # Kết nối và thêm dữ liệu vào database
        connection = sqlite3.connect('./data/database.db')
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO KhachHang (hoKhach, tenKhach, soDienThoai, gioiTinh, email, ngaySinh, nganHang, soTaiKhoan) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (hoKhach, tenKhach, soDienThoai, gioiTinh, email, ngaySinh, nganHang, soTaiKhoan))
        connection.commit()
        connection.close()

        # Chuyển hướng về trang chính sau khi thêm thành công
        return redirect('/HomeAdmin')

    # Nếu là GET, hiển thị trang thêm khách hàng
    return render_template('them_KH.html')

@app.route('/xoa_KH/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    try:
        # Giả sử bạn có một hàm để kết nối và xóa dữ liệu từ database
        dao.delete_customer_from_db(customer_id)  # X óa khách hàng theo ID
        return jsonify({"success": True}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False}), 500

def get_db_connection():
    conn = sqlite3.connect('./data/database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route để hiển thị trang chỉnh sửa
@app.route('/chinhSua_KH/<int:id>')
def edit_customer(id):
    conn = get_db_connection()
    customer = conn.execute('SELECT * FROM KhachHang WHERE idKhachHang = ?', (id,)).fetchone()
    conn.close()
    if customer:
        return render_template('capNhat_KH.html', customer=customer)
    return "Customer not found", 404

# Route để cập nhật thông tin khách hàng
@app.route('/capNhat_KH/<int:id>', methods=['POST'])
def update_customer(id):
    hoKhach = request.form['hoKhach']
    tenKhach = request.form['tenKhach']
    soDienThoai = request.form['soDienThoai']
    gioiTinh = request.form['gioiTinh']
    email = request.form['email']
    ngaySinh = request.form['ngaySinh']
    nganHang = request.form['nganHang']
    soTaiKhoan = request.form['soTaiKhoan']

    conn = get_db_connection()
    conn.execute('''UPDATE KhachHang SET hoKhach = ?, tenKhach = ?, soDienThoai = ?, gioiTinh = ?, 
                    email = ?, ngaySinh = ?, nganHang = ?, soTaiKhoan = ? WHERE idKhachHang = ?''',
                 (hoKhach, tenKhach, soDienThoai, gioiTinh, email, ngaySinh, nganHang, soTaiKhoan, id))
    conn.commit()
    conn.close()
    return redirect(url_for('home_admin'))  # Chuyển hướng về trang chủ sau khi cập nhật thành công


@app.route('/loginAd', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Kiểm tra xem email và password có được nhập không
        if not email or not password:
            flash("Vui lòng nhập email và mật khẩu!", "danger")
        elif email == "admin@example.com" and password == "password":
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for('home_admin'))  # Chuyển hướng đến route 'home_admin'
        else:
            flash("Email hoặc mật khẩu không đúng!", "danger")

    return render_template('login_new.html')


@app.route('/verify_Save', methods=['get', 'post'])
def verify():
    app.secret_key = 'aiughiakjf'
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()
    if request.method == 'GET':
        otp = generate_otp()
        session['otp'] = otp
        nhanOTP(session.get('otp'), session.get('email'))
        print(session.get('otp'))
    if request.method == 'POST':
        otpcheck = request.form['otp']
        print(session.get('otp'))
        if session.get('otp') == otpcheck:
            query = "UPDATE KhachHang SET soDienThoai = ?, diaChi = ?, email = ? WHERE idKhachHang = 1"
            cursor.execute(query, (session.get('soDienThoai'), session.get('diaChi'), session.get('email')))
            conn.commit()
            conn.close()
            return redirect(url_for('tt_ca_nhan'))
        if session.get('otp') != otpcheck:
            print("SAI OTP")
            return redirect(url_for('tt_ca_nhan'))
    return render_template("verify.html")


def send_email(to_email, subject, message):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'lequangvinhkanghaneul@gmail.com'
    sender_password = 'vorv rxwe giey jpmq'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")


def generate_otp():
    return str(random.randint(100000, 999999))


def nhanOTP(otp, usermail):
    send_email(usermail, "Password Reset Code", f"Your password reset code is: {otp}")


@app.route('/ttcanhan', methods=['get', 'post'])
def tt_ca_nhan():
    thongTin = getThongTin()
    if request.method == 'POST':
        session['soDienThoai'] = request.form['sdt']
        session['diaChi'] = request.form['diaChi']
        session['email'] = request.form['email']
        return redirect(url_for('verify'))
    return render_template("ThongTinCaNhan.html", tt=thongTin)


@app.route('/vecuatoi')
def ve_cua_toi():
    data = getVe()

    return render_template("VeCuaToi.html", data=data)


def getVe():
    db_path = os.path.join(os.path.dirname(__file__), 'data/database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = 'SELECT Ben_Xe_Di.ten_ben_xe, Ben_Xe_Den.ten_ben_xe, TuyenDuong.khoangCach, LichTrinh.thoiGianDi, Ve.trangThaiVe FROM Ve JOIN  DonHang ON Ve.idDonHang  = DonHang.idDonHang JOIN LichTrinh ON LichTrinh.idLichTrinh = DonHang.idLichTrinh JOIN TuyenDuong ON TuyenDuong.idTuyenDuong = LichTrinh.idTuyenDuong JOIN Ben_Xe AS Ben_Xe_Di ON TuyenDuong.diemDi = Ben_Xe_Di.ben_xe_id JOIN Ben_Xe AS Ben_Xe_Den ON TuyenDuong.diemDen = Ben_Xe_Den.ben_xe_id; '
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


def searchLichTrinh(diemDi=None, diemDen=None):
    with sqlite3.connect('data/database.db') as conn:
        c = conn.cursor()
        c.execute(
            "SELECT  BenXeDi.ten_ben_xe AS ten_diem_di, BenXeDen.ten_ben_xe AS ten_diem_den, TuyenDuong.khoangCach, LichTrinh.thoiGianDi, Ben_xe.tinh_code FROM LichTrinh, Ben_xe JOIN  TuyenDuong ON LichTrinh.idTuyenDuong = TuyenDuong.idTuyenDuong  JOIN Ben_Xe AS BenXeDi ON TuyenDuong.diemDi = BenXeDi.ben_xe_id  JOIN Ben_Xe AS BenXeDen ON TuyenDuong.diemDen = BenXeDen.ben_xe_id GROUP BY BenXeDi.ten_ben_xe, BenXeDen.ten_ben_xe, TuyenDuong.khoangCach, LichTrinh.thoiGianDi ")
        data = c.fetchall()
    if diemDi != None:
        data = [p for p in data if str(p[4]) == str(diemDi)]
    if diemDen != None:
        data = [p for p in data if str(p[4]) == str(diemDen)]
    conn.close()
    return data


def getThongTin():
    db_path = os.path.join(os.path.dirname(__file__), 'data/database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = 'select hoKhach, tenKhach, email, soDienThoai, nganHang, diaChi, soTaiKhoan, ngaySinh, gioiTinh from KhachHang where idKhachHang = 1;'
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


@app.route('/search')
def search():
    diemdi = request.args.get("departure")
    diemden = request.args.get("destination")
    data = searchLichTrinh(diemdi, diemden)
    with sqlite3.connect('data/database.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM provinces ")
        provinces = c.fetchall()
    conn.close()
    return render_template('home.html', data=data, provinces=provinces)


@app.route('/ttlienhe')
def tt_lien_he():
    return render_template("ThongTinLienHe.html")


@app.route('/lichtrinh')
def lich_trinh():
    diemDi = request.args.get("diemDi")
    diemDen = request.args.get("diemDen")
    data = getLichTrinh(diemDi, diemDen)
    return render_template("lichtrinh.html", data=data)


def getLichTrinh(diemDi=None, diemDen=None):
    db_path = os.path.join(os.path.dirname(__file__), 'data/database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = (
        'SELECT BenXeDi.ten_ben_xe AS ten_diem_di, BenXeDen.ten_ben_xe AS ten_diem_den, TuyenDuong.khoangCach, LichTrinh.thoiGianDi ' 'FROM LichTrinh JOIN  TuyenDuong ON LichTrinh.idTuyenDuong = TuyenDuong.idTuyenDuong JOIN Ben_Xe AS BenXeDi ON TuyenDuong.diemDi = BenXeDi.ben_xe_id ' 'JOIN Ben_Xe AS BenXeDen ON TuyenDuong.diemDen = BenXeDen.ben_xe_id; ')
    cursor.execute(query)
    data = cursor.fetchall()
    if diemDi != None:
        data = [p for p in data if str(p[0]) == str(diemDi)]
    if diemDen != None:
        data = [p for p in data if str(p[1]) == str(diemDen)]
    conn.close()
    return data


app.secret_key = 'your_secret_key'


# Đọc dữ liệu từ file JSON
def load_users():
    user_path = os.path.join(os.path.dirname(__file__), 'data/user.json')
    with open(user_path, 'r') as file:
        data = json.load(file)
    return data['users']


# Lưu dữ liệu vào file JSON
def save_users(users):
    user_path = os.path.join(os.path.dirname(__file__), 'data/user.json')
    with open(user_path, 'w') as file:
        json.dump({"users": users}, file, indent=4)


@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        username = request.form['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Kiểm tra người dùng trong file JSON
        users = load_users()
        user_found = False

        for user in users:
            if user['username'] == username and user['password'] == old_password:
                user_found = True
                # Kiểm tra mật khẩu mới và xác nhận mật khẩu có giống nhau không
                if new_password == confirm_password:
                    # Cập nhật mật khẩu mới
                    user['password'] = new_password
                    save_users(users)  # Lưu lại dữ liệu
                    flash('Password changed successfully!', 'success')
                else:
                    flash('New password and confirm password do not match!', 'danger')
                break

        if not user_found:
            flash('Incorrect username or old password!', 'danger')

        return redirect(url_for('change_password'))

    # Render trang HTML với form
    return render_template('change_password.html')


invoice_data = {
    "invoices": [
        {
            "ticket_id": "P392",
            "seat": "160",
            "route": "Vũng Tàu - TP.Hồ Chí Minh",
            "date": "2024-10-21",
            "created_date": "2024-10-19",
            "amount": "160000 VNĐ",
            "status": "Đã thanh toán"
        },
        {
            "ticket_id": "P772",
            "seat": "150",
            "route": "Cần Thơ - Bến Tre",
            "date": "2024-10-22",
            "created_date": "2024-10-19",
            "amount": "150000 VNĐ",
            "status": "Chờ thanh toán"
        }
    ],
    "total_amount": "310000 VNĐ"
}


@app.route('/lshoadon')
def invoice_history():
    return render_template('lshoadon.html', data=invoice_data)


@app.route('/generate_pdf')
def generate_pdf():
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.drawString(100, 750, "Chi tiết hóa đơn")
    pdf.drawString(100, 735, "Tên khách hàng: Thế Nguyên")
    pdf.drawString(100, 720, "Email: phamthenguyen2004@gmail.com")
    pdf.drawString(100, 705, "SDT: 0932109822")
    pdf.drawString(100, 690, "Địa chỉ: Q. Tân Phú, TP.HCM")
    # Add more content if needed
    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return make_response(buffer.getvalue(), 200, {
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'attachment; filename="HoaDon.pdf"'
    })


@app.route('/delete_invoice/<ticket_id>', methods=['POST'])
def delete_invoice(ticket_id):
    # Gọi hàm xóa hóa đơn từ cơ sở dữ liệu theo ticket_id
    # Ví dụ: db.delete_invoice(ticket_id)
    # Nếu thành công:
    return '', 200
    # Nếu không thành công:
    # return '', 400


if __name__ == '__main__':
    app.run(debug=True)
