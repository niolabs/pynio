from unittest.mock import MagicMock
from pynio import properties, Block, Instance


def throw(error):
    raise error

template = {
    'name': 'template',
    'properties': {
        'name': {
            'type': 'str',
            'title': None,
        },
        'type': {
            "type": "str",
            "title": None
        },
        'value': {
            'type': 'int',
            'title': 'Value',
            'default': 0
        }
    }
}

templates = {'type': template}

config = {
    'name': 'name',
    'type': 'type',
    'value': 0
}

service_config = {
    "mappings": [],
    "execution": [],
    "sys_metadata": "",
    "type": "Service",
    "status": "started",
    "log_level": "ERROR",
    "auto_start": True,
    "name": "name"
}

class _Instance(Instance):
    def __init__(self):
        pass


def mock_instance(type=template):
    instance = MagicMock(wraps=_Instance, spec=[
        'config', 'droplog',
        'blocks', 'blocks_types', 'services',
        '_put'])()
    instance.droplog = MagicMock()
    instance._put = MagicMock()
    instance._get = MagicMock()
    instance._delete = MagicMock()
    instance.blocks = {}
    instance.services = {}
    b = Block('type', 'type', instance=instance)
    b._load_template('type', template)
    instance.blocks_types = {
        'type': b
    }
    return instance


def mock_service():
    service = MagicMock(spec=[
        'start', 'stop', 'delete', 'command'])
    service.start = MagicMock()
    service.stop = MagicMock()
    service.stop = MagicMock()
    service.delete = MagicMock()
    service.command = MagicMock()
    return service
