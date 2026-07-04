import ctypes
import pathlib
import sys

FILE_EXTENSION = {"darwin": "dylib", "linux": "so", "win32": "dll", "windows": "dll"}


def _locate_library() -> pathlib.Path:
    ext = FILE_EXTENSION.get(sys.platform, "so")
    name = f"libcwevent.{ext}"
    pkg_root = pathlib.Path(__file__).absolute().parent.parent

    primary = pkg_root / "lib" / "cwevent" / name
    if primary.exists():
        return primary

    # editable installs build the lib out-of-tree; search for the artifact
    for root in (pkg_root, pkg_root.parent):
        matches = sorted(root.rglob(name))
        if matches:
            return matches[0]

    # fall through to the expected path so ctypes raises a clear load error
    return primary


class _ChadwickLibrary:
    library_path = _locate_library()

    def __init__(self):
        self._dll = None

    @property
    def libchadwick(self):
        if self._dll is None:
            self._dll = ctypes.cdll.LoadLibrary(str(self.library_path))
        return self._dll
