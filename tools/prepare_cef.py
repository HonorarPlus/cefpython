"""Download, verify, extract, and synchronize the pinned CEF distribution."""

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


def load_manifest() -> dict:
    """Return the pinned CEF version manifest."""
    with MANIFEST_PATH.open(encoding="utf-8") as manifest_file:
        return json.load(manifest_file)


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

    temporary_path = build_dir / f"{distribution_name}.extracting"
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
    extracted_path.replace(distribution_path)
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


def synchronize_headers(distribution_path: Path, manifest: dict) -> None:
    """Replace vendored headers and generated version metadata deterministically."""
    source_include = distribution_path / "include"
    destination_include = ROOT_DIR / "src" / "include"
    if destination_include.exists():
        shutil.rmtree(destination_include)
    shutil.copytree(source_include, destination_include)

    version_header = source_include / "cef_version.h"
    version_dir = ROOT_DIR / "src" / "version"
    for platform_name in ("win", "mac", "linux"):
        shutil.copyfile(version_header, version_dir / f"cef_version_{platform_name}.h")
    write_api_metadata(manifest)
    print(f"[prepare_cef.py] Synchronized headers from {distribution_path.name}")


def prepare_cef(platform_name: str = "windows64", synchronize: bool = True) -> Path:
    """Prepare the pinned CEF distribution for a supported platform."""
    manifest = load_manifest()
    platform_manifest = manifest["platforms"][platform_name]
    required_keys = {"archive", "url", "sha256"}
    if not required_keys.issubset(platform_manifest):
        raise RuntimeError(f"CEF binaries for {platform_name} are not pinned yet")

    build_dir = ROOT_DIR / "build"
    build_dir.mkdir(exist_ok=True)
    archive_path = build_dir / platform_manifest["archive"]
    if not archive_path.exists():
        download_archive(platform_manifest["url"], archive_path)
    verify_archive(archive_path, platform_manifest["sha256"])
    distribution_path = extract_archive(archive_path, build_dir)
    if synchronize:
        synchronize_headers(distribution_path, manifest)
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
