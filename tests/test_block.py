import unittest
from unittest.mock import MagicMock, patch
import json
from pynio import Block


class TestBlock(unittest.TestCase):

    def test_create_block(self):
        b = Block('name', 'type')
        b.instance = MagicMock()
        self.assertEqual(b.name, 'name')
        self.assertEqual(b.type, 'type')
        self.assertDictEqual(b.config, {'name': 'name', 'type': 'type'})
        self.assertTrue(isinstance(b.config, dict))

    def test_create_block_with_bad_config(self):
        with self.assertRaises(Exception) as context:
            b = Block('name', 'type', 'not a dict')

    def test_create_block_with_no_name(self):
        with self.assertRaises(ValueError):
            Block('', 'type')

    @patch('requests.put')
    def test_save_block(self, put):
        instance = MagicMock()
        instance._url = 'http://127.0.0.1:8181/{}'
        b = Block('name', 'type', {})
        b.instance = instance
        b.save()
        self.assertEqual(put.call_count, 1)
        self.assertEqual(put.call_args[0][0],
                         instance._url.format('blocks/name'))
        self.assertDictEqual(json.loads(put.call_args[1]['data']),
                             {'name': 'name',
                              'type': 'type'})

    @patch('requests.put')
    def test_save_block_with_no_instance(self, put):
        b = Block('name', 'type', {'key': 'val'})
        with self.assertRaises(Exception) as context:
            b.save()
        self.assertTrue('Block is not associated with an instance' in
                        context.exception.args[0])
        self.assertFalse(put.called)

    @patch('requests.delete')
    def test_delete_block(self, delete):
        instance = MagicMock()
        instance._url = 'http://127.0.0.1:8181/{}'
        b = Block('name', 'type', {'key': 'val'})
        b.instance = instance
        b.delete()
