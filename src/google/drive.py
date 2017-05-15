from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload, MediaIoBaseUpload
from httplib2 import Http
import io


class DriveManager:
    """Manages the interface with Google Drive."""

    def __init__(self, service):
        """Constructor.

        Args:
            service: The service object to use to interact with Google Drive.
        """
        # TODO: think about what to do if credentials expire
        self.service = service

    def list_files(self, name, order_by=None, exact=False, mime_type=None):
        """Lists the files matching or containing the given name.

        Args:
            name: The name to look for.
            order_by: Order criteria to list the files (e.g., 'createdTime').
                      See Google Drive API for more information.
            exact: Whether an exact match for the name is required.
            mime_type: MIME type of the files to list.

        Returns:
            A list of the matching files. Each file is represented as
            a dictionary with a single key: 'id' (the file identifier).
        """
        params = {
            'q': 'trashed=false',
            'spaces': 'drive',
            'fields': 'files(id)'
        }

        if exact:
            params['q'] += " and name='{}'".format(name)
        else:
            params['q'] += " and name contains '{}'".format(name)

        if mime_type is not None:
            params['q'] += " and mimeType='{}'".format(mime_type)

        if order_by is not None:
            params['orderBy'] = order_by

        result = self.service.files().list(**params).execute()
        return result['files']

    def download_file(self, file_id):
        """Downloads the file matching the given file identifier.

        Args:
            file_id: The file identifier for the file to download.

        Returns:
            The contents of the file as a byte string.
        """
        request = self.service.files().get_media(fileId=file_id)
        buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(buffer, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()

        return buffer.getvalue()

    def upload_file(self, src_name, dest_name, mime_type, parent=None):
        """Uploads an existing file.

        Args:
            src_name: Name of the source file (local name).
            dest_name: Name of the destination file (name on Google Drive).
            mime_type: media type.

        Returns:
            The file identifier of the uploaded file.
        """
        media = MediaFileUpload(src_name, mime_type)
        file_metadata = {'name': dest_name}
        if parent is not None:
            file_metadata['parents'] = [parent]

        return self._upload(file_metadata, media)

    def create_file(self, name, data, mime_type, parent=None):
        """Creates a new file on Google Drive.

        Args:
            name: The name of the file to create.
            data: Byte string containing the file data.
            mime_type: Media type.

        Returns:
            The file identifier of the uploaded file.
        """
        buffer = io.BytesIO(data)
        media = MediaIoBaseUpload(buffer, mime_type)
        file_metadata = {'name': name}
        if parent is not None:
            file_metadata['parents'] = [parent]

        return self._upload(file_metadata, media)

    def create_folder(self, name):
        """Creates a new folder on Google Drive.

        Args:
            name: The folder name.

        Returns:
            The file identifier for the folder created.
        """
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        return self._upload(file_metadata)

    def _upload(self, metadata, media=None):
        file = self.service.files().create(
            body=metadata,
            media_body=media,
            fields='id').execute()
        return file['id']

    def delete_file(self, file_id):
        """Deletes a file on Google Drive.

        Args:
            file_id: The file identifier for the file to delete.
        """
        self.service.files().delete(fileId=file_id).execute()


def build_service(credentials):
    """Creates a Google Drive service object.

    Args:
        credentials: OAuth credentials to use.

    Returns:
        The Google Drive service object.
    """
    http = credentials.authorize(Http())
    return build('drive', 'v3', http=http)
