import logging
import os
import sys

sys.path.append('../')
from common.settings import LOG_LEVEL


client_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(client_formatter)
stream_handler.setLevel(logging.ERROR)

path = os.path.join(os.path.dirname(os.getcwd()), 'client.log')

file_handler = logging.FileHandler(path, encoding='utf8')
file_handler.setFormatter(client_formatter)

client_logger = logging.getLogger('client')
client_logger.addHandler(stream_handler)
client_logger.addHandler(file_handler)
client_logger.setLevel(LOG_LEVEL)


if __name__ == '__main__':
    client_logger.info('Информационное  сообщение')
    client_logger.debug('Отладочное сообщение')
    client_logger.error('Сообщение об ошибке')
    client_logger.critical('Критическая ошибка')

