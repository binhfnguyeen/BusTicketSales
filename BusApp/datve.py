import sqlite3

import stripe
from flask import Blueprint, Flask, render_template, request
from flask import jsonify
app = Flask(__name__)
datve_blueprints = Blueprint("datve", __name__)

stripe.api_key = "pk_test_51QKFWxHwA2xtXgiVY28lvYyNRSeIkIIVOb7vVR2Aj4uuf3nWhKEqdQZefcBsdXYYZlU4GvntWQRPitT53ifoCwXK005lLME6HA"
def get_data_from_db(query, params):
    try:
        conn = sqlite3.connect('./data/database.db')
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        print("Lỗi cơ sở dữ liệu:", e)
        return None
    finally:
        conn.close()
@datve_blueprints.route("/api/chuyenxe", methods=["GET"])
def get_chuyenxe():
    diem_di = request.args.get('diem_di')
    diem_den = request.args.get('diem_den')
    ben_di = request.args.get('ben_di')
    ben_den = request.args.get('ben_den')
    query = """
    SELECT * FROM Chuyen_Xe
    WHERE DiemDi = ? AND DiemDen = ? AND BenDi = ? AND BenDen = ?
    """
    result = get_data_from_db(query, (diem_di, diem_den, ben_di, ben_den))

    if result:
        return jsonify({"status": "found", "data": result})
    else:
        return jsonify({"status": "not_found"})

@datve_blueprints.route("/api/bienso")
def get_bienso():
    bien_so = get_data_from_db("SELECT DISTINCT bienSo FROM Xe")
    data = {
        "bien_so": [row[0] for row in bien_so]
    }
    return jsonify(data)


@app.route('/charge', methods=['POST'])
def charge():
    try:
        # Tạo session thanh toán Stripe Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Sản phẩm ví dụ',
                        },
                        'unit_amount': 1000,  # Số tiền là 10.00 USD (1000 cent)
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.host_url + 'success',
            cancel_url=request.host_url + 'cancel',
        )

        return jsonify({
            'id': session.id
        })
    except Exception as e:
        return str(e), 500

@datve_blueprints.route('/success')
def success():
    return 'Thanh toán thành công!'

@datve_blueprints.route('/cancel')
def cancel():
    return 'Thanh toán bị hủy.'

@datve_blueprints.route('/checkout')
def checkout():
    return render_template('checkout.html', key='sk_test_51QKFWxHwA2xtXgiVV3nkxS8tuCsiDbIVbpOfLPtnoa82UGwlwyYRdlw9I2SnO3Ix6PtaReYomTMr6AhGUPCEW5kI00bovmtMxJ')

@datve_blueprints.route('/datve')
def index():
    return render_template("datve.html")


if __name__ == "main":
    app.run(debug=True)