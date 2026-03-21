import os
from pathlib import Path
import shutil


OUTPUT_DIRECTORY = Path("C:/Users/Work/Desktop/DriftoResources")
ROOT = Path("Assets")


def clear_directory(directory: Path):
    if directory.exists():
        if directory.is_dir():
            shutil.rmtree(directory)
        else:
            os.remove(directory)
    directory.mkdir(parents=True)


def find_all_resource_folders(root: Path):
    for entry in os.listdir(root):
        path = Path(os.path.join(root, entry))

        if not path.is_dir():
            continue

        if entry == "Resources":
            yield path 
        else:
            yield from find_all_resource_folders(path)


clear_directory(OUTPUT_DIRECTORY)
resource_paths = list(find_all_resource_folders(ROOT))

for resource_path in resource_paths:
    resource_path_relative = resource_path.relative_to(ROOT)
    destination_path = Path(os.path.join(OUTPUT_DIRECTORY, resource_path_relative))
    shutil.copytree(resource_path, destination_path)
