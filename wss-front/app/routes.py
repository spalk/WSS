import hashlib
from flask import render_template
from flask import request
from app import app
from app import db
from app.config import config


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


@app.route('/sensor-data')
def sensor_data():
    # http://localhost:5000/sensor-data?sensorname=esp8266&parameter=t&value=24&key=123
    sensor_name = request.args.get('sensorname')
    parameter = request.args.get('parameter')
    value = request.args.get('value')
    received_key = request.args.get('key')
    true_key = get_md5(sensor_name)[:6]
    if received_key == true_key:
        db_inst = db.DB()
        db_inst.save_sensor_data(sensor_name, parameter, value)
        db_inst.db_close()
        return 'ok'
    else:
        return 'Error: key is wrong'


def get_md5(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()

