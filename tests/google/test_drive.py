import io
from googleapiclient.http import MediaIoBaseDownload
from mockito import expect, mock, patch, unstub, verifyNoUnwantedInteractions, when

from google.drive import DriveManager
from tests.common import ChainedMockBuilder


def test_that_list_files_returns_an_empty_list_if_file_does_not_exist():
    service = ChainedMockBuilder() \
        .add_call('files') \
        .add_call('list', ...) \
        .end_call('execute', {'files': []})

    result = DriveManager(service).list_files('non-existing-file')
    assert result == []


def test_that_list_files_returns_a_file_if_it_exists():
    service = ChainedMockBuilder() \
        .add_call('files') \
        .add_call('list', ...) \
        .end_call('execute', {'files': [{'id': '1'}]})

    result = DriveManager(service).list_files('existing-file')
    assert len(result) == 1
    assert result[0]['id'] == '1'


def test_that_list_files_returns_multiple_files_if_more_than_one_match_exists():
    service = ChainedMockBuilder() \
        .add_call('files') \
        .add_call('list', ...) \
        .end_call('execute', {'files': [{'id': '1'}, {'id': '2'}]})

    result = DriveManager(service).list_files('existing-file')
    assert len(result) == 2
    assert result[0]['id'] == '1'
    assert result[1]['id'] == '2'


def test_that_list_files_uses_a_non_exact_query_if_requested():
    query = "trashed=false and name contains 'dummy'"
    service = ChainedMockBuilder() \
        .add_call('files') \
        .add_call('list', q=query, spaces="drive", fields="files(id)") \
        .end_call('execute', {'files': []})

    DriveManager(service).list_files('dummy')


def test_that_list_files_uses_an_exact_query_if_requested():
    query = "trashed=false and name='dummy'"
    service = ChainedMockBuilder() \
        .add_call('files') \
        .add_call('list', q=query, spaces="drive", fields="files(id)") \
        .end_call('execute', {'files': []})

    DriveManager(service).list_files('dummy', exact=True)


def test_that_list_files_includes_mimetype_in_query_if_requested():
    query = "trashed=false and name contains 'dummy' and mimeType='text/plain'"
    service = ChainedMockBuilder() \
        .add_call('files') \
        .add_call('list', q=query, spaces="drive", fields="files(id)") \
        .end_call('execute', {'files': []})

    DriveManager(service).list_files('dummy', mime_type='text/plain')


def test_that_list_files_includes_order_if_requested():
    query = "trashed=false and name contains 'dummy'"
    order_by = "createdTime"
    service = ChainedMockBuilder() \
        .add_call('files') \
        .add_call('list', q=query, spaces="drive", fields="files(id)", orderBy=order_by) \
        .end_call('execute', {'files': []})

    DriveManager(service).list_files('dummy', order_by='createdTime')


def test_that_content_is_correct_when_downloading_a_file():
    bytes_io_mock = mock(strict=True)
    when(bytes_io_mock).getvalue() \
        .thenReturn('data')
    when(io).BytesIO().thenReturn(bytes_io_mock)

    downloader_mock = mock(strict=True)
    expect(downloader_mock, times=2).next_chunk() \
        .thenReturn((None, False)) \
        .thenReturn((None, True))

    patch(MediaIoBaseDownload.__new__, lambda buffer, request: downloader_mock)

    service = ChainedMockBuilder() \
        .add_call('files') \
        .add_call('get_media', ...) \
        .end_call('execute', None)

    result = DriveManager(service).download_file('1')
    assert result == 'data'

    verifyNoUnwantedInteractions()

    unstub()
