from nioapi.api_rest import REST
from nioapi.block import Block
from nioapi.service import Service


class Instance(REST):
    """ Interface for a running nio instance.

    """

    def __init__(self, host='127.0.0.1', port=8181, creds=None):
        super().__init__(host, port, creds)

    def _nio(self):
        """ Returns nio version info.

        """
        return self._get('nio')

    def blocks(self, name=None):
        """ Returns a single Block if specified or dict of Blocks.

        """
        if name:
            resp = self._get('blocks/{}'.format(name))
            return Block(resp)
        else:
            blks = {}
            resp = self._get('blocks')
            for blk in resp:
                blks[blk] = Block(resp[blk])
            return blks

    def blocks_types(self):
        return self._get('blocks_types')

    def services(self, name=None):
        """ Returns a single Service if specified or dict of Services.

        """
        if name:
            resp = self._get('services/{}'.format(name))
            return Service(self, resp)
        else:
            services = {}
            resp = self._get('services')
            for s in resp:
                services[s] = Service(self, resp[s])
            return services

    def services_types(self):
        return self._get('services_types')
