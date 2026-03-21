"""
Fetch all remotes and create local tracking branches for any remote branches
that do not yet exist locally.

Example usage:
python pull_all_remote_branches.py
"""
import argparse
from pathlib import Path
import subprocess
import sys

sys.path.append(str(Path(__file__).parent))
from get_repo_root import get_repo_root


def pull_all_remote_branches() -> int:
	repo_root = get_repo_root()
	_fetch_all(repo_root)
	remote_branches = _get_remote_branches(repo_root)
	local_branches = _get_local_branches(repo_root)
	_create_missing_local_branches(repo_root, remote_branches, local_branches)
	return 0


def _fetch_all(repo_root: Path) -> None:
	subprocess.run(
		["git", "-C", str(repo_root), "fetch", "--all", "--prune"],
		check=True
	)


def _get_remote_branches(repo_root: Path) -> list[str]:
	result = subprocess.run(
		["git", "-C", str(repo_root), "branch", "-r"],
		capture_output=True,
		text=True,
		check=True
	)
	branches = []
	for line in result.stdout.splitlines():
		branch = line.strip()
		if not branch:
			continue
		if "->" in branch:
			continue
		if branch.endswith("/HEAD"):
			continue
		branches.append(branch)
	return branches


def _get_local_branches(repo_root: Path) -> set[str]:
	result = subprocess.run(
		["git", "-C", str(repo_root), "branch", "--format", "%(refname:short)"],
		capture_output=True,
		text=True,
		check=True
	)
	branches = set()
	for line in result.stdout.splitlines():
		branch = line.strip()
		if branch:
			branches.add(branch)
	return branches


def _create_missing_local_branches(repo_root: Path, remote_branches: list[str], local_branches: set[str]) -> None:
	for remote_branch in remote_branches:
		remote, branch = remote_branch.split("/", 1)
		if branch in local_branches:
			continue
		subprocess.run(
			["git", "-C", str(repo_root), "branch", "--track", branch, remote_branch],
			check=True
		)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Fetch all remotes and create local tracking branches for any remote branches that do not yet exist locally.")
	parser.parse_args()

	raise SystemExit(pull_all_remote_branches())
