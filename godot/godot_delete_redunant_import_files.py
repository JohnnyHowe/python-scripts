import argparse
import os
from pathlib import Path


def find_redundant_import_files(project_path: Path):
	for root, dirs, files in os.walk(project_path):
		for filename in find_redundant_import_files_in_folder(files):
			yield os.path.join(root, filename)


def find_redundant_import_files_in_folder(files_names: list):
	files_names = sorted(files_names)

	# construct dict of {basename: (filename, import_filename), ...}
	pairings = {}
	for filename in files_names:
		name = filename.split(".")[0]
		if not name in pairings: pairings[name] = [None, None]

		if filename.endswith(".import"):
			pairings[name][1] = filename
		else:
			pairings[name][0] = filename

	# Find redundant imports
	for filename, import_filename in pairings.values():
		if filename == None:
			yield import_filename


def delete_files(file_paths: list):
	for file_path in file_paths:
		os.remove(file_path)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("path", default=".", nargs="?")
	parser.add_argument("--silent", action="store_true", default=False)
	args = parser.parse_args()

	redundant_import_files = list(find_redundant_import_files(Path(args.path)))
	delete_files(redundant_import_files)

	if args.silent: return
	print("Redundant .import files deleted: %s" % len(redundant_import_files))
	for filename in redundant_import_files:
		print(" - %s" % filename)


if __name__ == "__main__":
	main()