import sqlite3
from operator import itemgetter

from app.config import config


class DB:
    def __init__(self):
        db_file = config['DB']['db_file']
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()

    def get_data_for_chart(self):
        # SELECT * FROM session WHERE stop_time > (SELECT DATETIME('now', '-7 day'))
        history_days = config['DB']['history_days']
        cur_dt_req = '''(SELECT DATETIME('now', '-%s day')''' % history_days
        req = ''' SELECT * 
            FROM temperature 
            WHERE service = ?
            AND datetime > %s)''' % cur_dt_req
        self.c.execute(req, ('yandex',))
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
