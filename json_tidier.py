"""
Tidy all JSON files in a directory and subdirectories by removing trailing commas.
"""
import argparse
import os
from pathlib import Path
import re

_IGNORE_DIRS = [".vscode"]


def json_tidier(path: Path) -> int:
	count = 0
	for file_name in _get_all_json_files_in_folder_and_subfolders(path):
		if _tidy_file(file_name):
			count += 1
	print(f"JSON files tidied: {count}")
	return 0


def _get_all_json_files_in_folder_and_subfolders(path: Path):
	candidates = [str(path.resolve())]
	while len(candidates) > 0:
		candidate_path = candidates.pop()

		if os.path.isdir(candidate_path):
			if not _should_search_dir(candidate_path):
				continue
			for child in os.listdir(candidate_path):
				candidates.append(os.path.join(candidate_path, child))

		elif candidate_path.endswith(".json"):
			yield candidate_path


def _should_search_dir(path: str) -> bool:
	for dir_name in _IGNORE_DIRS:
		if path.endswith(dir_name):
			return False
	return True


def _tidy_file(file_path: str) -> bool:
	with open(file_path, "r", encoding="utf-8") as file:
		original = file.read()

	pattern = r"(,)( *\n*\t*[}\]])"
	modified = re.sub(pattern, r"\2", original)

	if modified == original:
		return False

	with open(file_path, "w", encoding="utf-8") as file:
		file.write(modified)
	return True


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Tidy JSON files by removing trailing commas.")
	parser.add_argument("path", type=Path, default=Path("./"), nargs="?", help="Root folder to scan.")
	args = parser.parse_args()

	raise SystemExit(json_tidier(args.path))
