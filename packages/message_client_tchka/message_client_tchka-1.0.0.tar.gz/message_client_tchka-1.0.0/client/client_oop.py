'''
Основной модуль для клиента мессенджера. Содержит класс клиента
'''
import os
import sys
import argparse
from logging import getLogger

from Cryptodome.PublicKey import RSA
from PyQt5.QtWidgets import QApplication, QMessageBox

from common_oop import CommonApi
from errors import ServerError
from database import ClientDatabase
from transport import ClientTransport
from main_window import ClientMainWindow
from start_dialog import UserNameDialog
import log.config.client_log_config

class Client(CommonApi):
    '''
    Основной класс клиента мессенджера
    '''

    def __init__(self):
        super().__init__()
        parser = argparse.ArgumentParser()
        parser.add_argument('addr', default=self.IP_ADDRESS, nargs='?')
        parser.add_argument(
            'port',
            default=self.CONNECTION_PORT,
            type=int,
            nargs='?')
        parser.add_argument('-n', '--name', default=None, nargs='?')
        parser.add_argument('-p', '--password', default='', nargs='?')
        namespace = parser.parse_args(sys.argv[1:])
        self.server_address = namespace.addr
        self.server_port = namespace.port
        self.client_name = namespace.name
        self.client_passwd = namespace.password

    CLIENT_LOGGER = getLogger('client')

    def main(self):
        '''
        Метод класса клиента мессенджера. Запускает клиента.
        :return:
        '''
        client_app = QApplication(sys.argv)

        # Если имя пользователя не было указано в командной строке то запросим
        # его
        start_dialog = None
        if not self.client_name or not self.client_passwd:
            start_dialog = UserNameDialog()
            client_app.exec_()
            # Если пользователь ввёл имя и пароль и нажал ОК, то сохраняем
            # ведённое и удаляем объект, инааче выходим
            if start_dialog.ok_pressed:
                self.client_name = start_dialog.client_name.text()
                self.client_passwd = start_dialog.client_passwd.text()
                self.CLIENT_LOGGER.debug(
                    f'Using USERNAME = {self.client_name}, \
                    PASSWD = {self.client_passwd}.')
            else:
                sys.exit(0)
        print(f'Консольный месседжер. Клиент {self.client_name}.')

        self.CLIENT_LOGGER.info(
            f'Запущен клиент {self.client_name}, порт: {self.server_port}, \
            имя пользователя: {self.client_name}.')

        # Загружаем ключи с файла, если же файла нет, то генерируем.
        dir_path = os.getcwd()
        key_file = os.path.join(dir_path, f'{self.client_name}.key')
        if not os.path.exists(key_file):
            keys = RSA.generate(2048, os.urandom)
            with open(key_file, 'wb') as key:
                key.write(keys.export_key())
        else:
            with open(key_file, 'rb') as key:
                keys = RSA.import_key(key.read())

        # !!!keys.publickey().export_key()
        self.CLIENT_LOGGER.debug("Keys sucsessfully loaded.")

        database = ClientDatabase(self.client_name)

        try:
            transport = ClientTransport(
                self.server_port,
                self.server_address,
                database,
                self.client_name,
                self.client_passwd,
                keys)
        except ServerError as error:
            message = QMessageBox()
            message.critical(start_dialog, 'Ошибка сервера', error.text)
            sys.exit(1)
        transport.setDaemon(True)
        transport.start()

        if start_dialog:
            del start_dialog

        # Создаём GUI
        main_window = ClientMainWindow(database, transport, keys)
        main_window.make_connection(transport)
        main_window.setWindowTitle(
            f'Чат Программа alpha release - {self.client_name}')
        client_app.exec_()

        # Раз графическая оболочка закрылась, закрываем транспорт
        transport.transport_shutdown()
        transport.join()


if __name__ == '__main__':
    my_client = Client()
    my_client.main()
