import tempfile
import tarfile
import unittest
from io import BytesIO
from pathlib import Path
from pathlib import PureWindowsPath
from unittest.mock import patch

from tools import prepare_cef


class PrepareCefTest(unittest.TestCase):
    def test_extract_archive_uses_compact_temporary_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            build_dir = Path(temp_dir) / "build"
            build_dir.mkdir()
            distribution_name = (
                "cef_binary_150.0.10+g8042e43+chromium-150.0.7871.101_"
                "windows64_minimal"
            )
            archive_path = build_dir / f"{distribution_name}.tar.bz2"
            member_name = f"{distribution_name}/libcef.dll"
            contents = b"cef"
            with tarfile.open(archive_path, "w:bz2") as archive:
                member = tarfile.TarInfo(member_name)
                member.size = len(contents)
                archive.addfile(member, BytesIO(contents))

            distribution_path = prepare_cef.extract_archive(
                archive_path,
                build_dir,
            )

            self.assertEqual(build_dir / distribution_name, distribution_path)
            self.assertEqual(
                contents,
                (distribution_path / "libcef.dll").read_bytes(),
            )
            self.assertFalse(
                (build_dir / prepare_cef.EXTRACTION_TEMP_DIRNAME).exists()
            )

    def test_extraction_path_keeps_legacy_windows_headroom(self):
        typical_repository_path_length = 70
        required_headroom = 20
        distribution_name = (
            "cef_binary_150.0.10+g8042e43+chromium-150.0.7871.101_"
            "windows64_minimal"
        )
        longest_member = PureWindowsPath(
            distribution_name,
            "libcef_dll",
            "ctocpp",
            "test",
            "api_version_test_ref_ptr_library_child_child_v2_ctocpp.cc",
        )
        relative_target = PureWindowsPath(
            "build",
            prepare_cef.EXTRACTION_TEMP_DIRNAME,
            longest_member,
        )
        projected_length = (
            typical_repository_path_length + 1 + len(str(relative_target))
        )

        self.assertLessEqual(projected_length, 260 - required_headroom)

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
