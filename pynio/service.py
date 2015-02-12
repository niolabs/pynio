from .block import Block

class Service(object):

    def __init__(self, name, type='Service', config=None, instance=None):
        self._name = name
        self._type = type
        self.config = config or {}
        self._instance = instance

    def save(self, instance=None):
        """ PUTs the service config to nio.

        Will create a new service if one does not exist by this name.
        Otherwise it will update the existing service config.
        """

        # Add service to an instance if one is specified
        if instance:
            self._instance = instance

        if self._instance:
            config = self.config
            config['name'] = self._name
            config['type'] = self._type
            self._put('services/{}'.format(self._name), config)
        else:
            raise Exception('Service is not associated with an instance')

    def _put(self, endpoint, config):
        self._instance._put(endpoint, config)

    def connect(self, blk1, blk2):
        # initialize execution to an empty list if it doesn't already exist
        execution = self.config.get('execution', [])
        self.config['execution'] = execution
        # check if source block is already in config
        connection = None
        for blk in execution:
            if blk.get('name') == blk1.name:
                connection = blk
                break
        # if block exists, add the receiever, otherwise init connection
        if connection:
            connection.get('receivers').append(blk2.name)
        else:
            connection = {'name': blk1.name, 'receivers': [blk2.name]}
            execution.append(connection)

    def start(self):
        """ Starts the nio Service. """
        self._instance._get('services/{}/start'.format(self._name))

    def stop(self):
        """ Stops the nio Service. """
        self._instance._get('services/{}/stop'.format(self._name))

    def command(self, *args, data=None):
        '''send a command to the service or to the block.
        To the service:
            service.command('command')
        To a block in the service:
            service.command(block, 'command')
        '''
        get = self._instance._get
        cmd_structure = '{}/{}/{}'.format
        if isinstance(args[0], Block):
            blk, cmd = args
            return get(cmd_structure('blocks', blk._name, cmd), data=data)
        else:
            cmd, = args
            return get(cmd_structure('services', self._name, cmd), data=data)

    def _status(self):
        """ Returns the status of the Service. """
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
        return self._status().get('status')

    @property
    def pid(self):
        return self._status().get('pid')
