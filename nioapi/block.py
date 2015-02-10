class Block(object):

    def __init__(self, cfg):
        self._name = cfg.get('name')
        self._type = cfg.get('type')
        self._cfg = cfg

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
