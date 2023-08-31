from array import array
import unittest
from unittest.mock import Mock, call, mock_open, patch
import internals.dropboxutils
import dropbox


class DropboxUtilsTests(unittest.TestCase):
    @patch("dropbox.Dropbox.users_get_current_account", return_value={})
    def test_setup_works_correctly_with_valid_auth(self, _):
        dropbox_utils = internals.dropboxutils.DropboxUtils()
        result = dropbox_utils.setup("demo")

        self.assertEqual(result, dropbox_utils)
        self.assertEqual(dropbox_utils.account, {})

    @patch("sys.exit")
    @patch("builtins.print")
    def test_setup_fails_with_invalid_token(self, _, mock_print):
        dropbox_utils = internals.dropboxutils.DropboxUtils()
        with patch("builtins.print") as mock_print:
            dropbox_utils.setup("demo")
            self.assertEqual(mock_print.call_count, 2)

            self.assertEqual(
                mock_print.call_args_list,
                [
                    call(
                        "Looks like your access token is incorrect. Please see README.md to configure and set it."
                    ),
                    call("Error from Dropbox: AuthError('invalid_access_token', None)"),
                ],
            )

    @patch("dropbox.Dropbox.users_get_current_account", return_value={})
    @patch(
        "dropbox.Dropbox.files_list_folder",
        side_effect=dropbox.exceptions.ApiError("", "", "", ""),
    )
    def test_list_folder_returns_empty_dict_on_error(self, _, __):
        dropbox_utils = internals.dropboxutils.DropboxUtils().setup("asd")
        result = dropbox_utils.list_folder("blag")
        self.assertEqual(result, {})

    @patch("dropbox.Dropbox.users_get_current_account", return_value={})
    @patch(
        "dropbox.Dropbox.files_list_folder",
        return_value=Mock(entries=[]),
    )
    def test_list_folder_returns_empty_when_no_files(self, _, __):
        dropbox_utils = internals.dropboxutils.DropboxUtils().setup("asd")
        result = dropbox_utils.list_folder("blag")
        self.assertEqual(result, {})

    @patch("dropbox.Dropbox.users_get_current_account", return_value={})
    def test_list_folder_returns_files_when_exists(self, _):
        dropbox_utils = internals.dropboxutils.DropboxUtils().setup("asd")
        mockFile =  Mock(client_modified=1, size=1)
        mockFile.name = "demo.txt"
        with patch("dropbox.Dropbox.files_list_folder", return_value=Mock(entries=[mockFile])):
          result = dropbox_utils.list_folder("blag")

        self.assertEqual(result, {"demo.txt": {"modified": 1, "size": 1}})

    @patch("dropbox.Dropbox.users_get_current_account", return_value={})
    @patch(
        "dropbox.Dropbox.files_download",
        side_effect=dropbox.exceptions.HttpError("id", 500, "error"),
    )
    def test_download_fails_when_http_error(self, _, __):
        dropbox_utils = internals.dropboxutils.DropboxUtils().setup("asd")
        with patch("builtins.print") as mock_print:
            dropbox_utils.download("asd", "asd", "asd")
            self.assertEqual(
                mock_print.call_args_list,
                [
                    call("*** HTTP download error: error"),
                ],
            )

    @patch("dropbox.Dropbox.users_get_current_account", return_value={})
    @patch(
        "dropbox.Dropbox.files_download",
        return_value=(Mock(), Mock(content=array("b"))),
    )
    def test_download_writes_file_successfully(self, _, __):
        dropbox_utils = internals.dropboxutils.DropboxUtils().setup("asd")
        mock_open_handler = mock_open()
        with patch("builtins.open", mock_open_handler):
            dropbox_utils.download("asd", "asd", "asd")

        mock_open_handler.assert_called()
        handle = mock_open_handler()
        handle.write.assert_called()

    @patch("dropbox.Dropbox.users_get_current_account", return_value={})
    @patch(
        "dropbox.Dropbox.files_upload",
        side_effect=dropbox.exceptions.ApiError("id", "error", "user_message_text", ""),
    )
    def test_upload_fails_when_api_error(self, _, upload_mock):
        dropbox_utils = internals.dropboxutils.DropboxUtils().setup("asd")
        mock_open_handler = mock_open()

        with patch("builtins.print") as mock_print:
            with patch("builtins.open", mock_open_handler):
                dropbox_utils.upload("asd", "asd", "asd")

            self.assertEqual(
                mock_print.call_args_list,
                [
                    call("*** API upload error: user_message_text"),
                ],
            )

        mock_open_handler.assert_called()
        handle = mock_open_handler()
        handle.read.assert_called()
        upload_mock.assert_called()

    @patch("dropbox.Dropbox.users_get_current_account", return_value={})
    @patch("dropbox.Dropbox.files_upload")
    def test_upload_writes_file_successfully(self, _, upload_mock):
        dropbox_utils = internals.dropboxutils.DropboxUtils().setup("asd")
        mock_open_handler = mock_open()
        with patch("builtins.open", mock_open_handler):
            dropbox_utils.upload("asd", "asd", "asd")

        mock_open_handler.assert_called()
        handle = mock_open_handler()
        handle.read.assert_called()
        upload_mock.assert_called()
