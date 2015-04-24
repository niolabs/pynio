from copy import deepcopy
import pprint


class Block(object):
    """n.io Service

    Blocks are units inside of services. They perform functions on incomming
    signals and put the signals out.

    Args:
        name (str): Name of new block.
        type (str, optional): BlockType of new block.
        config (dict, optional): Optional configuration of block.
        instance (Instance, optional): Optional instance to add the block to.

    Attributes:
        name (str): Name of service.
        type (str): ServiceType of service.
        config (dict): Configuration of service.

    """

    def __init__(self, name, type, config=None, instance=None):
        config = config or {}
        if not name:
            raise ValueError("Name cannot be blank")
        self._name = name
        self._type = type
        self._instance = instance
        config['name'] = name
        if 'type' in config:
            if type != config['type']:
                raise ValueError("Types do not match: {} != {}".format(
                    type, config['type']))
        else:
            config['type'] = type
        self._config = deepcopy(config) or {}

    def save(self):
        """ PUTs the block config to nio.

        Will create a new block if one does not exist by this name.
        Otherwise it will update the existing block config.

        Raises:
            Exception: If service is not associated with an instance.

        """

        if not self._instance:
            raise Exception('Block is not associated with an instance')

        # setup config
        self.config['name'] = self._name
        self.config['type'] = self._type
        # put onto the web
        self._put('blocks/{}'.format(self._name), self.config)
        self._instance.blocks[self._name] = self

    def _put(self, endpoint, config):
        self._instance._put(endpoint, config)

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        if isinstance(value, dict):
            self._config = deepcopy(value)
        else:
            raise ValueError('config needs to be a dictionary')

    def delete(self):
        """Delete the block from the instance"""
        self._instance._delete('blocks/{}'.format(self._name))
        for s in self._instance.services.values():
            s.remove_block(self)
        self._instance.blocks.pop(self._name)
        self._instance = None  # make sure it isn't used anymore

    def in_use(self):
        """Return a list of services that use this block.

        Raises:
            TypeError: If block is not associated with an instance.

        """
        if not self._instance:
            raise TypeError("Block must be tied to instance")
        name = self.name
        return [service for service in
                self._instance.services.values()
                if next((True for b in service.blocks if b.name == name), False)
                ]

    def __str__(self):
        config = '\n  '.join(pprint.pformat(self.config).split('\n'))
        return ("Block({}, {}).config:{{\n  ".format(self.name, self.type) +
                                        config + '\n}\n')
