from wss.data.parser_rp5 import ParserRP5
from wss.data.parser_yandex import ParserYandex

import logging

logger = logging.getLogger('root')


class Parser:
    def __init__(self, service, page_content):
        self.service = service
        self.page_content = page_content

    def get_data(self):
        if self.service == 'rp5':
            try:
                logger.debug('Try parse ' + self.service)
                data = self.parse_rp5()
                return data
            except Exception as e:
                logger.critical(e, exc_info=True)
        elif self.service == 'yandex':
            try:
                logger.debug('Try parse ' + self.service)
                data = self.parse_yandex()
                return data
            except Exception as e:
                logger.critical(e, exc_info=True)

    def parse_rp5(self):
        parser = ParserRP5()
        parser.feed(self.page_content.decode('utf-8'))
        parser.set_data_types()
        data = parser.get_data()
        return data

    def parse_yandex(self):
        parser = ParserYandex()
        parser.feed(self.page_content.decode('utf-8'))
        parser.set_data_types()
        data = parser.get_data()
        return data
