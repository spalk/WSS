import sqlite3
from operator import itemgetter

from app.config import config


class DB:
    def __init__(self):
        db_file = config['DB']['db_file']
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()

    def get_data_for_chart(self, service):
        # SELECT * FROM session WHERE stop_time > (SELECT DATETIME('now', '-7 day'))
        history_days = config['DB']['history_days']
        forecast_days = config['DB']['forecast_days']
        history_dt_req = '''(SELECT DATETIME('now', '-%s day'))''' % history_days
        forecast_dt_req = '''(SELECT DATETIME('now', '+%s day'))''' % forecast_days
        req = ''' SELECT * 
            FROM temperature 
            WHERE service = ?
            AND datetime > %s
            AND datetime < %s''' % (history_dt_req, forecast_dt_req)
        print (req)
        self.c.execute(req, (service,))
        rows = self.c.fetchall()

        data = []
        used_keys = []
        for r in rows:
            dt = r[2]
            if dt in used_keys:
                for dic in data:
                    if dic['date'] == dt:
                        if dic['close'] < r[3]:
                            dic['close'] = r[3]
                        elif dic['open'] > r[3]:
                            dic['open'] = r[3]
            else:
                data.append(
                    {'date': dt,
                     'open': r[3],
                     'close': r[3]}
                )
                used_keys.append(dt)
        data_sorted = sorted(data, key=itemgetter('date'))
        return data_sorted

    def db_close(self):
        self.conn.close()
