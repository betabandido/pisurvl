from PIL import Image
from unittest import TestCase

from camera.opencv import OpenCVCamera


class TestOpenCVCamera(TestCase):
    def test_that_frames_are_captured(self):
        settings = {
            'resolution': (640, 480),
            'warmup_time': 0
        }
        with OpenCVCamera(settings) as camera:
            camera.warm_up()
            frame = camera.get_frame()
            assert frame is not None

            img = Image.fromarray(frame, 'RGB')
            assert img.width == settings['resolution'][0]
            assert img.height == settings['resolution'][1]
