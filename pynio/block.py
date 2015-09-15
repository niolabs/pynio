from copy import deepcopy
import json
import requests


class Block(object):
    """n.io Block

    Blocks are units inside of services. They perform functions on incomming
    signals and put the signals out.

    Args:
        name (str): Name of new block.
        type (str, optional): BlockType of new block.
        config (dict, optional): Optional configuration of block.

    Attributes:
        name (str): Name of block.
        type (str): BlockType of block.
        config (dict): Configuration of block.
        instance (Instance): This n.io Instance this block is associated with.
    """

    def __init__(self, name, type, config=None):
        config = config or {}
        if not name:
            raise ValueError("Name cannot be blank")
        self.name = name
        self.type = type
        config['name'] = name
        if 'type' in config:
            if type != config['type']:
                raise ValueError("Types do not match: {} != {}".format(
                    type, config['type']))
        else:
            config['type'] = type
        self.config = deepcopy(config) or {}
        self.instance = None

    def save(self):
        """ PUTs the block config to nio.

        Will create a new block if one does not exist by this name.
        Otherwise it will update the existing block config.

        Raises:
            Exception: If block is not associated with an instance.

        """

        if not self.instance:
            raise Exception('Block is not associated with an instance')

        self.config['name'] = self.name
        self.config['type'] = self.type
        url = self.instance._url.format('blocks/{}'.format(self.name))
        requests.put(url, data=json.dumps(self.config))

    def delete(self):
        """Delete the block from the instance"""
        url = self.instance._url.format('blocks/{}'.format(self.name))
        requests.delete(url)

    def in_use(self):
        """Find all the Services tht use this block"""
        services = []
        for service in self.instance.services:
            if self in service.blocks:
                services.append(service)
        return services
