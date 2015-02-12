import unittest
from pynio import Instance, Block, Service

host = '127.0.0.1'
port = '7357'
creds = 'User', 'User'


class TestLive(unittest.TestCase):
    NUM_SERVICES = 20

    def setUp(self):
        '''Create instance with blocks'''
        self.nio = Instance(host, port, creds)
        self.nio.DELETE_ALL()
        self.services = [Service('sim_{}'.format(n)) for n in range(20)]
        sim = Block('sim', 'SimulatorFast')
        log = Block('log', 'LoggerBlock')
        for s in self.services:
            s.connect(sim, log)
            self.nio.add_service(s)

    def test_start_stop(self):
        for s in self.services:
            s.start()
        for s in self.services:
            s.stop()
