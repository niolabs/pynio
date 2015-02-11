import unittest
from pynio.service import Service

class TestService(unittest.TestCase):

        def test_service(self):
            s = Service('name', 'type')
            self.assertEqual(s.name, 'name')
            self.assertEqual(s.type, 'type')
