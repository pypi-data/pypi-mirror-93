import inspect
import sys
import traceback
from socket import socket

sys.path.append('../')
from logs import client_log_config
from logs import server_log_config
import logging

if sys.argv[0].find('client') == -1:
    logger = logging.getLogger('server')
else:
    logger = logging.getLogger('client')


def log_decorator(func):
    """
    Декоратор, выполняющий логирование вызовов функций.
    Сохраняет события типа debug, содержащие
    информацию о имени вызываемой функиции, параметры с которыми
    вызывается функция, и модуль, вызывающий функцию.
    """

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.debug(
            f'Была вызвана функция {func.__name__} c параметрами {args}, {kwargs}. '
            f'Вызов из модуля {func.__module__}.'
            f'Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}.'
            f'Вызов из функции {inspect.stack()[1][3]}'
        )
        return result
    return wrapper


class LogDecorator:
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            logger.debug(
                f'Была вызвана функция {func.__name__} c параметрами {args}, {kwargs}. '
                f'Вызов из модуля {func.__module__}.'
                f' Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}.'
                f'Вызов из функции {inspect.stack()[1][3]}'
            )
            return result
        return wrapper


def login_required(func):
    """
    Декоратор, проверяющий, что клиент авторизован на сервере.
    Проверяет, что передаваемый объект сокета находится в
    списке авторизованных клиентов.
    За исключением передачи словаря-запроса
    на авторизацию. Если клиент не авторизован,
    генерирует исключение TypeError
    """
    def checker(*args, **kwargs):
        # проверяем, что первый аргумент - экземпляр MessageProcessor
        # Импортить необходимо тут, иначе ошибка рекурсивного импорта.
        from server.server_core import MessageProcessor
        if isinstance(args[0], MessageProcessor):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    # Проверяем, что данный сокет есть в списке names класса
                    # MessageProcessor
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True

            # Теперь надо проверить, что передаваемые аргументы не presence
            # сообщение. Если presense, то разрешаем
            for arg in args:
                if isinstance(arg, dict):
                    if 'action' in arg and arg['action'] == 'presense':
                        found = True
            # Если не не авторизован и не сообщение начала авторизации, то
            # вызываем исключение.
            if not found:
                raise TypeError
        return func(*args, **kwargs)

    return checker
