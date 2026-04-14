# Usage
See [INDEX.md](./INDEX.md)

This folder and subfolders contain a bunch of `python` scripts and `bat` wrappers

Runing `python` scripts
```
python <script-path>.py [args]
```
Or using bat wrapper
```
<script-path> [args]
```

# Developing

## Index and Bat Wrappers
All scripts are to have `.bat` file wrappers and be in the `INDEX.md` file for their folder.

This is to be done by two scripts already present.
```
# CWD=<repo-root>

python generate_bat_wrappers.py --folder-recursive .
python .\generate_scripts_index.py --recursive 
```

## Reusability
All scripts reusable from command line, aside from where it would be redundant.

## Just Inputs and Outputs 
No system, every script takes inputs from command line.\
Any calls to other scripts are pure input-output.

## Communication Between Scripts
* While a script could use another through CLI (say with `subprocess`), it will import it as a python module.
* CWD is not guaranteed. Using import path hacks ("sys.path...") is OK.

## Script Format
* ONE public method (private prefixed with "_").
* File docstrings giving a brief outline. Should be same or similar to description given by --help
* Uses `argparse` for CLI args
* `if __name__ == "__main__":` block at end of file contains arg parsing and calling the public method
* Wherever appropriate, scripts have `--verbose` flag. Defaults to false.
* Scripts are minimal. Where appropriate, helpers are moved to new scripts.

### Method ordering
* Methods are ordered with most abstract first (the one with same name as file).
* Helper methods are placed directly after, in order of the line their call appears in caller method.
* Sub-helpers are ordered as closely to the above format without violating that of more abstract methods.

### Minimal Example
```python
"""Brief description here."""
import argparse


def script_template() -> int:
	return 0


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Brief description here.")
	parser.parse_args()
	raise SystemExit(script_template())
```

## Script Filenames
* Filename matches the public method.
* Name format consistent.

## Other
* Unit tests not required
* Platform assumed to be Windows 11
* git assumed to be on Path
* Python 3 assumed
* Scripts return code 0 on success.
* Scripts return error code after printing error.
* Output is deterministic. For example, lists are sorted appropriately (alphabetical or numeric if no other method makes sense).
