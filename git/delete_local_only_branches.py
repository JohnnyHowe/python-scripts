"""Delete local Git branches that do not exist on any remote."""
import argparse
from pathlib import Path
import subprocess
import sys

sys.path.append(str(Path(__file__).parent))
from get_repo_root import get_repo_root


def delete_local_only_branches() -> int:
	repo_root = get_repo_root()
	_fetch_and_prune(repo_root)

	current_branch = _get_current_branch(repo_root)
	local_branches = _get_local_branches(repo_root)
	remote_branches = _get_remote_branch_names(repo_root)
	branches_to_delete = [
		branch
		for branch in local_branches
		if branch != current_branch and branch not in remote_branches
	]

	print("Local-only branches:")
	if not branches_to_delete:
		print("(none)")
		return 0

	for branch in branches_to_delete:
		print(branch)

	if not _confirm_delete(len(branches_to_delete)):
		return 0

	for branch in branches_to_delete:
		subprocess.run(
			["git", "-C", str(repo_root), "branch", "-D", branch],
			check=True,
		)
	return 0


def _fetch_and_prune(repo_root: Path) -> None:
	subprocess.run(
		["git", "-C", str(repo_root), "fetch", "--all", "--prune"],
		check=True,
	)


def _get_current_branch(repo_root: Path) -> str:
	result = subprocess.run(
		["git", "-C", str(repo_root), "branch", "--show-current"],
		capture_output=True,
		text=True,
		check=True,
	)
	return result.stdout.strip()


def _get_local_branches(repo_root: Path) -> list[str]:
	result = subprocess.run(
		["git", "-C", str(repo_root), "for-each-ref", "--format=%(refname:short)", "refs/heads"],
		capture_output=True,
		text=True,
		check=True,
	)
	return [branch for branch in result.stdout.splitlines() if branch]


def _get_remote_branch_names(repo_root: Path) -> set[str]:
	result = subprocess.run(
		[
			"git",
			"-C",
			str(repo_root),
			"for-each-ref",
			"--format=%(refname)",
			"refs/remotes",
		],
		capture_output=True,
		text=True,
		check=True,
	)

	branch_names = set()
	for ref_name in result.stdout.splitlines():
		parts = ref_name.split("/", 3)
		if len(parts) != 4 or parts[3] == "HEAD":
			continue
		branch_names.add(parts[3])
	return branch_names


def _confirm_delete(branch_count: int) -> bool:
	prompt = f"Permanently delete {branch_count} local-only branches? (y/N): "
	response = input(prompt).strip().lower()
	return response in ["y", "yes"]


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description="Delete local Git branches that do not exist on any remote."
	)
	parser.parse_args()
	raise SystemExit(delete_local_only_branches())
