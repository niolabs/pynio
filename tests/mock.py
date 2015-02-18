from unittest.mock import MagicMock
from pynio import properties


def mock_instance(types):
    instance = MagicMock(spec=[
        'config', 'blocks_types', 'droplog', 'blocks'])
    instance = MagicMock(spec=[
        'config', 'blocks_types', 'droplog', 'blocks'])
    instance.droplog = MagicMock()
    instance.blocks = {}
    instance.blocks_types = {
        'type': properties.TypedDict({'template':
                                        {'type': 'type',
                                        'name': '',
                                        'key': 'std'}})
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
