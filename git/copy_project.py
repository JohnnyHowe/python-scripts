"""
Copy a git repo folder recursively, honoring .gitignore.

Ignores files caught by any .gitignores.
Does include files and folders not yet committed.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import shutil
import subprocess
from typing import Iterable, List, Set


def copy_project(source: str, destination: str, verbose: bool, only_folder: str | None, ignore_patterns: list[str] = []) -> int:
	source_path = Path(source)
	destination_path = Path(destination)
	repo_root = _get_repo_root(source_path)
	_ensure_destination_empty(destination_path)

	paths = _get_copy_paths(repo_root, only_folder, ignore_patterns)
	if not paths:
		print("No files to copy.")
		return 0

	for rel_path in paths:
		_copy_file(repo_root, destination_path, rel_path, verbose)

	if verbose:
		print(f"Copied {len(paths)} file(s).")
	return 0


def _run_git(args: List[str], cwd: Path, input_bytes: bytes | None = None) -> bytes:
	result = subprocess.run(
		["git", *args],
		cwd=str(cwd),
		input=input_bytes,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		check=False,
	)
	if result.returncode != 0:
		stderr = result.stderr.decode("utf-8", errors="replace").strip()
		raise RuntimeError(f"git {' '.join(args)} failed: {stderr}")
	return result.stdout


def _get_repo_root(source_path: Path) -> Path:
	if not source_path.exists():
		raise RuntimeError(f"Source path does not exist: {source_path}")
	output = _run_git(["rev-parse", "--show-toplevel"], cwd=source_path)
	return Path(output.decode("utf-8", errors="replace").strip())


def _get_copy_paths(repo_root: Path, only_folder: str | None, ignore_patterns: list[str]) -> List[str]:
	output = _run_git(
		["ls-files", "-z", "--cached", "--others", "--exclude-standard"],
		cwd=repo_root,
	)
	if not output:
		return []

	candidates = [p for p in output.decode("utf-8", errors="replace").split("\0") if p]

	git_ignored = _get_git_ignored_paths(repo_root, candidates)
	paths = [p for p in candidates if p not in git_ignored]

	paths = [p for p in candidates if not _matches_ignore_patterns(p, ignore_patterns)]

	if only_folder:
		folder = _normalize_folder(only_folder)
		prefix = folder + "/"
		paths = [p for p in paths if p == folder or p.startswith(prefix)]
	paths.sort()
	return paths


def _matches_ignore_patterns(path: str, ignore_patterns: list[str]) -> bool:
	for pattern in ignore_patterns:
		if re.match(pattern, path):
			return True
	return False


def _get_git_ignored_paths(repo_root: Path, paths: Iterable[str]) -> Set[str]:
	if not paths:
		return set()
	input_bytes = "\0".join(paths).encode("utf-8")
	try:
		output = _run_git(["check-ignore", "-z", "--stdin"],
						  cwd=repo_root, input_bytes=input_bytes)
	except RuntimeError:
		return set()
	if not output:
		return set()
	return {p for p in output.decode("utf-8", errors="replace").split("\0") if p}


def _normalize_folder(folder: str) -> str:
	if not folder:
		raise RuntimeError("Only-folder path is empty.")
	folder_path = Path(folder)
	if folder_path.is_absolute():
		raise RuntimeError(
			"Only-folder path must be relative to the repo root.")
	normalized = folder.replace("\\", "/")
	normalized = normalized.lstrip("./")
	normalized = normalized.rstrip("/")
	if not normalized:
		raise RuntimeError("Only-folder path is empty.")
	return normalized


def _ensure_destination_empty(destination_path: Path) -> None:
	if destination_path.exists():
		if destination_path.is_file():
			raise RuntimeError(f"Destination is a file: {destination_path}")
		if any(destination_path.iterdir()):
			raise RuntimeError(f"Destination is not empty: {destination_path}")
	else:
		destination_path.mkdir(parents=True, exist_ok=True)


def _copy_file(repo_root: Path, destination_root: Path, rel_path: str, verbose: bool) -> None:
	source_path = repo_root / rel_path
	destination_path = destination_root / rel_path

	if source_path.is_dir():
		destination_path.mkdir(parents=True, exist_ok=True)
		return

	destination_path.parent.mkdir(parents=True, exist_ok=True)
	shutil.copy2(source_path, destination_path, follow_symlinks=False)
	if verbose:
		print(rel_path)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description="Copy a git repo folder recursively, honoring .gitignore."
	)
	parser.add_argument(
		"source",
		help="Path to the source git repo.")
	parser.add_argument(
		"destination",
		help="Path to the destination directory.")
	parser.add_argument(
		"--only-folder",
		help="Only copy files under this repo-relative folder.",
	)
	parser.add_argument(
		"--ignore",
		action="append",
		default=[],
		help="Additional regex match patterns to exclude (repeatable).",
	)
	parser.add_argument(
		"--verbose",
		action="store_true",
		help="Print copied files."
	)
	args = parser.parse_args()

	try:
		raise SystemExit(copy_project(
			args.source,
			args.destination,
			args.verbose,
			args.only_folder,
			args.ignore
		))
	except Exception as exc:
		print(f"Error: {exc}")
		raise SystemExit(1)
