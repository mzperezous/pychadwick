.PHONY: install install-dev test lint build clean

install:
	uv pip install -e .

install-dev:
	uv pip install -e ".[dev]"

test: install-dev
	uv run pytest tests/

lint: install-dev
	uv run ruff check pychadwick tests

build:
	uv build

clean:
	rm -rf build dist *.egg-info pychadwick/lib
