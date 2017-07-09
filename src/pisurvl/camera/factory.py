class CameraFactory:
    _camera_classes = {}

    @classmethod
    def register(cls, name, camera):
        cls._camera_classes[name] = camera

    @classmethod
    def create(cls, settings):
        camera_settings = settings['camera']
        name = camera_settings['name']
        if name not in cls._camera_classes:
            raise RuntimeError('Unknown camera class: {}'.format(name))
        return cls._camera_classes[name](camera_settings)
