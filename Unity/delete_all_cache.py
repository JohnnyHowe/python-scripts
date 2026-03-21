import os
from pathlib import Path
import subprocess
from send2trash import send2trash


def delete_fast(path):
    run_on_folder(path, _unsafe_delete_fast)


def _unsafe_delete_fast(path):
    subprocess.run(['rmdir', '/S', '/Q', path], shell=True)


def delete_safe(path): 
    run_on_folder(path, send2trash)


def run_on_folder(path, func):
    path = Path(path)
    full_path = get_full_path(path)

    path_display_str = f"\"{path}\""
    if path != full_path:
        path_display_str = f"\"{path}\" (\"{full_path}\")"

    if not os.path.exists(full_path):
        print(f"No folder at {path_display_str} (deepest parent: {get_first_parent_that_exists(full_path)})")
        return

    print(f"Deleting {path_display_str}")
    func(full_path)



def get_full_path(path: str):
    path = str(path)
    path = path.replace("%USERPROFILE%", str(Path.home()))
    return Path(path).absolute()


def get_first_parent_that_exists(path: str) -> str:
    parts = path.parts

    for i in range(len(parts) -1, 0, -1):
        current_path = os.path.join(*parts[:i])
        if os.path.exists(current_path):
            return current_path

    return ""

# Project cache
delete_fast("./Library")
delete_fast("./Temp")
delete_fast("./obj")

# Unity cache
delete_fast(r"%USERPROFILE%\AppData\Local\Unity\Caches\GI")
delete_fast(r"%USERPROFILE%\AppData\Local\Unity\cache")
delete_fast(r"%USERPROFILE%\AppData\Roaming\Unity\Packages")

# Gradle cache
delete_fast(r"%USERPROFILE%\.gradle\caches")