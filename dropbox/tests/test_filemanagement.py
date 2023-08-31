import datetime
import unittest
from unittest.mock import patch
import internals.filemanagement


class FileManagementTests(unittest.TestCase):
    @patch("os.path.exists", return_value=False)
    def test_create_folder_if_needed_creates_a_folder_if_needed(
        self,
        _,
    ):  # I love the ridiculous of this test name
        with patch("os.makedirs") as mock_makedirs:
            internals.filemanagement.FileManagement().create_folder_if_needed("asd")

        mock_makedirs.assert_called()

    @patch("os.path.exists", return_value=True)
    @patch("os.makedirs")
    def test_create_folder_if_needed_DOES_NOT_creates_a_folder_if_it_exists(
        self, _, mock_makedirs
    ):
        with patch("os.makedirs") as mock_makedirs:
            internals.filemanagement.FileManagement().create_folder_if_needed("asd")

        mock_makedirs.assert_not_called()

    def test_get_valid_files_returns_empty_dict_if_no_files(self):
        with patch("os.walk", return_value=[("asd", [], [])]):
            result = internals.filemanagement.FileManagement().get_valid_files("asd")

        self.assertEqual(result, {})

    def test_get_valid_files_returns_empty_dict_if_filename_is_invalid(self):
        with patch("os.walk", return_value=[("asd", [], [".demo"])]):
            result = internals.filemanagement.FileManagement().get_valid_files("asd")

        self.assertEqual(result, {})

    def test_get_valid_files_returns_data_when_file_exists(self):
        with patch("os.walk", return_value=[("asd", [], ["demo.txt"])]):
            with patch("os.path.getmtime", return_value=1):
                with patch("os.path.getsize", return_value=42):
                    result = internals.filemanagement.FileManagement().get_valid_files("asd")

        self.assertEqual(
            result,
            {
                "demo.txt": {
                    "fullname": "asd/demo.txt",
                    "modified": datetime.datetime(1970, 1, 1, 0, 0, 1),
                    "size": 42,
                }
            },
        )
