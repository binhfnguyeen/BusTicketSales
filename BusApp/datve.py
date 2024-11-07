import sqlite3
from flask import Blueprint, Flask, render_template, request
from flask import jsonify

app = Flask(__name__)
datve_blueprints = Blueprint("datve",__name__)
def get_data_from_db(query):
    try:
        connection = sqlite3.connect("data/database.db")
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        data = []
    finally:
        connection.close()
    return data

@datve_blueprints.route("/api/bienso")
def get_bienso():
    bien_so = get_data_from_db("SELECT DISTINCT bienSo FROM Xe")
    data = {
        "bien_so": [row[0] for row in bien_so]
    }
    return jsonify(data)

@datve_blueprints.route("/api/vitri")
def get_location():
    # Lấy các điểm đi và điểm đến từ bảng `provinces`
    diem_di = get_data_from_db("SELECT DISTINCT name FROM provinces")
    diem_den = get_data_from_db("SELECT DISTINCT name FROM provinces")

    # Lấy các quận huyện đi và quận huyện đến từ bảng `districts`
    quan_huyen_di = get_data_from_db("SELECT DISTINCT name FROM districts")
    quan_huyen_den = get_data_from_db("SELECT DISTINCT name FROM districts")

    # Lấy các bến xe đi và bến xe đến từ bảng `Ben_Xe`
    ben_di = get_data_from_db("SELECT DISTINCT ten_ben_xe FROM Ben_Xe")
    ben_den = get_data_from_db("SELECT DISTINCT ten_ben_xe FROM Ben_Xe")

    data = {
        "diem_di": [row[0] for row in diem_di],
        "diem_den": [row[0] for row in diem_den],
        "quan_huyen_di": [row[0] for row in quan_huyen_di],
        "ben_di": [row[0] for row in ben_di],
        "quan_huyen_den": [row[0] for row in quan_huyen_den],
        "ben_den": [row[0] for row in ben_den]
    }

    return jsonify(data)

@datve_blueprints.route('/datve')
def index():
    return render_template("datve.html")


@datve_blueprints.route('/api/results')
def get_results():
    diem_di = request.args.get('diem_di')
    diem_den = request.args.get('diem_den')

    # Truy vấn database để lấy kết quả dựa trên điểm đi và điểm đến
    query = f"SELECT * FROM xe WHERE diem_di = ? AND diem_den = ?"
    results = get_data_from_db(query, (diem_di, diem_den))

    # Định dạng dữ liệu trả về
    data = []
    for result in results:
        data.append({
            'gia_ve': result[0],  # Ví dụ: cột 'gia_ve'
            'loai': result[1],  # Ví dụ: cột 'loai'
            'so_cho': result[2],  # Cột 'so_cho'
            'ben_di': result[3],  # Cột 'ben_di'
            'ben_den': result[4],  # Cột 'ben_den'
            'ngay_di': result[5],  # Cột 'ngay_di'
            'ngay_ve': result[6],  # Cột 'ngay_ve'
            'diem_di': result[7],  # Cột 'diem_di'
            'diem_den': result[8],  # Cột 'diem_den'
            'bien_so': result[9]  # Cột 'bien_so'
        })

    return jsonify(data)

if __name__ == "main":
    app.run(debug=True)