import unittest
from pathlib import Path
from unittest.mock import patch

from tools import common


class BuildPathTest(unittest.TestCase):
    def test_wrapper_cache_name_is_compact_and_revision_scoped(self):
        version = {"CEF_COMMIT_HASH": "8042e43d20cca43f182c3fc72e762b000f6ee22f"}
        with patch.object(common, "get_cefpython_version", return_value=version):
            self.assertEqual(
                "w8042e43t26",
                common.get_wrapper_build_basename("MT", "2026"),
            )
            self.assertEqual(
                "w8042e43d22",
                common.get_wrapper_build_basename("MD", "2022"),
            )

    def test_native_object_directories_are_compact(self):
        self.assertEqual("o", Path(common.BUILD_CEFPYTHON).name)
        self.assertEqual(
            f"app{common.PYVERSION}{common.OS_POSTFIX2}",
            Path(common.BUILD_CEFPYTHON_APP).name,
        )
        self.assertEqual(
            f"client{common.PYVERSION}{common.OS_POSTFIX2}",
            Path(common.BUILD_CLIENT_HANDLER).name,
        )
        self.assertEqual(
            f"utils{common.PYVERSION}{common.OS_POSTFIX2}",
            Path(common.BUILD_CPP_UTILS).name,
        )
        self.assertEqual(
            f"subprocess{common.PYVERSION}{common.OS_POSTFIX2}",
            Path(common.BUILD_SUBPROCESS).name,
        )


if __name__ == "__main__":
    unittest.main()
