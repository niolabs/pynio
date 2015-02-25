import unittest
from pynio import Instance, Block, Service
from unittest.mock import MagicMock, patch
from .mock import mock_service, mock_instance, config, template


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

    def test_add_block(self):
        i = MockInstance()
        i.blocks_types = MagicMock()
        i._put = MagicMock()
        name = 'name'
        self.assertTrue(name not in i.blocks)
        i.add_block(Block(name, 'type'))
        self.assertTrue(name in i.blocks)

    def test_add_service(self):
        i = MockInstance()
        i._put = MagicMock()
        name = 'name'
        self.assertTrue(name not in i.services)
        i.add_service(Service(name))
        self.assertTrue(name in i.services)

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

    def test_create_block(self):
        instance = mock_instance()
        blk = instance.create_block('name', 'type')
        self.assertFalse(instance.droplog.called)
        self.assertDictEqual(config, blk.json())
        self.assertIsInstance(blk, Block)
        self.assertIn(blk.name, instance.blocks)
        self.assertIn(blk, instance.blocks.values())

    def test_create_service(self):
        instance = mock_instance()
        service = instance.create_service('name')
        self.assertIsInstance(service, Service)
        self.assertIn(service.name, instance.services)
        self.assertIn(service, instance.services.values())

    def test_copy_block(self):
        in1 = mock_instance()
        in2 = mock_instance()

        b1 = in1.create_block('name', 'type')
        b2 = in2.copy_block(b1)
        self.assertIsNot(b1, b2)
        self.assertIsNot(b1._instance, b2._instance)
        self.assertDictEqual(b1.json(), b2.json())

        # cannot overwrite
        with self.assertRaises(ValueError):
            in1.copy_block(b2)

        # unless specified
        in1.copy_block(b2, True)

    def test_copy_service(self):
        in1 = mock_instance()
        in2 = mock_instance()

        s1 = in1.create_service('ser')
        b1 = s1.create_block('b1', 'type')
        s2, (b2,) = in2.copy_service(s1)

        # test block
        self.assertIsNot(b1, b2)
        self.assertIsNot(b1._instance, b2._instance)
        self.assertDictEqual(b1.json(), b2.json())

        # test service
        self.assertIsNot(s1, s2)
        self.assertIsNot(s1._instance, s2._instance)
        self.assertDictEqual(s1.config, s2.config)

    def test_copy_service_blocks(self):
        in1 = mock_instance()
        in2 = mock_instance()

        s1 = in1.create_service('ser')
        b1 = s1.create_block('b1', 'type')
        s2, (b2,) = in2.copy_service(s1)
        s3 = in1.create_service('ser3')
        b3 = s3.create_block('b3', 'type')
        s3.connect(b1, b3)

        # cannot copy if any blocks are the same
        with self.assertRaises(ValueError):
            in2.copy_service(s3)

        # make sure nothing was written
        self.assertNotIn(b3.name, in2.blocks)
        self.assertNotIn(s3.name, in2.services)

        # unless overwritten
        b1.config.value = 42
        self.assertNotEqual(b1.config.value, b2.config.value)
        s4, (b4, b5) = in2.copy_service(s3, True)
        self.assertEqual(b1.config.value, b2.config.value)

        # test blocks
        s4_b1 = s4.blocks['b1']
        self.assertEqual(s4_b1, b2.name)
        self.assertIsNot(s4_b1, b2)  # the object has been replaced
        self.assertIsNot(s4_b1._instance, b2._instance)
        self.assertNotEqual(s4_b1.config.value, b2.config.value)

        # test service
        self.assertIsNot(s1, s2)
        self.assertIsNot(s1._instance, s2._instance)
        self.assertDictEqual(s1.config, s2.config)
