import datetime
import unittest
from unittest.mock import patch
import internals.sync
import internals.filemanagement
import internals.dropboxutils


class SyncTests(unittest.TestCase):
    @patch("dropbox.Dropbox.users_get_current_account", return_value={})
    def test_setup_constructs_the_object_correctly(self, _):
        result = internals.sync.Sync().setup("token", "local_path", "remote_path")
        self.assertEqual(result.full_local_path, "local_path")
        self.assertEqual(result.folder_name, "remote_path")
        self.assertIsInstance(result.dropbox, internals.dropboxutils.DropboxUtils)
        self.assertIsInstance(result.fileman, internals.filemanagement.FileManagement)

    @patch("dropbox.Dropbox.users_get_current_account", return_value={})
    @patch("internals.filemanagement.FileManagement.create_folder_if_needed")
    @patch("internals.filemanagement.FileManagement.get_valid_files", return_value={
                "demo.txt": {
                    "fullname": "asd/demo.txt",
                    "modified": datetime.datetime(1970, 1, 1, 0, 0, 1),
                    "size": 42,
                }
            })
    @patch("internals.dropboxutils.DropboxUtils.list_folder", return_value={})
    def test_sync_upload_files_if_it_does_not_exist_remotely(self, _, __, ___, ____):
        sync = internals.sync.Sync().setup("token", "local_path", "remote_path")
        with patch("builtins.print") as mock_print:
            with patch("internals.dropboxutils.DropboxUtils.upload") as mock_upload:
              sync.sync()

        mock_print.assert_called_once_with("Sync complete!")
        mock_upload.assert_called_once_with("asd/demo.txt", 'remote_path', "demo.txt")

    @patch("dropbox.Dropbox.users_get_current_account", return_value={})
    @patch("internals.filemanagement.FileManagement.create_folder_if_needed")
    @patch("internals.filemanagement.FileManagement.get_valid_files", return_value={})
    @patch("internals.dropboxutils.DropboxUtils.list_folder", return_value={
                "demo.txt": {
                    "modified": datetime.datetime(1970, 1, 1, 0, 0, 1),
                    "size": 42,
                }
            })
    def test_sync_download_files_if_it_does_not_exist_locally(self, _, __, ___, ____):
        sync = internals.sync.Sync().setup("token", "local_path", "remote_path")
        with patch("builtins.print") as mock_print:
            with patch("internals.dropboxutils.DropboxUtils.download") as mock_download:
              sync.sync()

        mock_print.assert_called_once_with("Sync complete!")
        mock_download.assert_called_once_with('remote_path', 'demo.txt', 'local_path/demo.txt')

    @patch("dropbox.Dropbox.users_get_current_account", return_value={})
    @patch("internals.filemanagement.FileManagement.create_folder_if_needed")
    @patch("internals.filemanagement.FileManagement.get_valid_files", return_value={
                "demo.txt": {
                    "fullname": "asd/demo.txt",
                    "modified": datetime.datetime(1970, 1, 1, 0, 0, 1),
                    "size": 42,
                }
            })
    @patch("internals.dropboxutils.DropboxUtils.list_folder", return_value={
                "demo.txt": {
                    "modified": datetime.datetime(1970, 1, 1, 0, 0, 1),
                    "size": 42,
                }
            })
    def test_sync_does_nothing_if_files_match(self, _, __, ___, ____):
        sync = internals.sync.Sync().setup("token", "local_path", "remote_path")
        with patch("builtins.print") as mock_print:
            with patch("internals.dropboxutils.DropboxUtils.upload") as mock_upload:
              sync.sync()

        mock_print.assert_called_once_with("Sync complete!")
        mock_upload.assert_not_called()

    @patch("dropbox.Dropbox.users_get_current_account", return_value={})
    @patch("internals.filemanagement.FileManagement.create_folder_if_needed")
    @patch("internals.filemanagement.FileManagement.get_valid_files", return_value={
                "demo.txt": {
                    "fullname": "asd/demo.txt",
                    "modified": datetime.datetime(1970, 1, 1, 0, 0, 1),
                    "size": 42,
                }
            })
    @patch("internals.dropboxutils.DropboxUtils.list_folder", return_value={
                "demo.txt": {
                    "modified": datetime.datetime(1970, 1, 1, 0, 0, 1),
                    "size": 0,
                }
            })
    def test_sync_upload_files_if_it_differs_in_size(self, _, __, ___, ____):
        sync = internals.sync.Sync().setup("token", "local_path", "remote_path")
        with patch("builtins.print") as mock_print:
            with patch("internals.dropboxutils.DropboxUtils.upload") as mock_upload:
              sync.sync()

        mock_print.assert_called_once_with("Sync complete!")
        mock_upload.assert_called_once_with("asd/demo.txt", 'remote_path', "demo.txt", True)

    @patch("dropbox.Dropbox.users_get_current_account", return_value={})
    @patch("internals.filemanagement.FileManagement.create_folder_if_needed")
    @patch("internals.filemanagement.FileManagement.get_valid_files", return_value={
                "demo.txt": {
                    "fullname": "asd/demo.txt",
                    "modified": datetime.datetime(1970, 1, 1, 0, 0, 2),
                    "size": 42,
                }
            })
    @patch("internals.dropboxutils.DropboxUtils.list_folder", return_value={
                "demo.txt": {
                    "modified": datetime.datetime(1970, 1, 1, 0, 0, 1),
                    "size": 42,
                }
            })
    def test_sync_upload_files_if_it_differs_in_modified(self, _, __, ___, ____):
        sync = internals.sync.Sync().setup("token", "local_path", "remote_path")
        with patch("builtins.print") as mock_print:
            with patch("internals.dropboxutils.DropboxUtils.upload") as mock_upload:
              sync.sync()

        mock_print.assert_called_once_with("Sync complete!")
        mock_upload.assert_called_once_with("asd/demo.txt", 'remote_path', "demo.txt", True)
