import base64
import io
import json

from PIL import Image
from pisurvl.google.credentials import get_credentials
from pisurvl.google.drive import build_service, DriveManager

from pisurvl.messaging import naming


class ResponseProcessor:
    # TODO: use application/json once there is no need to debug often.
    RESPONSE_MIME_TYPE = 'text/plain'

    def __init__(self):
        super().__init__()
        self._command_handlers = {
            'peek':         self._process_peek,
            'query-state':  self._process_state_query,
            'enable':       self._process_state_query,
            'disable':      self._process_state_query
        }

    def process(self, response):
        print('Response: {}'.format(response))

        handler = self._command_handlers.get(response['cmd'], None)
        if handler is None:
            print('Unknown response: {}'.format(response['cmd']))
            return

        handler(response)

    def _process_peek(self, response):
        frame = response['frame']
        del response['frame']

        img = Image.fromarray(frame, 'RGB')
        data = io.BytesIO()
        img.save(data, 'jpeg')
        response['image'] = base64.b64encode(data.getvalue()).decode()
        response_contents = json.dumps(response)

        drive_manager = self._drive_manager()
        drive_manager.create_file(
            naming.make_file_name('response-{}'.format(response['id'])),
            bytes(response_contents, 'utf-8'),
            self.RESPONSE_MIME_TYPE)

    def _process_state_query(self, response):
        response_contents = json.dumps(response)

        drive_manager = self._drive_manager()
        drive_manager.create_file(
            naming.make_file_name('response-{}'.format(response['id'])),
            bytes(response_contents, 'utf-8'),
            self.RESPONSE_MIME_TYPE)

    @staticmethod
    def _drive_manager():
        return DriveManager(build_service(get_credentials()))
