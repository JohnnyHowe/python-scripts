"""
Normalize all audio files in a folder.
"""
import argparse
from pathlib import Path
from typing import Iterable
from pydub import AudioSegment


DEFAULT_EXTENSIONS = [".wav", ".mp3"]


def normalize_audio(folder: Path, extensions: list[str], target_dbfs: float, verbose: bool = False) -> int:
	extensions = _normalize_extensions(extensions)
	for file_path in _get_audio_files(folder, extensions):
		_normalize_file(file_path, target_dbfs, verbose)
	return 0


def _normalize_extensions(extensions: list[str]) -> list[str]:
	normalized = [ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in extensions]
	return normalized or DEFAULT_EXTENSIONS


def _get_audio_files(folder: Path, extensions: list[str]) -> Iterable[Path]:
	for file_path in folder.rglob("*"):
		if not file_path.is_file():
			continue

		if file_path.suffix.lower() not in extensions:
			continue

		yield file_path


def _normalize_file(file_path: Path, target_dbfs: float, verbose: bool = False) -> None:
	audio = AudioSegment.from_file(file_path)
	gain_change = _get_required_gain_change(audio, target_dbfs)
	if gain_change is None:
		return

	normalized_audio = audio.apply_gain(gain_change)
	normalized_audio.export(file_path, format=file_path.suffix[1:])
	if verbose:
		print(f"Normalized {file_path} by {gain_change:.2f} dB to {target_dbfs:.2f} dBFS")


def _get_required_gain_change(audio: AudioSegment, target_dbfs: float) -> float | None:
	if audio.max_dBFS == float("-inf"):
		return None

	gain_change = target_dbfs - audio.max_dBFS
	if abs(gain_change) < 0.01:
		return None

	return gain_change


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Normalize all audio files in a folder.")
	parser.add_argument("folder", type=Path, help="Folder to scan recursively.")
	parser.add_argument("--ext", action="append", default=[], help="File extension to include (repeatable).")
	parser.add_argument("--target-dbfs", type=float, default=0, help="Target peak dBFS (default: 0).")
	parser.add_argument("--quiet", action="store_true")
	args = parser.parse_args()

	raise SystemExit(normalize_audio(args.folder, args.ext, args.target_dbfs, not args.quiet))
