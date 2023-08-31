# Dropbox API Demo

This app is a small demo of using Dropbox via Python. It will sync a single local folder to a single folder in Dropbox and will continue to do that with a 30-second interval between attempts. It handles both uploading and downloading of files.

## Setup

This uses Python 3.11 and requirements can be installed with PiP, for example: `pip3 install -r requirements.txt`

## Configure it

To use this you will first need an access token, which you can get [from Dropbox](https://www.dropbox.com/developers/apps). For this access token make sure you select the following options when creating the app
1. Selected scoped access
2. Full Dropbox access
3. Use any name you like

Next click the Permissions tab in the Dropbox console and add the following permissions
1. `files.metadata.write` (this should automatically enable `files.metadata.read` too)
2. `files.content.write`
3. `files.content.read`

Once the permissions are set, you can click the generate access token button to get the token. If you create the token before setting the permissions, or do not submit the permissions first, then the token will be invalid and will need to be regenerated.

Next create a `.env` and add the following

```
DROPBOX_ACCESS_TOKEN=[YOUR TOKEN GOES HERE]
ROOT_FOLDER=syncfolder
```

The `ROOT_FOLDER` config defines the folder, relative to the code, to use as the root for syncing. If the folder does not exist, it will create it. If omitted, it will default to `syncfolder`

## Running it

As easy as possible: `python3 dropboxcli.py`

### Development Tools

If you want to lint the code, you can run `./lint.sh`
If you want to run the unit tests, you can run `./test.sh`

## Code Trade-offs

1. If I was building this for more reuse, I would have a lot more guards on the code. For example
   1. the setup in dropbox utils should check the access token is not empty/None
   2. the list_folder in dropbox utils should check setup is called first

2. Testing is not exhaustive; there is a lot of edge cases to think of.

## Additional Product Features

If we wanted this to be fully featured option we should add
- ability to set access token using environmental variables, so it is more useful in containers;
- ability to select which folders to sync as currently it does everything;
- ability to filter files or folders based on RegEx or other similar syntax for the name or metadata like tags, so a user can pull specific items down;
- full support for Dropbox additional features, like profile management, contact management, sharing, teams, paper etc...;
- support for smarter root folder logic, like handling user folders `~`;
- Might be useful to support appkey/app secret too if we were to productise this;
- This is based on polling, using something like watchdog to respond to events would greatly improve performance;
- Ability to handle subfolders (recursion) would be useful;
- prioritisation logic for when downloads should win over uploads, or vice versa. Things like checking which is newest would be an easier first step, but when the size differs and date/time does not, what to do logic with some sort of user interaction.
