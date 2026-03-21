"""
List files that are not in snake_case.
"""
import argparse
import os
from pathlib import Path
import re
import string
from typing import Iterable


def get_all_non_snake_case_files(root: Path, ignore_patterns: list[str]) -> int:
	for file in _iter_non_snake_case_files(root, ignore_patterns):
		print(file)
	return 0


def _iter_non_snake_case_files(root: Path, ignore_patterns: list[str]) -> Iterable[Path]:
	ignore_res = [re.compile(ignore_pattern) for ignore_pattern in ignore_patterns]

	for dirpath, _, filenames in os.walk(root):
		dirpath = Path(dirpath)
		for filename in filenames:
			path = dirpath / filename

			if _should_file_be_ignored(path, ignore_res):
				continue

			if not _is_path_snake_case(path):
				yield path


def _should_file_be_ignored(path: Path, ignore_res: list[re.Pattern]) -> bool:
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
		if char not in allowed_chars:
			return False

	return True


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="List files that are not in snake_case.")
	parser.add_argument("root", type=Path, help="Root folder to scan.")
	parser.add_argument("--ignore", action="append", default=[], help="Regex pattern to ignore (repeatable).")
	args = parser.parse_args()

	raise SystemExit(get_all_non_snake_case_files(args.root, args.ignore))
