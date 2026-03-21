"""
Copies the project files and folders tracked in gitignore.
"""
import argparse
import asyncio
import os
from pathlib import Path
import re
import shutil
import subprocess
from gitignore_parser import parse_gitignore

# Logging
LOG_HIGH_LEVEL_TASKS = True


def main():
	parser = argparse.ArgumentParser(description="Copy a repo's tracked files into a clean destination directory.")
	parser.add_argument("project_directory", type=Path, help="Path to the project repo to copy.")
	parser.add_argument("destination_directory", type=Path, help="Path to the destination directory to create and populate.")
	args = parser.parse_args()

	copy_project(args.project_directory, args.destination_directory)


def create_fresh_destination(full_system_path: Path):
	""" 
	Ensures destination path is empty. 
	Deletes old contents if there is some, creates folder if it doesn't exist.
	"""
	if LOG_HIGH_LEVEL_TASKS: print("Clearing clone destination...")

	full_system_path = full_system_path.resolve()

	if not is_safe_directory(full_system_path):
		raise Exception(f"Given path deemed unsafe! \"{full_system_path}\"")

	# Delete old
	if full_system_path.exists():
		subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(full_system_path)], shell=True)

	# Create new
	full_system_path.mkdir(exist_ok=True, parents=True)


def is_safe_directory(full_system_path: Path):
	pattern = r"C:\\Users\\.*\\"
	return re.match(pattern, str(full_system_path)) != None
	

def copy_project(project_directory, destination_directory):
	create_fresh_destination(destination_directory)

	if LOG_HIGH_LEVEL_TASKS: print("Copying files...")

	repo_full_path = os.path.abspath(project_directory)

	result = subprocess.run(
		["git", "-C", str(repo_full_path), "ls-files"],
		capture_output=True,
		text=True,
		check=True
	)
	repo_relative_file_directories = result.stdout.splitlines()

	asyncio.run(copy_files(repo_relative_file_directories, project_directory, destination_directory))


async def copy_files(repo_relative_file_directories, project_directory, destination_directory):
	files_heirarcy = sort_files_into_hierarchy(repo_relative_file_directories, project_directory)
	await copy_files_dict(files_heirarcy, project_directory, destination_directory)


async def copy_files_dict(folder_info_dict, project_directory, destination_directory):
	ensure_parent_folder_exists(folder_info_dict["project_path"])

	# files
	files_list_project_relative = folder_info_dict["files"]
	file_tasks = [
		async_copy_file(project_relative_file_path, project_directory, destination_directory)
		for project_relative_file_path in files_list_project_relative
	]

	# folders
	folder_tasks = []
	for folder_name in folder_info_dict["folders"].keys():
		folder_tasks.append(copy_files_dict(folder_info_dict["folders"][folder_name], project_directory, destination_directory))

	await asyncio.gather(*(file_tasks + folder_tasks))


async def async_copy_file(project_relative_file_path, project_directory, destination_directory):
	src = os.path.join(project_directory, project_relative_file_path)
	dst = os.path.join(destination_directory, project_relative_file_path)

	os.makedirs(os.path.dirname(dst), exist_ok=True)
	await asyncio.to_thread(shutil.copy2, src, dst)  # copy with metadata


def ensure_parent_folder_exists(full_file_path):
	parent_path = os.path.dirname(full_file_path)
	if os.path.exists(parent_path): return
	if not parent_path: return  # Avoid issues if full_file_path is just a filename
	os.makedirs(parent_path, exist_ok=True)


def get_items_to_copy_project_relative(project_directory):
	full_system_path = os.path.abspath(project_directory)
	gitignore_path = os.path.join(full_system_path, ".gitignore")

	# no gitignore, return all
	if not os.path.exists(gitignore_path):
		return os.listdir(full_system_path)

	# yield all that are not ignored
	matches_gitignore = parse_gitignore(gitignore_path)

	for item_name in os.listdir(full_system_path):
		full_item_system_path = os.path.join(full_system_path, item_name)
		if not matches_gitignore(full_item_system_path):
			yield item_name


def sort_files_into_hierarchy(all_files, project_directory):
	files = {"project_path": "./", "folders": {}, "files": []}
	for file_name in all_files:
		sort_file_into_hierarchy(file_name, Path(file_name).parts, files, project_directory)
	return files


def sort_file_into_hierarchy(file_path_project_relative, file_name_parts_left: list, sorted_files: dict, project_directory) -> None:
	# is file
	if len(file_name_parts_left) == 1:
		if not os.path.isfile(os.path.join(project_directory, file_path_project_relative)): return
		sorted_files["files"].append(file_path_project_relative)
		return

	# is folder
	folders_dict = sorted_files["folders"]

	# create if needed 
	folder_name = file_name_parts_left[0]
	if not folder_name in folders_dict:
		file_path_in_current_folder = os.path.sep.join(file_name_parts_left[1:])
		chars_in_current_dir = len(file_path_project_relative) - len(file_path_in_current_folder)
		current_folder_dir = file_path_project_relative[:chars_in_current_dir]

		folders_dict[folder_name] = {}
		folders_dict[folder_name]["project_path"] = current_folder_dir
		folders_dict[folder_name]["folders"] = {}
		folders_dict[folder_name]["files"] = []

	sort_file_into_hierarchy(file_path_project_relative, file_name_parts_left[1:], folders_dict[folder_name], project_directory)


def get_item_in_dict_create_if_none_exists(d, parts_list):
	current = d
	for part in parts_list:
		if not part in current:
			current[part] = {}
		current = current[part]
	return current


def get_items_in_folder(repo_relative_file_directories, repo_relative_folder):
	for item in repo_relative_file_directories:
		if item.startswith(repo_relative_folder):
			yield item


if __name__ == "__main__":
	main()
