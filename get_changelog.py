"""
Print the changelog for a given version.
Assumes this format: https://keepachangelog.com/en/1.0.0/
"""
import argparse
from pathlib import Path
from typing import Iterator, Optional
import re


VERSION_HEADER_PATTERN = r"^## \[([a-zA-Z0-9.]*)\] *$"
VERSION_HEADER_RE = re.compile(VERSION_HEADER_PATTERN)

SUB_HEADING_PATTERN = r"^### (.*)$"
SUB_HEADING_RE = re.compile(SUB_HEADING_PATTERN)


def get_changelog(path: Path, version: str, strip_version_header: bool, custom_sub_header: Optional[str]) -> str:
	if not path.exists():
		raise FileNotFoundError(
			f"Could not find anything at {str(path.resolve)}")
	if not path.suffix.lower() == ".md":
		raise FileNotFoundError(f"Expected file with \".md\" extension")

	with open(path, "r") as file:
		lines = file.readlines()

	changelog_lines = _get_changelog_from_lines(lines, version)

	if strip_version_header:
		changelog_lines = changelog_lines[1:]

	if custom_sub_header is not None:
		changelog_lines = list(_apply_custom_sub_heading(
			changelog_lines, custom_sub_header))

	changelog = "".join(changelog_lines)
	return changelog.strip()


def _get_changelog_from_lines(lines: list[str], version: str) -> str:
	start, end = _get_changelog_line_range(lines, version)
	return lines[start: end]


def _get_changelog_line_range(lines: list[str], version: str) -> tuple[int, int]:
	"""
	(start, end)
	start: inclusive
	end: exclusive
	"""
	take_first = version == None or version.strip == ""

	start = None

	header_line_number_generator = _get_version_header_line_numbers(lines)
	for header, line_number in header_line_number_generator:
		if header == version or take_first:
			start = line_number
			break

	next_header = next(header_line_number_generator, ("<eof>", len(lines)))
	end = next_header[1]

	return (start, end)


def _get_version_header_line_numbers(lines: list[str]) -> Iterator[tuple[str, int]]:
	for line_index in range(len(lines)):
		match = VERSION_HEADER_RE.match(lines[line_index])
		if match:
			yield (match.group(1), line_index)


def _apply_custom_sub_heading(lines: list[str], custom_sub_header: str) -> Iterator[str]:
	for i in range(len(lines)):
		match = SUB_HEADING_RE.match(lines[i])
		if not match:
			yield lines[i]
		else:
			yield custom_sub_header + match.group(1) + "\n"


def _parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser()

	parser.add_argument(
		"--path",
		required=False,
		type=Path,
		default=Path("CHANGELOG.md")
	)

	parser.add_argument(
		"--version",
		required=False,
		help="Defaults to most recent"
	)

	parser.add_argument(
		"--no-version-header",
		action="store_true"
	)

	parser.add_argument(
		"--custom-sub-header",
		nargs="?",
		const="",
		default=None,
		help="Replaces the \"### \" before subheadings like \"Fixed\"."
	)

	return parser.parse_args()


if __name__ == "__main__":
	args = _parse_args()
	changelog = get_changelog(
		args.path,
		args.version,
		args.no_version_header,
		args.custom_sub_header
	)
	print(changelog)
