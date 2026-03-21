"""
Count lines for files with a given extension under a directory.
"""
import argparse
from pathlib import Path


def count_lines(directory: Path, extension: str) -> int:
	total_lines = 0
	total_files = 0

	for path in directory.rglob(f"*{extension}"):
		if not path.is_file():
			continue
		total_files += 1
		try:
			with open(path, "r", encoding="utf-8") as file:
				for _ in file:
					total_lines += 1
		except Exception:
			print(f"Error reading file: {path}")

	print(f"Total number of files: {total_files}")
	print(f"Total lines of code: {total_lines}")
	return 0


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Count lines for files with a given extension.")
	parser.add_argument("directory", type=Path, nargs="?", default=Path.cwd(), help="Root directory to scan.")
	parser.add_argument("--ext", default=".cs", help="File extension to include (default: .cs).")
	args = parser.parse_args()

	extension = args.ext.lower()
	if not extension.startswith("."):
		extension = f".{extension}"

	raise SystemExit(count_lines(args.directory, extension))
