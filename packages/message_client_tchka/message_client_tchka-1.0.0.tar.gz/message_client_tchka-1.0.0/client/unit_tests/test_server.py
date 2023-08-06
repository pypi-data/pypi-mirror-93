import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))

from server_oop import Server


class TestServer(unittest.TestCase):
    '''
    тест функции process_client_mess()
    '''
    test_server = Server()

    err_dict = {
        test_server.RESPONSE: 400,
        test_server.ERROR: 'Incorrect response'
    }
    ok_dict = {test_server.RESPONSE: 200}

    def test_without_action(self):
        '''
        проверка наличия в словаре ключа action
        :return:
        '''
        self.assertEqual(self.test_server.process_client_mess(
            {self.test_server.TIME: 1536000770, self.test_server.USER: {self.test_server.ACCOUNT_NAME: 'Guest'}}
        ), self.err_dict)

    def test_incorrect_action(self):
        '''
        проверка ответа на словарь с ошибкой в значении action
        :return:
        '''
        self.assertEqual(self.test_server.process_client_mess(
            {
                self.test_server.ACTION: 'wrong',
                self.test_server.TIME: 1536000770,
                self.test_server.USER: {self.test_server.ACCOUNT_NAME: 'Guest'}
            }
        ), self.err_dict)

    def test_without_time(self):
        '''
        проверка наличия в словаре ключа time
        :return:
        '''
        self.assertEqual(self.test_server.process_client_mess(
            {
                self.test_server.ACTION: self.test_server.PRESENSE,
                self.test_server.USER: {self.test_server.ACCOUNT_NAME: 'Guest'}
            }
        ), self.err_dict)

    def test_without_user(self):
        '''
        проверка наличия в словаре ключа user
        :return:
        '''
        self.assertEqual(self.test_server.process_client_mess(
            {
                self.test_server.ACTION: self.test_server.PRESENSE,
                self.test_server.TIME: 1536000770
            }
        ), self.err_dict)

    def test_incorrect_user(self):
        '''
        проверка ответа на словарь с ошибкой в значении user
        :return:
        '''
        self.assertEqual(self.test_server.process_client_mess(
            {
                self.test_server.ACTION: self.test_server.PRESENSE,
                self.test_server.TIME: 1536000770,
                self.test_server.USER: {self.test_server.ACCOUNT_NAME: 'Petya'}
            }
        ), self.err_dict)

    def test_everything_ok(self):
        '''
        проверка ответа на корректный словарь
        :return:
        '''
        self.assertEqual(self.test_server.process_client_mess(
            {
                self.test_server.ACTION: self.test_server.PRESENSE,
                self.test_server.TIME: 1536000770,
                self.test_server.USER: {self.test_server.ACCOUNT_NAME: 'Guest'}
            }
        ), self.ok_dict)


if __name__ == '__main__':
    unittest.main()
