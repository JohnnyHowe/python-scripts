import os
from pathlib import Path
import re
import subprocess

ndk_path = Path(r"C:\Program Files\Unity\Hub\Editor\6000.3.5f1\Editor\Data\PlaybackEngines\AndroidPlayer\NDK")
readelf_path = os.path.join(ndk_path, Path(r"toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-readelf.exe"))

build_path = Path(r"C:\Users\Work\Documents\Projects\drifto\build\build")
so_dir = os.path.join(build_path, Path(r"lib\arm64-v8a"))


def check_file(path):
    size_ok = get_min_load_size(path) >= int("0x4000", 16)
    print(f"{"✅" if size_ok else "❌"} {os.path.basename(path)}")


def get_min_load_size(path):
    command = [readelf_path, "-l", path]
    output = subprocess.run(command,capture_output=True, text=True, check=True) 
    versions_hex = get_align_versions(output.stdout)
    versions = [int(x, 16) for x in versions_hex]
    return min(versions)


def get_align_versions(stdout: str) :
    pattern = re.compile("LOAD.*(0x.*)")
    return pattern.findall(stdout)


for file_path in os.listdir(so_dir):
    check_file(os.path.join(so_dir, file_path))