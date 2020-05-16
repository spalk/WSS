from flask import render_template
from app import app

import json


@app.route('/')
@app.route('/index')
def index():
    series = ['ya_min', 'ya_max', 'rp5_min', 'rp5_max']
    data = [
            {"date": "2018-01-01T21:00:00.000Z", "value_ya_min": 1},
            {"date": "2018-01-02T21:00:00.000Z", "value_ya_min": 3},
            {"date": "2018-01-03T21:00:00.000Z", "value_ya_min": 2},
            {"date": "2018-01-01T21:00:00.000Z", "value_ya_max": 2},
            {"date": "2018-01-02T21:00:00.000Z", "value_ya_max": 5},
            {"date": "2018-01-03T21:00:00.000Z", "value_ya_max": 3},
            {"date": "2018-01-01T21:00:00.000Z", "value_rp5_min": 2},
            {"date": "2018-01-02T21:00:00.000Z", "value_rp5_min": 1},
            {"date": "2018-01-03T21:00:00.000Z", "value_rp5_min": 4},
            {"date": "2018-01-01T21:00:00.000Z", "value_rp5_max": 3},
            {"date": "2018-01-02T21:00:00.000Z", "value_rp5_max": 5},
            {"date": "2018-01-03T21:00:00.000Z", "value_rp5_max": 6}
            ]

    return render_template('index.html', wss_data=data, wss_series=series)
