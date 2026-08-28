"""Download, verify, extract, and synchronize pinned CEF distributions."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tarfile
from urllib.request import urlopen


TOOLS_DIR = Path(__file__).resolve().parent
ROOT_DIR = TOOLS_DIR.parent
MANIFEST_PATH = TOOLS_DIR / "cef_version.json"
REQUIRED_PLATFORM_KEYS = frozenset({"archive", "url", "sha256"})
EXTRACTION_TEMP_DIRNAME = ".cef-x"
VERSION_POSTFIXES = {
    "windows": "win",
    "macos": "mac",
    "linux": "linux",
}


def load_manifest() -> dict:
    """Return the pinned CEF version manifest."""
    with MANIFEST_PATH.open(encoding="utf-8") as manifest_file:
        return json.load(manifest_file)


def get_pinned_platform_names(manifest: dict) -> tuple[str, ...]:
    """Return platforms whose archives are fully pinned in the manifest."""
    return tuple(
        platform_name
        for platform_name, platform_manifest in manifest["platforms"].items()
        if REQUIRED_PLATFORM_KEYS.issubset(platform_manifest)
    )


def get_version_postfix(platform_name: str) -> str:
    """Return the CEFPython version-header postfix for a manifest platform."""
    for platform_prefix, version_postfix in VERSION_POSTFIXES.items():
        if platform_name.startswith(platform_prefix):
            return version_postfix
    raise RuntimeError(f"Unknown CEF platform family: {platform_name}")


def calculate_sha256(path: Path) -> str:
    """Calculate the SHA-256 checksum for a file."""
    digest = hashlib.sha256()
    with path.open("rb") as source_file:
        for chunk in iter(lambda: source_file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_archive(url: str, destination: Path) -> None:
    """Download an archive atomically to the requested destination."""
    temporary_path = destination.with_suffix(destination.suffix + ".part")
    print(f"[prepare_cef.py] Downloading {url}")
    with urlopen(url) as response, temporary_path.open("wb") as output_file:
        shutil.copyfileobj(response, output_file)
    temporary_path.replace(destination)


def verify_archive(archive_path: Path, expected_sha256: str) -> None:
    """Reject an archive whose SHA-256 does not match the manifest."""
    actual_sha256 = calculate_sha256(archive_path)
    if actual_sha256.lower() != expected_sha256.lower():
        raise RuntimeError(
            f"CEF archive checksum mismatch: expected {expected_sha256}, got {actual_sha256}"
        )
    print(f"[prepare_cef.py] Verified {archive_path.name}: {actual_sha256}")


def extract_archive(archive_path: Path, build_dir: Path) -> Path:
    """Safely extract the CEF archive and return its root directory."""
    distribution_name = archive_path.name.removesuffix(".tar.bz2")
    distribution_path = build_dir / distribution_name
    if distribution_path.is_dir():
        return distribution_path

    temporary_path = build_dir / EXTRACTION_TEMP_DIRNAME
    if temporary_path.exists():
        shutil.rmtree(temporary_path)
    temporary_path.mkdir(parents=True)
    build_root = build_dir.resolve()
    with tarfile.open(archive_path, "r:bz2") as archive:
        for member in archive.getmembers():
            target_path = (build_dir / member.name).resolve()
            if build_root not in target_path.parents and target_path != build_root:
                raise RuntimeError(f"Unsafe path in CEF archive: {member.name}")
        archive.extractall(temporary_path, filter="data")

    extracted_path = temporary_path / distribution_name
    if not extracted_path.is_dir():
        raise RuntimeError(f"CEF archive did not contain {distribution_name}")
    # Path.replace() can fail with WinError 5 when a Linux or macOS archive is
    # extracted on Windows. shutil.move() falls back to copy-and-remove when
    # the native directory rename is unavailable.
    shutil.move(str(extracted_path), str(distribution_path))
    temporary_path.rmdir()
    return distribution_path


def write_api_metadata(manifest: dict) -> None:
    """Write CEFPython's compact, parser-friendly API version metadata."""
    hashes = manifest["api_hashes"]
    contents = f"""// Generated from tools/cef_version.json by tools/prepare_cef.py.
#ifndef CEFPYTHON_CEF_API_HASH_H_
#define CEFPYTHON_CEF_API_HASH_H_

#define CEF_API_VERSION {manifest["api_version"]}
#if defined(OS_WIN)
#define CEF_API_HASH_PLATFORM \"{hashes["windows"]}\"
#elif defined(OS_MAC)
#define CEF_API_HASH_PLATFORM \"{hashes["macos"]}\"
#elif defined(OS_LINUX)
#define CEF_API_HASH_PLATFORM \"{hashes["linux"]}\"
#endif
#define CEF_API_HASH_UNIVERSAL CEF_API_HASH_PLATFORM

#endif  // CEFPYTHON_CEF_API_HASH_H_
"""
    metadata_path = ROOT_DIR / "src" / "version" / "cef_api_hash.h"
    metadata_path.write_text(contents, encoding="utf-8", newline="\n")


def copy_text_file(source_path: Path | str, destination_path: Path | str) -> str:
    """Copy a vendored text file with repository-standard LF line endings."""
    source_path = Path(source_path)
    destination_path = Path(destination_path)
    contents = source_path.read_bytes().replace(b"\r\n", b"\n")
    destination_path.write_bytes(contents)
    shutil.copymode(source_path, destination_path)
    return str(destination_path)


