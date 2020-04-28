import datetime

from wss.data.page import Page
from wss.data.config import config

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
        page_content = Page(url)
        print(page_content.get())