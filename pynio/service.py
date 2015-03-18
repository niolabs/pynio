from copy import deepcopy
from .block import Block


class Service(object):
    """n.io Service

    Args:
        name (str): Name of new service.
        type (str, optional): ServiceType of new service.
        config (dict, optional): Optional configuration of service.
        instance (Instance, optional): Optional instance to add the service to.

    Attributes:
        name (str): Name of service.
        type (str): ServiceType of service.
        config (dict): Configuration of service.
        status (str): Status of service.

    """

    def __init__(self, name, type='Service', config=None, instance=None):
        if not name:
            raise ValueError("name cannot be blank")
        self._name = name
        self._type = type
        self.config = deepcopy(config) or {}
        self._instance = instance

    def save(self):
        """PUTs the service config to nio.

        Will create a new service if one does not exist by this name.
        Otherwise it will update the existing service config.

        Raises:
            Exception: If service is not associated with an instance.

        """

        if not self._instance:
            raise Exception('Service is not associated with an instance')
        config = self.config
        config['name'] = self._name
        config['type'] = self._type
        self._put('services/{}'.format(self._name), config)
        self._instance.services[self._name] = self

    def _put(self, endpoint, config):
        self._instance._put(endpoint, config)

    def connect(self, blk1, blk2=None):
        """Connect two blocks.

        Args:
            blk1 (Block): Sends signals to `blk2`. If `blk2` is not specified
                then `blk1` is added to the service with no receivers.
            blk2 (Block, optional): Receives signal form `blk1`.

        """
        # initialize execution to an empty list if it doesn't already exist
        execution = self.config.get('execution', [])
        self.config['execution'] = execution
        # check if source block is already in config
        connection = None
        for blk in execution:
            if blk['name'] == blk1.name:
                connection = blk
                break
        if blk2 is not None:
            for blk in execution:
                if blk['name'] == blk2.name:
                    break
            else:
                # block2 doesn't exist, so add it
                execution.append({'name': blk2.name, 'receivers': []})

        # if block exists, add the receiever, otherwise init connection
        receivers = [] if blk2 is None else [blk2.name]
        if connection:
            cr = connection['receivers']
            cr.extend(receivers)
            # remove duplicates but preserve order
            seen = set()
            seen_add = seen.add
            cr[:] = [x for x in cr if not(x in seen or seen_add(x))]
        else:
            connection = {'name': blk1.name, 'receivers': receivers}
            execution.append(connection)

    def remove_block(self, block):
        """Remove a block from service. Does NOT delete the block.

        Args:
            block (Block): Block to remove from service.

        """
        execution = self.config.get('execution', None)
        if execution is None:  # no blocks
            return
        block = block._name

        def clean(connection):
            '''removes block from connection if it is in the list.
            returns False if whole connection should be removed'''
            if connection['name'] == block:
                return False
            try:
                connection['receivers'].remove(block)
            except ValueError:
                pass
            return True

        execution[:] = [c for c in execution if clean(c)]

    def start(self, retry=0):
        """Starts the nio Service."""
        self.command('start', retry=retry)

    def stop(self, retry=0):
        """Stops the nio Service."""
        self.command('stop', retry=retry)

    def command(self, command, block=None, **request_kwargs):
        """Send a command to the service or to a block in the service.

        Args:
            command (str): The name of the command.
            block (str, optional): The name of the block if commanding a block.
            request_kwargs: Keyword arguments are passed to http request.
                Examples: data, timeout (set the request timeout).

        """

        get = self._instance._get
        if block is None:
            return get('services/{}/{}'.format(self._name, command),
                       **request_kwargs)
        else:
            return get('services/{}/{}/{}'.format(self._name, block._name,
                                                  command),
                       **request_kwargs)

    def create_block(self, name, type, config=None):
        """Create a new block and add it to the service.

        Args:
            name (str): Name of new block.
            type (str, optional): BlockType of new block.
            config (dict, optional): Optional configuration of block.

        """

        blk = Block(name, type, config=config, instance=self._instance)
        self.connect(blk)
        if self._instance:
            self.save()
            blk.save()
        return blk

    @property
    def blocks(self):
        """Return a list of blocks used by this service."""
        if not self._instance:
            raise TypeError("Can only get block objects when attached to an "
                            "instance")
        blocks = self._instance.blocks
        return [blocks[i['name']] for i in self.config.get('execution', [])]

    def _status(self):
        """Returns the status of the Service."""
        return self._instance._get(
            'services/{}/status'.format(self._name))

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        print('You cannot change this attribute.')
        pass

    @property
    def type(self):
        return self._type

    @property
    def status(self):
        return self._status()['status']

    def delete(self):
        """Delete the service from the instance"""
        self._instance._delete(
            'services/{}'.format(self._name))
        self._instance.services.pop(self._name)
        self._instance = None  # make sure it isn't used anymore

    @property
    def pid(self):
        return self._status()['pid']

    def __str__(self):
        # get connections, ones with most connections first
        execution = sorted(self.config.get('execution', []),
                           key=lambda i: len(i['receivers']),
                           reverse=True)
        name_fmat = '{} --> {}'.format
        outstr = []
        outstr = [name_fmat(i['name'], ', '.join(i['receivers'])) for i in
                   execution]
        return ('Service({}).connections:{{\n  '.format(self.name) +
                '\n  '.join(outstr) + '\n}\n')
