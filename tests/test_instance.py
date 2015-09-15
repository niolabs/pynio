from copy import deepcopy
import unittest
from pynio import Instance
from unittest.mock import MagicMock, patch


class TestInstance(unittest.TestCase):

    @patch('requests.get')
    def test_create_instance(self, get):
        instance = Instance()
        self.assertEqual(instance.host, '127.0.0.1')
        self.assertEqual(instance.port, 8181)

    @patch('requests.get')
    def test_add_block_to_service(self, get):
        instance = Instance()
        self.assertFalse(instance.blocks)
        block = MagicMock()
        self.assertFalse(block.save.called)
        instance.add_block(block)
        self.assertTrue(block.save.called)
        self.assertEqual(block.instance, instance)
        self.assertTrue(instance.blocks)

    @patch('requests.get')
    def test_get_blocks_from_instance(self, get):
        blocks_resp = MagicMock()
        blocks_resp.json.return_value = {
            "block1": {"name": "block1", "type": "type1"},
            "block2": {"name": "block2", "type": "type2"}
        }
        services_resp = MagicMock()
        services_resp.json.return_value = {
            "service1": {"name": "service1", "type": "Service"},
            "service2": {"name": "service2", "type": "Service"}
        }
        get.side_effect = [blocks_resp, services_resp]
        instance = Instance()
        # Check that we have two blocks
        self.assertEqual(len(instance.blocks), 2)
        # And make sure the blocks know they are a part of this instance
        self.assertEqual(instance.blocks[0].instance, instance)
        self.assertEqual(instance.blocks[1].instance, instance)
        # And make sure duplicate calls use local cache
        self.assertEqual(get.call_count, 2)
        self.assertEqual(len(instance.blocks), 2)
