#!/usr/bin/env python
"""Check GitHub CLI availability and login status."""

from __future__ import annotations

import shutil
import subprocess


def check_gh_auth() -> int:
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

	return 0


if __name__ == "__main__":
	raise SystemExit(check_gh_auth())
