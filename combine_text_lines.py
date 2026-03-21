"""
Combine unique non-empty lines from input files into a single output file.
"""
import argparse
from pathlib import Path


def combine_text_lines(output: Path, files: list[Path], sort: bool = False) -> int:
	combined = _get_combined(files, sort)
	with open(output, "w", encoding="utf-8") as file:
		file.write(combined)
	return 0


def _get_combined(paths: list[Path], sort=False) -> str:
	lines: list[str] = []
	for path in paths:

		if not path.exists():
			print(f"Could not load file at {path}. Skipping")
			continue

		with open(path, "r", encoding="utf-8") as file:
			for line in file.readlines():

				stripped = line.strip()
				if not stripped:
					continue

				if stripped not in lines:
					lines.append(stripped)

	if sort:
		lines.sort()

	return "\n".join(lines)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Combine unique non-empty lines from input files.")
	parser.add_argument("output", type=Path, help="Output file to write.")
	parser.add_argument("--file", action="append", required=True, type=Path, help="Input file to read.")
	parser.add_argument("--sort", action="store_true", help="Sort the lines?")
	args = parser.parse_args()

	raise SystemExit(combine_text_lines(args.output, args.file, args.sort))
