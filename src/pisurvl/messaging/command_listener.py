import json

from pisurvl.google.credentials import get_credentials
from pisurvl.google.drive import build_service, DriveManager

from pisurvl.messaging import naming


class CommandListener:
    """Listens for commands from Google Drive."""

    # TODO: "listener" somehow suggests this class actively polls
    # Google Drive for commands. In reality it just fetches commands.

    def cleanup(self):
        """Cleans up old files from Google Drive."""
        drive_manager = self._drive_manager()
        files = drive_manager.list_files(naming.FILE_NAME_PREFIX)
        for file in files:
            drive_manager.delete_file(file['id'])

    def fetch_request(self):
        """Fetches a request from Google Drive.

        Returns:
            The contents of the most recent request,
            or None if no request is found.
        """
        drive_manager = self._drive_manager()
        files = drive_manager.list_files(naming.make_file_name('request'),
                                         order_by='createdTime')
        if len(files) == 0:
            return None

        file_id = files[0]['id']

        data = drive_manager.download_file(files[0]['id'])
        drive_manager.delete_file(file_id)
        return json.loads(data)

    @staticmethod
    def _drive_manager():
        return DriveManager(build_service(get_credentials()))
