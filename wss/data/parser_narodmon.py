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
        # {"sensors":[{"id":2620,"type":1,"value":11.9,"time":1590437910,"changed":1590437910,"trend":0}]}
        self.value_t = content_dic['sensors'][0]['value']
        self.dt_unix = content_dic['sensors'][0]['time']

    def set_data_types(self):
        """Clearing data and converting from strings to datetime and int"""
        value = float(self.value_t)
        dt = datetime.datetime.fromtimestamp(int(self.dt_unix))
        self.data = [{'datetime': dt, 'parameter': 't', 'value': value}]

    def get_data(self):
        return self.data





