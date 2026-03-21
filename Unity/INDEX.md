This file was generated using the output of each script with "--help"
# check

## check_packages_page_size_in_apk.py
```text
usage: check_packages_page_size_in_apk.py [-h] --so-dir SO_DIR
                                          [--readelf-path READELF_PATH]
                                          [--ndk-path NDK_PATH]

Check native libraries for minimum LOAD alignment.

options:
  -h, --help            show this help message and exit
  --so-dir SO_DIR       Folder containing .so files.
  --readelf-path READELF_PATH
                        Path to llvm-readelf.exe.
  --ndk-path NDK_PATH   Path to the Unity NDK root (used to derive llvm-
                        readelf.exe).
```

# delete

## delete_all_cache.py
```text
usage: delete_all_cache.py [-h] [--project-root PROJECT_ROOT]
                           [--no-unity-cache] [--no-gradle-cache] [--safe]

Delete common Unity, Gradle, and project cache folders.

options:
  -h, --help            show this help message and exit
  --project-root PROJECT_ROOT
                        Unity project root.
  --no-unity-cache      Skip Unity global cache folders.
  --no-gradle-cache     Skip Gradle cache folders.
  --safe                Send folders to recycle bin instead of deleting.
```

## delete_corrupt_meta.py
```text
usage: delete_corrupt_meta.py [-h] [--yes]

Delete Unity .meta files that failed to parse in the Editor log.

options:
  -h, --help  show this help message and exit
  --yes       Delete without prompting.
```

# get

## get_all_resources.py
```text
usage: get_all_resources.py [-h] [--root ROOT] --output OUTPUT

Copy all Unity Resources folders to a single output directory.

options:
  -h, --help       show this help message and exit
  --root ROOT      Unity project Assets root.
  --output OUTPUT  Destination folder for copied Resources.
```

# move

## move_files_to_non_import_folders.py
```text
usage: move_files_to_non_import_folders.py [-h] [--root ROOT]
                                           [--pattern PATTERN]
                                           [--hidden-folder HIDDEN_FOLDER]
                                           [--include-submodules] [--yes]

Move files under Assets into hidden folders to prevent Unity imports.

options:
  -h, --help            show this help message and exit
  --root ROOT           Root folder to scan.
  --pattern PATTERN     Regex for files to move (repeatable).
  --hidden-folder HIDDEN_FOLDER
                        Hidden folder name to create.
  --include-submodules  Include files inside git submodules.
  --yes                 Skip confirmation prompt.
```
