class Service(object):

    def __init__(self, instance, cfg):
        self._name = cfg.get('name')
        self._type = cfg.get('type')
        self._cfg = cfg
        self._instance = instance

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
    def config(self):
        return self._cfg

    @property
    def status(self):
        return self._status().get('status')

    @property
    def pid(self):
        return self._status().get('pid')
