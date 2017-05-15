from settings import settings

_camera_classes = {}


def register_camera(name, camera):
    _camera_classes[name] = camera


def create_camera():
    camera_settings = settings['camera']
    name = camera_settings['name']
    if name not in _camera_classes:
        raise RuntimeError('Unknown camera class: {}'.format(name))
    return _camera_classes[name](camera_settings)
