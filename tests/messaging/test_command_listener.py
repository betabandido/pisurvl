import json
from mockito import ANY, mock, verify, when
from unittest import TestCase

from messaging.command_listener import CommandListener


class TestCommandListener(TestCase):
    A_REQUEST = {'foo': 'bar'}

    def setUp(self):
        self._drive_manager = mock(strict=True)
        when(CommandListener)._drive_manager() \
            .thenReturn(self._drive_manager)

        when(self._drive_manager).delete_file(ANY(str))
        when(self._drive_manager).download_file('id_new') \
            .thenReturn(json.dumps(self.A_REQUEST))

        self._command_listener = CommandListener()

    def test_that_old_files_are_deleted(self):
        self._setup_files('id1', 'id2')

        self._command_listener.cleanup()

        verify(self._drive_manager, times=1) \
            .delete_file('id1')
        verify(self._drive_manager, times=1) \
            .delete_file('id2')

    def test_that_no_action_is_taken_if_no_request_is_available(self):
        self._setup_files()

        request = self._command_listener.fetch_request()

        self.assertIsNone(request)
        verify(self._drive_manager, times=0) \
            .delete_file(ANY)

    def test_that_the_most_recent_request_is_returned(self):
        self._setup_files('id_new', 'id_old')

        request = self._command_listener.fetch_request()

        self.assertEqual(request, self.A_REQUEST)
        verify(self._drive_manager, times=1) \
            .delete_file('id_new')

    def _setup_files(self, *args):
        files = [{'id': id} for id in args]
        when(self._drive_manager).list_files(...) \
            .thenReturn(files)
