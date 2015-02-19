import unittest
from pynio import Instance
from unittest.mock import MagicMock, patch
from .mock import mock_service


class TestInstance(unittest.TestCase):
    def setUp(self):
        blks = patch.object(Instance, '_get_blocks')
        blks.start()
        Instance._get_blocks.return_value = None, None
        servs = patch.object(Instance, '_get_services')
        servs.start()

    def test_instance(self):
        i = Instance()
        self.assertEqual(i.host, '127.0.0.1')
        self.assertEqual(i.port, 8181)

    # TODO: Create a test that loads system settings

    def test_delete_all(self, *args):
        names = ['one', 'two', 'three']
        i = Instance()
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
