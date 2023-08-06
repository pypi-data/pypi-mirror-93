import binascii
import hmac
import json
import logging
import os
import socket
import select
import sys
import threading

from .server_db import ServerDB

sys.path.append('../')
from common.settings import default_port, MAX_NUM_CONN
from common.decorators import log_decorator
from common.descriptors import ServerPort
from common import utils

server_logger = logging.getLogger('server')


class MessageProcessor(threading.Thread):
    """
    Основной класс сервера. Принимает содинения, словари - пакеты
    от клиентов, обрабатывает поступающие сообщения.
    Работает в качестве отдельного потока.
    """
    port = ServerPort()

    def __init__(self, listen_address, listen_port, db):
        self.addr = listen_address
        self.port = listen_port

        self.db = db

        self.sock = None

        self.clients = []

        self.listen_sockets = None
        self.error_sockets = None

        self.running = True

        self.names = dict()

        super().__init__()

    def run(self):
        """Метод основного цикла потока."""
        self.create_socket()

        while self.running:
            try:
                client, client_addr = self.sock.accept()
            except OSError:
                pass
            else:
                server_logger.info(f'Установлено соединение с клиентом: {client_addr}.')
                client.settimeout(5)
                self.clients.append(client)

            receive_data_list = []
            send_data_list = []
            error_list = []

            try:
                if self.clients:
                    receive_data_list, self.listen_sockets, self.error_sockets = select.select(
                                                                                    self.clients, self.clients, [], 0
                                                                                  )
            except OSError as e:
                server_logger.error(f'Ошибка работы с сокетами: {e.errno}')

            if receive_data_list:
                for client_with_message in receive_data_list:
                    try:
                        self.process_client_message(utils.get_message(client_with_message), client_with_message)
                    except (OSError, json.JSONDecodeError, TypeError) as e:
                        server_logger.debug(f'Ошибка получения данных от клиента.', exc_info=e)
                        self.remove_client(client_with_message)

    def remove_client(self, client):
        """
        Метод обработчик клиента, с которым прервана связь.
        Ищет клиента и удаляет его из списков и базы.
        """
        server_logger.info(f'Клиент {client.getpeername()} отключился от сервера.')
        for name in self.names:
            if self.names[name] == client:
                self.db.user_logout(name)
                del self.names[name]
                break
        self.clients.remove(client)
        client.close()

    def create_socket(self):
        """Метод инициализации сокета."""
        server_logger.info(f'Запущен сервер, порт для подключений: {self.port}, '
                           f'адрес с которого принимаются подключения: {self.addr}. '
                           f'Если адрес не указан, принимаются соединения с любых адресов.')
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.addr, self.port))
        server_socket.settimeout(0.5)

        self.sock = server_socket
        self.sock.listen(MAX_NUM_CONN)

    def process_message(self, message):
        """Метод отправки сообщения клиенту."""
        if message['to'] in self.names and self.names[message['to']] in self.listen_sockets:
            try:
                utils.send_message(self.names[message['to']], message)
                server_logger.info(
                    f'Отправлено сообщение пользователю {message["to"]} от пользователя {message["from"]}.'
                )
            except OSError:
                self.remove_client(message['to'])
        elif message['to'] in self.names and self.names[message['to']] not in self.listen_sockets:
            server_logger.error(
                f'Связь с клиентом {message["to"]} была потеряна. Соединение закрыто, доставка невозможна.'
            )
            self.remove_client(self.names[message['to']])
        else:
            server_logger.info(f'Пользователь {message["to"]} не зарегистрирован на сервере')

    def process_client_message(self, message, client):
        """Метод отбработчик поступающих сообщений."""
        server_logger.debug(f'Разбор сообщения от клиента: {message}')

        if 'action' in message and message['action'] == 'presence' and 'time' in message \
                and 'user' in message:
            self.autorize_user(message, client)

        elif 'action' in message and message['action'] == 'message' and 'to' in message and 'time' in message\
                and 'from' in message and 'message_text' in message and self.names[message['from']] == client:
            if message['to'] in self.names:
                self.db.process_message(message['from'], message['to'])
                self.process_message(message)
                try:
                    utils.send_message(client, {'response': 200})
                except OSError:
                    self.remove_client(client)
            else:
                response = {
                    'response': 400,
                    'error': 'Пользователь не зарегестрирован'
                }
                try:
                    utils.send_message(client, response)
                except OSError:
                    pass
            return

        elif 'action' in message and message['action'] == 'exit' and 'account_name' in message \
                and self.names[message['account_name']] == client:
            self.remove_client(client)

        elif 'action' in message and message['action'] == 'get_contacts' and 'user' in message and \
                self.names[message['user']] == client:
            response = {
                'response': 202,
                'list_info': self.db.get_contacts(message['user'])
            }
            try:
                utils.send_message(client, response)
            except OSError:
                self.remove_client(client)

        elif 'action' in message and message['action'] == 'add_contact' and 'account_name' in message \
                and 'user' in message and self.names[message['user']] == client:
            self.db.add_contact(message['user'], message['account_name'])
            try:
                utils.send_message(client, {'response': 200})
            except OSError:
                self.remove_client(client)

        elif 'action' in message and message['action'] == 'remove_contact' and 'account_name' in message \
                and 'user' in message and self.names[message['user']] == client:
            self.db.remove_contact(message['user'], message['account_name'])
            try:
                utils.send_message(client, {'response': 200})
            except OSError:
                self.remove_client(client)

        elif 'action' in message and message['action'] == 'users_request' and 'account_name' in message \
                and self.names[message['account_name']] == client:
            response = {
                'response': 202,
                'list_info': [user[0] for user in self.db.all_users()]
            }
            try:
                utils.send_message(client, response)
            except OSError:
                self.remove_client(client)

        elif 'action' in message and message['action'] == 'public_key_request' and 'account_name' in message:
            response = {
                'response': 511,
                'data': self.db.get_pubkey(message['account_name'])
            }
            if response['data']:
                try:
                    utils.send_message(client, response)
                except OSError:
                    self.remove_client(client)
            else:
                response = {
                    'response': 400,
                    'error': 'Нет публичного ключа для данного пользователя'
                }
                try:
                    utils.send_message(client, response)
                except OSError:
                    self.remove_client(client)

        else:
            response = {
                'response': 400,
                'error': 'Запрос не корректен'
            }
            try:
                utils.send_message(client, response)
            except OSError:
                self.remove_client(client)

    def autorize_user(self, message, sock):
        """Метод реализующий авторизцию пользователей."""
        server_logger.debug(f'Начало процесса авторизации для {message["user"]}')
        if message['user']['account_name']  in self.names.keys():
            response = {
                'response': 400,
                'error': 'Имя пользователя уже занято.'
            }
            try:
                server_logger.debug(f'Имя пользователя занято')
                utils.send_message(sock, response)
            except OSError:
                server_logger.debug('OSError')
                pass
            self.clients.remove(sock)
            sock.close()

        elif not self.db.check_user(message['user']['account_name']):
            response = {
                'response': 400,
                'error': 'Пользователь не зарегистрирован.'
            }
            try:
                server_logger.debug('Пользователь не зарегистрирован.')
                utils.send_message(sock, response)
            except OSError:
                server_logger.debug('OSError')
                pass
            self.clients.remove(sock)
            sock.close()

        else:
            server_logger.debug('Корректное имя пользователя, начало проверки пароля')
            random_str = binascii.hexlify(os.urandom(64))
            message_auth = {
                    'response': 511,
                    'data': random_str.decode('ascii')
                }
            hash = hmac.new(self.db.get_hash(message['user']['account_name']), random_str, 'MD5')
            digest = hash.digest()
            server_logger.debug(f'Auth message = {message_auth}')
            try:
                utils.send_message(sock, message_auth)
                ans = utils.get_message(sock)
            except OSError as e:
                server_logger.debug('Ошибка авториpации: ', exc_info=e)
                sock.close()
                return

            client_digest = binascii.a2b_base64(ans['data'])

            if 'response' in ans and ans['response'] == 511 and hmac.compare_digest(digest, client_digest):
                self.names[message['user']['account_name']] = sock
                client_ip, client_port = sock.getpeername()
                try:
                    utils.send_message(sock, {'response': 200})
                except OSError:
                    self.remove_client(message['user']['account_name'])

                self.db.user_login(
                    message['user']['account_name'], client_ip, client_port, message['user']['public_key']
                )
            else:
                response = {
                    'response': 400,
                    'error': 'Неверный пароль.'
                }
                try:
                    utils.send_message(sock, response)
                except OSError:
                    pass
                self.clients.remove(sock)
                sock.close()

    def service_update_list(self):
        """Метод, реализующий отправки сервисного сообщения 205 клиентам."""
        for client in self.names:
            try:
                utils.send_message(self.names[client], {'response': 205})
            except OSError:
                self.remove_client(self.names[client])

