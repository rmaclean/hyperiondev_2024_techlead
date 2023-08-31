import unittest
import internals.config
from unittest.mock import call, patch


class ConfigTests(unittest.TestCase):
    @patch(
        "internals.config.Config.getConfig",
        return_value={"DROPBOX_ACCESS_TOKEN": "", "ROOT_FOLDER": ""},
    )
    @patch("sys.exit")
    def test_without_config_should_error_out_and_also_set_defaults(self, _, __):
        with patch("builtins.print") as mock_print:
            config = internals.config.Config().setup()

            self.assertEqual(config.access_token, "")
            self.assertEqual(config.syncfolder, "syncfolder")
            self.assertEqual(
                mock_print.call_args,
                call(
                    "Access token is not set. Please see README.md for how to configure this app."
                ),
            )

    @patch(
        "internals.config.Config.getConfig",
        return_value={"DROPBOX_ACCESS_TOKEN": "demo", "ROOT_FOLDER": ""},
    )
    def test_with_access_token_set_works(self, _):
        config = internals.config.Config().setup()

        self.assertEqual(config.access_token, "demo")
        self.assertEqual(config.syncfolder, "syncfolder")

    @patch(
        "internals.config.Config.getConfig",
        return_value={"DROPBOX_ACCESS_TOKEN": "demo", "ROOT_FOLDER": "awesome"},
    )
    def test_setting_root_folder_ignores_defaults(self, _):
        config = internals.config.Config().setup()

        self.assertEqual(config.access_token, "demo")
        self.assertEqual(config.syncfolder, "awesome")
