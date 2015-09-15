from copy import deepcopy
import json
import requests


class Service(object):
    """n.io Service

    Args:
        name (str): Name of new service.
        type (str, optional): ServiceType of new service.
        config (dict, optional): Optional configuration of service.

    Attributes:
        name (str): Name of service.
        type (str): ServiceType of service.
        config (dict): Configuration of service.
        instance (Instance): This n.io Instance this service is associated with.
        blocks (list(Block)): A collection of Block instances
    """

    def __init__(self, name, type="Service", config=None):
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
        """ PUTs the service config to nio.

        Will create a new service if one does not exist by this name.
        Otherwise it will update the existing service config.

        Raises:
            Exception: If service is not associated with an instance.

        """

        if not self.instance:
            raise Exception('Service is not associated with an instance')

        self.config['name'] = self.name
        self.config['type'] = self.type
        url = self.instance._url.format('services/{}'.format(self.name))
        requests.put(url, data=json.dumps(self.config))

    def delete(self):
        """Delete the service from the instance"""
        url = self.instance._url.format('services/{}'.format(self.name))
        requests.delete(url)

    @property
    def blocks(self):
        block_names_in_service = []
        blocks_in_service = []
        for block_name in self.config.get('execution', []):
            block_names_in_service.append(block_name['name'])
        for block in self.instance.blocks:
            if block.name in block_names_in_service:
                blocks_in_service.append(block)
        return blocks_in_service
