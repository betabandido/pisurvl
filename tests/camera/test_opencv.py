from PIL import Image

from camera.opencv import OpenCVCamera


def test_that_frames_are_captured():
    settings = {'resolution': (640, 480)}
    with OpenCVCamera(settings) as camera:
        camera.warm_up()
        frame = camera.get_frame()
        assert frame is not None

        img = Image.fromarray(frame, 'RGB')
        assert img.width == settings['resolution'][0]
        assert img.height == settings['resolution'][1]
