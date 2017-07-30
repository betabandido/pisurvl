import io
import queue
import time
from threading import Thread

from PIL import Image

from pisurvl.camera.factory import CameraFactory


class SurveillanceManager:
    def __init__(self, motion_detector, event_notifier, backup_service, settings):
        self._motion_detector = motion_detector
        self._event_notifier = event_notifier
        self._backup_service = backup_service
        self._settings = settings

        self._terminated = False
        self._request_queue = queue.Queue()
        self._last_frame = None
        self._thread = None

    def is_surveillance_enabled(self):
        return self._thread is not None

    def start_surveillance(self):
        if not self.is_surveillance_enabled():
            self._thread = Thread(target=self.run)
            self._thread.start()

    def stop_surveillance(self):
        if self.is_surveillance_enabled():
            self._terminated = True
            self._thread.join()
            self._thread = None

    def queue_surveillance_request(self, request, callback):
        if self.is_surveillance_enabled():
            self._request_queue.put_nowait(
                {'request': request, 'callback': callback})
        else:
            print('WARNING: Surveillance request received while surveillance is disabled')

    def run(self):
        with CameraFactory.create(self._settings) as camera:
            camera.warm_up()

            while not self._terminated:
                self._process_frame(camera)

    def _process_frame(self, camera):
        self._last_frame = camera.get_frame()
        if self._motion_detector.detect_motion(self._last_frame):
            self._handle_motion_detection(self._last_frame)
        self._process_requests()
        time.sleep(1)

    def _process_requests(self):
        if self._request_queue.empty():
            return

        elem = self._request_queue.get_nowait()
        request = elem['request']
        if request['cmd'] == 'peek':
            callback = elem['callback']
            callback(request, {'frame': self._last_frame})

    def _handle_motion_detection(self, frame):
        try:
            print('*** MOTION DETECTED ***')
            self._event_notifier.send_motion_notification()

            img = Image.fromarray(frame, 'RGB')
            data = io.BytesIO()
            img.save(data, 'jpeg')
            self._backup_service.backup_image(data.getvalue())
        except Exception as error:
            print('ERROR: {}'.format(error))
