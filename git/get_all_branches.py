"""List all local and remote branches."""
import argparse
from pathlib import Path
import subprocess
import sys

sys.path.append(str(Path(__file__).parent))
from get_repo_root import get_repo_root


def get_all_branches(
	include_remotes: bool = True,
	strip_origin: bool = True,
) -> list[str]:
	repo_root = get_repo_root()
	branches = _list_branches(repo_root, include_remotes)
	branches = _strip_quotes(branches)

	if strip_origin:
		branches = [branch.removeprefix("origin/") for branch in branches]

	branches = [branch for branch in branches if branch != "origin"]
	return sorted(set(branches))


def _list_branches(repo_root: Path, include_remotes: bool) -> list[str]:
	refs = ["refs/heads"]
	if include_remotes:
		refs.append("refs/remotes")

	result = subprocess.run(
		["git", "-C", str(repo_root), "for-each-ref", "--format='%(refname:short)'", *refs],
		capture_output=True,
		text=True,
		check=False
	)
	return result.stdout.strip().splitlines()


def _strip_quotes(branches: list[str]) -> list[str]:
	return [branch.removesuffix("'").removeprefix("'") for branch in branches]


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="List all local and remote branches.")
	parser.add_argument(
		"--local-only",
		action="store_true",
		help="Only include local branches.",
	)
	parser.add_argument(
		"--keep-origin",
		action="store_true",
		help="Keep the origin/ prefix on remote branches.",
	)
	args = parser.parse_args()

	for branch in get_all_branches(
		include_remotes=not args.local_only,
		strip_origin=not args.keep_origin,
	):
		print(branch)
