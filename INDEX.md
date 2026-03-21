This file was generated using the output of each script with "--help"
# combine

## [combine_text_lines.py](combine_text_lines.py)
```text
usage: combine_text_lines.py [-h] --file FILE [--sort] output

Combine unique non-empty lines from input files.

positional arguments:
  output       Output file to write.

options:
  -h, --help   show this help message and exit
  --file FILE  Input file to read.
  --sort       Sort the lines?
```

# convert

## [convert_to_mono.py](convert_to_mono.py)
```text
usage: convert_to_mono.py [-h] [--ext EXT] [--dry-run] folder

Convert all audio files in a folder to mono.

positional arguments:
  folder      Folder to scan recursively.

options:
  -h, --help  show this help message and exit
  --ext EXT   File extension to include (repeatable).
  --dry-run   Print what would change without writing files.
```

# count

## [count_lines.py](count_lines.py)
```text
usage: count_lines.py [-h] [--ext EXT] [directory]

Count lines for files with a given extension.

positional arguments:
  directory   Root directory to scan.

options:
  -h, --help  show this help message and exit
  --ext EXT   File extension to include (default: .cs).
```

# get

## [get_all_non_snake_case_files.py](get_all_non_snake_case_files.py)
```text
usage: get_all_non_snake_case_files.py [-h] [--ignore IGNORE] root

List files that are not in snake_case.

positional arguments:
  root             Root folder to scan.

options:
  -h, --help       show this help message and exit
  --ignore IGNORE  Regex pattern to ignore (repeatable).
```

# image

## [image_color_to_alpha.py](image_color_to_alpha.py)
```text
usage: image_color_to_alpha.py [-h]
                               [--max_color_difference MAX_COLOR_DIFFERENCE]
                               [--verbose]
                               input_image_path output_image_path
                               target_color_hex

Replace a target color in an image with transparency.

positional arguments:
  input_image_path      Path to the input image file.
  output_image_path     Path to write the output image file.
  target_color_hex      Target color in hex, e.g. #ff00aa.

options:
  -h, --help            show this help message and exit
  --max_color_difference MAX_COLOR_DIFFERENCE
                        Maximum color difference for replacement. Default: 1.
  --verbose             Print progress details.
```

## [image_crop_folders_to_multiples_of_4.py](image_crop_folders_to_multiples_of_4.py)
```text
usage: image_crop_folders_to_multiples_of_4.py [-h] [--ext EXT] folder

Crop images so width and height are multiples of 4.

positional arguments:
  folder      Path to the folder containing images.

options:
  -h, --help  show this help message and exit
  --ext EXT   File extension to include (repeatable).
```

## [image_crop_to_content.py](image_crop_to_content.py)
```text
usage: image_crop_to_content.py [-h] [--ext EXT] [folder]

Crop transparent borders from images in a folder.

positional arguments:
  folder      Folder to scan.

options:
  -h, --help  show this help message and exit
  --ext EXT   File extension to include (repeatable).
```

## [image_merge_as_layers.py](image_merge_as_layers.py)
```text
usage: image_merge_as_layers.py [-h] [--input_folder INPUT_FOLDER]
                                [--image IMAGE] [--verbose]
                                output_file

Merge images into one composited output image.

positional arguments:
  output_file           Path for the combined output image

options:
  -h, --help            show this help message and exit
  --input_folder INPUT_FOLDER
                        Folder containing images
  --image IMAGE         Image file path. Repeat for multiple.
  --verbose
```

# json

## [json_tidier.py](json_tidier.py)
```text
usage: json_tidier.py [-h] [path]

Tidy JSON files by removing trailing commas.

positional arguments:
  path        Root folder to scan.

options:
  -h, --help  show this help message and exit
```

# repo

## [repo_copier.py](repo_copier.py)
```text
usage: repo_copier.py [-h] project_directory destination_directory

Copy a repo's tracked files into a clean destination directory.

positional arguments:
  project_directory     Path to the project repo to copy.
  destination_directory
                        Path to the destination directory to create and
                        populate.

options:
  -h, --help            show this help message and exit
```

# scale

## [scale_and_crop_video.py](scale_and_crop_video.py)
```text
usage: scale_and_crop_video.py [-h] [-r RESOLUTION] [--overwrite]
                               source output

Wrapper around ffmpeg. Unknown arguments are passed through to ffmpeg.
-loglevel defaults to error.

positional arguments:
  source
  output                Where to put exported clips.

options:
  -h, --help            show this help message and exit
  -r, --resolution RESOLUTION
                        Resolutions to export to. Accepts <width>x<height> or
                        <width>,<height>.
  --overwrite           Overwrite modified files that already exist.
```
