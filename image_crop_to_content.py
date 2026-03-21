"""
Crop transparent borders from images in a folder.
"""
import argparse
from pathlib import Path
from PIL import Image, ImageChops


DEFAULT_EXTENSIONS = [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff"]


def crop_image_to_content(folder: Path, extensions: list[str]) -> int:
	images = _get_image_paths(folder, extensions)
	if not images:
		print("No matching images found.")
		return 0

	for image_path in images:
		_crop_to_content(image_path, image_path)

	print(f"Images cropped: {len(images)}")
	return 0


def _crop_to_content(path_in: Path, path_out: Path) -> None:
	image = Image.open(path_in)

	if not _has_transparency(image):
		raise Exception(f"Image type not supported for {path_in}")

	new_image = Image.new(image.mode, image.size, (0, 0, 0, 0))

	diff = ImageChops.difference(image, new_image)
	bbox = diff.getbbox()
	if bbox:
		image = image.crop(bbox)

	image.save(path_out)


def _has_transparency(image: Image.Image) -> bool:
	return image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info)


def _get_image_paths(folder: Path, extensions: list[str]) -> list[Path]:
	return [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in extensions]


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Crop transparent borders from images in a folder.")
	parser.add_argument("folder", type=Path, nargs="?", default=Path.cwd(), help="Folder to scan.")
	parser.add_argument("--ext", action="append", default=[], help="File extension to include (repeatable).")
	args = parser.parse_args()

	extensions = [ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in args.ext]
	if not extensions:
		extensions = DEFAULT_EXTENSIONS

	raise SystemExit(crop_image_to_content(args.folder, extensions))
