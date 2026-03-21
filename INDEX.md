This file was generated using the output of each script with "--help"
# Subfolders
 - [git/](git/INDEX.md)
 - [godot/](godot/INDEX.md)
 - [Unity/](Unity/INDEX.md)

# combine

## combine_text_lines.py
```text
usage: combine_text_lines.py [-h] --file FILE output

Combine unique non-empty lines from input files.

positional arguments:
  output           Output file to write.

options:
  -h, --help       show this help message and exit
  --file, -f FILE  Input file to read.
```

# convert

## convert_to_mono.py
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

## count_lines.py
```text
usage: count_lines.py [-h] [--ext EXT] [directory]

Count lines for files with a given extension.

positional arguments:
  directory   Root directory to scan.

options:
  -h, --help  show this help message and exit
  --ext EXT   File extension to include (default: .cs).
```

# crop

## crop_image_to_content.py
```text
usage: crop_image_to_content.py [-h] [--ext EXT] [folder]

Crop transparent borders from images in a folder.

positional arguments:
  folder      Folder to scan.

options:
  -h, --help  show this help message and exit
  --ext EXT   File extension to include (repeatable).
```

## crop_images_to_multiples_of_4.py
```text
usage: crop_images_to_multiples_of_4.py [-h] [--ext EXT] folder

Crop images so width and height are multiples of 4.

positional arguments:
  folder      Path to the folder containing images.

options:
  -h, --help  show this help message and exit
  --ext EXT   File extension to include (repeatable).
```

# get

## get_all_non_snake_case_files.py
```text
usage: get_all_non_snake_case_files.py [-h] [--ignore IGNORE] root

List files that are not in snake_case.

positional arguments:
  root             Root folder to scan.

options:
  -h, --help       show this help message and exit
  --ignore IGNORE  Regex pattern to ignore (repeatable).
```

# json

## json_tidier.py
```text
usage: json_tidier.py [-h] [path]

Tidy JSON files by removing trailing commas.

positional arguments:
  path        Root folder to scan.

options:
  -h, --help  show this help message and exit
```

# repo

## repo_copier.py
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

## scale_and_crop_video.py
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
