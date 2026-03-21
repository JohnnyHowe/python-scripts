"""Replace a target color in an image with transparency."""

from PIL import Image
import argparse


def image_color_to_alpha(
    input_image_path: str,
    output_image_path: str,
    target_color_hex: str,
    max_color_difference: int = 1,
    verbose: bool = False,
) -> int:
    """Replace a target color in an image with transparency."""
    try:
        target_color = _hex_to_rgb(target_color_hex)
        _replace_color_in_file(input_image_path, output_image_path, target_color, max_color_difference)
        if verbose:
            print(f"Wrote: {output_image_path}")
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        return 1


def _hex_to_rgb(h: str) -> tuple:
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def _replace_color_in_file(
    input_image_path: str,
    output_image_path: str,
    target_color,
    max_color_difference: int,
) -> None:
    img = Image.open(input_image_path).convert("RGBA")
    _replace_color(img, target_color, max_color_difference)
    img.save(output_image_path)


def _replace_color(img: Image, target_color, max_color_difference: int) -> None:
    data = img.getdata()
    new_data = []

    for r, g, b, a in data:
        if _get_color_difference((r, g, b), target_color) < max_color_difference:
            new_data.append((r, g, b, 0))
        else:
            new_data.append((r, g, b, a))

    img.putdata(new_data)


def _get_color_difference(c1: tuple, c2: tuple) -> float:
    return sum([c1[i] + c2[i] for i in range(3)])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace a target color in an image with transparency.")
    parser.add_argument("input_image_path", type=str, help="Path to the input image file.")
    parser.add_argument("output_image_path", type=str, help="Path to write the output image file.")
    parser.add_argument("target_color_hex", type=str, help="Target color in hex, e.g. #ff00aa.")
    parser.add_argument(
        "--max_color_difference",
        type=int,
        default=1,
        help="Maximum color difference for replacement. Default: 1.",
    )
    parser.add_argument("--verbose", action="store_true", help="Print progress details.")
    args = parser.parse_args()
    raise SystemExit(
        image_color_to_alpha(
            args.input_image_path,
            args.output_image_path,
            args.target_color_hex,
            args.max_color_difference,
            args.verbose,
        )
    )
