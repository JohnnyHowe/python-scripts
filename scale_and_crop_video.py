import argparse
from pathlib import Path
import subprocess


def _main():
	scale_and_crop(*_get_cli_args())


def _get_cli_args() -> tuple[Path, Path, list[tuple[int, int]], list[str]]:
	""" (source, output, resolutions, unknown_args) """
	parser = argparse.ArgumentParser(
		description="Wrapper around ffmpeg. Unknown arguments are passed through to ffmpeg. -loglevel by default set to error"
	)
	parser.add_argument("source", type=Path)
	parser.add_argument("output", help="Where to put exported clips.", type=Path)
	parser.add_argument("-r", "--resolution", help="Resolutions to export to. Will accept <width>x<height> or <width>,<height>", default=[], action="append", type=str)
	parser.add_argument("--overwrite", help="Overwrite modified files that already exist.", action="store_true")
	args, unknown_args = parser.parse_known_args()

	# Ensure source exists
	source = args.source.resolve()
	if not source.exists():
		raise FileNotFoundError(f"Source path {str(source)} does not exist!")

	# Ensure output dir exists
	output: Path = args.output.resolve()
	output.mkdir(parents=True, exist_ok=True)

	# Parse resolutions
	resolutions = []
	for resolution_arg in args.resolution:
		for char in ",x":
			if char in resolution_arg:
				parts = resolution_arg.split(char)
				break

		if len(parts) != 2:
			raise ValueError(f"Resolutions must contain two parts, split bt \",\" or \"x\". Got {resolution_arg} instead!")
		
		try:
			resolution = (int(parts[0]), int(parts[1]))
		except Exception as exception:
			raise ValueError(f"Could not parse resolution to (int, int). Got {parts}.") from exception

		output_name = _get_output_name(source, resolution)
		if not args.overwrite and (output / output_name).exists():
			print(f"File already exists in output with resolution {resolution} ({output_name}). Skipping. (use arg --overwrite to force rerender).")
			continue
	
		resolutions.append(resolution)

	# Set log level - only the last counts, so adding it to the start means it's overridden if user supplies one.
	unknown_args = ["-loglevel", "error"] + unknown_args

	return (source, output, resolutions, unknown_args)


def scale_and_crop(source: Path, output: Path, resolutions: list[tuple[int, int]], ffmpeg_args: list[str] = []) -> None:
	for resolution in resolutions:
		file_name = _get_output_name(source, resolution)
		print(f"Working on {resolution} ({file_name})")
		try:
			scale_and_crop_clip(source, output / file_name, resolution, ffmpeg_args)
		except Exception as exception:
			raise Exception(f"Could not crop {str(source.resolve())} to ({resolution[0]}, {resolution[1]}).") from exception


def _get_output_name(source: Path, resolution: tuple[int, int]) -> str:
	return f"{source.stem}-{resolution[0]}x{resolution[1]}{source.suffix}"


def scale_and_crop_clip(source: Path, output: Path, resolution: tuple[int, int], ffmpeg_args: list[str] = []) -> None:
	res_str = f"{resolution[0]}:{resolution[1]}"
	vf = f"scale={res_str}:force_original_aspect_ratio=increase,crop={res_str}"
	subprocess.run([
		"ffmpeg",
		"-i", str(source.resolve()),
		"-vf", vf,
		str(output.resolve()),
		*ffmpeg_args
	])


if __name__ == "__main__":
	_main()
