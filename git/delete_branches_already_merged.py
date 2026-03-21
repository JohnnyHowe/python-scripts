"""
Similar to list_branches_already_merged.py.

Give this a branch name and it will list branches already merged.
Waits for user confirmation then deletes them locally.

If "--remote" is present, branches are also deleted on remote.

Example usage:
python delete_branches_already_merged.py dev --remote
"""
import argparse
from pathlib import Path
import subprocess
import sys

sys.path.append(str(Path(__file__).parent))
from get_repo_root import get_repo_root


def delete_branches_already_merged(
	base_branch: str,
	remote: bool = False,
	ignore_branches: list[str] | None = None,
) -> int:
	repo_root = get_repo_root()
	ignore_branches = ignore_branches or []
	_ensure_branch_exists(repo_root, base_branch)

	current_branch = _get_current_branch(repo_root)
	local_branches = _list_merged_local_branches(repo_root, base_branch, current_branch, ignore_branches)
	remote_branches = []
	if remote:
		remote_branches = _list_merged_remote_branches(repo_root, base_branch, current_branch, ignore_branches)

	print("Merged local branches:")
	if local_branches:
		for branch in local_branches:
			print(branch)
	else:
		print("(none)")

	if remote:
		print("")
		print("Merged remote branches:")
		if remote_branches:
			for branch in remote_branches:
				print(branch)
		else:
			print("(none)")

	if not local_branches and not remote_branches:
		return 0

	if not _confirm_delete(local_branches, remote_branches):
		return 0

	if local_branches:
		_delete_local_branches(repo_root, local_branches)
	if remote_branches:
		_delete_remote_branches(repo_root, remote_branches)
	return 0


def _ensure_branch_exists(repo_root: Path, branch_name: str) -> None:
	subprocess.run(
		["git", "-C", str(repo_root), "rev-parse", "--verify", branch_name],
		capture_output=True,
		text=True,
		check=True
	)


def _get_current_branch(repo_root: Path) -> str:
	result = subprocess.run(
		["git", "-C", str(repo_root), "rev-parse", "--abbrev-ref", "HEAD"],
		capture_output=True,
		text=True,
		check=True
	)
	return result.stdout.strip()


def _list_merged_local_branches(
	repo_root: Path,
	base_branch: str,
	current_branch: str,
	ignore_branches: list[str],
) -> list[str]:
	result = subprocess.run(
		["git", "-C", str(repo_root), "branch", "--merged", base_branch],
		capture_output=True,
		text=True,
		check=True
	)
	ignore_set = set(ignore_branches)
	branches = []
	for line in result.stdout.splitlines():
		branch = line.replace("*", "").strip()
		if not branch:
			continue
		if branch == base_branch:
			continue
		if branch == current_branch:
			continue
		if branch == "HEAD":
			continue
		if branch in ignore_set:
			continue
		branches.append(branch)
	return branches


def _list_merged_remote_branches(
	repo_root: Path,
	base_branch: str,
	current_branch: str,
	ignore_branches: list[str],
) -> list[str]:
	result = subprocess.run(
		["git", "-C", str(repo_root), "branch", "-r", "--merged", base_branch],
		capture_output=True,
		text=True,
		check=True
	)
	ignore_set = set(ignore_branches)
	branches = []
	for line in result.stdout.splitlines():
		branch = line.strip()
		if not branch:
			continue
		if "->" in branch:
			continue
		if branch.endswith("/HEAD"):
			continue
		remote, short_name = branch.split("/", 1)
		if short_name == base_branch:
			continue
		if short_name == current_branch:
			continue
		if short_name in ignore_set:
			continue
		branches.append(branch)
	return branches


def _confirm_delete(local_branches: list[str], remote_branches: list[str]) -> bool:
	local_count = len(local_branches)
	remote_count = len(remote_branches)
	if remote_count > 0 and local_count > 0:
		prompt = f"Delete {local_count} local and {remote_count} remote branches? (y/N): "
	elif remote_count > 0:
		prompt = f"Delete {remote_count} remote branches? (y/N): "
	else:
		prompt = f"Delete {local_count} local branches? (y/N): "
	response = input(prompt).strip().lower()
	return response in ["y", "yes"]


def _delete_local_branches(repo_root: Path, branches: list[str]) -> None:
	for branch in branches:
		subprocess.run(
			["git", "-C", str(repo_root), "branch", "-d", branch],
			check=False
		)


def _delete_remote_branches(repo_root: Path, branches: list[str]) -> None:
	for branch in branches:
		remote, short_name = branch.split("/", 1)
		subprocess.run(
			["git", "-C", str(repo_root), "push", remote, "--delete", short_name],
			check=False
		)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Delete git branches already merged into a base branch.")
	parser.add_argument("base_branch", help="Base branch to check merged status against, e.g. dev or main.")
	parser.add_argument("--remote", action="store_true", help="Also delete merged remote branches.")
	parser.add_argument("--ignore", action="append", default=[], help="Branch name to ignore (can be repeated).")
	args = parser.parse_args()

	raise SystemExit(
		delete_branches_already_merged(
			base_branch=args.base_branch,
			remote=args.remote,
			ignore_branches=args.ignore,
		)
	)
