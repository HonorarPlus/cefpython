import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import prepare_cef


class PrepareCefTest(unittest.TestCase):
    def test_synchronize_headers_combines_pinned_platforms(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            root_path = temp_path / "repository"
            mac_distribution = temp_path / "mac"
            windows_distribution = temp_path / "windows"
            mac_include = mac_distribution / "include"
            windows_include = windows_distribution / "include"

            (mac_include / "internal").mkdir(parents=True)
            (windows_include / "internal").mkdir(parents=True)
            (root_path / "src" / "version").mkdir(parents=True)

            (mac_include / "common.h").write_text(
                "mac canonical\n", encoding="utf-8")
            (windows_include / "common.h").write_text(
                "windows variant\n", encoding="utf-8")
            (mac_include / "internal" / "cef_mac.h").write_text(
                "mac\n", encoding="utf-8")
            (windows_include / "internal" / "cef_win.h").write_bytes(
                b"windows\r\n")
            (mac_include / "cef_version.h").write_text(
                "mac version\n", encoding="utf-8")
            (windows_include / "cef_version.h").write_bytes(
                b"windows version\r\n")

            manifest = {
                "header_source_platform": "macosarm64",
                "api_version": 15101,
                "api_hashes": {
                    "windows": "windows hash",
                    "macos": "mac hash",
                    "linux": "linux hash",
                },
                "platforms": {
                    "windows64": {},
                    "macosarm64": {},
                    "linux64": {},
                },
            }
            distributions = {
                "windows64": windows_distribution,
                "macosarm64": mac_distribution,
            }

            with patch.object(prepare_cef, "ROOT_DIR", root_path):
                prepare_cef.synchronize_headers(distributions, manifest)

            destination_include = root_path / "src" / "include"
            self.assertEqual(
                "mac canonical\n",
                (destination_include / "common.h").read_text(encoding="utf-8"))
            self.assertTrue(
                (destination_include / "internal" / "cef_mac.h").is_file())
            self.assertTrue(
                (destination_include / "internal" / "cef_win.h").is_file())
            self.assertEqual(
                "mac version\n",
                (root_path / "src" / "version"
                 / "cef_version_mac.h").read_text(encoding="utf-8"))
            self.assertEqual(
                "windows version\n",
                (root_path / "src" / "version"
                 / "cef_version_win.h").read_text(encoding="utf-8"))
            self.assertEqual(
                b"windows\n",
                (destination_include / "internal"
                 / "cef_win.h").read_bytes())
            self.assertEqual(
                "mac version\n",
                (root_path / "src" / "version"
                 / "cef_version_linux.h").read_text(encoding="utf-8"))

    def test_get_pinned_platform_names_skips_metadata_only_platforms(self):
        manifest = {
            "platforms": {
                "windows64": {
                    "archive": "windows.tar.bz2",
                    "url": "https://example.invalid/windows",
                    "sha256": "windows hash",
                },
                "macosx64": {
                    "architecture": "x86_64",
                    "distribution": "minimal",
                },
                "macosarm64": {
                    "archive": "mac.tar.bz2",
                    "url": "https://example.invalid/mac",
                    "sha256": "mac hash",
                },
            },
        }

        self.assertEqual(
            ("windows64", "macosarm64"),
            prepare_cef.get_pinned_platform_names(manifest),
        )


if __name__ == "__main__":
    unittest.main()