def copy_missing_headers(source_include: Path, destination_include: Path) -> int:
    """Add headers that exist only in another platform distribution."""
    copied_count = 0
    for source_path in sorted(source_include.rglob("*")):
        if not source_path.is_file():
            continue
        relative_path = source_path.relative_to(source_include)
        destination_path = destination_include / relative_path
        if destination_path.exists():
            continue
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        copy_text_file(source_path, destination_path)
        copied_count += 1
    return copied_count


def add_linux_config(destination_include: Path, linux_include: Path) -> None:
    """Preserve Linux-only CEF configuration in the combined header tree."""
    linux_config = (linux_include / "cef_config.h").read_text(encoding="utf-8")
    if "#define CEF_X11 1" not in linux_config:
        return

    destination_config_path = destination_include / "cef_config.h"
    destination_config = destination_config_path.read_text(encoding="utf-8")
    if "#define CEF_X11 1" in destination_config:
        return

    header_guard = "#define CEF_INCLUDE_CEF_CONFIG_H_\n"
    linux_config_block = (
        "\n#if defined(__linux__)\n"
        "#define CEF_X11 1\n"
        "#endif\n"
    )
    destination_config = destination_config.replace(
        header_guard,
        header_guard + linux_config_block,
        1,
    )
    destination_config_path.write_text(destination_config, encoding="utf-8")


def synchronize_headers(
    distribution_paths: dict[str, Path],
    manifest: dict,
) -> None:
    """Assemble vendored headers from every pinned platform distribution."""
    canonical_platform = manifest["header_source_platform"]
    if canonical_platform not in distribution_paths:
        raise RuntimeError(
            f"Header source platform is not pinned: {canonical_platform}"
        )

    source_include = distribution_paths[canonical_platform] / "include"
    destination_include = ROOT_DIR / "src" / "include"
    if destination_include.exists():
        shutil.rmtree(destination_include)
    shutil.copytree(
        source_include,
        destination_include,
        copy_function=copy_text_file,
    )

    copied_headers = {}
    for platform_name, distribution_path in distribution_paths.items():
        if platform_name == canonical_platform:
            continue
        copied_headers[platform_name] = copy_missing_headers(
            distribution_path / "include",
            destination_include,
        )

    linux_platform = next(
        (
            platform_name
            for platform_name in distribution_paths
            if platform_name.startswith("linux")
        ),
        None,
    )
    if linux_platform:
        add_linux_config(
            destination_include,
            distribution_paths[linux_platform] / "include",
        )

    version_dir = ROOT_DIR / "src" / "version"
    written_version_postfixes = set()
    for platform_name, distribution_path in distribution_paths.items():
        version_postfix = get_version_postfix(platform_name)
        version_header = distribution_path / "include" / "cef_version.h"
        destination_version = version_dir / f"cef_version_{version_postfix}.h"
        if version_postfix in written_version_postfixes:
            existing_contents = destination_version.read_bytes()
            version_contents = version_header.read_bytes().replace(b"\r\n", b"\n")
            if existing_contents != version_contents:
                raise RuntimeError(
                    "CEF version headers differ within platform family "
                    f"{version_postfix}: {platform_name}"
                )
            continue
        copy_text_file(version_header, destination_version)
        written_version_postfixes.add(version_postfix)

    canonical_version = source_include / "cef_version.h"
    for platform_name in manifest["platforms"]:
        version_postfix = get_version_postfix(platform_name)
        if version_postfix in written_version_postfixes:
            continue
        copy_text_file(
            canonical_version,
            version_dir / f"cef_version_{version_postfix}.h",
        )
        written_version_postfixes.add(version_postfix)

    write_api_metadata(manifest)
    platform_summary = ", ".join(
        f"{platform_name} (+{copied_headers.get(platform_name, 0)} unique)"
        for platform_name in distribution_paths
    )
    print(
        "[prepare_cef.py] Synchronized headers from "
        f"{platform_summary}; common={canonical_platform}"
    )


def prepare_distribution(
    platform_name: str,
    manifest: dict,
) -> Path:
    """Download, verify, and extract one pinned CEF distribution."""
    platform_manifest = manifest["platforms"][platform_name]
    if not REQUIRED_PLATFORM_KEYS.issubset(platform_manifest):
        raise RuntimeError(f"CEF binaries for {platform_name} are not pinned yet")

    build_dir = ROOT_DIR / "build"
    build_dir.mkdir(exist_ok=True)
    archive_path = build_dir / platform_manifest["archive"]
    if not archive_path.exists():
        download_archive(platform_manifest["url"], archive_path)
    verify_archive(archive_path, platform_manifest["sha256"])
    return extract_archive(archive_path, build_dir)


def prepare_cef(platform_name: str = "windows64", synchronize: bool = True) -> Path:
    """Prepare one CEF distribution and optionally assemble all pinned headers."""
    manifest = load_manifest()
    distribution_path = prepare_distribution(platform_name, manifest)
    if synchronize:
        distribution_paths = {
            pinned_platform: (
                distribution_path
                if pinned_platform == platform_name
                else prepare_distribution(pinned_platform, manifest)
            )
            for pinned_platform in get_pinned_platform_names(manifest)
        }
        synchronize_headers(distribution_paths, manifest)
    return distribution_path


def main() -> None:
    """Run CEF preparation from the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", default="windows64")
    parser.add_argument("--no-sync", action="store_true")
    arguments = parser.parse_args()
    distribution_path = prepare_cef(arguments.platform, not arguments.no_sync)
    print(distribution_path)


if __name__ == "__main__":
    main()
