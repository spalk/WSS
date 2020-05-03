from wss.data.parser_rp5 import ParserRP5

import logging
logger = logging.getLogger('root')


class Parser:
    def __init__(self, service, page_content):
        self.service = service
        self.page_content = page_content
        logger.debug('Start parsing')

    def get_data(self):

        if self.service == 'rp5':
            data = self.parse_rp5()
        return data

    def parse_rp5(self):
        parser = ParserRP5()
        parser.feed(self.page_content.decode('utf-8'))
        parser.set_data_types()
        logger.debug('Raw data parsed: ' + str(parser.cnt_raw_data))
        logger.debug('Clean data parsed: ' + str(parser.cnt_clean_data))
        data = parser.get_data()
        return data
