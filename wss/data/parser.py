from wss.data.parser_rp5 import ParserRP5
from wss.data.parser_yandex import ParserYandex

import logging

logger = logging.getLogger('root')


class ParserService:
    def __init__(self, service, page_content):
        if service == 'rp5':
            self.parser = ParseRP5(page_content)
        elif service == 'yandex':
            self.parser = ParseYandex(page_content)
        self.parser.set_parser()

    def get_data(self):
        return self.parser.get_data()


class Parser:
    def __init__(self, page_content):
        self.page_content = page_content

    def get_data(self):
        try:
            data = self.parse()
            return data
        except Exception as e:
            logger.critical(e, exc_info=True)

    def parse(self):
        self.parser.feed(self.page_content.decode('utf-8'))
        self.parser.set_data_types()
        data = self.parser.get_data()
        return data


class ParseRP5(Parser):
    def set_parser(self):
        logger.debug('Try to parse RP5')
        self.parser = ParserRP5()


class ParseYandex(Parser):
    def set_parser(self):
        logger.debug('Try to parse Yandex')
        self.parser = ParserYandex()
