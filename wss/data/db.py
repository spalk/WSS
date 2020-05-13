import sqlite3
import os.path
import datetime

from wss.data.config import config

import logging

logger = logging.getLogger('root')


class DB:
    def __init__(self):
        db_file = config['DB']['db_file']
        logger.debug('Connecting to DB: ' + db_file)

        # Check if db-file exist
        self.db_file_exist(db_file)

        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()

        # Check if tables exist
        if not self.table_exist('temperature') or not self.table_exist('pressure'):
            self.create_tables()

    def save_forecast(self, data: list):
        temp_data = []
        pres_data = []
        timestamp = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
        for line in data:
            line['timestamp'] = timestamp
            if line['parameter'] == 't':
                if not self.raw_exist('temperature', line):
                    temp_data.append(self.dic2tuple(line))
            elif line['parameter'] == 'p':
                if not self.raw_exist('pressure', line):
                    pres_data.append(self.dic2tuple(line))
            else:
                logger.critical('Unexpected parameter in dic: ' + line['parameter'])

        self.c.executemany('INSERT INTO temperature(timestamp, datetime, value, service) VALUES (?,?,?,?)', temp_data)
        self.c.executemany('INSERT INTO pressure(timestamp, datetime, value, service) VALUES (?,?,?,?)', pres_data)
        self.conn.commit()

        logger.debug('>> saved in DB %s temperature values' % len(temp_data))
        logger.debug('>> saved in DB %s pressure values' % len(pres_data))

    def table_exist(self, table: str) -> bool:
        """Check if table exist"""
        table_name = (table,)
        self.c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?''', table_name)

        if self.c.fetchone()[0] == 1:
            return True
        else:
            return False

    def create_tables(self):
        """Create tables"""
        # temperature
        self.c.execute("""CREATE TABLE temperature
                              (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                               timestamp TEXT NOT NULL,
                               datetime TEXT NOT NULL,
                               value REAL NOT NULL,
                               service TEXT NOT NULL)
                       """)

        # pressure
        self.c.execute("""CREATE TABLE pressure
                                      (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                       timestamp TEXT NOT NULL,
                                       datetime TEXT NOT NULL,
                                       value REAL NOT NULL,
                                       service TEXT NOT NULL)
                               """)

    def raw_exist(self, table: str, data: dict) -> bool:
        """Check if forecast for this date and time already in DB"""
        request = 'SELECT id FROM %s WHERE datetime=:datetime and value=:value and service=:service' % table
        self.c.execute(request,
                       {"table": table, 'datetime': data['datetime'], 'value': data['value'],
                        'service': data['service']})
        result = self.c.fetchall()
        if len(result) == 0:
            return False
        else:
            return True

    def db_close(self):
        self.conn.close()

    @staticmethod
    def db_file_exist(path: str):
        """Create db-file if it's not exist"""
        if os.path.exists(path):
            logger.debug('>> DB-file found')
        else:
            open(path, 'a').close()
            logger.debug('>> DB-file not found. Creating...')

    @staticmethod
    def dic2tuple(dic: dict) -> tuple:
        """Preparing data for insert in db: convert from dict to tuple"""
        # {'datetime': datetime.datetime(2020, 5, 10, 15, 0), 'parameter': 'p', 'value': 743, 'service': 'rp5'}
        tpl = (dic['timestamp'],
               dic['datetime'].isoformat(sep=' ', timespec='seconds'),
               dic['value'],
               dic['service']
               )
        return tpl
