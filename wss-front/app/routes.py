from flask import render_template
from app import app
from app import db


@app.route('/')
@app.route('/index')
def index():
    db_inst = db.DB()
    data = db_inst.get_data_for_chart()
    db_inst.db_close()

    return render_template('index.html', wss_data=data)
