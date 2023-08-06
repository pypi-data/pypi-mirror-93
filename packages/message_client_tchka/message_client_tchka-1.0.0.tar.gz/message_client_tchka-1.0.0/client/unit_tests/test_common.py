import json
import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))

from common_oop import CommonApi


class TestSocket:
    '''
    тестовый класс для создания и отправки сообщения
    использует тестовый словарь
    '''

    test_common = CommonApi()

    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.test_json_str = None
        self.test_encoded = None
        self.test_received = None

    def send(self, dict_message_to_send):
        """
        Функция имитация отправки словаря,
        кодирует сообщение, сохраняет байты, отправленные в сокет
        :param dict_message_to_send:
        :return:
        """
        test_json_str = json.dumps(self.test_dict)
        self.test_encoded = test_json_str.encode(self.test_common.ENCODING)
        self.test_received = dict_message_to_send

    def recv(self, max_len):
        """
        Функция имитация получения данных из сокета
        :param max_len:
        :return:
        """
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(self.test_common.ENCODING)


class TestCommon(unittest.TestCase):
    '''
    тест функции get_mess()
    тест функции send_mess()
    '''
    test_common = CommonApi()

    test_message_dict_send = {
        test_common.ACTION: test_common.PRESENSE,
        test_common.TIME: 1536000770,
        test_common.USER: {
            test_common.ACCOUNT_NAME: 'Vasya'
        }
    }
    test_message_dict_recv_ok = {test_common.RESPONSE: 200}
    test_message_dict_recv_err = {
        test_common.RESPONSE: 400,
        test_common.ERROR: 'Error'
    }

    # def test_get_mess_no_dict(self):
    #     '''
    #     проверка декодирования сообщения, не являющегося словарем
    #     '''
    #     self.assertRaises(ValueError, self.test_common.get_mess, self.test_message_json_str_ok)
    #
    # def test_get_mess_not_encoded(self):
    #     '''
    #     проверка декодирования незакодированного сообщения
    #     '''
    #     self.assertRaises(ValueError, self.test_common.get_mess, self.test_message_encoded_err)

    def test_send_mess(self):
        '''
        проверка декодирования корректного сообщения
        '''
        test_socket = TestSocket(self.test_message_dict_send)
        self.test_common.send_mess(test_socket, self.test_message_dict_send)
        self.assertEqual(test_socket.test_encoded, test_socket.test_received)
        with self.assertRaises(Exception):
            self.test_common.send_mess(test_socket, test_socket)

    def test_get_mess(self):
        """
        проверка приёма сообщения
        :return:
        """
        test_sock_ok = TestSocket(self.test_message_dict_recv_ok)
        test_sock_err = TestSocket(self.test_message_dict_recv_err)
        self.assertEqual(self.test_common.get_mess(test_sock_ok), self.test_message_dict_recv_ok)
        self.assertEqual(self.test_common.get_mess(test_sock_err), self.test_message_dict_recv_err)


if __name__ == '__main__':
    unittest.main()
