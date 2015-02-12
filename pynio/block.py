class Block(object):

    def __init__(self, name, type, config=None, instance=None):
        self._name = name
        self._type = type
        self.config = config or {}
        self._instance = instance

    def save(self, instance=None):
        """ PUTs the block config to nio.

        Will create a new block if one does not exist by this name.
        Otherwise it will update the existing block config.
        """

        # Add block to an instance if one is specified
        if instance:
            self._instance = instance

        if not self._instance:
            raise Exception('Block is not associated with an instance')

        config = self.config
        config['name'] = self._name
        config['type'] = self._type
        self._put('blocks/{}'.format(self._name), config)
        self._instances.blocks[self._name] = self

    def _put(self, endpoint, config):
        self._instance._put(endpoint, config)

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

    def delete(self):
        '''Delete self from instance and services'''
        self._instance._delete('blocks/{}'.format(self._name))
        for s in self._instance.services.values():
            s._remove(self)
        self._instance.blocks.remove(self._name)
        self._instance = None  # make sure it isn't used anymore
