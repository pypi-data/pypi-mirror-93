import argparse
import binascii
import hashlib
import hmac
import json
import logging
import socket
import sys
import threading
import time

from PyQt5.QtCore import QObject, pyqtSignal

sys.path.append('../')
from common.errors import ServerError
from logs import client_log_config
from common.utils import send_message, get_message

client_logger = logging.getLogger('client')

sock_lock = threading.Lock()


class ClientSocket(threading.Thread, QObject):
    """
    Класс реализующий транспортную подсистему клиентского
    модуля. Отвечает за взаимодействие с сервером.
    """
    new_message = pyqtSignal(dict)
    message_205 = pyqtSignal()
    connection_lost = pyqtSignal()

    def __init__(self, port, ip_address, database, username, passwd, keys):
        threading.Thread.__init__(self)
        QObject.__init__(self)

        self.database = database
        self.client_sock = None
        self.username = username
        self.password = passwd
        self.keys = keys
        self.connection_init(port, ip_address)

        try:
            self.users_update()
            self.contacts_update()
        except OSError as e:
            if e.errno:
                client_logger.critical('Потеряно соединение с сервером')
                raise ServerError('Потеряно сооединение с сервером')
            client_logger.error('Timout соединения при обновлении списка пользователей')
        except json.JSONDecodeError:
            client_logger.critical(f'Потеряно соединение с сервером')
            raise ServerError('Потеряно соединение с сервером')

        self.running = True

    def connection_init(self, port, ip_address):
        """Метод, отвечающий за устанновку соединения с сервером."""
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client_sock.settimeout(5)

        connected = False
        for i in range(5):
            client_logger.info(f'Попытка подключения №{i + 1}')
            try:
                self.client_sock.connect((ip_address, port))
            except (OSError, ConnectionRefusedError):
                pass
            else:
                connected = True
                client_logger.debug('Соединение установлено')
                break
            time.sleep(1)

        if not connected:
            client_logger.critical('Не удалось установить соединение с сервером')
            raise ServerError('Не удалось установить соединение с сервером')

        client_logger.debug('Запуск диалога авторизации')

        passwd_bytes = self.password.encode('utf-8')
        salt = self.username.lower().encode('utf-8')
        passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bytes, salt, 10000)
        passwd_hash_string = binascii.hexlify(passwd_hash)

        client_logger.debug(f'Хеш пароля: {passwd_hash_string}')

        pubkey = self.keys.publickey().export_key().decode('ascii')

        with sock_lock:
            presense = {
                'action': 'presence',
                'time': time.time(),
                'user': {
                    'account_name': self.username,
                    'public_key': pubkey
                }
            }
            client_logger.debug(f'Приветственное сообщение: {presense}')

            try:
                send_message(self.client_sock, presense)
                ans = get_message(self.client_sock)
                if 'response' in ans:
                    if ans['response'] == 400:
                        raise ServerError(ans['error'])
                    elif ans['response'] == 511:
                        ans_data = ans['data']
                        hash = hmac.new(passwd_hash_string, ans_data.encode('utf-8'), 'MD5')
                        digest = hash.digest()
                        my_ans = {
                            'response': 511,
                            'data': binascii.b2a_base64(digest).decode('ascii')
                        }
                        send_message(self.client_sock, my_ans)
                        self.process_server_ans(get_message(self.client_sock))

            except (OSError, json.JSONDecodeError) as e:
                client_logger.critical('Ошибка соединения', exc_info=e)
                raise ServerError('Сбой соединения в процессе авторизации.')

        client_logger.info('Соединение с сервером успешно установлено.')

    def process_server_ans(self, message):
        """Метод обработчик поступающих сообщений с сервера."""
        client_logger.debug(f'Разбор сообщения от сервера {message}')

        if 'response' in message:
            if message['response'] == 200:
                return '200 : OK'
            elif message['response'] == 400:
                raise ServerError(f'400 : {message["error"]}')
            elif message['response'] == 205:
                self.users_update()
                self.contacts_update()
                self.message_205.emit()
            else:
                client_logger.debug(f'Принят неизвестный код подтверждения {message["response"]}')

        elif 'action' in message and message['action'] == 'message' and 'from' in message and 'to' in message \
                and 'message_text' in message and message['to'] == self.username:
            client_logger.debug(f'Получено сообщение от пользователя {message["from"]}:{message["message_text"]}')
            self.new_message.emit(message)

    def contacts_update(self):
        """Метод, обновляющий с сервера список контактов."""
        client_logger.debug(f'Запрос контактов для пользователя {self.username}')
        request = {
            'action': 'get_contacts',
            'time': time.time(),
            'user': self.username
        }
        client_logger.debug(f'Сформирован запрос {request}')
        with sock_lock:
            send_message(self.client_sock, request)
            answer = get_message(self.client_sock)
        client_logger.debug(f'Получен ответ {answer}')
        if 'response' in answer and answer['response'] == 202:
            for contact in answer['list_info']:
                self.database.add_contact(contact)
        else:
            client_logger.error('Не удалось обновить список контактов')

    def users_update(self):
        """Метод, обновляющий с сервера список пользователей."""
        client_logger.debug(f'Запрос списка пользователей от {self.username}')
        request = {
            'action': 'users_request',
            'time': time.time(),
            'account_name': self.username
        }
        with sock_lock:
            send_message(self.client_sock, request)
            answer = get_message(self.client_sock)
        if 'response' in answer and answer['response'] == 202:
            self.database.add_all_users(answer['list_info'])
        else:
            client_logger.error('Не удалось обновить список известных пользователей.')

    def key_request(self, user):
        """Метод, запрашивающий с сервера публичный ключ пользователя."""
        client_logger.debug(f'Запрос публичного ключа для {user}')
        request = {
            'action': 'public_key_request',
            'time': time.time(),
            'account_name': user
        }
        with sock_lock:
            send_message(self.client_sock, request)
            answer = get_message(self.client_sock)
        if 'response' in answer and answer['response'] == 511:
            return answer['data']
        else:
            client_logger.error(f'Не удалось получить ключ {user}')

    def add_contact(self, contact_name):
        """Метод, отправляющий на сервер сведения о добавлении контакта."""
        client_logger.debug(f'Создание контакта {contact_name}')
        request = {
            'action': 'add_contact',
            'time': time.time(),
            'user': self.username,
            'account_name': contact_name
        }
        with sock_lock:
            send_message(self.client_sock, request)
            self.process_server_ans(get_message(self.client_sock))

    def remove_contact(self, contact):
        """Метод, отправляющий на сервер сведения о удалении контакта."""
        client_logger.debug(f'Удаление контакта {contact}')
        request = {
            'action': 'remove_contact',
            'time': time.time(),
            'user': self.username,
            'account_name': contact
        }
        with sock_lock:
            send_message(self.client_sock, request)
            self.process_server_ans(get_message(self.client_sock))

    def client_sock_shutdown(self):
        """Метод, уведомляющий сервер о завершении работы клиента."""
        self.running = False
        message = {
            'action': 'exit',
            'time': time.time(),
            'account_name': self.username
        }
        with sock_lock:
            try:
                send_message(self.client_sock, message)
            except OSError:
                pass
        client_logger.debug('Клиент завершает работу')
        time.sleep(0.5)

    def send_message(self, to_user, message):
        """Метод, отправляющий на сервер сообщения для пользователя."""
        message_dict = {
            'action': 'message',
            'from': self.username,
            'to': to_user,
            'time': time.time(),
            'message_text': message
        }
        client_logger.debug(f'Сфомирован словать сообщения: {message_dict}')

        with sock_lock:
            send_message(self.client_sock, message_dict)
            self.process_server_ans(get_message(self.client_sock))
            client_logger.info(f'Отправлено сообщение для пользователя {to_user}')

    def run(self):
        client_logger.debug('Запущен процесс - приемник сообщений с сервера')

        while self.running:
            time.sleep(1)
            message = None
            with sock_lock:
                try:
                    self.client_sock.settimeout(0.5)
                    message = get_message(self.client_sock)
                except OSError as e:
                    if e.errno:
                        client_logger.critical(f'Потеряно соединение с сервером')
                        self.running = False
                        self.connection_lost.emit()
                except(ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError, TypeError):
                    client_logger.debug(f'Потеряно соединение с сервером')
                    self.running = False
                    self.connection_lost.emit()
                finally:
                    self.client_sock.settimeout(5)

            if message:
                client_logger.debug(f'Принято сообщение с сервера: {message}')
                self.process_server_ans(message)

