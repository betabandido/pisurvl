import time

import cv2

from pisurvl.camera.camera import Camera


class OpenCVCamera(Camera):
    def __init__(self, settings):
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise RuntimeError('Error opening camera')

        self._set_resolution(
            settings['resolution'][0],
            settings['resolution'][1])

        self._warmup_time = settings['warmup_time']

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.camera.release()

    def get_frame(self):
        (grabbed, frame) = self.camera.read()
        if not grabbed:
            return None
        return frame

    def warm_up(self):
        time.sleep(self._warmup_time)

    def _set_resolution(self, width, height):
        print('setting resolution to: {} x {}'.format(width, height))
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
