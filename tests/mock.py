from unittest.mock import MagicMock
from pynio import properties, Block

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

config = {
    'name': 'name',
    'type': 'type',
    'value': 0
}


def mock_instance(type=template):
    instance = MagicMock(spec=[
        'config', 'droplog',
        'blocks', 'blocks_types', 'services',
        '_put'])
    instance.droplog = MagicMock()
    instance._put = MagicMock()
    instance.blocks = {}
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


def throw(error):
    '''used for one-liner raising'''
    raise error
