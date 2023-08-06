import json

from .decorators import log_decorator
from .errors import IncorrectDataReceivedError, NonDictInputError
from .settings import MAX_PACK_LEN, ENCODING


@log_decorator
def get_message(sock):
    """
    Функция приёма сообщений от удалённых компьютеров.
    Принимает сообщения JSON, декодирует полученное сообщение
    и проверяет что получен словарь.
    :param sock: сокет для передачи данных.
    :return: словарь - сообщение.
    """
    encoded_message = sock.recv(MAX_PACK_LEN)
    if isinstance(encoded_message, bytes):
        json_message = encoded_message.decode(ENCODING)
        message = json.loads(json_message)
        if isinstance(message, dict):
            return message
        else:
            raise IncorrectDataReceivedError
    else:
        raise IncorrectDataReceivedError


@log_decorator
def send_message(sock, message):
    """
    Функция отправки словарей через сокет.
    Кодирует словарь в формат JSON и отправляет через сокет.
    :param sock: сокет для передачи
    :param message: словарь для передачи
    :return: ничего не возвращает
    """
    if not isinstance(message, dict):
        raise NonDictInputError
    json_message = json.dumps(message)
    encoded_message = json_message.encode(ENCODING)
    sock.send(encoded_message)
