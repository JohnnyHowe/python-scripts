"""
Convert all audio files in a folder to mono.
"""
import argparse
from pathlib import Path
from pydub import AudioSegment


DEFAULT_EXTENSIONS = [".wav", ".mp3"]


def convert_to_mono(folder: Path, extensions: list[str], dry_run: bool) -> int:
	converted = 0
	for file_path in folder.rglob("*"):
		if not file_path.is_file():
			continue

		if file_path.suffix.lower() not in extensions:
			continue

		audio = AudioSegment.from_file(file_path)
		if audio.channels <= 1:
			continue

		if dry_run:
			print(f"Would convert {file_path} to mono")
			converted += 1
			continue

		mono_audio = audio.set_channels(1)
		mono_audio.export(file_path, format=file_path.suffix[1:])
		print(f"Converted {file_path} to mono")
		converted += 1

	print(f"Files converted: {converted}")
	return 0


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Convert all audio files in a folder to mono.")
	parser.add_argument("folder", type=Path, help="Folder to scan recursively.")
	parser.add_argument("--ext", action="append", default=[], help="File extension to include (repeatable).")
	parser.add_argument("--dry-run", action="store_true", help="Print what would change without writing files.")
	args = parser.parse_args()

	extensions = [ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in args.ext]
	if not extensions:
		extensions = DEFAULT_EXTENSIONS

	raise SystemExit(convert_to_mono(args.folder, extensions, args.dry_run))
