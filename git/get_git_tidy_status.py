from enum import Enum
from pathlib import Path
import subprocess
import sys

sys.path.append(str(Path(__file__).parent))

from print_table import print_table
from get_branches_in_pull_request import get_branches_in_pull_request
from has_merge_conflicts import has_merge_conflicts
from get_repo_root import get_repo_root
from get_push_status import get_push_status, PushStatus

try:
	from git_script_config import *
except ImportError:
	ALWAYS_KEEP_BRANCHES = []
	MERGE_CHECK_TARGET = None	


class Status(Enum):
	ALWAYS_KEEP = 0
	IN_PR = 1
	MERGED_IN_TO_TARGET = 100
	READY_FOR_MERGE = 101
	MERGE_CONFLICTS = 102
	UNKNOWN = 999


def colorize(text, color):
    return f"{COLORS.get(color, '')}{text}{COLORS['reset']}"


COLORS = {
    "green": "\033[32m",
    "red": "\033[31m",
    "yellow": "\033[33m",
    "reset": "\033[0m",
}


STATUS_STRINGS = {
	Status.ALWAYS_KEEP: colorize("", "green"),
	Status.IN_PR: colorize("Open PR", "green"),
	Status.MERGED_IN_TO_TARGET: colorize(f"Merged into {MERGE_CHECK_TARGET}", "yellow"),
	Status.READY_FOR_MERGE: colorize(f"Ready for merge into {MERGE_CHECK_TARGET}", "yellow"),
	Status.MERGE_CONFLICTS: colorize(f"Conflicts with {MERGE_CHECK_TARGET}", "red"),
	Status.UNKNOWN: colorize(f"Unknown", "red"),
}


PUSH_STATUS_STRINGS = {
	PushStatus.REMOTE_UP_TO_DATE: colorize("Up to date", "green"),
	PushStatus.LOCAL_BEHIND: colorize("Local behind remote", "red"),
	PushStatus.REMOTE_BEHIND: colorize("Remote behind local", "red"),
	PushStatus.NOT_PUSHED: colorize("Not pushed", "yellow"),
}


def main():
	subprocess.run("git fetch".split(" "))

	all_branches = _get_all_branches()
	in_pr = get_branches_in_pull_request()

	rows = []
	for branch in all_branches:
		rows.append([branch, _get_status(branch, in_pr), get_push_status(branch)])

	rows.sort(key=lambda row: row[0])
	rows.sort(key=lambda row: row[1].value)

	rows_status_str = []
	for row in rows:
		row_copy = list(row)
		row_copy[1] = STATUS_STRINGS[row_copy[1]] 
		row_copy[2] = PUSH_STATUS_STRINGS[row_copy[2]] 
		rows_status_str.append(row_copy)

	print()
	print_table(["Branch", "Status", "Remote"], rows_status_str)


def _get_all_branches(strip_origin=True) -> set[str]:
	result = subprocess.run(
		["git", "for-each-ref", "--format='%(refname:short)'", "refs/heads", "refs/remotes"],
		capture_output=True,
		text=True,
		check=False
	)

	branches = result.stdout.strip().splitlines()
	branches = [branch.removesuffix("'").removeprefix("'") for branch in branches]

	if strip_origin:
		branches = [branch.removeprefix("origin/") for branch in branches]
	
	branches = [branch for branch in branches if branch != "origin"]
	return set(branches)


def _get_status(branch_name: str, branches_in_pr: list[str]) -> Status:
	if branch_name in ALWAYS_KEEP_BRANCHES:
		return Status.ALWAYS_KEEP

	if branch_name in branches_in_pr:
		return Status.IN_PR

	if not MERGE_CHECK_TARGET is None:
		if _is_merged(MERGE_CHECK_TARGET, branch_name):
			return Status.MERGED_IN_TO_TARGET

		return Status.MERGE_CONFLICTS if has_merge_conflicts(MERGE_CHECK_TARGET, branch_name) else Status.READY_FOR_MERGE
	
	return Status.UNKNOWN


def _is_merged(target, source):
    return subprocess.call(
        ["git", "merge-base", "--is-ancestor", source, target],
        cwd=get_repo_root()
    ) == 0


if __name__ == "__main__":
	main()
