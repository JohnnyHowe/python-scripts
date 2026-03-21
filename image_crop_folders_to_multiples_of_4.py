"""
Crop images so width and height are multiples of 4.
"""
import argparse
from pathlib import Path
from PIL import Image


DEFAULT_EXTENSIONS = [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]


def crop_images_to_multiples_of_4(folder: Path, extensions: list[str]) -> int:
	count = 0
	for path in folder.iterdir():
		if not path.is_file():
			continue
		if path.suffix.lower() not in extensions:
			continue

		img = Image.open(path)
		new_width = img.width - (img.width % 4)
		new_height = img.height - (img.height % 4)

		if new_width != img.width or new_height != img.height:
			cropped = img.crop((0, 0, new_width, new_height))
			cropped.save(path)
			print(f"Cropped {path.name} -> {new_width}x{new_height}")
			count += 1
		else:
			print(f"{path.name} already multiple of 4")

	print(f"Images cropped: {count}")
	return 0


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Crop images so width and height are multiples of 4.")
	parser.add_argument("folder", type=Path, help="Path to the folder containing images.")
	parser.add_argument("--ext", action="append", default=[], help="File extension to include (repeatable).")
	args = parser.parse_args()

	extensions = [ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in args.ext]
	if not extensions:
		extensions = DEFAULT_EXTENSIONS

	raise SystemExit(crop_images_to_multiples_of_4(args.folder, extensions))
