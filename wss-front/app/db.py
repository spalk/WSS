import sqlite3
import datetime
from operator import itemgetter

from app.config import config


class DB:
    def __init__(self):
        db_file = config['DB']['db_file']
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()

    def get_data_for_chart(self, service: str, parameter='temperature', history_days=config['DB']['history_days'],
                            forecast_days=config['DB']['forecast_days']) -> list:
        # SELECT * FROM session WHERE stop_time > (SELECT DATETIME('now', '-7 day'))
        history_dt_req = '''(SELECT DATETIME('now', '-%s day'))''' % history_days
        forecast_dt_req = '''(SELECT DATETIME('now', '+%s day'))''' % forecast_days
        req = ''' SELECT datetime 
            FROM %s 
            WHERE service = ?
            AND datetime > %s
            AND datetime < %s''' % (parameter, history_dt_req, forecast_dt_req)
        self.c.execute(req, (service,))
        rows = self.c.fetchall()

        dt_list = []
        for r in rows:
            if r not in dt_list:
                dt_list.append(r)

        data = []
        for dt in dt_list:
            dt = dt[0]
            abs_min = self.get_min(dt, parameter, service)
            abs_max = self.get_max(dt, parameter, service)
            latest = self.get_two_latest(dt, parameter, service)
            if len(latest) == 2:
                latest_min = latest[0][0]
                latest_max = latest[1][0]
            if len(latest) == 1:
                latest_min = latest_max = latest[0][0]
            if latest_min > latest_max:
                latest_min, latest_max = latest_max, latest_min

            dic = {
                'date': dt,
                'absolute_min': abs_min,
                'absolute_max': abs_max,
                'latest_min': latest_min,
                'latest_max': latest_max
            }

            data.append(dic)
        data_sorted = sorted(data, key=itemgetter('date'))
        return data_sorted

    def get_data_for_chart_(self, service):
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

    def get_max(self, dt, parameter, service):
        req = '''SELECT max("value") 
                 FROM %s 
                 WHERE service = "%s"
                 AND datetime = "%s"''' % (parameter, service, dt)
        self.c.execute(req)
        result_raw = self.c.fetchone()
        return result_raw[0]

    def get_min(self, dt, parameter, service):
        req = '''SELECT min("value") 
                 FROM %s 
                 WHERE service = "%s"
                 AND datetime = "%s"''' % (parameter, service, dt)
        self.c.execute(req)
        result_raw = self.c.fetchone()
        return result_raw[0]

    def get_two_latest(self, dt, parameter, service):
        req = '''SELECT "value" 
                 FROM %s 
                 WHERE service = "%s"
                 AND datetime = "%s"
                 ORDER BY timestamp DESC 
                 LIMIT 2''' % (parameter, service, dt)
        self.c.execute(req)
        result_raws = self.c.fetchall()
        return result_raws

    def db_close(self):
        self.conn.close()
