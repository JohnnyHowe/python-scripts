"""
Check native libraries in an APK build for minimum LOAD alignment.
"""
import argparse
import os
from pathlib import Path
import re
import subprocess


_DEFAULT_READ_ELF_RELATIVE = Path(r"toolchains\llvm\prebuilt\windows-x86_64\bin\llvm-readelf.exe")


def check_packages_page_size_in_apk(so_dir: Path, readelf_path: Path) -> int:
	if not readelf_path.exists():
		print(f"readelf not found: {readelf_path}")
		return 1

	if not so_dir.exists():
		print(f"so directory not found: {so_dir}")
		return 1

	for file_path in sorted(so_dir.iterdir()):
		if file_path.suffix.lower() != ".so":
			continue
			
		size_ok = _get_min_load_size(readelf_path, file_path) >= int("0x4000", 16)
		status = "OK" if size_ok else "FAIL"
		print(f"{status} {file_path.name}")

	return 0


def _get_min_load_size(readelf_path: Path, path: Path) -> int:
	command = [str(readelf_path), "-l", str(path)]
	output = subprocess.run(command, capture_output=True, text=True, check=True)
	versions_hex = _get_align_versions(output.stdout)
	versions = [int(x, 16) for x in versions_hex]
	return min(versions)


def _get_align_versions(stdout: str):
	pattern = re.compile("LOAD.*(0x.*)")
	return pattern.findall(stdout)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Check native libraries for minimum LOAD alignment.")
	parser.add_argument("--so-dir", type=Path, required=True, help="Folder containing .so files.")
	parser.add_argument("--readelf-path", type=Path, help="Path to llvm-readelf.exe.")
	parser.add_argument(
		"--ndk-path",
		type=Path,
		help="Path to the Unity NDK root (used to derive llvm-readelf.exe).",
	)
	args = parser.parse_args()

	readelf_path = args.readelf_path
	if readelf_path is None:
		if args.ndk_path is None:
			raise SystemExit("Either --readelf-path or --ndk-path is required.")
		readelf_path = args.ndk_path / _DEFAULT_READ_ELF_RELATIVE

	raise SystemExit(check_packages_page_size_in_apk(args.so_dir, readelf_path))
