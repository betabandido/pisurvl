from pisurvl.google.credentials import get_credentials
from pisurvl.google.drive import DriveManager, build_service

from pisurvl.infrastructure.date_provider import DateProvider


class ImageBackupService:
    def __init__(self):
        self.image_count = 0

    def backup_image(self, image):
        """Backs up an image to Drive.

        The file will be placed in a folder for better organization. The folder name
        is the current date and hour. That means all the files uploaded within the
        same hour will be uploaded to the same folder.

        Args:
          image: Image to upload.
        """
        folder_name = DateProvider.now().strftime('D%d-%m-%yT%I%p')
        folder_id = self._create_unique_folder(folder_name)

        filename = 'motion{0:04d}.jpg'.format(self.image_count)
        self.image_count += 1

        print('Uploading image {} to folder ID: {}'.format(filename, folder_id))
        self._drive_manager().create_file(
            filename,
            image,
            'image/jpeg',
            folder_id)

    def _create_unique_folder(self, name):
        """Create a folder in Drive only if it does not exist yet.

        If the folder already exists, this method returns the folder object.

        Args:
            name: The folder name.
        Returns:
            The folder object for the created or existing folder.
        """
        files = self._drive_manager().list_files(
            name,
            exact=True,
            mime_type='application/vnd.google-apps.folder')
        if len(files) == 1:
            return files[0]['id']

        if len(files) > 1:
            raise Exception('Duplicated folder name')

        return self._drive_manager().create_folder(name)

    @staticmethod
    def _drive_manager():
        return DriveManager(build_service(get_credentials()))
