import tempfile
import unittest
from pathlib import Path
from unittest.mock import call, patch

from cefpython3 import cx_freeze


class CxFreezeTest(unittest.TestCase):
    def test_copy_runtime_restores_extension_and_macos_bundle(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            package_path = temp_path / "package"
            build_path = temp_path / "build"
            runtime_path = build_path / "lib" / "cefpython3"
            package_path.mkdir()
            runtime_path.mkdir(parents=True)

            extension_name = "cefpython_py314.so"
            (package_path / extension_name).write_bytes(b"original")
            (package_path / "subprocess").write_bytes(b"subprocess")
            (package_path / "dxcompiler.dll").write_bytes(b"unused")
            (package_path / "examples").mkdir()
            (package_path / "examples" / "hello.py").write_text(
                    "print('hello')", encoding="utf-8")
            bundle_path = package_path / "cefpython3.app" / "Contents"
            bundle_path.mkdir(parents=True)
            (bundle_path / "Info.plist").write_bytes(b"plist")
            resources_path = (
                    bundle_path / "Frameworks"
                    / "Chromium Embedded Framework.framework" / "Resources")
            (resources_path / "en.lproj").mkdir(parents=True)
            (resources_path / "en.lproj" / "locale.pak").write_bytes(
                    b"english")
            (resources_path / "de.lproj").mkdir()
            (resources_path / "de.lproj" / "locale.pak").write_bytes(
                    b"german")

            (runtime_path / extension_name).write_bytes(b"rewritten")
            (build_path / extension_name).write_bytes(b"original")
            flattened_framework = (
                    build_path / "lib" / "Chromium Embedded Framework")
            flattened_framework.write_bytes(b"flattened")

            with patch("cefpython3.cx_freeze.sys.platform", "darwin"):
                copied_path = cx_freeze.copy_runtime(
                        build_path,
                        package_dir=package_path,
                        excluded_files={"dxcompiler.dll"})

            self.assertEqual(runtime_path.resolve(), copied_path)
            self.assertEqual(
                    b"original", (runtime_path / extension_name).read_bytes())
            self.assertTrue(
                    (runtime_path / "cefpython3.app"
                     / "Contents" / "Info.plist").is_file())
            copied_resources = (
                    runtime_path / "cefpython3.app" / "Contents" / "Frameworks"
                    / "Chromium Embedded Framework.framework" / "Resources")
            self.assertTrue((copied_resources / "en.lproj").is_dir())
            self.assertTrue((copied_resources / "de.lproj").is_dir())
            self.assertTrue((runtime_path / "subprocess").is_file())
            self.assertFalse((runtime_path / "dxcompiler.dll").exists())
            self.assertFalse((runtime_path / "examples").exists())
            self.assertFalse((build_path / extension_name).exists())
            self.assertFalse(flattened_framework.exists())

    def test_copy_runtime_filters_standard_and_macos_locales(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            package_path = temp_path / "package"
            build_path = temp_path / "build"
            package_path.mkdir()
            build_path.mkdir()

            locales_path = package_path / "locales"
            locales_path.mkdir()
            for filename in ("en-US.pak", "en-GB.pak", "de.pak", "enochian.pak"):
                (locales_path / filename).write_bytes(filename.encode())

            resources_path = (
                    package_path / "cefpython3.app" / "Contents" / "Frameworks"
                    / "Chromium Embedded Framework.framework" / "Resources")
            for locale_name in (
                    "en.lproj",
                    "en_GB.lproj",
                    "en_FEMININE.lproj",
                    "de.lproj",
            ):
                locale_path = resources_path / locale_name
                locale_path.mkdir(parents=True)
                (locale_path / "locale.pak").write_bytes(
                        locale_name.encode())

            with patch("cefpython3.cx_freeze.sys.platform", "darwin"):
                runtime_path = cx_freeze.copy_runtime(
                        build_path,
                        package_dir=package_path,
                        included_locales=("en",))

            copied_locales = runtime_path / "locales"
            self.assertEqual(
                    {"en-US.pak", "en-GB.pak"},
                    {path.name for path in copied_locales.iterdir()})
            copied_resources = (
                    runtime_path / "cefpython3.app" / "Contents" / "Frameworks"
                    / "Chromium Embedded Framework.framework" / "Resources")
            self.assertEqual(
                    {"en.lproj", "en_GB.lproj", "en_FEMININE.lproj"},
                    {path.name for path in copied_resources.iterdir()})

    def test_copy_runtime_rejects_empty_locale_selection(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            package_path = temp_path / "package"
            build_path = temp_path / "build"
            package_path.mkdir()
            build_path.mkdir()

            with self.assertRaises(ValueError):
                cx_freeze.copy_runtime(
                        build_path,
                        package_dir=package_path,
                        included_locales=())

    def test_copy_runtime_splits_linux_symbols_outside_build(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            package_path = temp_path / "package"
            build_path = temp_path / "build" / "game"
            package_path.mkdir()
            build_path.mkdir(parents=True)
            (package_path / "libcef.so").write_bytes(b"unstripped")

            with (
                patch("cefpython3.cx_freeze.sys.platform", "linux"),
                patch(
                    "cefpython3.cx_freeze._extract_and_strip_linux_symbols"
                ) as split_symbols,
            ):
                runtime_path = cx_freeze.copy_runtime(
                    build_path,
                    package_dir=package_path,
                )

            split_symbols.assert_called_once_with(
                runtime_path / "libcef.so",
                (build_path.parent / "game.debug" / "libcef.so.debug").resolve(),
            )

    def test_extract_and_strip_linux_symbols_uses_external_debuglink(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            libcef_path = temp_path / "runtime" / "libcef.so"
            debug_path = temp_path / "symbols" / "libcef.so.debug"
            libcef_path.parent.mkdir()
            libcef_path.write_bytes(b"unstripped")

            def create_debug_file(command, check):
                self.assertTrue(check)
                if "--only-keep-debug" in command:
                    Path(command[-1]).write_bytes(b"debug")

            with (
                patch(
                    "cefpython3.cx_freeze.shutil.which",
                    side_effect=lambda tool: "/usr/bin/" + tool,
                ),
                patch(
                    "cefpython3.cx_freeze.subprocess.run",
                    side_effect=create_debug_file,
                ) as run,
            ):
                cx_freeze._extract_and_strip_linux_symbols(
                    libcef_path,
                    debug_path,
                )

            self.assertEqual(b"debug", debug_path.read_bytes())
            self.assertEqual(
                [
                    call(
                        [
                            "/usr/bin/objcopy",
                            "--only-keep-debug",
                            str(libcef_path.resolve()),
                            str(debug_path.resolve()) + ".tmp",
                        ],
                        check=True,
                    ),
                    call(
                        [
                            "/usr/bin/strip",
                            "--strip-unneeded",
                            str(libcef_path.resolve()),
                        ],
                        check=True,
                    ),
                    call(
                        [
                            "/usr/bin/objcopy",
                            "--add-gnu-debuglink=" + str(debug_path.resolve()),
                            str(libcef_path.resolve()),
                        ],
                        check=True,
                    ),
                ],
                run.call_args_list,
            )

    def test_copy_runtime_rejects_linux_symbols_inside_build(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            package_path = temp_path / "package"
            build_path = temp_path / "build"
            package_path.mkdir()
            build_path.mkdir()
            (package_path / "libcef.so").write_bytes(b"unstripped")

            with (
                patch("cefpython3.cx_freeze.sys.platform", "linux"),
                self.assertRaisesRegex(ValueError, "outside the frozen build"),
            ):
                cx_freeze.copy_runtime(
                    build_path,
                    package_dir=package_path,
                    linux_debug_symbols_path=(
                        build_path / "lib" / "cefpython3" / "libcef.so.debug"
                    ),
                )

    def test_get_module_excludes_includes_macos_bundles(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            package_path = Path(temp_dir)
            (package_path / "cefpython3.app").mkdir()

            with patch("cefpython3.cx_freeze.sys.platform", "darwin"):
                excludes = cx_freeze.get_module_excludes(package_path)

            self.assertIn("cefpython3.examples", excludes)
            self.assertIn("cefpython3.cefpython3.app", excludes)


if __name__ == "__main__":
    unittest.main()
