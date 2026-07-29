"""Helpers for bundling the cefpython3 runtime with cx_Freeze."""

import filecmp
import shutil
import sys
from pathlib import Path


_CEF_RUNTIME_EXTENSIONS = {
    ".bin",
    ".dat",
    ".dll",
    ".dylib",
    ".exe",
    ".pak",
    ".plist",
    ".pyd",
    ".so",
}
_CEF_RUNTIME_DIRECTORIES = {"locales", "swiftshader"}
_MACOS_BUNDLE_SUFFIXES = (".app", ".framework")


def get_module_excludes(package_dir=None):
    """Return cefpython modules that cx_Freeze should not inspect or copy."""
    package_path = _get_package_dir(package_dir)
    excludes = ["cefpython3.examples"]
    if sys.platform == "darwin":
        excludes.extend(
            "cefpython3." + path.name
            for path in package_path.iterdir()
            if path.name.endswith(_MACOS_BUNDLE_SUFFIXES)
        )
    return excludes


def copy_runtime(
        build_root,
        package_dir=None,
        destination=None,
        excluded_files=(),
        included_locales=None,
):
    """Copy the platform CEF runtime into a completed cx_Freeze build.

    cx_Freeze may rewrite linked extension modules and flatten framework
    dependencies while analyzing them. This function restores cefpython's
    original extension module and copies platform runtime bundles intact.
    By default all locales are retained. Pass language or locale prefixes,
    such as ``("en",)`` or ``("en-US",)``, to retain only matching locales.
    """
    build_path = Path(build_root).resolve()
    package_path = _get_package_dir(package_dir)
    if destination is None:
        destination = Path("lib", "cefpython3")
    runtime_path = build_path / Path(destination)
    runtime_path.mkdir(parents=True, exist_ok=True)
    excluded_names = {str(name).lower() for name in excluded_files}

    for source_path in package_path.iterdir():
        if source_path.name.lower() in excluded_names:
            continue
        if not _is_runtime_path(source_path):
            continue
        _copy_path(source_path, runtime_path / source_path.name)

    _remove_duplicate_root_files(build_path, runtime_path)
    _filter_runtime_locales(
        build_path,
        runtime_path,
        included_locales,
    )
    if sys.platform == "darwin":
        _remove_flattened_macos_framework(build_path)
    return runtime_path


def _get_package_dir(package_dir):
    if package_dir is None:
        package_dir = Path(__file__).resolve().parent
    package_path = Path(package_dir).resolve()
    if not package_path.is_dir():
        raise FileNotFoundError(
            "cefpython3 package directory does not exist: " + str(package_path)
        )
    return package_path


def _is_runtime_path(path):
    if path.is_dir():
        return (
            path.name in _CEF_RUNTIME_DIRECTORIES
            or path.name.endswith(_MACOS_BUNDLE_SUFFIXES)
        )
    if path.name in {"subprocess", "chrome-sandbox"}:
        return True
    if path.name.startswith("cefpython_py") and path.suffix in {".pyd", ".so"}:
        return True
    return path.suffix.lower() in _CEF_RUNTIME_EXTENSIONS


def _copy_path(source_path, destination_path):
    if destination_path.is_dir():
        shutil.rmtree(destination_path)
    elif destination_path.exists():
        destination_path.unlink()
    if source_path.is_dir():
        shutil.copytree(source_path, destination_path)
    else:
        shutil.copy2(source_path, destination_path)


def _remove_duplicate_root_files(build_path, runtime_path):
    for root_file in build_path.iterdir():
        if not root_file.is_file():
            continue
        package_file = runtime_path / root_file.name
        if (
            package_file.is_file()
            and root_file.stat().st_size == package_file.stat().st_size
            and filecmp.cmp(root_file, package_file, shallow=False)
        ):
            root_file.unlink()

    root_locales = build_path / "locales"
    package_locales = runtime_path / "locales"
    if not root_locales.is_dir() or not package_locales.is_dir():
        return
    for locale_file in root_locales.iterdir():
        if not locale_file.is_file():
            continue
        package_file = package_locales / locale_file.name
        if (
            package_file.is_file()
            and locale_file.stat().st_size == package_file.stat().st_size
            and filecmp.cmp(locale_file, package_file, shallow=False)
        ):
            locale_file.unlink()
    if not any(root_locales.iterdir()):
        root_locales.rmdir()


def _filter_runtime_locales(build_path, runtime_path, included_locales):
    locale_prefixes = _normalize_locale_prefixes(included_locales)
    if locale_prefixes is None:
        return

    _filter_standard_locales(build_path / "locales", locale_prefixes)
    _filter_standard_locales(runtime_path / "locales", locale_prefixes)

    for framework_path in runtime_path.rglob(
            "Chromium Embedded Framework.framework"):
        resources_path = framework_path / "Resources"
        if not resources_path.is_dir():
            continue
        for locale_path in resources_path.glob("*.lproj"):
            if not _locale_matches(locale_path.stem, locale_prefixes):
                shutil.rmtree(locale_path)


def _normalize_locale_prefixes(included_locales):
    if included_locales is None:
        return None
    if isinstance(included_locales, str):
        included_locales = (included_locales,)
    locale_prefixes = tuple(
        str(locale).strip().lower().replace("_", "-")
        for locale in included_locales
    )
    if not locale_prefixes or any(not locale for locale in locale_prefixes):
        raise ValueError("included_locales must contain at least one locale")
    return locale_prefixes


def _filter_standard_locales(locales_path, locale_prefixes):
    if not locales_path.is_dir():
        return
    for locale_path in locales_path.iterdir():
        if (
            locale_path.is_file()
            and not _locale_matches(locale_path.stem, locale_prefixes)
        ):
            locale_path.unlink()
    if not any(locales_path.iterdir()):
        locales_path.rmdir()


def _locale_matches(locale_name, locale_prefixes):
    normalized_name = locale_name.lower().replace("_", "-")
    return any(
        normalized_name == prefix
        or normalized_name.startswith(prefix + "-")
        for prefix in locale_prefixes
    )


def _remove_flattened_macos_framework(build_path):
    framework_binary = build_path / "lib" / "Chromium Embedded Framework"
    if framework_binary.is_file():
        framework_binary.unlink()
