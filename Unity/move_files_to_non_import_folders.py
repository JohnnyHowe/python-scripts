"""
Move selected files under Assets into a hidden folder to prevent Unity imports.
"""
import argparse
import os
from pathlib import Path
import re
import shutil


_DEFAULT_PATTERNS = [
	r".*\.blend$",
	r".*\.xcf$",
]


def move_files_to_non_import_folders(
	root: Path,
	patterns: list[str],
	hidden_folder_name: str,
	ignore_git_submodules: bool,
	yes: bool,
) -> int:
	files_to_move_regex_compiled = [re.compile(p) for p in patterns]
	file_paths_to_move = list(_get_all_files_to_move(root, files_to_move_regex_compiled, ignore_git_submodules))

	if len(file_paths_to_move) == 0:
		print("No files found!")
		return 0

	print("Files found:")
	for path in file_paths_to_move:
		print(f"\t{path}")

	if not yes:
		if input(f"Move all to hidden folder {hidden_folder_name} (relative to each file)\n[Y/n]\n") != "Y":
			print("Aborting. Needed \"Y\" to continue.")
			return 1

	print("Moving all...")
	_move_all_to_hidden_folder(file_paths_to_move, hidden_folder_name)
	print("Done")
	return 0


def _get_all_files_to_move(root: Path, patterns: list[re.Pattern], ignore_git_submodules: bool):
	for entry in os.listdir(root):
		path = Path(os.path.join(root, entry)).absolute()

		if path.is_file():
			if _should_move_file(path, patterns):
				yield path

		elif path.is_dir():
			if _should_search_folder(path, ignore_git_submodules):
				yield from _get_all_files_to_move(path, patterns, ignore_git_submodules)


def _should_search_folder(folder_path: Path, ignore_git_submodules: bool) -> bool:
	folder_filters = [
		lambda folder_path: not _is_folder_hidden(folder_path),
		lambda folder_path: not (ignore_git_submodules and _is_folder_a_repository(folder_path)),
	]
	return all(passes_filter(folder_path) for passes_filter in folder_filters)


def _is_folder_hidden(folder_path: Path) -> bool:
	parts = os.path.split(folder_path)
	for part in parts:
		if part.startswith("."):
			return True
	return False


def _is_folder_a_repository(folder_path: Path) -> bool:
	return os.path.exists(os.path.join(folder_path, ".git"))


def _should_move_file(file_path: Path, patterns: list[re.Pattern]) -> bool:
	return any(r.search(str(file_path)) for r in patterns)


def _move_all_to_hidden_folder(file_paths: list[Path], hidden_folder_name: str):
	for file_path in file_paths:
		_move_to_hidden_folder(file_path, hidden_folder_name)


def _move_to_hidden_folder(file_path: Path, hidden_folder_name: str):
	hidden_folder_path = os.path.join(file_path.parent, hidden_folder_name)
	if not os.path.exists(hidden_folder_path):
		os.mkdir(hidden_folder_path)

	destination_file_path = os.path.join(hidden_folder_path, file_path.name)
	shutil.move(file_path, destination_file_path)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description="Move files under Assets into hidden folders to prevent Unity imports."
	)
	parser.add_argument("--root", type=Path, default=Path("Assets"), help="Root folder to scan.")
	parser.add_argument("--pattern", action="append", default=[], help="Regex for files to move (repeatable).")
	parser.add_argument("--hidden-folder", default=".do_not_import", help="Hidden folder name to create.")
	parser.add_argument("--include-submodules", action="store_true", help="Include files inside git submodules.")
	parser.add_argument("--yes", action="store_true", help="Skip confirmation prompt.")
	args = parser.parse_args()

	patterns = args.pattern if args.pattern else _DEFAULT_PATTERNS
	ignore_submodules = not args.include_submodules

	raise SystemExit(
		move_files_to_non_import_folders(
			args.root,
			patterns,
			args.hidden_folder,
			ignore_submodules,
			args.yes,
		)
	)
