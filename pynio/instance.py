from copy import deepcopy
from pynio.rest import REST
from pynio.block import Block
from pynio.service import Service


class Instance(REST):

    """ Interface for a running n.io instance.

    This is the main part of pynio. All communication with the n.io instance
    goes through this object. Blocks and Services contain a reference to an
    Instance in order to communication with the running instance.

    Args:
        host (str, optional): Host ip address of running n.io instance.
            Default is '127.0.0.1'.
        port (int, optional): Port of runing n.io instance. Default is 8181.
        creds ((str, str), optional): Username and password for basic
            authentication. Default is ('Admin', 'Admin').

    Attributes:
        blocks (dict of Block): A collection of block names with their Block
            instance.
        services (dict of Service): A collection of service names with their
            Service instance.

    """

    def __init__(self, host='127.0.0.1', port=8181, creds=None):
        super().__init__(host, port, creds)
        self.droplog = print
        self.blocks_types = {}
        self.blocks = {}
        self.services = {}
        # reset to initalize instance
        self.reset()

    def reset(self):
        self.blocks_types = self._get_blocks_types()
        self.blocks = self._get_blocks()
        self.services = self._get_services()

    def nio(self):
        """ Returns nio version info."""
        return self._get('nio')

    def add_block(self, block, overwrite=False):
        """Add block to instance.

        Args:
            block (Block): Block instanace to add.
            overwrite (bool, optional): If True, configuration will be updated
                if `block` is already in Instance. Default is False.

        Raises:
            ValueError: If `overwrite` is False and `block` is already in the
                instance.

        """
        if not overwrite and block.name in self.blocks:
            raise ValueError
        block = deepcopy(block)
        block._instance = self
        block.save()
        return block

    def add_service(self, service, overwrite=False, blocks=False):
        """Add service to instance.

        Args:
            service (Service): Service instanace to add.
            overwrite (bool, optional): If True, configuration will be updated
                if `service` is already in Instance. Default is False.

        Raises:
            ValueError: If `overwrite` is False and `block` is already in the
                instance.

        """
        if not overwrite and service.name in self.services:
            raise ValueError("Service already exists {}".format(service.name))
        if blocks:
            if not overwrite:
                # make sure no blocks have the same name
                bnames = {b.name for b in service.blocks}
                mybnames = set(self.blocks.keys())
                intersect = bnames.intersection(mybnames)
                if intersect:
                    raise ValueError(
                        "Some blocks from service {} already exist: {}".
                        format(service.name, intersect))
            [self.add_block(b, True) for b in service.blocks]
        service = deepcopy(service)
        service._instance = self
        service.save()
        return service

    def _get_blocks(self):
        blocks = {}
        for bname, config in self._get('blocks').items():
            btype = config['type']
            b = Block(bname, btype, config)
            #b = deepcopy(blocks_types[btype])
            #b._name = bname
            b._instance = self
            #b._config['name'] = bname
            blocks[bname] = b
        return blocks

    def _get_blocks_types(self):
        blocks_types = {}
        for btype, config in self._get('blocks_types').items():
            blocks_types[btype] = config
        return blocks_types

    def _get_services(self):
        services = {}
        resp = self._get('services')
        for s in resp:
            services[s] = Service(resp[s].get('name', s),
                                  config=resp[s],
                                  instance=self)
        return services

    def create_block(self, name, type, config=None):
        """Create a block in the instance.

        Args:
            name (str): Name of new block.
            type (str): BlockType of new block.
            config (dict, optional): Optional configuration of block properties.

        """
        block = Block(name, type, config, instance=self)
        block.save()
        return block

    def create_service(self, name, type=None, config=None):
        """Create a service in the instance.

        Args:
            name (str): Name of new service.
            type (str, optional): ServiceType of new service.
            config (dict, optional): Optional configuration of service.

        """
        if type is None:
            service = Service(name, config=config, instance=self)
        else:
            service = Service(name, type, config=config, instance=self)
        service.save()
        return service

    def save(self):
        """Save all blocks and all services in instance."""
        for b in self.blocks.items():
            b.save()
        for s in self.services.items():
            s.save()
