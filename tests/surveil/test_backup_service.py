import datetime
from mockito import ANY, mock, unstub, verify, when
from unittest import TestCase

from infrastructure.date_provider import DateProvider
from surveil.backup import ImageBackupService


class TestBackupService(TestCase):
    def setUp(self):
        self._drive_manager_mock = mock(strict=True)
        when(ImageBackupService)._drive_manager() \
            .thenReturn(self._drive_manager_mock)

    def tearDown(self):
        unstub()

    def test_that_it_throws_an_exception_if_target_dir_is_duplicated(self):
        self._setup_duplicated_target_dir()

        backup_service = ImageBackupService()
        with self.assertRaises(Exception) as contextManager:
            backup_service.backup_image(None)

        exception = contextManager.exception
        self.assertEqual(str(exception), 'Duplicated folder name')

    def test_that_no_folder_is_created_if_it_already_exists(self):
        self._setup_existing_target_dir()

        backup_service = ImageBackupService()
        backup_service.backup_image(None)

        verify(self._drive_manager_mock, times=0).create_folder(ANY(str))

    def test_that_target_folder_has_correct_name(self):
        self._setup_existing_target_dir()

        when(DateProvider).now() \
            .thenReturn(datetime.datetime(2017, 12, 31, 12))

        backup_service = ImageBackupService()
        backup_service.backup_image(None)

        verify(self._drive_manager_mock, times=1).list_files(
            'D31-12-17T12PM',
            exact=True,
            mime_type='application/vnd.google-apps.folder'
        )

    def test_that_file_name_uses_an_increasing_count(self):
        self._setup_existing_target_dir()

        backup_service = ImageBackupService()
        backup_service.backup_image(None)
        backup_service.backup_image(None)

        verify(self._drive_manager_mock, times=1).create_file(
            'motion0000.jpg', ANY, 'image/jpeg', ANY(str))

        verify(self._drive_manager_mock, times=1).create_file(
            'motion0001.jpg', ANY, 'image/jpeg', ANY(str))

    def _setup_duplicated_target_dir(self):
        when(self._drive_manager_mock).list_files(
            ANY(str), exact=True, mime_type='application/vnd.google-apps.folder') \
            .thenReturn([{'id': 'id1'}, {'id': 'id2'}])

    def _setup_existing_target_dir(self):
        when(self._drive_manager_mock).list_files(
            ANY(str), exact=True, mime_type='application/vnd.google-apps.folder') \
            .thenReturn([{'id': 'id1'}])

        when(self._drive_manager_mock).create_file(
            ANY(str), ANY, ANY(str), ANY(str)
        )
