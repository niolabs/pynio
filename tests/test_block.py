import unittest
from unittest.mock import MagicMock
from copy import deepcopy

from pynio import Block


class TestBlock(unittest.TestCase):

        def test_block(self):
            b = Block('name', 'type')
            self.assertEqual(b.name, 'name')
            self.assertEqual(b.type, 'type')

        def test_save(self):
            b = Block('name', 'type')
            b.config = {'key': 'val'}
            b._instance = MagicMock() # Associate with instance but not for real
            b._put = MagicMock()
            b.save()
            self.assertTrue(b._put.called)
            self.assertEqual(b._put.call_args[0][0], 'blocks/name')
            self.assertDictEqual(b._put.call_args[0][1],
                                 {'name': 'name',
                                  'type': 'type',
                                  'key': 'val'})

        def test_save_with_no_instance(self):
            b = Block('name', 'type')
            b.config = {'key': 'val'}
            b._put = MagicMock()
            with self.assertRaises(Exception) as context:
                b.save()
            self.assertTrue('Block is not associated with an instance' in
                            context.exception.args[0])
            self.assertFalse(b._put.called)

        def test_load_template(self):
            from .example_data import SimulatorFastTemplate
            btype = 'SimulatorFast'
            b = Block('sim', btype)
            b.load_template(btype, SimulatorFastTemplate)
            from pprint import pprint
            print()
            pprint(b.template)
            self.assertRaises(TypeError, setattr, b.template, 'type', 'foo')

        def test_typed_config(self):
            from .example_data import SimulatorFastTemplate, SimulatorFastConfig
            btype = 'SimulatorFast'
            b = Block('sim', btype, config=SimulatorFastConfig)
            b.load_template(btype, SimulatorFastTemplate)
            b.config.interval.days = 10
            self.assertEqual(b.config.interval.days, 10)
            self.assertRaises(ValueError, setattr,
                              b.config.interval, 'days', 'bad')

        def test_load_all_templates(self):
            from .example_data import BlocksTemplatesAll
            for btype, template in BlocksTemplatesAll.items():
                b = Block(btype, btype)
                b.load_template(btype, template)

        def test_load_all_configs(self):
            from .example_data import BlocksTemplatesAll, BlocksConfigsAll
            blocks_types = {}
            for btype, template in BlocksTemplatesAll.items():
                b = Block(btype, btype)
                b.load_template(btype, template)
                blocks_types[btype] = b

            blocks = {}
            for bname, config in BlocksConfigsAll.items():
                btype = config['type']
                b = deepcopy(blocks_types[btype])
                b.config = config
                blocks[bname] = b

