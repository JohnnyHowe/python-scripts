"""
Delete redundant Godot .import files when the source file is missing.
"""
import argparse
import os
from pathlib import Path


def godot_delete_redunant_import_files(project_path: Path, silent: bool) -> int:
	redundant_import_files = list(_find_redundant_import_files(project_path))
	_delete_files(redundant_import_files)

	if silent:
		return 0

	print(f"Redundant .import files deleted: {len(redundant_import_files)}")
	for filename in redundant_import_files:
		print(f" - {filename}")
	return 0


def _find_redundant_import_files(project_path: Path):
	for root, _, files in os.walk(project_path):
		for filename in _find_redundant_import_files_in_folder(files):
			yield os.path.join(root, filename)


def _find_redundant_import_files_in_folder(file_names: list):
	file_names = sorted(file_names)

	pairings = {}
	for filename in file_names:
		name = filename.split(".")[0]
		if name not in pairings:
			pairings[name] = [None, None]

		if filename.endswith(".import"):
			pairings[name][1] = filename
		else:
			pairings[name][0] = filename

	for filename, import_filename in pairings.values():
		if filename is None:
			yield import_filename


def _delete_files(file_paths: list):
	for file_path in file_paths:
		os.remove(file_path)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Delete redundant Godot .import files when the source file is missing.")
	parser.add_argument("path", type=Path, nargs="?", default=Path("."), help="Godot project root.")
	parser.add_argument("--silent", action="store_true", help="Suppress output.")
	args = parser.parse_args()

	raise SystemExit(godot_delete_redunant_import_files(args.path, args.silent))
