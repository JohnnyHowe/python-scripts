"""Create an INDEX.md for a Godot utility folder."""
from __future__ import annotations

import argparse
from pathlib import Path
import re

DEFAULT_INDEX_FILENAME = "INDEX.md"


class ClassInfo:
	name: str
	methods: list[MethodInfo]
	path: Path


class MethodInfo:
	name: str
	parameters: list[str, str, str]	# name, type (if applicable), (if applicable)
	docstring: str
	returns: str = "void"

	def __str__(self):
		return f"MethodInfo(name={self.name}, parameters={self.parameters})"
	
	def __repr__(self):
		return str(self)


def create_utility_folder_index(folder: Path) -> int:
	if not folder.exists():
		print(f"Folder does not exist: {folder}")
		return 1
	if not folder.is_dir():
		print(f"Not a folder: {folder}")
		return 1

	classes = []
	for file in _get_files(folder):
		class_info = _get_class(file)
		class_info.path = file.relative_to(folder)
		classes.append(class_info)

	output_path = folder / DEFAULT_INDEX_FILENAME
	output_path.write_text(_build_markdown(classes), encoding="utf-8")
	print(f"Created {output_path}")
	return 0


def _get_files(folder: Path) -> list[Path]:
	return sorted(
		[
			path
			for path in folder.iterdir()
			if path.is_file() and path.suffix.lower() == ".gd"
		],
		key=lambda path: path.name.lower(),
	)


def _get_class(file: Path) -> ClassInfo:
	info = ClassInfo()
	info.path = file
	info.methods = _get_methods(file)
	info.name = _get_class_name(file)
	return info


def _get_methods(file: Path) -> list[MethodInfo]:
	try:
		lines = file.read_text(encoding="utf-8").splitlines()
	except (OSError, UnicodeDecodeError):
		return []

	methods: list[MethodInfo] = []
	comment_block: list[str] = []

	for line in lines:
		stripped = line.strip()
		if stripped.startswith("#"):
			comment_block.append(_strip_comment_prefix(stripped))
			continue

		if stripped == "":
			if len(comment_block) > 0:
				comment_block = []
			continue

		match = re.match(r"^\s*static\s+func\s+([A-Za-z_]\w*)\s*\(([^)]*)\)\s*(?:->\s*([^\s:]+))?", line)
		if match:
			method = MethodInfo()
			method.name = match.group(1)
			method.parameters = _parse_gdscript_parameters(match.group(2))
			method.docstring = " ".join(comment_block).strip()
			methods.append(method)
			comment_block = []
			continue

		comment_block = []

	return methods


def _get_class_name(file: Path) -> str:
	try:
		lines = file.read_text(encoding="utf-8").splitlines()
	except (OSError, UnicodeDecodeError):
		return ""

	for line in lines:
		match = re.match(r"^\s*class_name\s+([A-Za-z_]\w*)", line)
		if match:
			return match.group(1)

	return ""


def _parse_gdscript_parameters(parameters: str) -> list[tuple[str, str, str]]:
	if parameters.strip() == "":
		return []

	parts = [part.strip() for part in parameters.split(",")]
	parsed: list[tuple[str, str, str]] = []

	for part in parts:
		if part == "":
			continue

		default_value = ""
		param_type = ""

		if "=" in part:
			left, default_value = part.split("=", maxsplit=1)
			part = left.strip()
			default_value = default_value.strip()

		if ":" in part:
			name, param_type = part.split(":", maxsplit=1)
			name = name.strip()
			param_type = param_type.strip()
		else:
			name = part.strip()

		parsed.append((name, param_type, default_value))

	return parsed


def _build_markdown(classes: list) -> str:
	result = ""
	for class_info in classes:
		result += f"# [`{class_info.name}`]({str(class_info.path)})\n"

		for method_info in class_info.methods:
			result += f"## `{_get_method_signature(method_info)}`\n"
			result += method_info.docstring + "\n\n"

	return result


def _get_method_signature(method: MethodInfo) -> str:
	return f"{method.name}({_get_parameters_str(method.parameters)}) -> {method.returns}"

def _get_parameters_str(params: list) -> str:
	params_strs = []
	for param in params:
		s = param[0]
		if param[1]:
			s += ": " + param[1]
		if param[2]:
			s += " = " + param[2]
		params_strs.append(s)
	return ", ".join(params_strs)


def _get_description(path: Path) -> str:
	try:
		with path.open("r", encoding="utf-8") as handle:
			for line in handle:
				stripped = line.strip()
				if stripped == "":
					continue
				return _strip_comment_prefix(stripped)
	except (OSError, UnicodeDecodeError):
		return ""

	return ""


def _strip_comment_prefix(line: str) -> str:
	for prefix in ("# ", "## ", "// ", "; ", "-- "):
		if line.startswith(prefix):
			return line[len(prefix):].strip()

	if line.startswith("#"):
		return line.lstrip("#").strip()
	if line.startswith("//"):
		return line.lstrip("/").strip()

	return line


def _parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Create an INDEX.md for a Godot utility folder.",
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
	)
	parser.add_argument(
		"folder",
		nargs="?",
		default=Path("."),
		type=Path,
		help="Folder to index.",
	)
	return parser.parse_args()


if __name__ == "__main__":
	args = _parse_args()
	raise SystemExit(create_utility_folder_index(args.folder))
