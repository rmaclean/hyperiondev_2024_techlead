import internals.dropboxutils
import internals.filemanagement


class Sync:
    def setup(self, access_token, full_local_path, folder_name):
        self.full_local_path = full_local_path
        self.folder_name = folder_name
        self.dropbox = internals.dropboxutils.DropboxUtils().setup(access_token)

        self.fileman = internals.filemanagement.FileManagement()
        return self

    def sync(self):
        self.fileman.create_folder_if_needed(self.full_local_path)

        local_files = self.fileman.get_valid_files(self.full_local_path)
        remote_files = self.dropbox.list_folder(self.folder_name)

        # We disabling this hint since we explitly want the key to work with,
        # not just the items
        # pylint: disable=consider-using-dict-items
        for local_file_key in local_files:
            local_file = local_files[local_file_key]

            # we do not eant a default value, we only need to know if it exists or not
            # pylint: disable=consider-using-get
            if local_file_key in remote_files:
                remote_file = remote_files[local_file_key]

                if not (
                    remote_file["size"] == local_file["size"]
                    and remote_file["modified"] == local_file["modified"]
                ):
                    self.dropbox.upload(
                        local_file["fullname"], self.folder_name, local_file_key, True
                    )
            else:
                self.dropbox.upload(
                    local_file["fullname"], self.folder_name, local_file_key
                )

        # We disabling this hint since we explitly want the key to work with,
        # not just the items
        # pylint: disable=consider-using-dict-items
        for remote_file_key in remote_files:
            remote_file = remote_files[remote_file_key]
            if not remote_file_key in local_files:
                self.dropbox.download(
                    self.folder_name,
                    remote_file_key,
                    f"{self.full_local_path}/{remote_file_key}",
                )

        print("Sync complete!")
        return self
