from flask import render_template
from app import app
from app import db


@app.route('/')
@app.route('/index')
def index():
    db_inst = db.DB()
    data_yandex = db_inst.get_data_for_chart('yandex')
    data_rp5 = db_inst.get_data_for_chart('rp5')
    data_narodmon = db_inst.get_data_for_chart('narodmon')
    db_inst.db_close()

    return render_template('index.html',
                           data_yandex=data_yandex,
                           data_rp5=data_rp5,
                           data_narodmon=data_narodmon)

@app.route('/pressure')
def pressure():
    db_inst = db.DB()
    data_yandex = db_inst.get_data_for_chart('yandex', parameter='pressure')
    data_rp5 = db_inst.get_data_for_chart('rp5', parameter='pressure')
    data_narodmon = db_inst.get_data_for_chart('narodmon', parameter='pressure')
    db_inst.db_close()

    return render_template('pressure.html',
                           data_yandex=data_yandex,
                           data_rp5=data_rp5,
                           data_narodmon=data_narodmon)
