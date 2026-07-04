# pychadwick

Python bindings to the [Chadwick](https://github.com/chadwickbureau/chadwick)
baseball tools — parse [Retrosheet](https://www.retrosheet.org/) event files into
Python dicts or pandas DataFrames, with no external `cwevent` binary required.

`pychadwick` is a thin `ctypes` wrapper: the upstream Chadwick C sources
(`cwlib` + `cwtools`) are compiled into a single shared library that ships
inside the wheel, and the Python layer declares the argtypes/restypes and
iterates games and events.

## Why this fork

The original [`bdilday/pychadwick`](https://github.com/bdilday/pychadwick)
(PyPI `0.6.1`) no longer builds on modern Python. The C sources compile fine;
the only broken part was the **build glue**. This fork revives it for
Python 3.9+ (validated on 3.13) under the `uv` toolchain.

### What changed

- **Build backend**: legacy `scikit-build` (`from skbuild import setup`, plus
  pinned old `cmake`/`ninja`) → **`scikit-build-core`**. Metadata moved from
  `setup.py` into `pyproject.toml` (PEP 621); `setup.py` removed.
- **CMake install destination**: the compiled library now installs to
  `pychadwick/lib/cwevent/`, the exact package-relative path the `ctypes`
  loader expects, and `cmake_minimum_required` was bumped to a modern range.
- **Robust library loader** (`libutils/cwlib.py`): loads the lib from the
  in-package path for wheel/regular installs, and falls back to locating the
  out-of-tree build artifact for editable installs, so `-e .` works in dev.
- **pandas 3.0 compatibility**: the DataFrame type-coercion step used an
  in-place `.loc` dtype swap that pandas >= 3.0 rejects; switched to
  whole-column assignment.
- **Tests**: event-file URLs updated to Retrosheet's current `seasons/<year>/`
  layout (the old `event/regular/` paths now 404 upstream).

## Install

Requires a C compiler and CMake; `scikit-build-core` provisions `cmake`/`ninja`
automatically at build time.

```bash
uv pip install -e .          # editable / dev
# or a normal build + install
uv build && uv pip install dist/pychadwick-*.whl
```

## Parse example

`event_file_to_dataframe` accepts a local path or an `http(s)` URL and returns
a pandas DataFrame (one row per event, 159 columns of Retrosheet fields).

```python
from pychadwick.chadwick import Chadwick

chadwick = Chadwick()
url = (
    "https://raw.githubusercontent.com/chadwickbureau/retrosheet/"
    "master/seasons/2023/2023SFN.EVN"
)
df = chadwick.event_file_to_dataframe(url)

print(df.shape)                       # (6150, 159)
print(df["GAME_ID"].nunique())        # 81
print(df[["GAME_ID", "INN_CT", "BAT_ID", "PIT_ID", "EVENT_TX"]].head())
```

Lower-level entry points on `Chadwick`:

- `games(path_or_url)` — yields C `CWGame` pointers.
- `process_game(game_ptr)` — yields per-event dicts (`dicticize_event_string`).
- `games_to_dataframe(games)` / `event_files_to_dataframe(paths)` — batch to DataFrame.

A `pycwevent` console script (a Python stand-in for Chadwick's `cwevent`) is
also installed.

## Roadmap

- **Prebuilt wheels** via `cibuildwheel` (manylinux / macOS / Windows) so
  downstream consumers install without a local toolchain.
- **Upstream PR** proposing the `scikit-build-core` migration back to
  `bdilday/pychadwick`.
- Broaden coverage beyond event files (box scores, sub logs, daily).

## License

GPL-2.0 (inherited from Chadwick). See `LICENSE`.
