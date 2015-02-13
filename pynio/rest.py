import requests
import json


class REST(object):
    '''Object for making it easier to communicate with a rest object.
    Stores host, port and credential information and uses it automatically.
    '''
    def __init__(self, host='127.0.0.1', port=8181, creds=None):
        self._host = host
        self._port = port
        self._creds = creds or ('User', 'User')
        self._url = 'http://{}:{}/{}'.format(host, port, '{}')

    def _get(self, endpoint, timeout=None):
        r = requests.get(self._url.format(endpoint),
                         auth=self._creds,
                         timeout=timeout)
        r.raise_for_status()
        return r.json()

    def _put(self, endpoint, config=None, timeout=None):
        config = config or {}
        r = requests.put(self._url.format(endpoint),
                         auth=self._creds,
                         data=json.dumps(config),
                         timeout=timeout)
        r.raise_for_status()

    def _delete(self, endpoint, timeout=None):
        r = requests.delete(self._url(endpoint), auth=self._auth,
                            timeout=timeout)
        r.raise_for_status()
        return r

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        raise TypeError('Create a new Instance for a new host')

    @property
    def port(self):
        return self._port
