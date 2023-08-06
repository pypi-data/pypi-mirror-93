from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator
import datetime


class ServerDB:
    """
    Класс - оболочка для работы с базой данных сервера.
    Использует SQLite базу данных, реализован с помощью
    SQLAlchemy ORM, используется классический подход.
    """
    class Users:
        """Класс - отображение таблицы всех пользователей."""
        def __init__(self, username, password_hash):
            self.id = None
            self.name = username
            self.last_login = datetime.datetime.now()
            self.password_hash = password_hash
            self.pub_key = None

    class ActiveUsers:
        """Класс - отображение таблицы активных пользователей."""
        def __init__(self, user_id, ip_address, port, login_time):
            self.id = None
            self.user = user_id
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time

    class LoginHistory:
        """Класс - отображение таблицы истории входов."""
        def __init__(self, name, date, ip, port):
            self.id = None
            self.username = name
            self.date_time = date
            self.ip = ip
            self.port = port

    class UsersContacts:
        """Класс - отображение таблицы контактов пользователей."""
        def __init__(self, user, contact):
            self.id = None
            self.user = user
            self.contact = contact

    class UsersHistory:
        """Класс - отображение таблицы истории действий."""
        def __init__(self, user):
            self.id = None
            self.user = user
            self.sent = 0
            self.accepted = 0

    def __init__(self, path):
        self.database_engine = create_engine(f'sqlite:///{path}', echo=False, pool_recycle=7200,
                                             connect_args={'check_same_thread': False})
        self.metadata = MetaData()

        users = Table('Users', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('name', String, unique=True),
                      Column('last_login', DateTime),
                      Column('password_hash', String),
                      Column('pub_key', Text)
                      )

        active_users = Table('Active_users', self.metadata,
                             Column('id', Integer, primary_key=True),
                             Column('user', ForeignKey('Users.id'), unique=True),
                             Column('ip_address', String),
                             Column('port', Integer),
                             Column('login_time', DateTime)
                             )

        user_login_history = Table('Login_history', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('name', ForeignKey('Users.id')),
                                   Column('date_time', DateTime),
                                   Column('ip', String),
                                   Column('port', String)
                                   )

        contacts = Table('Contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('user', ForeignKey('Users.id')),
                         Column('contact', ForeignKey('Users.id'))
                         )

        users_history = Table('History', self.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('user', ForeignKey('Users.id')),
                              Column('sent', Integer),
                              Column('accepted', Integer)
                              )

        self.metadata.create_all(self.database_engine)

        mapper(self.Users, users)
        mapper(self.ActiveUsers, active_users)
        mapper(self.LoginHistory, user_login_history)
        mapper(self.UsersContacts, contacts)
        mapper(self.UsersHistory, users_history)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def user_login(self, username, ip_address, port, key):
        """
        Метод, выполняющийся при входе пользователя, записывает в базу факт входа.
        Обновляет открытый ключ пользователя при его изменении.
        """
        users = self.session.query(self.Users).filter_by(name=username)

        if users.count():
            user = users.first()
            user.last_login = datetime.datetime.now()
            if user.pub_key != key:
                user.pub_key = key
        else:
            raise ValueError('Пользователь не зарегестрирован')

        new_active_user = self.ActiveUsers(user.id, ip_address, port, datetime.datetime.now())
        self.session.add(new_active_user)

        history = self.LoginHistory(user.id, datetime.datetime.now(), ip_address, port)
        self.session.add(history)

        self.session.commit()

    def add_user(self, name, password_hash):
        """
        Метод регистрации пользователя.
        Принимает имя и хэш пароля, создаёт запись в таблице статистики.
        """
        user = self.Users(name, password_hash)
        self.session.add(user)
        self.session.commit()
        user_in_history = self.UsersHistory(user.id)
        self.session.add(user_in_history)
        self.session.commit()

    def remove_user(self, name):
        """Метод, удаляющий пользователя из базы."""
        user = self.session.query(self.Users).filter_by(name=name).first()
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        self.session.query(self.LoginHistory).filter_by(name=user.id).delete()
        self.session.query(self.UsersContacts).filter_by(user=user.id).delete()
        self.session.query(self.UsersContacts).filter_by(contact=user.id).delete()
        self.session.query(self.UsersHistory).filter_by(name=user.id).delete()
        self.session.query(self.Users).filter_by(name=name).delete()
        self.session.commit()

    def get_hash(self, name):
        """Метод получения хэша пароля пользователя."""
        user = self.session.query(self.Users).filter_by(name=name).first()
        return user.password_hash

    def get_pubkey(self, name):
        """Метод получения публичного ключа пользователя."""
        user = self.session.query(self.Users).filter_by(name=name).first()
        return user.pub_key

    def check_user(self, name):
        """Метод, проверяющий существование пользователя."""
        if self.session.query(self.Users).filter_by(name=name).count():
            return True
        return False

    def user_logout(self, username):
        """Метод, фиксирующий отключения пользователя."""
        user = self.session.query(self.Users).filter_by(name=username).first()

        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()

        self.session.commit()

    def process_message(self, sender, recipient):
        """Метод, записывающий в таблицу статистики факт передачи сообщения."""
        sender = self.session.query(self.Users).filter_by(name=sender).first().id
        recipient = self.session.query(self.Users).filter_by(name=recipient).first().id
        sender_history = self.session.query(self.UsersHistory).filter_by(user=sender).first()
        sender_history.sent += 1
        recipient_history = self.session.query(self.UsersHistory).filter_by(user=recipient).first()
        recipient_history.accepted += 1

        self.session.commit()

    def add_contact(self, user, contact):
        """Метод добавления контакта для пользователя."""
        user = self.session.query(self.Users).filter_by(name=user).first()
        contact = self.session.query(self.Users).filter_by(name=contact).first()

        if not contact or self.session.query(self.UsersContacts).filter_by(user=user.id, contact=contact.id).count():
            return

        contact_row = self.UsersContacts(user.id, contact.id)
        self.session.add(contact_row)
        self.session.commit()

    def remove_contact(self, user, contact):
        """Метод удаления контакта пользователя."""
        user = self.session.query(self.Users).filter_by(name=user).first()
        contact = self.session.query(self.Users).filter_by(name=contact).first()

        if not contact:
            return

        self.session.query(self.UsersContacts).filter(
            self.UsersContacts.user == user.id,
            self.UsersContacts.contact == contact.id
        ).delete()
        self.session.commit()

    def all_users(self):
        """Метод, возвращающий список известных пользователей со временем последнего входа."""
        query = self.session.query(
            self.Users.name,
            self.Users.last_login
        )
        return query.all()

    def active_users(self):
        """Метод возвращающий список активных пользователей."""
        query = self.session.query(
            self.Users.name,
            self.ActiveUsers.ip_address,
            self.ActiveUsers.port,
            self.ActiveUsers.login_time
        ).join(self.Users)

        return query.all()

    def login_history(self, username=None):
        """Метод, возвращающий историю входов."""
        query = self.session.query(self.Users.name,
                                   self.LoginHistory.date_time,
                                   self.LoginHistory.ip,
                                   self.LoginHistory.port
                                   ).join(self.Users)
        if username:
            query = query.filter(self.Users.name == username)
        return query.all()

    def get_contacts(self, username):
        """Метод, возвращающий список контактов пользователя."""
        user = self.session.query(self.Users).filter_by(name=username).first()

        query = self.session.query(self.UsersContacts, self.Users.name).filter_by(user=user.id). \
            join(self.Users, self.UsersContacts.contact == self.Users.id)

        return [contact[1] for contact in query.all()]

    def message_history(self):
        """Метод возвращающий статистику сообщений."""
        query = self.session.query(
            self.Users.name,
            self.Users.last_login,
            self.UsersHistory.sent,
            self.UsersHistory.accepted
        ).join(self.Users)

        return query.all()
