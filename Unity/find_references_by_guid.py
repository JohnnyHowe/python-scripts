"""
Find all files that reference a Unity GUID.
"""
import argparse
import os
from pathlib import Path
import re
from concurrent.futures import ProcessPoolExecutor, as_completed


FILE_TYPES_TO_SEARCH = [
	".anim",
	".asset",
	".asmdef",
	".asmref",
	".controller",
	".guiskin",
	".json",
	".mat",
	".meta",
	".overridecontroller",
	".playable",
	".prefab",
	".shader",
	".shadergraph",
	".shadersubgraph",
	".spriteatlas",
	".txt",
	".unity",
	".uxml",
	".vfx",
	".xml",
	".yaml",
	".yml",
]

_GUID_PATTERN = re.compile(r"^[0-9a-fA-F]{32}$")
_IGNORE_DIR_NAMES = {
	".git",
	"Library",
	"Temp",
	"obj",
	"Build",
	"Builds",
	"Logs",
}


def find_references_by_guid(guid: str, project_root: Path, verbose: bool, jobs: int, ordered: bool) -> int:
	guid = _normalize_guid(guid)
	if not _GUID_PATTERN.match(guid):
		print(f"Invalid GUID: {guid}")
		return 1

	project_root = project_root.absolute()
	print(f"Searching for GUID {guid} under {project_root}...")

	match_count_total = 0
	file_count = 0

	if jobs > 1:
		results = _find_files_with_guid_concurrent(project_root, guid, jobs, ordered)
	else:
		results = _find_files_with_guid(project_root, guid)

	for file_path, match_count in results:
		file_count += 1
		match_count_total += match_count

		relative_path = file_path.relative_to(project_root)
		if verbose:
			print(f"\t{relative_path} ({match_count} matches)")
		else:
			print(f"\t{relative_path}")

	if file_count == 0:
		print(f"No references found for GUID {guid}.")
		return 0

	if verbose:
		print(f"Done. Found {file_count} files, {match_count_total} total matches.")
	else:
		print(f"Done. Found {file_count} files.")

	return 0


def _normalize_guid(guid: str) -> str:
	return guid.strip().lower().replace("-", "")


def _find_files_with_guid(project_root: Path, guid: str):
	guid_bytes = guid.encode("ascii")

	for file_path in sorted(_iter_candidate_files(project_root), key=lambda p: str(p).lower()):
		match_count = _count_guid_in_file(file_path, guid_bytes)
		if match_count > 0:
			yield file_path, match_count


def _find_files_with_guid_concurrent(project_root: Path, guid: str, jobs: int, ordered: bool):
	guid_bytes = guid.encode("ascii")
	candidates = sorted(_iter_candidate_files(project_root), key=lambda p: str(p).lower())

	with ProcessPoolExecutor(max_workers=jobs) as executor:
		futures = {}
		for index, file_path in enumerate(candidates):
			future = executor.submit(_scan_one_file, index, file_path, guid_bytes)
			futures[future] = index

		if ordered:
			buffer = {}
			next_index = 0
			for future in as_completed(futures):
				index, file_path, match_count = future.result()
				buffer[index] = (file_path, match_count)
				while next_index in buffer:
					file_path, match_count = buffer.pop(next_index)
					if match_count > 0:
						yield file_path, match_count
					next_index += 1
		else:
			for future in as_completed(futures):
				_, file_path, match_count = future.result()
				if match_count > 0:
					yield file_path, match_count


def _iter_candidate_files(project_root: Path):
	for root, dirnames, filenames in os.walk(project_root):
		dirnames[:] = [d for d in dirnames if d not in _IGNORE_DIR_NAMES]
		for filename in filenames:
			file_path = Path(os.path.join(root, filename))
			if _should_search_file(file_path):
				yield file_path


def _should_search_file(file_path: Path) -> bool:
	return file_path.suffix.lower() in FILE_TYPES_TO_SEARCH


def _count_guid_in_file(file_path: Path, guid_bytes: bytes) -> int:
	try:
		with open(file_path, "rb") as file:
			data = file.read().lower()
			return data.count(guid_bytes)
	except OSError:
		return 0


def _scan_one_file(index: int, file_path: Path, guid_bytes: bytes):
	match_count = _count_guid_in_file(file_path, guid_bytes)
	return index, file_path, match_count


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Find all files that reference a Unity GUID.")
	parser.add_argument("guid", help="Unity GUID to search for.")
	parser.add_argument("--project-root", type=Path, default=Path("."), help="Unity project root.")
	parser.add_argument("--verbose", action="store_true", help="Print match counts.")
	parser.add_argument("--jobs", type=int, default=1, help="Number of worker processes to use.")
	parser.add_argument(
		"--ordered",
		action="store_true",
		help="Preserve file order when using multiple workers.",
	)
	args = parser.parse_args()

	raise SystemExit(
		find_references_by_guid(
			args.guid,
			args.project_root,
			args.verbose,
			args.jobs,
			args.ordered,
		)
	)
