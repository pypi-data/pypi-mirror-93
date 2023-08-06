import datetime
import os

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator


class ClientDB:
    """
    Класс - оболочка для работы с базой данных клиента.
    Использует SQLite базу данных, реализован с помощью
    SQLAlchemy ORM и используется классический подход.
    """
    class AllUsers:
        """Класс - отображение для таблицы всех пользователей."""
        def __init__(self, username):
            self.id = None
            self.username = username

    class MessageHistory:
        """Класс - отображение для таблицы статистики переданных сообщений."""
        def __init__(self, from_user, to_user, message):
            self.id = None
            self.from_user = from_user
            self.to_user = to_user
            self.message = message
            self.date = datetime.datetime.now()

    class Contacts:
        """Класс - отображение для таблицы контактов."""
        def __init__(self, name):
            self.id = None
            self.name = name

    def __init__(self, username):
        path = os.path.dirname(os.getcwd())
        filename = f'client_{username}.db3'
        self.db_engine = create_engine(f'sqlite:///{os.path.join(path, filename)}', echo=False, pool_recycle=7200,
                                       connect_args={'check_same_thread': False})

        self.metadata = MetaData()

        all_users = Table('all_users', self.metadata,
                          Column('id', Integer, primary_key=True),
                          Column('username', String)
                          )

        message_history = Table('message_history', self.metadata,
                                Column('id', Integer, primary_key=True),
                                Column('from_user', String),
                                Column('to_user', String),
                                Column('message', Text),
                                Column('date', DateTime)
                                )

        contacts = Table('contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True)
                         )

        self.metadata.create_all(self.db_engine)

        mapper(self.AllUsers, all_users)
        mapper(self.MessageHistory, message_history)
        mapper(self.Contacts, contacts)

        Session = sessionmaker(bind=self.db_engine)
        self.session = Session()

        self.session.query(self.Contacts).delete()
        self.session.commit()

    def add_contact(self, name):
        """Метод добавляющий контакт в базу данных."""
        if not self.session.query(self.Contacts).filter_by(name=name).count():
            contact = self.Contacts(name)
            self.session.add(contact)
            self.session.commit()

    def contacts_clear(self):
        """Метод очищающий таблицу со списком контактов."""
        self.session.query(self.Contacts).delete()

    def del_contact(self, name):
        """Метод удаляющий определённый контакт."""
        self.session.query(self.Contacts).filter_by(name=name).delete()

    def add_all_users(self, users):
        """Метод заполняющий таблицу известных пользователей."""
        self.session.query(self.AllUsers).delete()
        for user in users:
            user_row = self.AllUsers(user)
            self.session.add(user_row)
            self.session.commit()

    def save_message(self, from_user, to_user, message):
        """Метод сохраняющий сообщение в базе данных."""
        message_row = self.MessageHistory(from_user, to_user, message)
        self.session.add(message_row)
        self.session.commit()

    def get_contacts(self):
        """Метод возвращающий список всех контактов."""
        return [contact[0] for contact in self.session.query(self.Contacts.name).all()]

    def get_all_users(self):
        """Метод возвращающий список всех известных пользователей."""
        return [user[0] for user in self.session.query(self.AllUsers.username).all()]

    def check_user(self, name):
        """Метод проверяющий существует ли пользователь."""
        if self.session.query(self.AllUsers).filter_by(username=name).count():
            return True
        return False

    def check_contact(self, name):
        """Метод проверяющий существует ли контакт."""
        if self.session.query(self.Contacts).filter_by(name=name).count():
            return True
        return False

    def get_history(self, contact):
        """Метод возвращающий историю сообщений с определённым пользователем."""
        query = self.session.query(self.MessageHistory).filter_by(from_user=contact)
        return [(history.from_user, history.to_user, history.message, history.date) for history in query.all()]


if __name__ == '__main__':
    test_db = ClientDB('user_1')
    # for user in ['user_2', 'user_3', 'user_4']:
    #     test_db.add_contact(user)
    #
    # test_db.add_all_users(['user_1', 'user_2', 'user_3', 'user_4'])
    # test_db.save_message('user_1', 'user_2', 'Hello!')
    # test_db.save_message('user_2', 'user_1', 'Hi!')
    #
    # print(test_db.get_contacts())
    # print(test_db.get_all_users())
    # print(test_db.check_user('user_1'))
    # print(test_db.check_user('user_5'))
    # print(test_db.get_history('user_1'))
    # print(test_db.get_history(to_user='user_1'))
    # print(test_db.get_history('user_3'))
    # test_db.del_contact('user_4')
    # print(test_db.get_contacts())
