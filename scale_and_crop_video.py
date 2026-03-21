"""
Scale and crop a video to one or more resolutions using ffmpeg.
"""
import argparse
from pathlib import Path
import subprocess


def scale_and_crop_video(
	source: Path,
	output: Path,
	resolutions: list[tuple[int, int]],
	ffmpeg_args: list[str],
	overwrite: bool,
) -> int:
	for resolution in resolutions:
		file_name = _get_output_name(source, resolution)
		output_path = output / file_name

		if output_path.exists() and not overwrite:
			print(f"File already exists for {resolution} ({file_name}). Skipping. Use --overwrite to force.")
			continue

		print(f"Working on {resolution} ({file_name})")
		try:
			_scale_and_crop_clip(source, output_path, resolution, ffmpeg_args)
		except Exception as exception:
			raise Exception(
				f"Could not crop {str(source.resolve())} to ({resolution[0]}, {resolution[1]})."
			) from exception

	return 0


def _parse_resolution(resolution_arg: str) -> tuple[int, int]:
	parts = None
	for char in ",x":
		if char in resolution_arg:
			parts = resolution_arg.split(char)
			break

	if not parts or len(parts) != 2:
		raise ValueError(
			f"Resolutions must contain two parts, split by ',' or 'x'. Got {resolution_arg} instead!"
		)

	try:
		return (int(parts[0]), int(parts[1]))
	except Exception as exception:
		raise ValueError(f"Could not parse resolution to (int, int). Got {parts}.") from exception


def _get_output_name(source: Path, resolution: tuple[int, int]) -> str:
	return f"{source.stem}-{resolution[0]}x{resolution[1]}{source.suffix}"


def _scale_and_crop_clip(source: Path, output: Path, resolution: tuple[int, int], ffmpeg_args: list[str]) -> None:
	res_str = f"{resolution[0]}:{resolution[1]}"
	vf = f"scale={res_str}:force_original_aspect_ratio=increase,crop={res_str}"
	subprocess.run(
		[
			"ffmpeg",
			"-i",
			str(source.resolve()),
			"-vf",
			vf,
			str(output.resolve()),
			*ffmpeg_args,
		]
	)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description=(
			"Wrapper around ffmpeg. Unknown arguments are passed through to ffmpeg. "
			"-loglevel defaults to error."
		)
	)
	parser.add_argument("source", type=Path)
	parser.add_argument("output", type=Path, help="Where to put exported clips.")
	parser.add_argument(
		"-r",
		"--resolution",
		help="Resolutions to export to. Accepts <width>x<height> or <width>,<height>.",
		default=[],
		action="append",
		type=str,
	)
	parser.add_argument("--overwrite", help="Overwrite modified files that already exist.", action="store_true")
	args, unknown_args = parser.parse_known_args()

	source = args.source.resolve()
	if not source.exists():
		raise FileNotFoundError(f"Source path {str(source)} does not exist!")

	output = args.output.resolve()
	output.mkdir(parents=True, exist_ok=True)

	resolutions = [_parse_resolution(resolution_arg) for resolution_arg in args.resolution]

	unknown_args = ["-loglevel", "error"] + unknown_args

	raise SystemExit(scale_and_crop_video(source, output, resolutions, unknown_args, args.overwrite))
