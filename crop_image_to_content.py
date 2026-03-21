"""
Tool to alpha borders off images.
Run from command line with folder path. If none given, it uses current working dir.

Example
python crop_to_content.py "C:\\Users\\Work\\Documents\\Images To Crop"
"""
import sys
from PIL import Image, ImageChops
from pathlib import Path


def crop_to_content(path_in, path_out):
	image = Image.open(path_in)

	if not has_transparency(image):
		raise Exception("Image type not supported for %s" % path_in)

	new_image = Image.new(image.mode, image.size, (0, 0, 0, 0))

	diff = ImageChops.difference(image, new_image)
	bbox = diff.getbbox()
	if bbox:
		image = image.crop(bbox)

	image.save(path_out)


def has_transparency(image):
	return image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info)


def get_image_paths(folder, exts=(".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff")):
    folder = Path(folder)
    return [p for p in folder.iterdir() if p.suffix.lower() in exts]


def crop(folder_path):
	for image in get_image_paths(folder_path):
		crop_to_content(image, image)


if __name__ == "__main__":
	path = "./"
	if len(sys.argv) > 2:
		raise Exception("Only accepts one (or none for this folder) arg: path")
	elif len(sys.argv) == 2:
		path = sys.argv[1]
	crop(path)