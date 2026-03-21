"""Get the root directory of the current git repository."""
import argparse
from pathlib import Path
import subprocess


def get_repo_root() -> Path:
	result = subprocess.run(
		["git", "rev-parse", "--show-toplevel"],
		capture_output=True,
		text=True,
		check=True
	)
	return Path(result.stdout.strip())


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Get the root directory of the current git repository.")
	parser.parse_args()
	print(get_repo_root())
