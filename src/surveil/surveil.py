import io
from PIL import Image
import queue
import time

from camera.factory import create_camera
from motion.detection import MotionDetector
from settings import settings
from surveil.backup import ImageBackupService
from surveil.event_notifier import EventNotifier
from threading import Thread


class SurveillanceManager(Thread):
    def __init__(self, camera_factory=create_camera):
        super().__init__()
        self.camera_factory = camera_factory
        self.terminated = False
        self.request_queue = queue.Queue()
        self.last_frame = None

        self.motion_detector = MotionDetector(settings['motion'])
        self.event_notifier = EventNotifier(settings['notification'])
        self.backup_service = ImageBackupService()

    def run(self):
        with self.camera_factory() as camera:
            camera.warm_up()

            while not self.terminated:
                self.last_frame = camera.get_frame()
                if self.motion_detector.detect_motion(self.last_frame):
                    self._handle_motion_detection(self.last_frame)
                self._process_requests()
                time.sleep(1)

    def stop(self):
        self.terminated = True
        self.join()

    def queue_request(self, request, callback):
        self.request_queue.put_nowait(
            {'request': request, 'callback': callback})

    def _process_requests(self):
        if self.request_queue.empty():
            return

        elem = self.request_queue.get_nowait()
        request = elem['request']
        if request['cmd'] == 'peek':
            callback = elem['callback']
            callback(request, {'frame': self.last_frame})

    def _handle_motion_detection(self, frame):
        """Handles motion detection.
        Args:
          frame: The frame to compare for movement.
        """
        try:
            print('*** MOTION DETECTED ***')
            self.event_notifier.send_motion_notification()

            img = Image.fromarray(frame, 'RGB')
            data = io.BytesIO()
            img.save(data, 'jpeg')
            self.backup_service.backup_image(data.getvalue())
        except Exception as error:
            print('ERROR: {}'.format(error))
