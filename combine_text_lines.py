"""
Combine unique non-empty lines from input files into a single output file.
"""
import argparse
from pathlib import Path


def combine_text_lines(output: Path, files: list[Path]) -> int:
	combined = _get_combined(files)
	with open(output, "w", encoding="utf-8") as file:
		file.write(combined)
	return 0


def _get_combined(paths: list[Path]) -> str:
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

	return "\n".join(lines)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Combine unique non-empty lines from input files.")
	parser.add_argument("output", type=Path, help="Output file to write.")
	parser.add_argument("--file", "-f", action="append", required=True, type=Path, help="Input file to read.")
	args = parser.parse_args()

	raise SystemExit(combine_text_lines(args.output, args.file))
