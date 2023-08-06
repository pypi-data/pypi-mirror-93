from logging import handlers, Formatter, StreamHandler, ERROR as LOGGING_ERROR, DEBUG, getLogger
import os
import sys

sys.path.append(os.path.join(os.getcwd(), '..'))
from common_oop import CommonApi

common = CommonApi()

SERVER_FORMATTER = Formatter('%(asctime)-10s %(levelname)s %(module)-30s %(message)s')

PATH = os.getcwd()
PATH = os.path.join(PATH, '../logs/server.log')

FILE_HANDLER = handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='D')
FILE_HANDLER.setFormatter(SERVER_FORMATTER)

STREAM_HANDLER = StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(SERVER_FORMATTER)
STREAM_HANDLER.setLevel(LOGGING_ERROR)

LOGGER = getLogger('server')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(common.LOGGING_LEVEL)

if __name__ == '__main__':
    LOGGER.debug('Отладка')
    LOGGER.info('Информация')
    LOGGER.warning('Внимание')
    LOGGER.error('Ошибка')
    LOGGER.critical('Критическая ошибка')
