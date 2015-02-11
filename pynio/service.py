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
        # TODO: this needs to add to the existing config instead of appending
        # if the block is already in the service.
        connection = {'name': blk1.name, 'receivers': [blk2.name]}
        execution = self.config.get('execution', [])
        execution.append(connection)
        self.config['execution'] = execution

    def start(self):
        """ Starts the nio Service. """
        self._instance._get('services/{}/start'.format(self._name))

    def stop(self):
        """ Stops the nio Service. """
        self._instance._get('services/{}/stop'.format(self._name))

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
