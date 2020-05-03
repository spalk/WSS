import datetime

from wss.data.config import config
from wss.data.page import Page
from wss.data.parser import Parser

import logging
logger = logging.getLogger('root')


class WeatherForecast:
    """WeatherForecast class description"""

    def __init__(self, service):
        self.service = service
        self.dt_init = datetime.datetime.now()
        logger.debug('WeatherForecast init for service: ' + service)

    def get_forecast(self):
        url = config[self.service]['url']
        page_content = Page(url).get()
        forecast_data = Parser(self.service, page_content)
        return forecast_data.get_data()
