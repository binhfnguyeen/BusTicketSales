from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from flask import Flask, url_for, render_template, redirect, request, flash, make_response
from main import login_blueprint
from datve import datve_blueprints
import sqlite3
import os
import json

app=Flask(__name__)
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

@app.route('/HomeAdmin')
def home_admin():
    return render_template("homeAd.html")

@app.route('/LoginAdmin')
def login_admin():
    return  render_template("loginAd.html")

@app.route('/ttcanhan')
def tt_ca_nhan():
    return render_template("ThongTinCaNhan.html")

@app.route('/vecuatoi')
def ve_cua_toi():
    data = getVe()
    return render_template("VeCuaToi.html", data = data)

def getVe():
    db_path = os.path.join(os.path.dirname(__file__), 'data/database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = 'SELECT Ben_Xe_Di.ten_ben_xe, Ben_Xe_Den.ten_ben_xe, TuyenDuong.khoangCach, LichTrinh.thoiGianDi, Ve.trangThaiVe FROM Ve JOIN  DonHang ON Ve.idDonHang  = DonHang.idDonHang JOIN LichTrinh ON LichTrinh.idLichTrinh = DonHang.idLichTrinh JOIN TuyenDuong ON TuyenDuong.idTuyenDuong = LichTrinh.idTuyenDuong JOIN Ben_Xe AS Ben_Xe_Di ON TuyenDuong.diemDi = Ben_Xe_Di.ben_xe_id JOIN Ben_Xe AS Ben_Xe_Den ON TuyenDuong.diemDen = Ben_Xe_Den.ben_xe_id; '
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

def searchLichTrinh(diemDi = None, diemDen = None):

    with sqlite3.connect('data/database.db') as conn:
        c = conn.cursor()
        c.execute("SELECT  BenXeDi.ten_ben_xe AS ten_diem_di, BenXeDen.ten_ben_xe AS ten_diem_den, TuyenDuong.khoangCach, LichTrinh.thoiGianDi, Ben_xe.tinh_code FROM LichTrinh, Ben_xe JOIN  TuyenDuong ON LichTrinh.idTuyenDuong = TuyenDuong.idTuyenDuong  JOIN Ben_Xe AS BenXeDi ON TuyenDuong.diemDi = BenXeDi.ben_xe_id  JOIN Ben_Xe AS BenXeDen ON TuyenDuong.diemDen = BenXeDen.ben_xe_id GROUP BY BenXeDi.ten_ben_xe, BenXeDen.ten_ben_xe, TuyenDuong.khoangCach, LichTrinh.thoiGianDi ")
        data = c.fetchall()
    if diemDi != None:
        data = [p for p in data if str(p[4]) == str(diemDi)]
    if diemDen != None:
        data = [p for p in data if str(p[4]) == str(diemDen)]
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
    return render_template('home.html', data = data, provinces=provinces)

@app.route('/ttlienhe')
def tt_lien_he():
    return  render_template("ThongTinLienHe.html")

@app.route('/lichtrinh')
def lich_trinh():
    diemDi = request.args.get("diemDi")
    diemDen = request.args.get("diemDen")
    data = getLichTrinh(diemDi, diemDen)
    return render_template("lichtrinh.html", data = data )

def getLichTrinh(diemDi = None, diemDen = None):
    db_path = os.path.join(os.path.dirname(__file__), 'data/database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = ('SELECT BenXeDi.ten_ben_xe AS ten_diem_di, BenXeDen.ten_ben_xe AS ten_diem_den, TuyenDuong.khoangCach, LichTrinh.thoiGianDi ' 'FROM LichTrinh JOIN  TuyenDuong ON LichTrinh.idTuyenDuong = TuyenDuong.idTuyenDuong JOIN Ben_Xe AS BenXeDi ON TuyenDuong.diemDi = BenXeDi.ben_xe_id ' 'JOIN Ben_Xe AS BenXeDen ON TuyenDuong.diemDen = BenXeDen.ben_xe_id; ')
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
