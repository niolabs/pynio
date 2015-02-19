import unittest
from pynio import Instance
from unittest.mock import MagicMock, patch
from .mock import mock_service


class MockInstance(Instance):

    def __init__(self, host='127.0.0.1', port=8181, creds=None):
        self._get_blocks = MagicMock()
        self._get_blocks.return_value = {}, {}
        self._get_services = MagicMock()
        self._get_services.return_value = {}
        super().__init__(host, port, creds)


class TestInstance(unittest.TestCase):

    def test_instance(self):
        i = MockInstance()
        self.assertEqual(i.host, '127.0.0.1')
        self.assertEqual(i.port, 8181)

    def test_delete_all(self, *args):
        names = ['one', 'two', 'three']
        i = MockInstance()
        i._get = MagicMock()
        i._get.return_value = names
        i._delete = MagicMock()

        i.DELETE_ALL()

        delete = ['blocks/{}'.format(n) for n in names]
        delete.extend('services/{}'.format(n) for n in names)
        get = ['blocks', 'services']
        get.extend('services/{}/stop'.format(n) for n in names)

        get_list = i._get.call_args_list
        get_called = [get_list[n][0][0] for n in range(len(get_list))]
        delete_list = i._delete.call_args_list
        delete_called = [delete_list[n][0][0] for
                            n in range(len(delete_list))]

        self.assertEqual(i._get.call_count, 2 + len(names))
        self.assertEqual(i._delete.call_count, len(names) * 2)
        self.assertEqual(get_called, get)
        self.assertEqual(delete_called, delete)
