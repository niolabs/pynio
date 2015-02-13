import unittest
from pynio import Instance, Block, Service

host = '127.0.0.1'
port = '8181'
creds = 'Admin', 'Admin'



class TestLive(unittest.TestCase):
    def test_simple(self):
        nio = Instance(host, port, creds)
        sim = Block('sim', 'SimulatorFast')
        log = Block('log', 'LoggerBlock')
        sim.save(nio)
        log.save(nio)

        service = Service('testsdk')
        service.connect(sim, log)
        service.save(nio)
        service.start()
        input('started')
        service.stop()

        input('stopped')
        sim.delete()
        log.delete()
        service.delete()

#     NUM_SERVICES = 20

#     def setUp(self):
#         '''Create instance with blocks'''
#         self.nio = Instance(host, port, creds)
#         # self.nio.DELETE_ALL()
#         self.services = [Service('sim_{}'.format(n)) for n in range(20)]
#         sim = Block('sim', 'SimulatorFast')
#         log = Block('log', 'LoggerBlock')
#         self.sim = sim
#         self.log = log
#         self.nio.add_block(sim)
#         self.nio.add_block(log)
#         for s in self.services:
#             s.connect(sim, log)
#             self.nio.add_service(s)

#     def test_start_stop(self):
#         for s in self.services:
#             s.start()
#         for s in self.services:
#             s.stop()

#     def tearDown(self):
#         self.sim.delete()
#         self.log.delete()
#         for s in self.services:
#             s.delete()
