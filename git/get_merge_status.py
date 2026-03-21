"""Compute ahead/behind status for a branch against its upstream."""
import argparse
from enum import Enum
from pathlib import Path
import subprocess
import sys

sys.path.append(str(Path(__file__).parent))
from get_repo_root import get_repo_root


class MergeStatus(Enum):
	REMOTE_UP_TO_DATE = 0
	REMOTE_BEHIND = 1
	LOCAL_BEHIND = 2
	NOT_PUSHED = 3


def get_push_status(branch_name: str, repo_root: Path | None = None) -> MergeStatus:
	repo_root = repo_root or get_repo_root()
	if not _local_branch_exists(branch_name, repo_root):
		return MergeStatus.LOCAL_BEHIND

	upstream = _get_upstream(branch_name, repo_root)
	if not upstream:
		return MergeStatus.NOT_PUSHED

	behind, ahead = _get_ahead_behind(upstream, branch_name, repo_root)
	if behind == 0 and ahead == 0:
		return MergeStatus.REMOTE_UP_TO_DATE
	if behind == 0 and ahead > 0:
		return MergeStatus.REMOTE_BEHIND
	if behind > 0 and ahead == 0:
		return MergeStatus.LOCAL_BEHIND

	# Diverged: local and remote both have unique commits.
	return MergeStatus.LOCAL_BEHIND


def _local_branch_exists(branch_name: str, repo_root: Path) -> bool:
	result = subprocess.run(
		["git", "-C", str(repo_root), "show-ref", "--verify", f"refs/heads/{branch_name}"],
		capture_output=True,
		text=True,
		check=False
	)
	return result.returncode == 0


def _get_upstream(branch_name: str, repo_root: Path) -> str:
	result = subprocess.run(
		["git", "-C", str(repo_root), "for-each-ref", "--format=%(upstream:short)", f"refs/heads/{branch_name}"],
		capture_output=True,
		text=True,
		check=False
	)
	return result.stdout.strip()


def _get_ahead_behind(upstream: str, branch_name: str, repo_root: Path) -> tuple[int, int]:
	result = subprocess.run(
		["git", "-C", str(repo_root), "rev-list", "--left-right", "--count", f"{upstream}...{branch_name}"],
		capture_output=True,
		text=True,
		check=False
	)
	if result.returncode != 0:
		return (0, 0)
	parts = result.stdout.strip().split()
	if len(parts) != 2:
		return (0, 0)
	return (int(parts[0]), int(parts[1]))


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Compute ahead/behind status for a branch against its upstream.")
	parser.add_argument("branch_name", help="Local branch name to check.")
	args = parser.parse_args()

	print(get_push_status(args.branch_name).name)
