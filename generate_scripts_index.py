"""Generate a markdown file with each script's --help output."""
from __future__ import annotations

import os
from pathlib import Path
import argparse
import shlex
import subprocess
import sys
from typing import Iterable

HEADER = "This file was generated using the output of each script with \"--help\"\n"
DEFAULT_OUTPUT_FILENAME = "INDEX.md"
FOLDERS_TO_IGNORE = [".git", ".vscode"]


def generate_scripts_index(filename: str | None = None, root: Path | None = None, recursive: bool = False) -> int:
	if root is None:
		root = Path.cwd()

	if filename is None:
		filename = DEFAULT_OUTPUT_FILENAME

	_generate_index_for_folder(filename, root, recursive)
	return 0


def _generate_index_for_folder(filename: str, path: Path, recursive: bool = False) -> bool:
	"""
	Returns whether any file was created.
	No file created if no scripts exist and no child indexes made (or would be made if they had scripts).
	"""
	child_indexes: list[Path] = []
	child_indexes_contents: str = ""

	if recursive:
		child_indexes = list(_generate_index_for_immediate_subfolders(filename, path))
		child_indexes_contents = _generate_markdown_for_child_indexes(child_indexes)
		if child_indexes_contents != "": child_indexes_contents += "\n"

	scripts = _get_scripts(path)

	if len(scripts) == 0 and len(child_indexes) == 0:
		return False

	scripts_content = _generate_markdown_for_scripts(scripts)
	contents = HEADER + child_indexes_contents + scripts_content

	output_path = path / filename 
	output_path.write_text(contents, encoding="utf-8")
	print(f"Created {str(output_path)}");
	return True


def _generate_index_for_immediate_subfolders(filename: str, path: Path) -> Iterable[Path]:
	"""
	Assumes recursive is True.
	Returns paths to child index files.
	"""
	for folder_path in _get_immediate_subfolders(path):
		if _generate_index_for_folder(filename, folder_path, True):
			yield folder_path / filename


def _get_immediate_subfolders(path: Path) -> Iterable[Path]:
	for file in os.scandir(path):
		if file.is_dir():
			if not file.name in FOLDERS_TO_IGNORE:
				yield Path(file.path)


def _generate_markdown_for_child_indexes(child_indexes: list[Path]) -> str:
	if len(child_indexes) == 0:
		return ""

	children_markdown_parts = []
	for child_index_path in child_indexes:
		markdown = f" - [{child_index_path.parent.name}/]({child_index_path.parent.name}/{child_index_path.name})"
		children_markdown_parts.append(markdown)

	children_markdown = "\n".join(children_markdown_parts)

	return f"# Subfolders\n{children_markdown}\n"


def _get_scripts(root: Path) -> list[Path]:
	return sorted(
		[
			path
			for path in root.glob("*.py")
			if path.name != Path(__file__).name
		],
		key=lambda path: path.name.lower(),
	)


def _generate_markdown_for_scripts(scripts: list[Path]) -> str:
	lines: list[str] = []
	grouped_scripts: dict[str, list[Path]] = {}
	for script_path in scripts:
		group_key = _get_group_key(script_path)
		grouped_scripts.setdefault(group_key, []).append(script_path)

	for group_key in sorted(grouped_scripts.keys()):
		lines.append(f"# {group_key}")
		lines.append("")
		for script_path in grouped_scripts[group_key]:
			lines.append(_get_script_markdown(script_path))
	return "\n".join(lines)


def _get_group_key(script_path: Path) -> str:
	return script_path.stem.split("_", maxsplit=1)[0]


def _get_script_markdown(script_path: Path) -> str:
	help_output, success = _get_help_output(script_path)

	header = script_path.name
	if not success:
		header = f"<span style=\"color:red\">{header}</span>"

	return f"## {header}\n{help_output}"


def _get_help_output(script_path: Path) -> (str, bool):
	command = [sys.executable, str(script_path), "--help"]

	result = subprocess.run(command, capture_output=True, text=True)
	output = (result.stdout or "") + (result.stderr or "")
	output = output.strip()

	if result.returncode != 0:
		return (f"```\n{shlex.join(command)}\n```\n\nResulted in\n```\n{output}\n```", False)

	return (f"```text\n{output}\n```\n", True)


def _parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Generate a markdown file with each script's --help output.",
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
	)
	parser.add_argument(
		"--filename",
		default=DEFAULT_OUTPUT_FILENAME,
		type=str,
		help=f"Output file name.",
	)
	folder_default = Path("./")
	parser.add_argument(
		"--folder",
		default=folder_default,
		type=Path,
		help=f"Folder to create INDEX.md for."
	)
	parser.add_argument(
		"--recursive",
		action="store_true",
		help=f"Create index for subfolders?"
	)
	return parser.parse_args()


if __name__ == "__main__":
	args = _parse_args()
	raise SystemExit(generate_scripts_index(args.filename, args.folder, args.recursive))
