import time

from exectools.exectools import is_execution_terminated
from messaging.command_listener import CommandListener
from messaging.request_processor import RequestProcessor
from messaging.response_processor import ResponseProcessor
from surveil.surveil import SurveillanceManager


class Application:
    # TODO: increase retry time
    REQUEST_FETCHING_RETRY_TIME = 1

    def __init__(self):
        self._surveillance_manager = None
        self._cmd_listener = CommandListener()
        self._response_processor = ResponseProcessor()
        self._request_processor = RequestProcessor(self, self._response_processor)

    def start(self):
        print('Starting PiSurvl')
        self._cmd_listener.cleanup()

        while not is_execution_terminated():
            request = self._cmd_listener.fetch_request()
            if request is None:
                time.sleep(self.REQUEST_FETCHING_RETRY_TIME)
                continue
            self._request_processor.process(request)

        print('Application is cleaning up')
        self.stop_surveillance()
        self._cmd_listener.cleanup()

    def is_surveillance_enabled(self):
        return self._surveillance_manager is not None

    def start_surveillance(self):
        if not self.is_surveillance_enabled():
            self._surveillance_manager = SurveillanceManager()
            self._surveillance_manager.start()

    def stop_surveillance(self):
        if self.is_surveillance_enabled():
            self._surveillance_manager.stop()
            self._surveillance_manager = None

    def queue_surveillance_request(self, request, callback):
        if self.is_surveillance_enabled():
            self._surveillance_manager.queue_request(request, callback)
        else:
            print('WARNING: Surveillance request received while surveillance is disabled')
