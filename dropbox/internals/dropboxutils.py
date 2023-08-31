import datetime
import os
import sys
import time
import dropbox


class DropboxUtils:
    def setup(self, access_token):
        self.dbx = dropbox.Dropbox(access_token)

        try:
            self.account = self.dbx.users_get_current_account()
        except dropbox.exceptions.AuthError as error:
            print(
                "Looks like your access token is incorrect. Please see README.md to configure" +
                " and set it."
            )
            print(f"Error from Dropbox: {error.error}")
            sys.exit(-1)

        return self

    def list_folder(self, subfolder):
        try:
            res = self.dbx.files_list_folder(f"/{subfolder}")
            result = {}
            for entry in res.entries:
                fileinfo = {}
                fileinfo["modified"] = entry.client_modified
                fileinfo["size"] = entry.size
                result[entry.name] = fileinfo
            return result
        except dropbox.exceptions.ApiError:
            # empty or does not exist
            return {}

    def download(self, folder, filename, full_local_filename):
        try:
            _, res = self.dbx.files_download(f"/{folder}/{filename}")
        except dropbox.exceptions.HttpError as err:
            print(f"*** HTTP download error: {err.body}")
            return

        with open(full_local_filename, "wb") as file:
            file.write(res.content)

    def upload(self, full_local_filename, dropbox_path, filename, overwrite=False):
        mode = (
            dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add
        )

        mtime = os.path.getmtime(full_local_filename)
        with open(full_local_filename, "rb") as file:
            data = file.read()
        try:
            self.dbx.files_upload(
                data,
                f"/{dropbox_path}/{filename}",
                mode,
                client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
                mute=True,
            )
        except dropbox.exceptions.ApiError as err:
            print(f"*** API upload error: {err.user_message_text}")
