"""
Copy all Unity Resources folders to a single output directory.
"""
import argparse
import os
from pathlib import Path
import shutil


def get_all_resources(root: Path, output_directory: Path) -> int:
	_clear_directory(output_directory)
	resource_paths = list(_find_all_resource_folders(root))

	for resource_path in resource_paths:
		resource_path_relative = resource_path.relative_to(root)
		destination_path = output_directory / resource_path_relative
		shutil.copytree(resource_path, destination_path)

	print(f"Resources folders copied: {len(resource_paths)}")
	return 0


def _clear_directory(directory: Path):
	if directory.exists():
		if directory.is_dir():
			shutil.rmtree(directory)
		else:
			os.remove(directory)
	directory.mkdir(parents=True)


def _find_all_resource_folders(root: Path):
	for entry in os.listdir(root):
		path = Path(os.path.join(root, entry))

		if not path.is_dir():
			continue

		if entry == "Resources":
			yield path
		else:
			yield from _find_all_resource_folders(path)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Copy all Unity Resources folders to a single output directory.")
	parser.add_argument("--root", type=Path, default=Path("Assets"), help="Unity project Assets root.")
	parser.add_argument("--output", type=Path, required=True, help="Destination folder for copied Resources.")
	args = parser.parse_args()

	raise SystemExit(get_all_resources(args.root, args.output))
