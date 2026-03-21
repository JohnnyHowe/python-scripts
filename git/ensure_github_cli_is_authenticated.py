#!/usr/bin/env python
"""Check GitHub CLI availability and login status."""
from __future__ import annotations

import argparse
import shutil
import subprocess


def ensure_github_cli_is_authenticated(verbose: bool = False) -> int:
	gh_path = shutil.which("gh")
	if not gh_path:
		print("GitHub CLI (gh) not found on PATH.")
		return 1

	result = subprocess.run(
		["gh", "auth", "status", "-h", "github.com"],
		stdout=subprocess.DEVNULL,
		stderr=subprocess.DEVNULL,
	)
	if result.returncode != 0:
		print("GitHub CLI found, but no user is logged in.")
		return 2

	if verbose:
		print("GitHub CLI authenticated.")

	return 0


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Check GitHub CLI availability and login status.")
	parser.add_argument("--verbose", action="store_true", help="Print success details.")
	args = parser.parse_args()

	raise SystemExit(ensure_github_cli_is_authenticated(verbose=args.verbose))
