import logging
from wss import app
from wss.data import log

if __name__ == '__main__':
    logger = log.logger_setup('root')
    logger.debug('START APP')
    app.run()
