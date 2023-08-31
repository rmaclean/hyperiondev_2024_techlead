import sys
from dotenv import dotenv_values


class Config:
    def getConfig(self):
        return dotenv_values(".env")

    def setup(self):
        config = self.getConfig()
        self.access_token = config.get("DROPBOX_ACCESS_TOKEN")
        self.syncfolder = config.get("ROOT_FOLDER")
        self.__validate()
        return self

    def __validate(self):
        if not self.syncfolder or self.syncfolder is None:
            self.syncfolder = "syncfolder"

        if not self.access_token or self.access_token is None:
            print(
                "Access token is not set. Please see README.md for how to configure this app."
            )
            sys.exit(-1)
