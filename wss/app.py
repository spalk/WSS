
from wss.data.config import config
from wss.data.weatherforecast import WeatherForecast

import logging
logger = logging.getLogger('root')


def run():
    active_services = []

    for service in config['SERVICES']:
        if config['SERVICES'][service] == '1':
            active_services.append(service)

    all_data = []
    for service in active_services:
        logger.debug('Get forecast from: ' + service)
        try:
            w = WeatherForecast(service)
            data = w.get_forecast()
            for line in data:
                line['service'] = service
                all_data.append(line)
        except Exception as e:
            logger.critical(e, exc_info=True)
            pass

    for line in all_data:
        print(line)



