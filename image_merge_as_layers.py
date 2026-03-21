"""Merge a folder of images into one composited output image."""

import argparse
from pathlib import Path
from PIL import Image


def merge_images_as_layers(
    output_file: str,
    input_folder: str | None = None,
    image_files: list | None = None,
    verbose: bool = False,
) -> int:
    """Merge images into one composited output image."""
    try:
        selected_files = _resolve_image_files(input_folder, image_files)
        if not selected_files:
            if input_folder:
                print(f"Error: no image files found in '{input_folder}'.")
            else:
                print("Error: no image files provided.")
            return 1

        base_image = Image.open(selected_files[0]).convert("RGBA")
        for file_path in selected_files[1:]:
            img = Image.open(file_path).convert("RGBA")
            base_image = Image.alpha_composite(base_image, img)

        base_image.save(output_file)
        if verbose:
            print(f"Wrote: {output_file}")
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        return 1


def _resolve_image_files(input_folder: str | None, image_files: list | None) -> list:
    if image_files:
        return [Path(p) for p in image_files if _is_image_file(Path(p))]
    if input_folder:
        return _get_image_files(Path(input_folder))
    return []


def _get_image_files(input_folder: Path) -> list:
    image_files = [p for p in input_folder.iterdir() if _is_image_file(p)]
    return sorted(image_files, key=lambda p: p.name.lower())


def _is_image_file(path: Path) -> bool:
    return path.suffix.lower() in (".png", ".jpg", ".jpeg")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge images into one composited output image.")
    parser.add_argument("--input_folder", help="Folder containing images")
    parser.add_argument("--image", action="append", help="Image file path. Repeat for multiple.")
    parser.add_argument("output_file", help="Path for the combined output image")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    raise SystemExit(merge_images_as_layers(args.output_file, args.input_folder, args.image, args.verbose))
