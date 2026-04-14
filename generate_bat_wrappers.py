"""
Generate .bat wrappers for Python scripts.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable


def generate_bat_wrappers(
	files: list[Path] | None = None,
	folders: list[Path] | None = None,
	folders_recursive: list[Path] | None = None,
	overwrite: bool = False,
) -> int:
	files = files or []
	folders = folders or []
	folders_recursive = folders_recursive or []

	scripts = _get_unique_scripts(files, folders, folders_recursive)

	for script_path in scripts:
		_create_wrapper(script_path, overwrite)

	return 0


def _get_unique_scripts(
	files: list[Path],
	folders: list[Path],
	folders_recursive: list[Path],
) -> list[Path]:
	seen: set[Path] = set()
	results: list[Path] = []

	for script_path in _iter_scripts(files, folders, folders_recursive):
		resolved = script_path.resolve()
		if resolved in seen:
			continue

		seen.add(resolved)
		results.append(resolved)

	return sorted(results, key=lambda path: str(path).lower())


def _iter_scripts(
	files: list[Path],
	folders: list[Path],
	folders_recursive: list[Path],
) -> Iterable[Path]:
	for file_path in files:
		yield from _iter_script_from_file(file_path)

	for folder_path in folders:
		yield from _iter_scripts_in_folder(folder_path, recursive=False)

	for folder_path in folders_recursive:
		yield from _iter_scripts_in_folder(folder_path, recursive=True)


def _iter_script_from_file(path: Path) -> Iterable[Path]:
	if not path.exists():
		print(f"Could not find file: {path}")
		return

	if path.suffix.lower() != ".py":
		print(f"Skipping non-Python file: {path}")
		return

	if path.name.startswith("_"):
		print(f"Skipping private script: {path}")
		return

	yield path


def _iter_scripts_in_folder(path: Path, recursive: bool) -> Iterable[Path]:
	if not path.exists():
		print(f"Could not find folder: {path}")
		return

	if not path.is_dir():
		print(f"Path is not a folder: {path}")
		return

	glob_pattern = "**/*.py" if recursive else "*.py"
	for script_path in sorted(path.glob(glob_pattern), key=lambda item: str(item).lower()):
		if script_path.name.startswith("_"):
			continue
		yield script_path


def _create_wrapper(script_path: Path, overwrite: bool) -> None:
	wrapper_path = script_path.with_suffix(".bat")

	if wrapper_path.exists() and not overwrite:
		print(f"Exists, skipping: {wrapper_path}")
		return

	wrapper_contents = _get_wrapper_contents(script_path)
	wrapper_path.write_text(wrapper_contents, encoding="utf-8")
	print(f"Created {wrapper_path}")


def _get_wrapper_contents(script_path: Path) -> str:
	script_filename = script_path.name
	return (
		"@echo off\n"
		"setlocal\n"
		f"python \"%~dp0{script_filename}\" %*\n"
		"exit /b %errorlevel%\n"
	)


def _parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Generate .bat wrappers for Python scripts.",
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
	)
	parser.add_argument("--file", action="append", default=[], type=Path, help="Python script file. Repeatable.")
	parser.add_argument("--folder", action="append", default=[], type=Path, help="Folder to scan for Python scripts. Repeatable.")
	parser.add_argument(
		"--folder-recursive",
		action="append",
		default=[],
		type=Path,
		help="Folder to scan recursively for Python scripts. Repeatable.",
	)
	parser.add_argument("--overwrite", action="store_true", help="Overwrite existing .bat wrappers.")
	return parser.parse_args()


if __name__ == "__main__":
	args = _parse_args()
	raise SystemExit(generate_bat_wrappers(args.file, args.folder, args.folder_recursive, args.overwrite))
