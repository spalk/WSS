
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
        w = WeatherForecast(service)
        w.get_forecast()
