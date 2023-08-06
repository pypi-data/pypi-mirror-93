import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))

from client_oop import Client


class TestClient(unittest.TestCase):
    '''
    тест функции process_answer()
    тест функции create_presence()
    '''
    test_client = Client()

    err_answer = '400: my_error'
    ok_answer = '200: OK'

    def test_no_response_answer(self):
        '''
        проверка распаковки некорректного ответа
        '''
        self.assertRaises(ValueError, self.test_client.process_answer, {self.test_client.ERROR: 'my_error'})

    def test_err_answer(self):
        '''
        проверка распаковки ответа 400
        '''
        self.assertEqual(self.test_client.process_answer(
            {self.test_client.RESPONSE: 400, self.test_client.ERROR: 'my_error'}
        ), self.err_answer)

    def test_ok_answer(self):
        '''
        проверка распаковки ответа 200
        '''
        self.assertEqual(self.test_client.process_answer(
            {self.test_client.RESPONSE: 200}
        ), self.ok_answer)

    def test_create_presence(self):
        '''
        проверка создания запроса
        '''
        test_message = self.test_client.create_presence()
        print(test_message)
        test_message[self.test_client.TIME] = 1536000770
        self.assertEqual(test_message,
                         {
                             self.test_client.ACTION: self.test_client.PRESENSE,
                             self.test_client.TIME: 1536000770,
                             self.test_client.USER: {
                                 self.test_client.ACCOUNT_NAME: 'Guest'}
                         }
                         )


if __name__ == '__main__':
    unittest.main()
