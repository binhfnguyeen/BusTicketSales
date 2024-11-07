from flask import Flask, url_for, render_template, redirect
from DatVe.index import datve_bp
app = Flask(__name__)

app.register_blueprint(datve_bp, url_prefix='/datve')
@app.route('/')
def index():
    return render_template("datve.html")

if __name__ == '__main__':
    app.run(debug=True)

