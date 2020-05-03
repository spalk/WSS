
from wss.data.config import config
from wss.data.weatherforecast import WeatherForecast

import logging
logger = logging.getLogger('root')


def run():
    active_services = []

    for service in config['SERVICES']:
        if config['SERVICES'][service] == '1':
            active_services.append(service)

    for service in active_services:
        logger.debug('Get forecast from: ' + service)
        w = WeatherForecast(service)
        data = w.get_forecast()

        for d in data:
            print(d)
