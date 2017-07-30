import time

from pisurvl.exceptions import UnknownCommandException
from pisurvl.messaging.command_listener import CommandListener
from pisurvl.messaging.request_processor import RequestProcessor
from pisurvl.messaging.response_processor import ResponseProcessor
from pisurvl.motion.detection import MotionDetector
from pisurvl.surveil.event_notifier import EventNotifier
from pisurvl.surveil.surveil import SurveillanceManager

from pisurvl.exectools.exectools import is_execution_terminated
from pisurvl.settings import settings
from pisurvl.surveil.backup import ImageBackupService


class Application:
    # TODO: increase retry time
    REQUEST_FETCHING_RETRY_TIME = 1

    def __init__(self):
        self._surveillance_manager = SurveillanceManager(
            MotionDetector(settings['motion']),
            EventNotifier(settings['notifications']),
            ImageBackupService(),
            settings
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
