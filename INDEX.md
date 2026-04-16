This file was generated using the output of each script with "--help"
# Subfolders
 - [audio/](audio/INDEX.md)
 - [git/](git/INDEX.md)
 - [godot/](godot/INDEX.md)
 - [Unity/](Unity/INDEX.md)

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

## [convert_video_to_gif.py](convert_video_to_gif.py)
```text
usage: convert_video_to_gif.py [-h] [--file FILE] [--folder FOLDER]
                               [--folder-recursive FOLDER_RECURSIVE]
                               [--ext EXT] [--fps FPS] [--width WIDTH]
                               [--jobs JOBS] [--overwrite] [--verbose]

Convert one or more video files to GIF using ffmpeg.

options:
  -h, --help            show this help message and exit
  --file FILE           Video file to convert. Repeatable.
  --folder FOLDER       Folder to scan for videos. Repeatable.
  --folder-recursive FOLDER_RECURSIVE
                        Folder to scan recursively for videos. Repeatable.
  --ext EXT             Video extension to include. Repeatable.
  --fps FPS             GIF frames per second. Default=12
  --width WIDTH         Output width in pixels. Height is scaled
                        automatically.
  --jobs JOBS           Number of files to convert concurrently. Default=8
  --overwrite           Overwrite GIFs that already exist.
  --verbose             Print progress details.
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

# generate

## [generate_bat_wrappers.py](generate_bat_wrappers.py)
```text
usage: generate_bat_wrappers.py [-h] [--file FILE] [--folder FOLDER]
                                [--folder-recursive FOLDER_RECURSIVE]
                                [--overwrite]

Generate .bat wrappers for Python scripts.

options:
  -h, --help            show this help message and exit
  --file FILE           Python script file. Repeatable. (default: [])
  --folder FOLDER       Folder to scan for Python scripts. Repeatable.
                        (default: [])
  --folder-recursive FOLDER_RECURSIVE
                        Folder to scan recursively for Python scripts.
                        Repeatable. (default: [])
  --overwrite           Overwrite existing .bat wrappers. (default: False)
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

## [get_changelog.py](get_changelog.py)
```text
usage: get_changelog.py [-h] [--path PATH] [--version VERSION]
                        [--no-version-header]
                        [--custom-sub-header [CUSTOM_SUB_HEADER]]

options:
  -h, --help            show this help message and exit
  --path PATH
  --version VERSION     Defaults to most recent
  --no-version-header
  --custom-sub-header [CUSTOM_SUB_HEADER]
                        Replaces the "### " before subheadings like "Fixed".
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
