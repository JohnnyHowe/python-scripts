This file was generated using the output of each script with "--help"
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

# normalize

## [normalize_audio.py](normalize_audio.py)
```text
usage: normalize_audio.py [-h] [--ext EXT] [--target-dbfs TARGET_DBFS]
                          [--quiet]
                          folder

Normalize all audio files in a folder.

positional arguments:
  folder                Folder to scan recursively.

options:
  -h, --help            show this help message and exit
  --ext EXT             File extension to include (repeatable).
  --target-dbfs TARGET_DBFS
                        Target peak dBFS (default: 0).
  --quiet
```
