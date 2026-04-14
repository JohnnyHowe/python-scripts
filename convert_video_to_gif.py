"""
Convert one or more video files to GIF using ffmpeg.
"""
import argparse
from pathlib import Path
import subprocess
import tempfile
from typing import Iterable


DEFAULT_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"]


def convert_video_to_gif(
	files: list[Path],
	folders: list[Path],
	recursive_folders: list[Path],
	extensions: list[str],
	fps: int,
	width: int | None,
	overwrite: bool = False,
	verbose: bool = False,
) -> int:
	video_files = _get_video_files(files, folders, recursive_folders, extensions)
	if len(video_files) == 0:
		print("Error: no video files found.")
		return 1

	for file_path in video_files:
		output_path = file_path.with_suffix(".gif")
		if output_path.exists() and not overwrite:
			print(f"Skipping existing file: {output_path}")
			continue

		if verbose:
			print(f"Converting {file_path} -> {output_path}")

		try:
			_convert_file(file_path, output_path, fps, width, overwrite)
		except Exception as exception:
			print(f"Error converting {file_path}: {exception}")
			return 1

	return 0


def _get_video_files(
	files: list[Path],
	folders: list[Path],
	recursive_folders: list[Path],
	extensions: list[str],
) -> list[Path]:
	normalized_extensions = _normalize_extensions(extensions)
	results: set[Path] = set()

	for file_path in files:
		resolved_path = file_path.resolve()
		if not resolved_path.is_file():
			continue
		if resolved_path.suffix.lower() not in normalized_extensions:
			continue
		results.add(resolved_path)

	for folder_path in folders:
		results.update(_get_folder_video_files(folder_path.resolve(), normalized_extensions, recursive=False))

	for folder_path in recursive_folders:
		results.update(_get_folder_video_files(folder_path.resolve(), normalized_extensions, recursive=True))

	return sorted(results, key=lambda path: str(path).lower())


def _normalize_extensions(extensions: list[str]) -> list[str]:
	normalized = [extension.lower() if extension.startswith(".") else f".{extension.lower()}" for extension in extensions]
	return normalized or DEFAULT_EXTENSIONS


def _get_folder_video_files(folder: Path, extensions: list[str], recursive: bool) -> Iterable[Path]:
	if not folder.is_dir():
		return []

	iterator = folder.rglob("*") if recursive else folder.glob("*")
	return sorted(
		[
			file_path.resolve()
			for file_path in iterator
			if file_path.is_file() and file_path.suffix.lower() in extensions
		],
		key=lambda path: str(path).lower(),
	)


def _convert_file(source: Path, output: Path, fps: int, width: int | None, overwrite: bool) -> None:
	filter_chain = _get_filter_chain(fps, width)
	overwrite_flag = "-y" if overwrite else "-n"

	with tempfile.TemporaryDirectory() as temp_dir:
		palette_path = Path(temp_dir) / "palette.png"
		subprocess.run(
			[
				"ffmpeg",
				"-i",
				str(source),
				"-vf",
				f"{filter_chain},palettegen",
				overwrite_flag,
				str(palette_path),
			],
			check=True,
			capture_output=True,
			text=True,
		)
		subprocess.run(
			[
				"ffmpeg",
				"-i",
				str(source),
				"-i",
				str(palette_path),
				"-lavfi",
				f"{filter_chain} [x]; [x][1:v] paletteuse",
				overwrite_flag,
				str(output),
			],
			check=True,
			capture_output=True,
			text=True,
		)


def _get_filter_chain(fps: int, width: int | None) -> str:
	scale = "scale=iw:-1:flags=lanczos"
	if width is not None:
		scale = f"scale={width}:-1:flags=lanczos"

	return f"fps={fps},{scale}"


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Convert one or more video files to GIF using ffmpeg.")
	parser.add_argument("--file", action="append", default=[], type=Path, help="Video file to convert. Repeatable.")
	parser.add_argument("--folder", action="append", default=[], type=Path, help="Folder to scan for videos. Repeatable.")
	parser.add_argument(
		"--folder-recursive",
		action="append",
		default=[],
		type=Path,
		help="Folder to scan recursively for videos. Repeatable.",
	)
	parser.add_argument("--ext", action="append", default=[], help="Video extension to include. Repeatable.")
	parser.add_argument("--fps", type=int, default=12, help="GIF frames per second.")
	parser.add_argument("--width", type=int, help="Output width in pixels. Height is scaled automatically.")
	parser.add_argument("--overwrite", action="store_true", help="Overwrite GIFs that already exist.")
	parser.add_argument("--verbose", action="store_true", help="Print progress details.")
	args = parser.parse_args()

	raise SystemExit(
		convert_video_to_gif(
			args.file,
			args.folder,
			args.folder_recursive,
			args.ext,
			args.fps,
			args.width,
			args.overwrite,
			args.verbose,
		)
	)
