"""
Delete Unity .meta files that failed to parse in the Editor log.
"""
import argparse
import os
from pathlib import Path
import re


_LOCAL_APPDATA_EDITOR_LOG_FILEPATH = r"Unity\Editor\Editor.log"
_BAD_META_PATTERN = re.compile(r"(Assets/.*?\.meta).*?YAML Parser", re.S)
_PROJECT_PATH_PATTERN = re.compile(r"Successfully changed project path to: (.*)")


def delete_corrupt_meta(yes: bool) -> int:
	corrupt = list(_find_corrupt_meta_files())

	if not corrupt:
		print("No corrupt meta files found in Editor.log.")
		return 0

	print("meta files Unity could not open:")
	for file_path in corrupt:
		print("  * " + file_path)

	if not yes:
		confirmation_input = input("y to delete: ")
		if confirmation_input.lower() != "y":
			print("Aborting")
			return 1

	print("Deleting...")
	_delete_files(corrupt)
	return 0


def _find_corrupt_meta_files():
	editor_log = _get_editor_log()

	match = _PROJECT_PATH_PATTERN.search(editor_log)
	if not match:
		return []
	project_path = match.group(1)

	results = []
	for file_path in sorted(set(_BAD_META_PATTERN.findall(editor_log))):
		results.append(os.path.join(project_path, file_path))
	return results


def _get_editor_log() -> str:
	filepath = os.path.join(Path(os.environ["LOCALAPPDATA"]), _LOCAL_APPDATA_EDITOR_LOG_FILEPATH)
	with open(filepath, "r", encoding="utf-8") as file:
		return file.read()


def _delete_files(file_paths):
	for file_path in file_paths:
		os.remove(file_path)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Delete Unity .meta files that failed to parse in the Editor log.")
	parser.add_argument("--yes", action="store_true", help="Delete without prompting.")
	args = parser.parse_args()

	raise SystemExit(delete_corrupt_meta(args.yes))
