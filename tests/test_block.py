import unittest
from nioapi.block import Block

class TestBlock(unittest.TestCase):

        def test_block(self):
            b = Block({'name': 'name', 'type': 'type'})
            self.assertEqual(b.name, 'name')
            self.assertEqual(b.type, 'type')
