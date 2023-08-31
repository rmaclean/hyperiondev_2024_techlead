import threading
import os
from internals.config import Config
import internals.sync


def set_interval(function_to_run, interval_seconds):
    threading_event = threading.Event()
    while not threading_event.wait(interval_seconds):
        function_to_run()


config = Config().setup()

rootDir = os.path.dirname(__file__)
fullSyncPath = os.path.join(rootDir, config.syncfolder)

print(f"Begining sync of {fullSyncPath}")

syncman = internals.sync.Sync().setup(config.access_token, fullSyncPath, config.syncfolder).sync()

# Future change would be to keep the above sync and change this to event driven
# as mentioned in the readme.md

set_interval(syncman.sync, 30)
