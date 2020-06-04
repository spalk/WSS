import sqlite3
import datetime
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

    def get_data_for_chart2(self, service: str, history_days=config['DB']['history_days'],
                            forecast_days=config['DB']['forecast_days']) -> list:
        # SELECT * FROM session WHERE stop_time > (SELECT DATETIME('now', '-7 day'))
        history_dt_req = '''(SELECT DATETIME('now', '-%s day'))''' % history_days
        forecast_dt_req = '''(SELECT DATETIME('now', '+%s day'))''' % forecast_days
        req = ''' SELECT * 
            FROM temperature 
            WHERE service = ?
            AND datetime > %s
            AND datetime < %s''' % (history_dt_req, forecast_dt_req)
        # print(req)
        self.c.execute(req, (service,))
        rows = self.c.fetchall()

        # [{date, latest_min, latest_max, latest_timestamp, absolute_min, absolute_max}]
        data = []
        used_keys = []
        for r in rows:

            dt = r[2]
            if dt in used_keys:
                for dic in data:
                    if dic['date'] == dt:
                        if r[3] > dic['absolute_max']:
                            dic['absolute_max'] = r[3]
                        elif r[3] < dic['absolute_min']:
                            dic['absolute_min'] = r[3]

                        timestamp = datetime.datetime.strptime(r[1], '%Y-%m-%d %H:%M:%S')
                        print(timestamp, ' -- ', dic['latest_timestamp'], timestamp > dic['latest_timestamp'])
                        if timestamp > dic['latest_timestamp']:
                            dic['latest_max'] = dic['latest_min'] = r[3]
                        if timestamp == dic['latest_timestamp']:
                            if r[3] > dic['latest_max']:
                                dic['latest_min'] = dic['latest_max']
                                dic['latest_max'] = r[3]
                            else:
                                dic['latest_max'] = dic['latest_min']
                                dic['latest_min'] = r[3]

            else:
                timestamp = datetime.datetime.strptime(r[1], '%Y-%m-%d %H:%M:%S')
                data.append(
                    {
                        'date': dt,
                        'latest_min': r[3],
                        'latest_max': r[3],
                        'latest_timestamp': timestamp,
                        'absolute_min': r[3],
                        'absolute_max': r[3],
                    }
                )
                used_keys.append(dt)
        data_sorted = sorted(data, key=itemgetter('date'))
        return data_sorted

    def get_data_for_chart3(self, service: str, parameter='temperature', history_days=config['DB']['history_days'],
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
            print ('*'*5, dt)
            abs_min = self.get_min(dt, parameter, service)
            print('abs_min',abs_min)
            abs_max = self.get_max(dt, parameter, service)
            print('abs_max',abs_max)
            latest = self.get_two_latest(dt, parameter, service)
            latest_min = latest[0][0]
            latest_max = latest[1][0]
            print('latest_min',latest_min)
            print('latest_max',latest_max)
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

    def get_max(self, dt, parameter, service):
        req = '''SELECT max("value") 
                 FROM %s 
                 WHERE service = "%s"
                 AND datetime = "%s"''' % (parameter, service, dt)
        self.c.execute(req)
        print(req)
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
