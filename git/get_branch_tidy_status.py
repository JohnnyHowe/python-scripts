"""Generate local git branch tidy status as comma-separated rows."""
from enum import Enum
from pathlib import Path
import argparse
import subprocess
import sys
from typing import Iterable

sys.path.append(str(Path(__file__).parent))

from get_branches_in_pull_request import get_branches_in_pull_request
from has_merge_conflicts import has_merge_conflicts
from get_repo_root import get_repo_root
from get_merge_status import get_push_status, MergeStatus
from get_all_branches import get_all_branches

try:
	from git_script_config import git_script_config
except ImportError:
	ALWAYS_KEEP_BRANCHES = []
	MERGE_CHECK_TARGET = None
else:
	_config = git_script_config()
	ALWAYS_KEEP_BRANCHES = _config.get("always_keep_branches", [])
	MERGE_CHECK_TARGET = _config.get("merge_check_target")


class BranchStatus(Enum):
	ALWAYS_KEEP = 0
	IN_PR = 1
	MERGED = 100
	READY_FOR_MERGE = 101
	MERGE_CONFLICTS = 102
	UNKNOWN = 999


def get_branch_tidy_status() -> Iterable[list[str | BranchStatus | MergeStatus]]:
	repo_root = get_repo_root()
	subprocess.run(["git", "-C", str(repo_root), "fetch"])

	branches = set(get_all_branches(repo_root))

	for status in BranchStatus:
		branches_with_status = list(_get_branches_with_status(branches, status))
		branches_with_status.sort()
		for branch in branches_with_status:
			branches.remove(branch)
			yield([branch, status, get_push_status(branch)])

	for branch in branches:
		yield [branch, BranchStatus.UNKNOWN, get_push_status(branch)]


def _get_branches_with_status(branches: list[str], status: BranchStatus) -> Iterable[str]:
	# Return none if UNKNOWN
	if status == BranchStatus.UNKNOWN:
		return

	# ALWAYS_KEEP?
	if status == BranchStatus.ALWAYS_KEEP:
		for branch in branches:
			if branch in ALWAYS_KEEP_BRANCHES:
				yield branch
		return
	
	# IN_PR?
	if status == BranchStatus.IN_PR:
		in_pr = get_branches_in_pull_request()
		for branch in branches:
			if branch in in_pr:
				yield branch
		return

	# MERGED, READY_FOR_MERGE, and MERGE_CONFLICTS from here on
	repo_root = get_repo_root()

	# If merge target then we can't check for target state
	if MERGE_CHECK_TARGET is None:
		return

	# MERGED
	if status == BranchStatus.MERGED:
		for branch in branches:
			if _is_merged(MERGE_CHECK_TARGET, branch, repo_root):
				yield branch
		return

	# READY FOR MERGE
	if status == BranchStatus.READY_FOR_MERGE:
		for branch in branches:
			if not has_merge_conflicts(MERGE_CHECK_TARGET, branch, repo_path=repo_root):
				yield branch
		return

	# MERGE_CONFLICTS?
	if status == BranchStatus.MERGE_CONFLICTS:
		for branch in branches:
			if has_merge_conflicts(MERGE_CHECK_TARGET, branch, repo_path=repo_root):
				yield branch
		return	
	

def _is_merged(target: str, source: str, repo_root: Path) -> bool:
	return subprocess.call(
		["git", "-C", str(repo_root), "merge-base", "--is-ancestor", source, target],
	) == 0


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Print branch tidy status as comma-separated rows.")
	parser.parse_args()

	for (branch, status, remote_status) in get_branch_tidy_status():
		print(",".join([branch, status.name, remote_status.name]))

	raise SystemExit(0)
