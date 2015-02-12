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

        if not self._instance:
            raise Exception('Service is not associated with an instance')
        config = self.config
        config['name'] = self._name
        config['type'] = self._type
        self._put('services/{}'.format(self._name), config)
        self._instances.services[self._name] = self

    def _put(self, endpoint, config):
        self._instance._put(endpoint, config)

    def connect(self, blk1, blk2):
        # initialize execution to an empty list if it doesn't already exist
        execution = self.config.get('execution', [])
        self.config['execution'] = execution
        # check if source block is already in config
        connection = None
        for blk in execution:
            if blk['name'] == blk1.name:
                connection = blk
                break
        # if block exists, add the receiever, otherwise init connection
        if connection:
            connection['receivers'].append(blk2.name)
        else:
            connection = {'name': blk1.name, 'receivers': [blk2.name]}
            execution.append(connection)

    def _remove(self, block):
        '''remove a block from service. Does NOT delete the block'''
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
        return self._status()['status']

    def delete(self):
        '''Delete self from instance'''
        self._instance._delete(
            'services/{}'.format(self._name))
        self._instance.services.remove(self._name)
        self._instance = None  # make sure it isn't used anymore

    @property
    def pid(self):
        return self._status()['pid']
