"""
List all the git branches already merged.

Example usage:
python get_branches_already_merged.py dev
"""
import argparse
from pathlib import Path
import subprocess
import sys

sys.path.append(str(Path(__file__).parent))
from get_repo_root import get_repo_root


def get_branches_already_merged(
	base_branch: str,
	include_remotes: bool = False,
	include_all: bool = False,
) -> list[str]:
	repo_root = get_repo_root()
	_ensure_branch_exists(repo_root, base_branch)

	return _list_merged_branches(repo_root, base_branch, include_remotes, include_all)



def _ensure_branch_exists(repo_root: Path, branch_name: str) -> None:
	subprocess.run(
		["git", "-C", str(repo_root), "rev-parse", "--verify", branch_name],
		capture_output=True,
		text=True,
		check=True
	)


def _list_merged_branches(
	repo_root: Path,
	base_branch: str,
	include_remotes: bool,
	include_all: bool,
) -> list[str]:
	command = ["git", "-C", str(repo_root), "branch", "--merged", base_branch]
	if include_all:
		command.insert(4, "--all")
	elif include_remotes:
		command.insert(4, "--remotes")

	result = subprocess.run(command, capture_output=True, text=True, check=True)
	branches = []
	for line in result.stdout.splitlines():
		branch = line.replace("*", "").strip()
		if not branch:
			continue
		if branch == base_branch:
			continue
		if branch == "HEAD":
			continue
		if branch == "origin/HEAD":
			continue
		branches.append(branch)
	return branches


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="List git branches already merged into a base branch.")
	parser.add_argument("base_branch", help="Base branch to check merged status against, e.g. dev or main.")
	parser.add_argument("--remotes", action="store_true", help="Include remote branches.")
	parser.add_argument("--all", action="store_true", help="Include both local and remote branches.")
	args = parser.parse_args()

	for branch in get_branches_already_merged(
		base_branch=args.base_branch,
		include_remotes=args.remotes,
		include_all=args.all,
	):
		print(branch)
