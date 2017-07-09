from unittest import TestCase

from mockito import mock, verify, when
from parameterized import parameterized

from pisurvl.exceptions import UnknownCommandException
from pisurvl.messaging.request_processor import RequestProcessor


class TestRequestProcessor(TestCase):
    def setUp(self):
        self._surveillance_manager = mock(strict=True)
        self._response_processor = mock(strict=True)

    def test_that_an_exception_is_thrown_if_command_is_not_known(self):
        request_processor = RequestProcessor(
            self._surveillance_manager,
            self._response_processor)

        with self.assertRaises(UnknownCommandException):
            request_processor.process(self.create_request('unknown-cmd'))

    def test_that_it_starts_surveillance_when_requested(self):
        when(self._surveillance_manager).start_surveillance()
        when(self._surveillance_manager).is_surveillance_enabled() \
            .thenReturn(True)

        request = self.create_request('enable')

        when(self._response_processor).process(
            self.create_response(request, enabled=True))

        request_processor = RequestProcessor(
            self._surveillance_manager,
            self._response_processor)

        request_processor.process(request)

        verify(self._surveillance_manager, times=1).start_surveillance()

    def test_that_it_stops_surveillance_when_requested(self):
        when(self._surveillance_manager).stop_surveillance()
        when(self._surveillance_manager).is_surveillance_enabled() \
            .thenReturn(False)

        request = self.create_request('disable')

        when(self._response_processor).process(
            self.create_response(request, enabled=False))

        request_processor = RequestProcessor(
            self._surveillance_manager,
            self._response_processor)

        request_processor.process(request)

        verify(self._surveillance_manager, times=1).stop_surveillance()

    @parameterized.expand([
        (False, False),
        (True, True)
    ])
    def test_that_it_correctly_detects_surveillance_state(self, actual, expected):
        when(self._surveillance_manager).is_surveillance_enabled() \
            .thenReturn(actual)

        request = self.create_request('query-state')

        when(self._response_processor).process(
            self.create_response(request, enabled=expected))

        request_processor = RequestProcessor(
            self._surveillance_manager,
            self._response_processor)

        request_processor.process(request)

    @staticmethod
    def create_request(cmd):
        return {'id': '1', 'cmd': cmd}

    @staticmethod
    def create_response(request, **kwargs):
        return {**request, **kwargs}
