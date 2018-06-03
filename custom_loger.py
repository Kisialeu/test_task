import logging


class Log():
    formatter = logging.Formatter('%(asctime)s  %(levelname)6s:%(module)s: %(funcName)17s() :: %(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    console.setFormatter(formatter)
    file_handler = logging.FileHandler('log.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler) 