import unittest
from unittest.mock import MagicMock
from pynio import Block
from .mock import mock_instance, config


class TestBlock(unittest.TestCase):

    def test_block(self):
        b = Block('name', 'type')
        b._instance = MagicMock()
        self.assertEqual(b.name, 'name')
        self.assertEqual(b.type, 'type')
        self.assertDictEqual(b.config, {'name': 'name', 'type': 'type'})
        self.assertTrue(isinstance(b.config, dict))

    def test_block_config_attr(self):
        b = Block('name', 'type')
        b._instance = MagicMock()
        self.assertEqual(b.config.name, 'name')
        self.assertEqual(b.config.type, 'type')
        # test config access as attributes
        b.config.attr = 'attr'
        self.assertDictEqual(b.config,
                             {'name': 'name', 'type': 'type', 'attr': 'attr'})
        self.assertTrue(isinstance(b.config, dict))

    def test_noname(self):
        with self.assertRaises(ValueError):
            Block('', 'type')

    def test_save(self):
        b = Block('name', 'type', config)
        b._instance = mock_instance()
        b._put = MagicMock()
        b.save()
        self.assertTrue(b._put.called)
        self.assertEqual(b._put.call_args[0][0], 'blocks/name')
        self.assertDictEqual(b._put.call_args[0][1],
                                {'name': 'name',
                                'type': 'type',
                                'value': 0})

    def test_save_with_no_instance(self):
        b = Block('name', 'type')
        b._config = {'key': 'val'}
        b._put = MagicMock()
        with self.assertRaises(Exception) as context:
            b.save()
        self.assertTrue('Block is not associated with an instance' in
                        context.exception.args[0])
        self.assertFalse(b._put.called)

    def test_delete_block(self):
        instance = mock_instance()
        s = instance.create_service('foo')
        b = s.create_block('one', 'type')
        b2 = s.create_block('two', 'type')
        s.connect(b, b2)
        b.delete()
        execution = s.config['execution']
        self.assertListEqual(execution, [
            {'name': 'two', 'receivers': []}
        ])

    def test_in_use(self):
        instance = mock_instance()
        s = instance.create_service('foo')
        instance.create_service('bar')
        blk = s.create_block('one', 'type')
        use = blk.in_use()
        self.assertListEqual(use, [s])
