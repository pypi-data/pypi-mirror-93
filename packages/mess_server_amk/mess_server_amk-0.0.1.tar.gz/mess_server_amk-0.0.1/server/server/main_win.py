import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QTableView, QApplication, QLabel

from .add_user import RegisterUser
from .config_win import ConfigWindow
from .remove_user import DelUserDialog
from .stat_win import StatWindow


class MainWindow(QMainWindow):
    """Класс - основное окно сервера."""
    def __init__(self, db, server, config):
        super().__init__()

        self.db = db
        self.server_thread = server
        self.config = config

        self.exit_action = QAction('Выход', self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.triggered.connect(qApp.quit)

        self.refresh_btn = QAction('Обновить список', self)

        self.config_btn = QAction('Настройки сервера', self)

        self.register_btn = QAction('Регистрация пользователя', self)

        self.remove_btn = QAction('Удаление пользователя', self)

        self.show_history_btn = QAction('История клиентов', self)

        self.statusBar()
        self.statusBar().showMessage('Server working')

        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.addAction(self.exit_action)
        self.toolbar.addAction(self.refresh_btn)
        self.toolbar.addAction(self.show_history_btn)
        self.toolbar.addAction(self.config_btn)
        self.toolbar.addAction(self.register_btn)
        self.toolbar.addAction(self.remove_btn)

        self.setFixedSize(800, 600)
        self.setWindowTitle('Messaging Server alpha release')

        self.label = QLabel('Список подключенных клиентов', self)
        self.label.setFixedSize(240, 15)
        self.label.move(10, 25)

        self.active_clients = QTableView(self)
        self.active_clients.move(10, 45)
        self.active_clients.setFixedSize(780, 400)

        self.timer = QTimer()
        self.timer.timeout.connect(self.create_user_model)
        self.timer.start(1000)

        self.refresh_btn.triggered.connect(self.create_user_model)
        self.show_history_btn.triggered.connect(self.show_statistics)
        self.config_btn.triggered.connect(self.server_config)
        self.register_btn.triggered.connect(self.reg_user)
        self.remove_btn.triggered.connect(self.rem_user)

        self.show()

    def create_user_model(self):
        """Метод, заполняющий таблицу активных пользователей."""
        users = self.db.active_users()
        list = QStandardItemModel()
        list.setHorizontalHeaderLabels(['Имя клиета', 'IP адрес', 'Порт', 'Время подключения'])
        for row in users:
            user, ip, port, time = row
            user = QStandardItem(user)
            user.setEditable(False)
            ip = QStandardItem(ip)
            ip.setEditable(False)
            port = QStandardItem(str(port))
            port.setEditable(False)
            time = QStandardItem(str(time.replace(microsecond=0)))
            time.setEditable(False)
            list.appendRow([user, ip, port, time])
        self.active_clients.setModel(list)
        self.active_clients.resizeColumnsToContents()
        self.active_clients.resizeRowsToContents()

    def show_statistics(self):
        """Метод, создающий окно со статистикой клиентов."""
        global stat_window
        stat_window = StatWindow(self.db)
        stat_window.show()

    def server_config(self):
        """Метод, создающий окно с настройками сервера."""
        global config_window
        config_window = ConfigWindow(self.config)

    def reg_user(self):
        """Метод, создающий окно регистрации пользователя."""
        global reg_window
        reg_window = RegisterUser(self.db, self.server_thread)
        reg_window.show()

    def rem_user(self):
        """Метод, создающий окно удаления пользователя."""
        global rem_window
        rem_window = DelUserDialog(self.db, self.server_thread)
        rem_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()

    # app = QApplication(sys.argv)
    # window = HistoryWindow()
    # app.exec_()

    # app = QApplication(sys.argv)
    # window = ConfigWindow()
    # app.exec_()
