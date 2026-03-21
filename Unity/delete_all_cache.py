"""
Delete common Unity, Gradle, and project cache folders.
"""
import argparse
import os
from pathlib import Path
import subprocess
from send2trash import send2trash


def delete_all_cache(project_root: Path, include_unity_cache: bool, include_gradle_cache: bool, safe: bool) -> int:
	cache_paths = [
		project_root / "Library",
		project_root / "Temp",
		project_root / "obj",
	]

	if include_unity_cache:
		cache_paths += [
			Path(r"%USERPROFILE%\AppData\Local\Unity\Caches\GI"),
			Path(r"%USERPROFILE%\AppData\Local\Unity\cache"),
			Path(r"%USERPROFILE%\AppData\Roaming\Unity\Packages"),
		]

	if include_gradle_cache:
		cache_paths.append(Path(r"%USERPROFILE%\.gradle\caches"))

	deleter = send2trash if safe else _unsafe_delete_fast

	for path in cache_paths:
		_run_on_folder(path, deleter)

	return 0


def _unsafe_delete_fast(path):
	subprocess.run(["rmdir", "/S", "/Q", str(path)], shell=True)


def _run_on_folder(path, func):
	path = Path(path)
	full_path = _get_full_path(path)

	path_display_str = f"\"{path}\""
	if path != full_path:
		path_display_str = f"\"{path}\" (\"{full_path}\")"

	if not os.path.exists(full_path):
		print(f"No folder at {path_display_str} (deepest parent: {_get_first_parent_that_exists(full_path)})")
		return

	print(f"Deleting {path_display_str}")
	func(full_path)


def _get_full_path(path: Path) -> Path:
	path = str(path)
	path = path.replace("%USERPROFILE%", str(Path.home()))
	return Path(path).absolute()


def _get_first_parent_that_exists(path: Path) -> str:
	parts = path.parts

	for i in range(len(parts) - 1, 0, -1):
		current_path = os.path.join(*parts[:i])
		if os.path.exists(current_path):
			return current_path

	return ""


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Delete common Unity, Gradle, and project cache folders.")
	parser.add_argument("--project-root", type=Path, default=Path("."), help="Unity project root.")
	parser.add_argument("--no-unity-cache", action="store_true", help="Skip Unity global cache folders.")
	parser.add_argument("--no-gradle-cache", action="store_true", help="Skip Gradle cache folders.")
	parser.add_argument("--safe", action="store_true", help="Send folders to recycle bin instead of deleting.")
	args = parser.parse_args()

	raise SystemExit(
		delete_all_cache(
			args.project_root,
			include_unity_cache=not args.no_unity_cache,
			include_gradle_cache=not args.no_gradle_cache,
			safe=args.safe,
		)
	)
