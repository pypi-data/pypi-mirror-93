import base64
import json
import logging
import sys

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtWidgets import QMainWindow, QMessageBox, qApp
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA


from .del_cont import DelContactDialog
from .main_window_conv import Ui_MainClientWindow
from .add_cont import AddContactDialog

sys.path.append('../')
from common.errors import ServerError
from logs import client_log_config


client_logger = logging.getLogger('client')


class ClientMainWindow(QMainWindow):
    """
    Класс - основное окно пользователя.
    Содержит всю основную логику работы клиентского модуля.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированого файла main_window_conv.py
    """
    def __init__(self, db, client_sock, keys):
        super().__init__()
        self.db = db
        self.client_sock = client_sock

        self.decrypter = PKCS1_OAEP.new(keys)

        self.ui = Ui_MainClientWindow()
        self.ui.setupUi(self)

        self.ui.menu_exit.triggered.connect(qApp.exit)

        self.ui.btn_send.clicked.connect(self.send_message)

        self.ui.btn_add_contact.clicked.connect(self.add_cont_win)
        self.ui.menu_add_contact.triggered.connect(self.add_cont_win)

        self.ui.btn_remove_contact.clicked.connect(self.del_contact_win)
        self.ui.menu_del_contact.triggered.connect(self.del_contact_win)

        self.contacts_model = None
        self.history_model = None
        self.messages = QMessageBox()
        self.current_chat = None
        self.encryptor = None
        self.ui.list_messages.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.list_messages.setWordWrap(True)

        self.ui.list_contacts.doubleClicked.connect(self.select_active_user)

        self.clients_update()
        self.set_disabled_input()
        self.show()

    def set_disabled_input(self):
        """Метод, делающий поля ввода неактивными"""
        self.ui.label_new_message.setText('Для выбора получателя дважды кликните на него в окне контактов')
        self.ui.text_message.clear()
        if self.history_model:
            self.history_model.clear()

        self.ui.btn_clear.setDisabled(True)
        self.ui.btn_send.setDisabled(True)
        self.ui.text_message.setDisabled(True)

        self.encryptor = None
        self.current_chat = None
        self.current_chat_key = None

    def history_update(self):
        """
        Метод заполняющий соответствующий QListView
        историей переписки с текущим собеседником.
        """
        history = sorted(self.db.get_history(self.current_chat), key=lambda item: item[3])
        if not self.history_model:
            self.history_model = QStandardItemModel()
            self.ui.list_messages.setModel(self.history_model)

        self.history_model.clear()

        length = len(history)
        start_ind = 0
        if length > 20:
            start_ind = length - 20

        for i in range(start_ind, length):
            item = history[i]
            if item[1] == 'in':
                message = QStandardItem(f'Входящее от {item[3].replace(microsecond=0)}:\n {item[2]}')
                message.setEditable(False)
                message.setBackground(QBrush(QColor(255, 213, 213)))
                message.setTextAlignment(Qt.AlignLeft)
                self.history_model.appendRow(message)
            else:
                message = QStandardItem(f'Исходящее от {item[3].replace(microsecond=0)}:\n {item[2]}')
                message.setEditable(False)
                message.setTextAlignment(Qt.AlignRight)
                message.setBackground(QBrush(QColor(204, 255, 204)))
                self.history_model.appendRow(message)
        self.ui.list_messages.scrollToBottom()

    def select_active_user(self):
        """Метод обработчик события двойного клика по списку контактов."""
        self.current_chat = self.ui.list_contacts.currentIndex().data()
        self.set_active()

    def set_active(self):
        """Метод активации чата с собеседником."""
        try:
            self.current_chat_key = self.client_sock.key_request(self.current_chat)
            client_logger.debug(f'Загружен открытый ключ для {self.current_chat}')
            if self.current_chat_key:
                self.encryptor = PKCS1_OAEP.new(RSA.import_key(self.current_chat_key))
        except (OSError, json.JSONDecodeError):
            self.current_chat_key = None
            self.encryptor = None
            client_logger.debug(f'Не удалось получить ключ для {self.current_chat}')

        if not self.current_chat_key:
            self.messages.warning(self, 'Ошибка', 'Для выбранного пользователя нет ключа шифрования')
            return

        self.ui.label_new_message.setText(f'Введите сообщение для {self.current_chat}:')
        self.ui.btn_clear.setDisabled(False)
        self.ui.btn_send.setDisabled(False)
        self.ui.text_message.setDisabled(False)

        self.history_update()

    def clients_update(self):
        """Метод, обновляющий список контактов."""
        contacts = self.db.get_contacts()
        self.contacts_model = QStandardItemModel()
        for i in sorted(contacts):
            item = QStandardItem(i)
            item.setEditable(False)
            self.contacts_model.appendRow(item)
        self.ui.list_contacts.setModel(self.contacts_model)

    def add_cont_win(self):
        """Метод, создающий окно - диалог добавления контакта"""
        global select_dialog
        select_dialog = AddContactDialog(self.client_sock, self.db)
        select_dialog.btn_ok.clicked.connect(lambda: self.add_contact_action(select_dialog))
        select_dialog.show()

    def add_contact_action(self, item):
        """Метод обработчк нажатия кнопки 'Добавить'"""
        new_contact = item.selector.currentText()
        self.add_contact(new_contact)
        item.close()

    def add_contact(self, contact):
        """
        Метод добавляющий контакт в серверную и клиентсткую BD.
        После обновления баз данных обновляет и содержимое окна.
        """
        try:
            self.client_sock.add_contact(contact)
        except ServerError as e:
            self.messages.critical(self, 'Ошибка сервера', e.text)
        except OSError as e:
            if e.errno:
                self.messages.critical(self, 'Ошибка', 'Потеряно соеднинение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения')
        else:
            self.db.add_contact(contact)
            contact = QStandardItem(contact)
            contact.setEditable(False)
            self.contacts_model.appendRow(contact)
            client_logger.info(f'Успешно добавлен контакт {contact}')
            self.messages.information(self, 'Успех', 'Контакт успешно добавлен')

    def del_contact_win(self):
        """Метод создающий окно удаления контакта."""
        global remove_dialog
        remove_dialog = DelContactDialog(self.db)
        remove_dialog.btn_ok.clicked.connect(lambda: self.del_contact(remove_dialog))
        remove_dialog.show()

    def del_contact(self, item):
        """
        Метод удаляющий контакт из серверной и клиентсткой BD.
        После обновления баз данных обновляет и содержимое окна.
        """
        selected = item.selector.currentText()
        try:
            self.client_sock.remove_contact(selected)
        except ServerError as e:
            self.messages.critical(self, 'Ошибка сервера', e.text)
        except OSError as e:
            if e.errno:
                self.messages.critical(self, 'Ошибка', 'Потеряно сооединение с сервером')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        else:
            self.db.del_contact(selected)
            self.clients_update()
            client_logger.info(f'Успешно удален контакт {selected}')
            self.messages.information(self, 'Успех', 'Контакт успешно удален.')
            item.close()
            if selected == self.current_chat:
                self.current_chat = None
                self.set_disabled_input()

    def send_message(self):
        """
        Метод отправки сообщения текущему собеседнику.
        Реализует шифрование сообщения и его отправку.
        """
        message = self.ui.text_message.toPlainText()
        self.ui.text_message.clear()
        if not message:
            return
        message_text_encrypted = self.encryptor.encrypt(message.encode('utf8'))
        message_text_encrypted_base64 = base64.b64encode(message_text_encrypted)

        try:
            self.client_sock.send_message(self.current_chat, message_text_encrypted_base64.decode('ascii'))
            pass
        except ServerError as e:
            self.messages.critical(self, 'Ошибка', e.text)
        except OSError as e:
            if e.errno:
                self.messages.critical(self, 'Ошибка', 'Потеряно соединение с сервером')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        except (ConnectionResetError, ConnectionError):
            self.messages.critical(self, 'Ошибка', 'Потеряно соединение с сервером')
            self.close()
        else:
            self.db.save_message(self.current_chat, 'out', message)
            client_logger.debug(f'Отправлено сообщение для {self.current_chat}: {message}')
            self.history_update()

    @pyqtSlot(dict)
    def message(self, message):
        """
        Слот обработчик поступающих сообщений, выполняет дешифровку
        сообщений и их сохранение в истории сообщений.
        Запрашивает пользователя если пришло сообщение не от текущего
        собеседника. При необходимости меняет собеседника.
        """
        encrypted_message = base64.b64decode(message['message_text'])
        try:
            decrypted_message = self.decrypter.decrypt(encrypted_message)
        except (ValueError, TypeError):
            self.messages.warning(self, 'Ошибка', 'Не удалось декодировать сообщение.')
            return
        self.db.save_message(self.current_chat, 'in', decrypted_message.decode('utf8'))

        sender = message['from']
        if sender == self.current_chat:
            self.history_update()
        else:
            if self.db.check_contact(sender):
                if self.messages.question(self, 'Новое сообщение',
                                          f'Получено новое сообщение от {sender}, открыть чат с ним?',
                                          QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
                    self.current_chat = sender
                    self.db.save_message(self.current_chat, 'in', decrypted_message.decode('utf8'))
                    self.set_active()
            else:
                print('NO')
                if self.messages.question(self, 'Новое сообщение',
                                          f'Получено новое сообщение от {sender}.\n'
                                          f' Данного пользователя нет в вашем контакт-листе.'
                                          f'\n Добавить в контакты и открыть чат с ним?',
                                          QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
                    self.add_contact(sender)
                    self.current_chat = sender
                    self.db.save_message(self.current_chat, 'in', decrypted_message.decode('utf8'))
                    self.set_active()

    @pyqtSlot()
    def connection_lost(self):
        """
        Слот обработчик потери соеднинения с сервером.
        Выдаёт окно предупреждение и завершает работу приложения.
        """
        self.messages.warning(self, 'Сбой соединения', 'Потеряно соединение с сервером.')
        self.close()

    @pyqtSlot()
    def sig_205(self):
        """Слот выполняющий обновление баз данных по команде сервера."""
        if  self.current_chat and not self.db.check_contact(self.current_chat):
            self.messages.warning(self, 'Сожалею', 'Собеседник был удален с всервера')
            self.set_disabled_input()
            self.current_chat = None
        self.clients_update()

    def make_connection(self, obj):
        """Метод, обеспечивающий соединение сигналов и слотов."""
        obj.new_message.connect(self.message)
        obj.connection_lost.connect(self.connection_lost)
        obj.message_205.connect(self.sig_205)

