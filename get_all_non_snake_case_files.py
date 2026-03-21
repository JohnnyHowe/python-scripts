"""
e.g.
python get_all_non_snake_case_files.py ./ --ignore "\..*" --ignore "addons/sentry"
"""
import argparse
import os
from pathlib import Path
import re
import string
from typing import Iterable


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("root", type=Path)
	parser.add_argument("--ignore", action="append", default=[])
	args = parser.parse_args()
	for file in get_all_non_snake_case_files(args.root, args.ignore):
		print(file)


def get_all_non_snake_case_files(root: Path, ignore_patterns: list[str]) -> Iterable[Path]:
	ignore_res = [re.compile(ignore_pattern) for ignore_pattern in ignore_patterns]

	for dirpath, dirnames, filenames in os.walk(root):
		dirpath = Path(dirpath)
		for filename in filenames:
			path = dirpath / filename

			if _should_file_be_ignored(path, ignore_res):
				continue

			if not _is_path_snake_case(path):
				yield path


def _should_file_be_ignored(path: Path, ignore_res: list) -> bool:
	text = str(path).replace("\\", "/").replace("//", "/")
	for ignore_re in ignore_res:
		if ignore_re.match(text):
			return True
	return False


def _is_path_snake_case(path: Path) -> bool:
	for part in path.parts:
		if not _is_snake_case(part):
			return False
	return True


def _is_snake_case(text: str) -> bool:
	allowed_chars = "_" + string.ascii_lowercase + string.digits

	for char in text:
		if not char in allowed_chars:
			return False

	return True


if __name__ == "__main__":
	main()
