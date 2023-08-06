import configparser
import logging
import os
import sys
import argparse
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from server.main_win import MainWindow
from server.server_core import MessageProcessor
from common.settings import default_port
from common.decorators import log_decorator
from server.server_db import ServerDB


server_logger = logging.getLogger('server')

new_connection = False
conflag_lock = threading.Lock()


@log_decorator
def argument_parse(default_port, default_ip):
    """Парсер аргументов коммандной строки."""
    server_logger.debug(f'Инициализация парсера аргументов командной строки: {sys.argv}')
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-p', default=default_port, type=int, nargs='?')
    arg_parser.add_argument('-a', default=default_ip, nargs='?')
    arg_parser.add_argument('--no_gui', action='store_true')
    namespace = arg_parser.parse_args(sys.argv[1:])
    server_address = namespace.a
    server_port = namespace.p
    gui_flag = namespace.no_gui
    server_logger.debug('Аргументы успешно загружены.')
    return server_address, server_port, gui_flag


@log_decorator
def load_config():
    """Парсер конфигурационного ini файла."""
    conf = configparser.ConfigParser()
    dir_path = os.path.dirname(os.getcwd())
    conf.read(f"{dir_path}/{'server.ini'}")
    if 'SETTINGS' in conf:
        return conf
    else:
        conf.add_section('SETTINGS')
        conf.set('SETTINGS', 'Default_port', str(default_port))
        conf.set('SETTINGS', 'Listen_address', '')
        conf.set('SETTINGS', 'Database_path', '')
        conf.set('SETTINGS', 'Database_file', 'server_db.db3')
        return conf


@log_decorator
def main():
    """Основная функция"""
    config = load_config()

    server_address, server_port, gui_flag = argument_parse(config['SETTINGS']['Default_port'], config['SETTINGS']['Listen_address'])

    database = ServerDB(os.path.join(config['SETTINGS']['Database_path'], config['SETTINGS']['Database_file']))

    server = MessageProcessor(server_address, server_port, database)
    server.daemon = True
    server.start()

    if gui_flag:
        while True:
            command = input('Введите exit для завершения работы сервера')
            if command == 'exit':
                server.running = False
                server.join()
                break
    else:
        server_app = QApplication(sys.argv)
        server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        main_window = MainWindow(database, server, config)

        server_app.exec_()

        server.running = False


if __name__ == '__main__':
    main()
