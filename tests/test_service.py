import unittest
from unittest.mock import MagicMock, patch
import json
from pynio import Service


class TestService(unittest.TestCase):

    def test_create_service(self):
        b = Service('name')
        b.instance = MagicMock()
        self.assertEqual(b.name, 'name')
        self.assertEqual(b.type, 'Service')
        self.assertDictEqual(b.config, {'name': 'name', 'type': 'Service'})
        self.assertTrue(isinstance(b.config, dict))

    def test_create_serivce_with_bad_config(self):
        with self.assertRaises(Exception) as context:
            b = Service('name', 'type', 'not a dict')

    def test_create_service_with_no_name(self):
        with self.assertRaises(ValueError):
            Service('', 'type')

    @patch('requests.put')
    def test_save_service(self, put):
        instance = MagicMock()
        instance._url = 'http://127.0.0.1:8181/{}'
        b = Service('name', 'type', {})
        b.instance = instance
        b.save()
        self.assertEqual(put.call_count, 1)
        self.assertEqual(put.call_args[0][0],
                         instance._url.format('services/name'))
        self.assertDictEqual(json.loads(put.call_args[1]['data']),
                             {'name': 'name',
                              'type': 'type'})

    @patch('requests.put')
    def test_save_service_with_no_instance(self, put):
        b = Service('name')
        with self.assertRaises(Exception) as context:
            b.save()
        self.assertTrue('Service is not associated with an instance' in
                        context.exception.args[0])
        self.assertFalse(put.called)

    @patch('requests.delete')
    def test_delete_service(self, delete):
        instance = MagicMock()
        instance._url = 'http://127.0.0.1:8181/{}'
        b = Service('name', 'type', {'key': 'val'})
        b.instance = instance
        b.delete()
