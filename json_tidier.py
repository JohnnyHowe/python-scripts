"""
Tidy all JSON files in a directory and sub directories.
Currently:
* removes extra commas
"""
import argparse
import os
from pathlib import Path
import re

IGNORE_DIRS = [".vscode"]

def tidy_all_in_folder(path: Path) -> int:
	count = 0
	for file_name in get_all_json_files_in_folder_and_subfolders(path):
		if tidy_file(file_name): count += 1
	return count


def get_all_json_files_in_folder_and_subfolders(path: Path):
	candidates = [str(path.resolve())]
	while len(candidates) > 0:
		candidate_path = candidates.pop()

		if os.path.isdir(candidate_path):
			if not should_search_dir(candidate_path): continue
			for child in os.listdir(candidate_path):
				candidates.append(os.path.join(candidate_path, child))

		elif candidate_path.endswith(".json"):
			yield candidate_path


def should_search_dir(path):
	for dir_name in IGNORE_DIRS:
		if path.endswith(dir_name):
			return False
	return True


def tidy_file(file_path: str) -> bool:
	file = open(file_path, "r")
	original = file.read()
	file.close()
	
	# remove trailing commas
	pattern = r"(,)( *\n*\t*[}\]])"
	modified = re.sub(pattern, r"\2", original)

	if modified == original: return False

	file = open(file_path, "w")
	file.write(modified)
	file.close()
	return True


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("path", default="./", nargs="?")
	args = parser.parse_args()

	files_tidied = tidy_all_in_folder(Path(args.path))
	print("JSON files tidied: %s" % files_tidied)