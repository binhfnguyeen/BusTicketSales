from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
@app.route('/')
def index():
    return render_template("test.html")

def dbconnection():
    # Kết nối tới file SQLite
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()
    return
@app.route('/')
def indexhome():


    # Truy vấn lấy dữ liệu điểm đi và điểm đến (ví dụ từ bảng 'locations')
    cursor.execute("SELECT code, name FROM provinces ")
    provinces = cursor.fetchall()  # Lấy tất cả các dòng kết quả

    # Đóng kết nối sau khi xong
    conn.close()
    return render_template("test.html", provinces=provinces)


if __name__ == '__main__':
    app.run(debug=True)
