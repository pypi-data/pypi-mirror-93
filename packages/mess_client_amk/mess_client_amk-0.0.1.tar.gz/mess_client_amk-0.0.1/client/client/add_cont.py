import logging
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton

sys.path.append('../')
from logs import client_log_config

client_logger = logging.getLogger('client')


class AddContactDialog(QDialog):
    """
    Диалог добавления пользователя в список контактов.
    Предлагает пользователю список возможных контактов и
    добавляет выбранный в контакты.
    """

    def __init__(self, client_sock, db):
        super().__init__()
        self.client_sock = client_sock
        self.db = db

        self.setFixedSize(350, 120)
        self.setWindowTitle('Выберите контакт для добавления:')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Выберите контакт для добавления:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_refresh = QPushButton('Обновить список', self)
        self.btn_refresh.setFixedSize(100, 30)
        self.btn_refresh.move(60, 60)

        self.btn_ok = QPushButton('Добавить', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)

        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        self.contacts_update()
        self.btn_refresh.clicked.connect(self.update_possible_contacts)

    def contacts_update(self):
        """
        Метод заполнения списка возможных контактов.
        Создаёт список всех зарегистрированных пользователей
        за исключением уже добавленных в контакты и самого себя.
        """
        self.selector.clear()
        contacts = set(self.db.get_contacts())
        users = set(self.db.get_all_users())
        users.remove(self.client_sock.username)
        self.selector.addItems(users - contacts)
        print('push_contacts_update: ')

    def update_possible_contacts(self):
        """
        Метод обновления списка возможных контактов. Запрашивает с сервера
        список известных пользователей и обновляет содержимое окна.
        """
        try:
            self.client_sock.users_update()
        except OSError:
            pass
        else:
            client_logger.debug('Обновление списка пользователей выполнено')
            self.contacts_update()





