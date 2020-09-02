import json
import unittest
from io import StringIO
from unittest import mock

import main_json as my_module


class TestMaxNumberApp(unittest.TestCase):
    def setUp(self):
        my_module.app.config['TESTING'] = True
        my_module.app.config['DEBUG'] = False
        self.app = my_module.app.test_client()
        self.add_url = '/users'
        self.calculate_url = '/users/<int:_id>'
        print(f'CALLED {self.shortDescription()}', flush=True)
        self.deceiver_json = json.dumps([{"id": 1, "name": "Roman"}, {"id": 2, "name": "Alexey"}])

    def test_add_storage(self):
        """test return list users"""
        mock_open = mock.mock_open(read_data=self.deceiver_json)
        with mock.patch('builtins.open', mock_open):
            response = self.app.get(self.add_url)
            response_text = response.data.decode()
            assert (response_text == '["Roman","Alexey"]\n')

    def test_add_user(self):
        mock_open = mock.mock_open(read_data=self.deceiver_json)
        with mock.patch('builtins.open', mock_open):
            response = self.app.post(self.add_url, data={"id": 111, "name": "PyConf"})
            self.assertEqual(b'"Add user PyConf"\n', response.data)
