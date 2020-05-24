from flask import render_template
from app import app
from app import db


@app.route('/')
@app.route('/index')
def index():
    db_inst = db.DB()
    data_yandex = db_inst.get_data_for_chart('yandex')
    data_rp5 = db_inst.get_data_for_chart('rp5')
    db_inst.db_close()

    return render_template('index.html', data_yandex=data_yandex, data_rp5=data_rp5)
