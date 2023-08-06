'''
Модуль соединения с сервером: создание соединения, обработка событий
'''
import binascii
import hashlib
import hmac
import socket
import sys
import time
import json
import threading
from logging import getLogger
from PyQt5.QtCore import pyqtSignal, QObject

from common_oop import CommonApi
from errors import ServerError

# Логер и объект блокировки для работы с сокетом.
socket_lock = threading.Lock()


class ClientTransport(CommonApi, threading.Thread, QObject):
    '''
    Класс соединения с сервером
    '''
    # Сигналы новое сообщение и потеря соединения
    new_message = pyqtSignal(dict)
    message_205 = pyqtSignal()
    connection_lost = pyqtSignal()
    CLIENT_LOGGER = getLogger('client')

    def __init__(self, port, ip_address, database, username, passwd, keys):
        # Вызываем конструктор предка
        CommonApi.__init__(self)
        threading.Thread.__init__(self)
        QObject.__init__(self)

        # Класс База данных - работа с базой
        self.database = database
        # Имя пользователя
        self.username = username
        # Пароль
        self.password = passwd
        # Сокет для работы с сервером
        self.transport = None
        # Набор ключей для шифрования
        self.keys = keys
        # Устанавливаем соединение:
        self.connection_init(port, ip_address)
        # Обновляем таблицы известных пользователей и контактов
        try:
            self.user_list_update()
            self.contacts_list_update()
        except OSError as err:
            if err.errno:
                self.CLIENT_LOGGER.critical(f'Потеряно соединение с сервером.')
                raise ServerError('Потеряно соединение с сервером!')
            self.CLIENT_LOGGER.error('Timeout соединения при обновлении \
            списков пользователей.')
        except json.JSONDecodeError:
            self.CLIENT_LOGGER.critical(f'Потеряно соединение с сервером.')
            raise ServerError('Потеряно соединение с сервером!')
            # Флаг продолжения работы транспорта.
        self.running = True

    def connection_init(self, port, ip):
        '''
        Метод инициализации соединения с сервером.
        :param port:
        :param ip:
        :return:
        '''
        # Инициализация сокета и сообщение серверу о нашем появлении
        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Таймаут необходим для освобождения сокета.
        self.transport.settimeout(5)

        # Соединяемся, 5 попыток соединения,
        # флаг успеха ставим в True если удалось
        connected = False
        for i in range(5):
            self.CLIENT_LOGGER.info(f'Попытка подключения №{i + 1}')
            try:
                self.transport.connect((ip, port))
            except (OSError, ConnectionRefusedError):
                pass
            else:
                connected = True
                break
            time.sleep(1)

        # Если соединится не удалось - исключение
        if not connected:
            self.CLIENT_LOGGER.critical('Не удалось установить соединение \
            с сервером')
            raise ServerError('Не удалось установить соединение с сервером')

        self.CLIENT_LOGGER.debug('Установлено соединение с сервером')

        # Запускаем процедуру авторизации
        # Получаем хэш пароля
        passwd_bytes = self.password.encode('utf-8')
        salt = self.username.lower().encode('utf-8')
        passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bytes, salt, 10000)
        passwd_hash_string = binascii.hexlify(passwd_hash)

        self.CLIENT_LOGGER.debug(f'Passwd hash ready: {passwd_hash_string}')

        # Получаем публичный ключ и декодируем его из байтов
        pubkey = self.keys.publickey().export_key().decode('ascii')
        # Авторизируемся на сервере
        with socket_lock:
            presense = {
                self.ACTION: self.PRESENSE,
                self.TIME: time.time(),
                self.USER: {
                    self.ACCOUNT_NAME: self.username,
                    self.PUBLIC_KEY: pubkey
                }
            }
            self.CLIENT_LOGGER.debug(f"Presense message = {presense}")
            # Отправляем серверу приветственное сообщение.
            try:
                self.send_mess(self.transport, presense)
                ans = self.get_mess(self.transport)
                self.CLIENT_LOGGER.debug(f'Server response = {ans}.')
                # Если сервер вернул ошибку, бросаем исключение.
                if self.RESPONSE in ans:
                    if ans[self.RESPONSE] == 400:
                        raise ServerError(ans[self.ERROR])
                    elif ans[self.RESPONSE] == 511:
                        # Если всё нормально, то продолжаем процедуру
                        # авторизации.
                        ans_data = ans[self.DATA]
                        hash = hmac.new(passwd_hash_string,
                                        ans_data.encode('utf-8'), 'MD5')
                        digest = hash.digest()
                        my_ans = self.RESPONSE_511
                        my_ans[self.DATA] = binascii.b2a_base64(
                            digest).decode('ascii')
                        self.send_mess(self.transport, my_ans)
                        self.process_server_ans(self.get_mess(self.transport))
            except (OSError, json.JSONDecodeError) as err:
                self.CLIENT_LOGGER.debug(f'Connection error.', exc_info=err)
                raise ServerError('Сбой соединения в процессе авторизации.')

    def process_server_ans(self, message):
        '''
        Метод обработки сообщения от сервера. Ничего не возращает.
        Генерирует исключение при ошибке.
        :param message:
        :return:
        '''
        self.CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')

        # Если это подтверждение чего-либо
        if self.RESPONSE in message:
            if message[self.RESPONSE] == 200:
                return
            elif message[self.RESPONSE] == 400:
                raise ServerError(f'{message[self.ERROR]}')
            elif message[self.RESPONSE] == 205:
                self.user_list_update()
                self.contacts_list_update()
                self.message_205.emit()
            else:
                self.CLIENT_LOGGER.debug(f'Принят неизвестный \
                код подтверждения {message[self.RESPONSE]}')

        # Если это сообщение от пользователя добавляем в базу,
        # даём сигнал о новом сообщении
        elif self.ACTION in message and message[
            self.ACTION] == self.MESSAGE and self.SENDER in message \
                and self.DESTINATION in message \
                and self.MESSAGE_TEXT in message \
                and message[self.DESTINATION] == self.username:
            self.CLIENT_LOGGER.debug(
                f'Получено сообщение от пользователя \
{message[self.SENDER]}:{message[self.MESSAGE_TEXT]}')
            self.new_message.emit(message)

    def contacts_list_update(self):
        '''
        Метод обноления контакт-листа с сервера
        :return:
        '''
        self.database.contacts_clear()
        self.CLIENT_LOGGER.debug(f'Запрос контакт листа для \
        пользователся {self.name}')
        req = {
            self.ACTION: self.GET_CONTACTS,
            self.TIME: time.time(),
            self.USER: self.username
        }
        self.CLIENT_LOGGER.debug(f'Сформирован запрос {req}')
        with socket_lock:
            self.send_mess(self.transport, req)
            ans = self.get_mess(self.transport)
        self.CLIENT_LOGGER.debug(f'Получен ответ {ans}')
        if self.RESPONSE in ans and ans[self.RESPONSE] == 202:
            for contact in ans[self.LIST_INFO]:
                self.database.add_contact(contact)
        else:
            self.CLIENT_LOGGER.error('Не удалось обновить список контактов.')

    def user_list_update(self):
        '''
        Метод обновления таблицы известных пользователей.
        :return:
        '''
        self.CLIENT_LOGGER.debug(f'Запрос списка известных \
        пользователей {self.username}')
        req = {
            self.ACTION: self.USERS_REQUEST,
            self.TIME: time.time(),
            self.ACCOUNT_NAME: self.username
        }
        with socket_lock:
            self.send_mess(self.transport, req)
            ans = self.get_mess(self.transport)
        if self.RESPONSE in ans and ans[self.RESPONSE] == 202:
            self.database.add_users(ans[self.LIST_INFO])
        else:
            self.CLIENT_LOGGER.error('Не удалось обновить список известных \
            пользователей.')

    def key_request(self, user):
        '''
        Метод запроса с сервера публичного ключа пользователя.
        :param user:
        :return:
        '''
        self.CLIENT_LOGGER.debug(f'Запрос публичного ключа для {user}')
        req = {
            self.ACTION: self.PUBLIC_KEY_REQUEST,
            self.TIME: time.time(),
            self.ACCOUNT_NAME: user
        }
        with socket_lock:
            self.send_mess(self.transport, req)
            ans = self.get_mess(self.transport)
        if self.RESPONSE in ans and ans[self.RESPONSE] == 511:
            return ans[self.DATA]
        else:
            self.CLIENT_LOGGE.error(f'Не удалось получить ключ \
            собеседника{user}.')

    def add_contact(self, contact):
        '''
        Метод оповещения сервера о добавлении нового контакта
        :param contact:
        :return:
        '''
        self.CLIENT_LOGGER.debug(f'Создание контакта {contact}')
        req = {
            self.ACTION: self.ADD_CONTACT,
            self.TIME: time.time(),
            self.USER: self.username,
            self.ACCOUNT_NAME: contact
        }
        with socket_lock:
            self.send_mess(self.transport, req)
            self.process_server_ans(self.get_mess(self.transport))

    def remove_contact(self, contact):
        '''
        Метод удаления клиента на сервере
        :param contact:
        :return:
        '''
        self.CLIENT_LOGGER.debug(f'Удаление контакта {contact}')
        req = {
            self.ACTION: self.REMOVE_CONTACT,
            self.TIME: time.time(),
            self.USER: self.username,
            self.ACCOUNT_NAME: contact
        }
        with socket_lock:
            self.send_mess(self.transport, req)
            self.process_server_ans(self.get_mess(self.transport))

    def transport_shutdown(self):
        '''
        Метод удаления клиента на серверезакрытия соединения,
        отправляет сообщение о выходе.
        :return:
        '''
        self.running = False
        message = {
            self.ACTION: self.EXIT,
            self.TIME: time.time(),
            self.ACCOUNT_NAME: self.username
        }
        with socket_lock:
            try:
                self.send_mess(self.transport, message)
            except OSError:
                pass
        self.CLIENT_LOGGER.debug('Транспорт завершает работу.')
        time.sleep(0.5)

    def send_message(self, to, message):
        '''
        Метод отправки сообщения на сервер.
        :param to:
        :param message:
        :return:
        '''
        message_dict = {
            self.ACTION: self.MESSAGE,
            self.SENDER: self.username,
            self.DESTINATION: to,
            self.TIME: time.time(),
            self.MESSAGE_TEXT: message
        }
        self.CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: \
{message_dict}')

        # Необходимо дождаться освобождения сокета для отправки сообщения
        with socket_lock:
            self.send_mess(self.transport, message_dict)
            self.process_server_ans(self.get_mess(self.transport))
            self.CLIENT_LOGGER.info(f'Отправлено сообщение для \
            пользователя {to}')

    def run(self):
        '''
        Метод запуска соединения с свервером
        :return:
        '''
        self.CLIENT_LOGGER.debug('Запущен процесс - приёмник сообщений \
        с сервера.')
        while self.running:
            # Отдыхаем секунду и снова пробуем захватить сокет.
            time.sleep(1)
            message = None
            with socket_lock:
                try:
                    self.transport.settimeout(0.5)
                    message = self.get_mess(self.transport)
                except OSError as err:
                    if err.errno:
                        self.CLIENT_LOGGER.critical(f'Потеряно соединение \
                        с сервером.')
                        self.running = False
                        self.connection_lost.emit()
                # Проблемы с соединением
                except (ConnectionError, ConnectionAbortedError,
                        ConnectionResetError, json.JSONDecodeError, TypeError):
                    self.CLIENT_LOGGER.debug(f'Потеряно соединение с \
                    сервером.')
                    self.running = False
                    self.connection_lost.emit()
                finally:
                    self.transport.settimeout(5)

            # Если сообщение получено, то вызываем функцию обработчик:
            if message:
                self.CLIENT_LOGGER.debug(f'Принято сообщение с сервера: \
{message}')
                self.process_server_ans(message)
