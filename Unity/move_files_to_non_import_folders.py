"""
# What?
Move every non import file in working_dir/Assets to a hidden folder in place of the original file.
So all .blend files in Assets/Models/Weapons gets moved to Assets/Models/Weapons/.blend_files
Important notes
* Will NOT move files if they're already hidden (any parent folder prefixed with ".")
* WILL change everything else: files in git submodules

# How to Use
For the love of god, make a backup, this is a one way script.
Run from project root. Easiest way is to just put this there and run it. If you've got python installed, just double click it.

# Why?
Unity ignores folders prefixed with the period character when importing files.
.blend files can be slow to import.
This script will put all .blend files into ignored folders.
"""
import os
from pathlib import Path
import re
import shutil


HIDDEN_FOLDER_NAME = ".do_not_import"
IGNORE_GIT_SUBMODULE_CONTENTS = True

FILES_TO_MOVE_REGEX = [
    r".*\.blend$",
    r".*\.xcf$"
]

files_to_move_regex_compiled = [re.compile(p) for p in FILES_TO_MOVE_REGEX]


def get_all_files_to_move(root: Path):
    for entry in os.listdir(root):
        path = Path(os.path.join(root, entry)).absolute()

        if path.is_file():
            if should_move_file(path):
                yield path

        elif path.is_dir():
            if should_search_folder(path):
                yield from get_all_files_to_move(path)


def should_search_folder(folder_path: Path) -> bool:
    # filters return true if folder passes check 
    folder_filters = [
        lambda folder_path: not is_folder_hidden(folder_path), 
        lambda folder_path: not (IGNORE_GIT_SUBMODULE_CONTENTS and is_folder_a_repository(folder_path)),
    ]
    return all(passes_filter(folder_path) for passes_filter in folder_filters)


def is_folder_hidden(folder_path: Path) -> bool:
    parts = os.path.split(folder_path)
    for part in parts:
        if part.startswith("."):
            return True
    return False


def is_folder_a_repository(folder_path: Path) -> bool:
    return os.path.exists(os.path.join(folder_path, ".git"))


def should_move_file(file_path: Path) -> bool:
    return any(r.search(str(file_path)) for r in files_to_move_regex_compiled)


def move_all_to_hidden_folder(file_paths: list):
    for file_path in file_paths:
        move_to_hidden_folder(file_path)


def move_to_hidden_folder(file_path: Path):
    hidden_folder_path = os.path.join(file_path.parent, HIDDEN_FOLDER_NAME)
    if not os.path.exists(hidden_folder_path):
        os.mkdir(hidden_folder_path)

    destination_file_path = os.path.join(hidden_folder_path, file_path.name)
    shutil.move(file_path, destination_file_path)


def main():
    root_folder = Path("Assets")

    file_paths_to_move = list(get_all_files_to_move(root_folder))

    if len(file_paths_to_move) == 0:
        print("No files found!")
        return

    print("Files found:")
    for path in file_paths_to_move:
        print(f"\t{path}")

    if not input(f"Move all to hidden folder {HIDDEN_FOLDER_NAME} (relative to each file)\n[Y/n]\n") == "Y":
        print("Aborting. Needed \"Y\" to continue.Y")
        return

    print("Moving all...")
    move_all_to_hidden_folder(file_paths_to_move)
    print("Done")


if __name__ == "__main__":
    main()