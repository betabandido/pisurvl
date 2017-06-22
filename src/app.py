import time

from exceptions import UnknownCommandException
from exectools.exectools import is_execution_terminated
from messaging.command_listener import CommandListener
from messaging.request_processor import RequestProcessor
from messaging.response_processor import ResponseProcessor
from motion.detection import MotionDetector
from settings import settings
from surveil.backup import ImageBackupService
from surveil.event_notifier import EventNotifier
from surveil.surveil import SurveillanceManager


class Application:
    # TODO: increase retry time
    REQUEST_FETCHING_RETRY_TIME = 1

    def __init__(self):
        self._surveillance_manager = SurveillanceManager(
            MotionDetector(settings['motion']),
            EventNotifier(settings['notifications']),
            ImageBackupService()
        )
        self._cmd_listener = CommandListener()
        self._response_processor = ResponseProcessor()
        self._request_processor = RequestProcessor(
            self._surveillance_manager,
            self._response_processor
        )

    def start(self):
        print('Starting PiSurvl')
        self._cmd_listener.cleanup()

        while not is_execution_terminated():
            request = self._cmd_listener.fetch_request()
            if request is None:
                time.sleep(self.REQUEST_FETCHING_RETRY_TIME)
                continue

            try:
                self._request_processor.process(request)
            except UnknownCommandException as e:
                print('ERROR: {}'.format(e))

        print('Application is cleaning up')
        self._surveillance_manager.stop_surveillance()
        self._cmd_listener.cleanup()
