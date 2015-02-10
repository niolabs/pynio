import unittest
from nioapi.service import Service

class TestService(unittest.TestCase):

        def test_service(self):
            s = Service(None, {'name': 'name', 'type': 'type'})
            self.assertEqual(s.name, 'name')
            self.assertEqual(s.type, 'type')
