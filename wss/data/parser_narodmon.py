import json
import datetime

import logging
logger = logging.getLogger('root')


class ParserNarodmon():
    def __init__(self):
        logger.debug('Start Narodmon parser processor')

    def feed(self, content_json):
        self.content = content_json
        content_dic = json.loads(content_json)
        # http://narodmon.ru/api/sensorsValues?sensors=2620,2621&uuid=53ad04c130d27cdce00a52ffc9570c30&api_key=Fv2PUCB4UKGGe
        self.t_value = content_dic['sensors'][0]['value']
        self.t_dt_unix = content_dic['sensors'][0]['time']
        self.p_value = content_dic['sensors'][1]['value']
        self.p_dt_unix = content_dic['sensors'][1]['time']

    def set_data_types(self):
        """Clearing data and converting from strings to datetime and int"""
        t_value = float(self.t_value)
        t_dt = datetime.datetime.fromtimestamp(int(self.t_dt_unix))
        p_value = float(self.p_value)
        p_dt = datetime.datetime.fromtimestamp(int(self.p_dt_unix))
        self.data = [
            {'datetime': t_dt, 'parameter': 't', 'value': t_value},
            {'datetime': p_dt, 'parameter': 'p', 'value': p_value}
        ]

    def get_data(self):
        return self.data





