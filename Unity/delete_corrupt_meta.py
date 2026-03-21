import os
from pathlib import Path
import re


LOCAL_APPDATA_EDITOR_LOG_FILEPATH = r"Unity\Editor\Editor.log"
BAD_META_PATTERN = re.compile(r"(Assets/.*?\.meta).*?YAML Parser", re.S)
PROJECT_PATH_PATTERN = re.compile(r"Successfully changed project path to: (.*)")


def find_corrupt_meta_files():
    editor_log = get_editor_log()

    match = PROJECT_PATH_PATTERN.search(editor_log)
    project_path = match.group(1)

    for file_path in sorted(set(BAD_META_PATTERN.findall(editor_log))):
        yield os.path.join(project_path, file_path)
        

def get_editor_log() -> str:
    filepath = os.path.join(Path(os.environ["LOCALAPPDATA"]), LOCAL_APPDATA_EDITOR_LOG_FILEPATH)
    with open(filepath, "r") as file:
        return file.read()


def delete_files(file_paths):
    for file_path in file_paths:
        os.remove(file_path)


def main():
    corrupt = list(find_corrupt_meta_files())

    print("meta files Unity could not open:")
    for file_path in corrupt:
        print("  * " + file_path)
    confirmation_input = input("y to delete: ")

    if confirmation_input.lower() != "y":
        print("Aborting")
        return
    
    print("Deleting...")
    delete_files(corrupt)


if __name__ == "__main__":
    main()