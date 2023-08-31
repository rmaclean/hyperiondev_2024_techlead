import datetime
import os
import time
import unicodedata
import six

class FileManagement:
    def __allow_filesync_by_filename(self, filename):
        return not (
            filename.startswith(".")
            or filename.startswith("@")
            or filename.endswith("~")
            or filename.endswith(".pyc")
            or filename.endswith(".pyo")
        )

    def create_folder_if_needed(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def get_valid_files(self, path):
        result = {}
        for directory_path, _, files in os.walk(path):
            for name in files:
                if self.__allow_filesync_by_filename(name):
                    file_data = {}
                    file_data["fullname"] = os.path.join(directory_path, name)
                    if not isinstance(name, six.text_type):
                        name = name.decode("utf-8")
                    normalised_name = unicodedata.normalize("NFC", name)
                    modified = os.path.getmtime(file_data["fullname"])
                    file_data["modified"] = datetime.datetime(
                        *time.gmtime(modified)[:6]
                    )
                    file_data["size"] = os.path.getsize(file_data["fullname"])
                    result[normalised_name] = file_data

        return result
