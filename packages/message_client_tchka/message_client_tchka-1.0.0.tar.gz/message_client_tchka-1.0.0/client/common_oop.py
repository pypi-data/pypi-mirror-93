import json
import logging


class CommonApi:

    def __init__(self):

        self._ip_address = '127.0.0.1'
        self._connection_port = 7777
        self._encoding = 'utf-8'
        self._max_connections = 5
        self._max_package_length = 10240
        self._action = 'action'
        self._time = 'time'
        self._user = 'user'
        self._data = 'bin'
        self._public_key = 'pubkey'
        self._account_name = 'account_name'
        self._sender = 'sender'
        self._exit = 'exit'
        self._get_contacts = 'get_contacts'
        self._add_contact = 'add_contact'
        self._list_info = 'list_info'
        self._remove_contact = 'remove_contact'
        self._users_request = 'get_users'
        self._public_key_request = 'pubkey_need'
        self._presense = 'presense'
        self._response = 'response'
        self._message = 'message'
        self._destination = 'destination'
        self._mess_text = 'message_text'
        self._error = 'error'
        self._logging_level = logging.DEBUG
        self._server_db = 'sqlite:///server_base.db3'
        self._response_200 = {self.RESPONSE: 200}
        self._response_202 = {self.RESPONSE: 202, self.LIST_INFO: None}
        self._response_205 = {self.RESPONSE: 205}
        self._response_400 = {self.RESPONSE: 400}
        self._response_511 = {self.RESPONSE: 511}
        self._list_info = 'data_list'
        self._remove_contact = 'remove'
        self._add_contact = 'add'

    @property
    def IP_ADDRESS(self):
        return self._ip_address

    @property
    def CONNECTION_PORT(self):
        return self._connection_port

    @property
    def ENCODING(self):
        return self._encoding

    @property
    def MAX_CONNECTIONS(self):
        return self._max_connections

    @property
    def MAX_PACKAGE_LENGTH(self):
        return self._max_package_length

    @property
    def ACTION(self):
        return self._action

    @property
    def USER(self):
        return self._user

    @property
    def DATA(self):
        return self._data

    @property
    def PUBLIC_KEY(self):
        return self._public_key

    @property
    def TIME(self):
        return self._time

    @property
    def ACCOUNT_NAME(self):
        return self._account_name

    @property
    def SENDER(self):
        return self._sender

    @property
    def EXIT(self):
        return self._exit

    @property
    def GET_CONTACTS(self):
        return self._get_contacts

    @property
    def ADD_CONTACTS(self):
        return self._add_contact

    @property
    def LIST_INFO(self):
        return self._list_info

    @property
    def REMOVE_CONTACT(self):
        return self._remove_contact

    @property
    def USERS_REQUEST(self):
        return self._users_request

    @property
    def PUBLIC_KEY_REQUEST(self):
        return self._public_key_request

    @property
    def PRESENSE(self):
        return self._presense

    @property
    def RESPONSE(self):
        return self._response

    @property
    def ERROR(self):
        return self._error

    @property
    def MESSAGE(self):
        return self._message

    @property
    def DESTINATION(self):
        return self._destination

    @property
    def MESSAGE_TEXT(self):
        return self._mess_text

    @property
    def LOGGING_LEVEL(self):
        return self._logging_level

    @property
    def SERVER_DB(self):
        return self._server_db

    @property
    def RESPONSE_200(self):
        return self._response_200

    @property
    def RESPONSE_202(self):
        return self._response_202

    @property
    def RESPONSE_400(self):
        return self._response_400

    @property
    def RESPONSE_205(self):
        return self._response_205

    @property
    def RESPONSE_511(self):
        return self._response_511

    @property
    def LIST_INFO(self):
        return self._list_info

    @property
    def REMOVE_CONTACT(self):
        return self._remove_contact

    @property
    def ADD_CONTACT(self):
        return self._add_contact

    def get_mess(self, sock):
        '''
        Функция выполяет прием и декодирование сообщения. Принимает сообщение в байтах.
        Возвращает словарь или ошибку значения.
        :param sock:
        :return: словарь или ошику значения
        '''

        response_encoded = sock.recv(self.MAX_PACKAGE_LENGTH)
        if isinstance(response_encoded, bytes):
            response_json_str = response_encoded.decode(self.ENCODING)
            response_dict = json.loads(response_json_str)
            if isinstance(response_dict, dict):
                return response_dict
            raise ValueError

        raise ValueError

    def send_mess(self, sock, message_dict):
        '''
        Функция выполяет кодирование и отправку сообщения от клиента. Принимает словарь.
        :param sock:
        :return:
        '''

        message_json_str = json.dumps(message_dict)
        message_encoded = message_json_str.encode(self.ENCODING)
        sock.send(message_encoded)
