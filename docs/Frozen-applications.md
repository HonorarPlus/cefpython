# Frozen applications

CEF Python resolves its framework, resources, locales, and subprocess from the
installed `cefpython3` package. Applications should normally omit
`framework_dir_path`, `resources_dir_path`, `locales_dir_path`,
`browser_subprocess_path`, and `main_bundle_path`.

Standalone applications can use `cef.MessageLoop()` on every platform.
Closing the last cefpython-owned top-level browser releases its native window
and exits the message loop automatically. Browsers embedded into an
application-owned window remain under the host toolkit's lifecycle control.

## cx_Freeze

CEF contains native runtime files and, on macOS, nested application and
framework bundles that must be copied without modification. Use the packaged
helper after `cx_Freeze.setup()` has completed:

```python
from pathlib import Path

from cefpython3 import cx_freeze as cefpython_cx_freeze


build_root = Path("build", "exe.macosx-arm64-3.14")

excludes = [
    # Application exclusions...
    *cefpython_cx_freeze.get_module_excludes(),
]

# Pass ``excludes`` to cx_Freeze.setup(), then copy CEF after setup returns.
cefpython_cx_freeze.copy_runtime(build_root)
```

`get_module_excludes()` prevents cx_Freeze from analyzing package examples and
macOS bundles. `copy_runtime()` restores the original Cython extension, copies
the platform runtime into `lib/cefpython3`, removes duplicate root files, and
removes the framework binary that cx_Freeze may flatten on macOS.

Applications may omit unused root-level runtime files:

```python
cefpython_cx_freeze.copy_runtime(
    build_root,
    excluded_files={"dxcompiler.dll", "dxil.dll"},
)
```

All CEF locales are retained by default. Applications that ship a smaller
locale set can pass language or locale prefixes. Prefixes work with both
Windows/Linux locale files and macOS `.lproj` directories:

```python
cefpython_cx_freeze.copy_runtime(
    build_root,
    included_locales=("en",),
)
```

The example retains all English variants, such as `en-US`, `en-GB`, `en`, and
`en_GB`. Use a more specific prefix such as `("pt-BR",)` when appropriate.

The application remains responsible for its own executable or app-bundle
signing, entitlements, notarization, and platform installer.
