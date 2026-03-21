"""
Copy a repo's tracked files into a clean destination directory.
"""
import argparse
import asyncio
import os
from pathlib import Path
import re
import shutil
import subprocess
from gitignore_parser import parse_gitignore

LOG_HIGH_LEVEL_TASKS = True


def repo_copier(project_directory: Path, destination_directory: Path) -> int:
	_copy_project(project_directory, destination_directory)
	return 0


def _create_fresh_destination(full_system_path: Path) -> None:
	if LOG_HIGH_LEVEL_TASKS:
		print("Clearing clone destination...")

	full_system_path = full_system_path.resolve()

	if not _is_safe_directory(full_system_path):
		raise Exception(f"Given path deemed unsafe! \"{full_system_path}\"")

	if full_system_path.exists():
		subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(full_system_path)], shell=True)

	full_system_path.mkdir(exist_ok=True, parents=True)


def _is_safe_directory(full_system_path: Path) -> bool:
	pattern = r"C:\\Users\\.*\\"
	return re.match(pattern, str(full_system_path)) is not None


def _copy_project(project_directory: Path, destination_directory: Path) -> None:
	_create_fresh_destination(destination_directory)

	if LOG_HIGH_LEVEL_TASKS:
		print("Copying files...")

	repo_full_path = os.path.abspath(project_directory)

	result = subprocess.run(
		["git", "-C", str(repo_full_path), "ls-files"],
		capture_output=True,
		text=True,
		check=True,
	)
	repo_relative_file_directories = result.stdout.splitlines()

	asyncio.run(_copy_files(repo_relative_file_directories, project_directory, destination_directory))


async def _copy_files(repo_relative_file_directories, project_directory, destination_directory):
	files_hierarchy = _sort_files_into_hierarchy(repo_relative_file_directories, project_directory)
	await _copy_files_dict(files_hierarchy, project_directory, destination_directory)


async def _copy_files_dict(folder_info_dict, project_directory, destination_directory):
	_ensure_parent_folder_exists(folder_info_dict["project_path"])

	files_list_project_relative = folder_info_dict["files"]
	file_tasks = [
		_async_copy_file(project_relative_file_path, project_directory, destination_directory)
		for project_relative_file_path in files_list_project_relative
	]

	folder_tasks = []
	for folder_name in folder_info_dict["folders"].keys():
		folder_tasks.append(
			_copy_files_dict(folder_info_dict["folders"][folder_name], project_directory, destination_directory)
		)

	await asyncio.gather(*(file_tasks + folder_tasks))


async def _async_copy_file(project_relative_file_path, project_directory, destination_directory):
	src = os.path.join(project_directory, project_relative_file_path)
	dst = os.path.join(destination_directory, project_relative_file_path)

	os.makedirs(os.path.dirname(dst), exist_ok=True)
	await asyncio.to_thread(shutil.copy2, src, dst)


def _ensure_parent_folder_exists(full_file_path):
	parent_path = os.path.dirname(full_file_path)
	if os.path.exists(parent_path):
		return
	if not parent_path:
		return
	os.makedirs(parent_path, exist_ok=True)


def _get_items_to_copy_project_relative(project_directory):
	full_system_path = os.path.abspath(project_directory)
	gitignore_path = os.path.join(full_system_path, ".gitignore")

	if not os.path.exists(gitignore_path):
		return os.listdir(full_system_path)

	matches_gitignore = parse_gitignore(gitignore_path)

	for item_name in os.listdir(full_system_path):
		full_item_system_path = os.path.join(full_system_path, item_name)
		if not matches_gitignore(full_item_system_path):
			yield item_name


def _sort_files_into_hierarchy(all_files, project_directory):
	files = {"project_path": "./", "folders": {}, "files": []}
	for file_name in all_files:
		_sort_file_into_hierarchy(file_name, Path(file_name).parts, files, project_directory)
	return files


def _sort_file_into_hierarchy(file_path_project_relative, file_name_parts_left: list, sorted_files: dict, project_directory) -> None:
	if len(file_name_parts_left) == 1:
		if not os.path.isfile(os.path.join(project_directory, file_path_project_relative)):
			return
		sorted_files["files"].append(file_path_project_relative)
		return

	folders_dict = sorted_files["folders"]

	folder_name = file_name_parts_left[0]
	if folder_name not in folders_dict:
		file_path_in_current_folder = os.path.sep.join(file_name_parts_left[1:])
		chars_in_current_dir = len(file_path_project_relative) - len(file_path_in_current_folder)
		current_folder_dir = file_path_project_relative[:chars_in_current_dir]

		folders_dict[folder_name] = {}
		folders_dict[folder_name]["project_path"] = current_folder_dir
		folders_dict[folder_name]["folders"] = {}
		folders_dict[folder_name]["files"] = []

	_sort_file_into_hierarchy(
		file_path_project_relative,
		file_name_parts_left[1:],
		folders_dict[folder_name],
		project_directory,
	)


def _get_item_in_dict_create_if_none_exists(d, parts_list):
	current = d
	for part in parts_list:
		if part not in current:
			current[part] = {}
		current = current[part]
	return current


def _get_items_in_folder(repo_relative_file_directories, repo_relative_folder):
	for item in repo_relative_file_directories:
		if item.startswith(repo_relative_folder):
			yield item


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Copy a repo's tracked files into a clean destination directory.")
	parser.add_argument("project_directory", type=Path, help="Path to the project repo to copy.")
	parser.add_argument("destination_directory", type=Path, help="Path to the destination directory to create and populate.")
	args = parser.parse_args()

	raise SystemExit(repo_copier(args.project_directory, args.destination_directory))
