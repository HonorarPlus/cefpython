import sys
import unittest
from pathlib import Path
from unittest.mock import patch


TOOLS_DIR = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS_DIR))
import automate


class AutomateTest(unittest.TestCase):
    def test_prebuilt_linux_wrapper_does_not_require_sample_apps(self):
        with patch.object(automate.Options, "prebuilt_cef", True):
            wrapper_path = automate.get_linux_wrapper_library_path("cef")

        self.assertEqual(
            "cef/build_wrapper/libcef_dll_wrapper/libcef_dll_wrapper.a",
            wrapper_path.replace("\\", "/"),
        )

    def test_source_linux_wrapper_uses_sample_build(self):
        with patch.object(automate.Options, "prebuilt_cef", False):
            wrapper_path = automate.get_linux_wrapper_library_path("cef")

        self.assertEqual(
            "cef/build_cefclient/libcef_dll_wrapper/libcef_dll_wrapper.a",
            wrapper_path.replace("\\", "/"),
        )
