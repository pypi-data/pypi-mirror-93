import logging
from logging import handlers
import os
import sys

sys.path.append('../')
from common.settings import LOG_LEVEL



server_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

log_path = os.path.join(os.path.dirname(os.getcwd()), 'server.log')

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(server_formatter)
stream_handler.setLevel(logging.INFO)

file_handler = handlers.TimedRotatingFileHandler(log_path, encoding='utf8', interval=1, when='D')
file_handler.setFormatter(server_formatter)

server_logger = logging.getLogger('server')
server_logger.addHandler(stream_handler)
server_logger.addHandler(file_handler)
server_logger.setLevel(LOG_LEVEL)


if __name__ == '__main__':
    server_logger.info('Информационное  сообщение')
    server_logger.debug('Отладочное сообщение')
    server_logger.error('Сообщение об ошибке')
    server_logger.critical('Критическая ошибка')