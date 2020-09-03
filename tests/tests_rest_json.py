import json
from unittest import mock, TestCase

import __main_json__ as my_module


class TestUserApp(TestCase):
    def setUp(self):
        my_module.app.config['TESTING'] = True
        my_module.app.config['DEBUG'] = False
        self.app = my_module.app.test_client()
        self.add_url = '/users'
        print(f'CALLED {self.shortDescription()}', flush=True)

        self.deceiver_json = json.dumps([{"id": 1, "name": "Roman"}, {"id": 2, "name": "Alexey"}])

    def test_return_users(self):
        """test return list users or by id"""
        mock_open = mock.mock_open(read_data=self.deceiver_json)
        with mock.patch('builtins.open', mock_open):
            response = self.app.get(self.add_url)
            response_text = response.data.decode()
            assert (response_text == '["Roman","Alexey"]\n')

            response = self.app.get(f'{self.add_url}/{1}')
            response_text = response.data.decode()
            assert (response_text == '"Hello, my name is Roman. Im here"\n')

    def test_add_user(self):
        """test add user"""
        mock_open = mock.mock_open(read_data=self.deceiver_json)
        with mock.patch('builtins.open', mock_open):
            response = self.app.post(self.add_url, data={"id": 111, "name": "TrueConf"})
            self.assertEqual(b'"Add user TrueConf"\n', response.data)

    def test_put_user(self):
        """test rename user"""
        mock_open = mock.mock_open(read_data=self.deceiver_json)
        with mock.patch('builtins.open', mock_open):
            response = self.app.put(f'{self.add_url}/{1}', data={"name": "Andrey"})
            self.assertEqual(b'"Fix _name_ user with id 1 on Andrey"\n', response.data)

    def test_delete_user(self):
        """test delete user"""
        mock_open = mock.mock_open(read_data=self.deceiver_json)
        with mock.patch('builtins.open', mock_open):
            response = self.app.delete(f'{self.add_url}/{1}')
            self.assertEqual(b'"User with id 1 is deleted."\n', response.data)
