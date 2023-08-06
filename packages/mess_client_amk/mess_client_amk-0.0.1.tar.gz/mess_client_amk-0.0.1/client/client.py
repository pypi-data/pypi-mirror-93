import argparse
import os
import sys

from Cryptodome.PublicKey import RSA

from PyQt5.QtWidgets import QApplication, QMessageBox

from client import start_dial
from client.main_win import ClientMainWindow
from client.start_dial import UserNameDialog
from client.client_db import ClientDB
from common.errors import ServerError
from client.client_sock import ClientSocket
from logs.client_log_config import client_logger
from common import settings
from common.decorators import log_decorator


@log_decorator
def argument_parser():
    """
    Парсер аргументов командной строки, возвращает кортеж из 4 элементов
    адрес сервера, порт, имя пользователя, пароль.
    Выполняет проверку на корректность номера порта.
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--addr', default=settings.default_ip, nargs='?')
    arg_parser.add_argument('--port', default=settings.default_port, type=int, nargs='?')
    arg_parser.add_argument('-n', '--name', default=None, nargs='?')
    arg_parser.add_argument('-p', '--password', default='', nargs='?')
    namespace = arg_parser.parse_args(sys.argv[1:])
    server_addr = namespace.addr
    server_port = namespace.port
    client_name = namespace.name
    client_passwd = namespace.password

    if server_port < 1024 or server_port > 65535:
        client_logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.'
        )
        sys.exit(1)

    return server_addr, server_port, client_name, client_passwd


if __name__ == '__main__':
    server_address, server_port, client_name, client_passwd = argument_parser()
    client_logger.debug('Аргументы загружены')

    client_app = QApplication(sys.argv)

    start_dial = UserNameDialog()

    if not client_name or not client_passwd:
        client_app.exec_()
        if start_dial.ok_pressed:
            client_name = start_dial.client_name.text()
            client_passwd = start_dial.client_passwd.text()
            client_logger.debug(f'USERNAME = {client_name}, PASSWD = {client_passwd}.')
        else:
            sys.exit(0)

    client_logger.info(f'Запущен клиент с параметрами: адрес сервера: {server_address}'
                       f'порт: {server_port}, имя пользователя {client_name}')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    key_file = os.path.join(dir_path, f'{client_name}.key')
    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())

    # keys.publichkey().export_key()
    client_logger.debug('Ключи успешно загружены')

    db = ClientDB(client_name)

    try:
        client_sock = ClientSocket(server_port, server_address, db, client_name, client_passwd, keys)
        client_logger.debug('Сокет готов')
    except ServerError as e:
        message = QMessageBox()
        message.critical(start_dial, 'Ошибка сервера', e.text)
        sys.exit(1)
    client_sock.setDaemon(True)
    client_sock.start()

    del start_dial

    main_window = ClientMainWindow(db, client_sock, keys)
    main_window.make_connection(client_sock)
    main_window.setWindowTitle(f'Чат программа alpha release - {client_name}')
    client_app.exec_()

    client_sock.client_sock_shutdown()
    client_sock.join()

