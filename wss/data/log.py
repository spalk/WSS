import logging
from logging.handlers import SMTPHandler

from wss.data.config import config


def logger_setup(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    if config['LOGGING']['console'] == '1':
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if config['LOGGING']['file'] == '1':
        file_handler = logging.FileHandler('wss/wss.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if config['LOGGING']['email'] == '1':
        mail_handler = SMTPHandler(
            mailhost=(config['EMAIL']['host'], config['EMAIL']['port']),
            fromaddr=config['EMAIL']['from'],
            toaddrs=config['EMAIL']['recipient'],
            subject='WSS - Weather Service Statistics - Logging: CRITICAL',
            credentials=(config['EMAIL']['login'], config['EMAIL']['password']),
            secure=()
        )
        mail_handler.setFormatter(formatter)
        # send to mail only critical logs
        mail_handler.setLevel(logging.CRITICAL)
        logger.addHandler(mail_handler)

    return logger
