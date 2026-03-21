"""Generate a markdown file with each script's --help output."""
from __future__ import annotations

from pathlib import Path
import argparse
import subprocess
import sys

DEFAULT_OUTPUT_FILENAME = "INDEX.md"


def generate_scripts_index(output_filename: str | None = None) -> int:
	root = Path(__file__).parent
	output_path = _resolve_output_path(root, output_filename)
	scripts = _get_scripts(root)

	_generate_markdown(output_path, scripts)
	print(f"Wrote {output_path}")
	return 0


def _resolve_output_path(root: Path, output_filename: str | None) -> Path:
	if not output_filename:
		output_filename = DEFAULT_OUTPUT_FILENAME
	return (root / output_filename).resolve()


def _get_scripts(root: Path) -> list[Path]:
	return sorted(
		[
			path
			for path in root.glob("*.py")
			if path.name != Path(__file__).name
		],
		key=lambda path: path.name.lower(),
	)


def _generate_markdown(output_path: Path, scripts: list[Path]) -> None:
	lines: list[str] = ["This file was generated using the output of each script with \"--help\""]
	grouped_scripts: dict[str, list[Path]] = {}
	for script_path in scripts:
		group_key = _get_group_key(script_path)
		grouped_scripts.setdefault(group_key, []).append(script_path)

	for group_key in sorted(grouped_scripts.keys()):
		lines.append(f"# {group_key}")
		lines.append("")
		for script_path in grouped_scripts[group_key]:
			help_output = _get_help_output(script_path)
			lines.append(f"## {script_path.name}")
			lines.append("")
			lines.append("```text")
			lines.append(help_output)
			lines.append("```")
			lines.append("")

	output_path.write_text("\n".join(lines), encoding="utf-8")


def _get_group_key(script_path: Path) -> str:
	return script_path.stem.split("_", maxsplit=1)[0]


def _get_help_output(script_path: Path) -> str:
	result = subprocess.run(
		[sys.executable, str(script_path), "--help"],
		capture_output=True,
		text=True,
	)
	output = (result.stdout or "") + (result.stderr or "")
	return output.strip()


def _parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Generate a markdown file with each script's --help output.",
	)
	parser.add_argument(
		"--output",
		default=DEFAULT_OUTPUT_FILENAME,
		help=f"Output markdown file path (default: {DEFAULT_OUTPUT_FILENAME}).",
	)
	return parser.parse_args()


if __name__ == "__main__":
	args = _parse_args()
	raise SystemExit(generate_scripts_index(args.output))
