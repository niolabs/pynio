from copy import deepcopy
import requests
from pynio.block import Block
from pynio.service import Service


class Instance():

    """ Interface for a running n.io instance.

    This is the main part of pynio. All communication with the n.io instance
    goes through this object. Blocks and Services contain a reference to an
    Instance in order to communicate with the running instance.

    Args:
        host (str, optional): Host ip address of running n.io instance.
            Default is '127.0.0.1'.
        port (int, optional): Port of runing n.io instance. Default is 8181.
        creds ((str, str), optional): Username and password for basic
            authentication. Default is ('User', 'User').

    Attributes:
        blocks (list(Block)): A collection of Block instances
        services (list(Service)): A collection of Service instances

    """

    def __init__(self, host='127.0.0.1', port=8181, creds=None):
        self.host = host
        self.port = port
        self.creds = creds or ('User', 'User')
        self._url = 'http://{}:{}@{}:{}/{}'.format(
            self.creds[0], self.creds[1], host, port, '{}')
        self._blocks = []
        self._blocks = self.blocks
        self._services = []
        self._services = self.services

    def add_block(self, block):
        """Add block to instance.

        Args:
            block (Block): Block instanace to add.
                if `block` is already in Instance. Default is False.

        """
        block.instance = self
        block.save()
        self.blocks.append(block)
        return block

    @property
    def blocks(self):
        if self._blocks:
            # Use local cache if it exists
            return self._blocks
        resp = requests.get(self._url.format('blocks'), )
        for name, config in resp.json().items():
            type = config['type']
            b = Block(name, type, config)
            b.instance = self
            self._blocks.append(b)
        return self._blocks

    @property
    def services(self):
        if self._services:
            # Use local cache if it exists
            return self._services
        resp = requests.get(self._url.format('services'), )
        for name, config in resp.json().items():
            type = config['type']
            s = Service(name, config=config)
            s.instance = self
            self._services.append(s)
        return self._services
