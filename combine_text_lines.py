"""
Given a list of files, make a new one with all unique lines.

Made for combining app-ads.txt files
"""

import argparse
from pathlib import Path


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("output", type=Path)
	parser.add_argument("--file", "-f", action="append", required=True, type=Path)
	args = parser.parse_args()

	combined = _get_combined(args.file)
	with open(args.output, "w") as file:
		file.write(combined)


def _get_combined(paths: list[Path]) -> str:
	lines = []
	for path in paths:

		if not path.exists():
			print(f"Could not load file at {path}. Skipping")
			continue

		with open(path, "r") as file:
			for line in file.readlines():

				stripped = line.strip()
				if not stripped:
					continue

				if not stripped in lines:
					lines.append(stripped)

	return "\n".join(lines)



if __name__ == "__main__":
	main()
