import unittest
from nioapi import Instance

class TestInstance(unittest.TestCase):

        def test_instance(self):
            i = Instance()
            self.assertEqual(i.host, '127.0.0.1')
            self.assertEqual(i.port, 8181)
