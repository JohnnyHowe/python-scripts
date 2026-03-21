from enum import Enum
import subprocess


class PushStatus(Enum):
	REMOTE_UP_TO_DATE = 0
	REMOTE_BEHIND = 1
	LOCAL_BEHIND = 2
	NOT_PUSHED = 3


def get_push_status(branch_name: str) -> PushStatus:
	if not _local_branch_exists(branch_name):
		return PushStatus.LOCAL_BEHIND

	upstream = _get_upstream(branch_name)
	if not upstream:
		return PushStatus.NOT_PUSHED

	behind, ahead = _get_ahead_behind(upstream, branch_name)
	if behind == 0 and ahead == 0:
		return PushStatus.REMOTE_UP_TO_DATE
	if behind == 0 and ahead > 0:
		return PushStatus.REMOTE_BEHIND
	if behind > 0 and ahead == 0:
		return PushStatus.LOCAL_BEHIND

	# Diverged: local and remote both have unique commits.
	return PushStatus.LOCAL_BEHIND


def _local_branch_exists(branch_name: str) -> bool:
	result = subprocess.run(
		["git", "show-ref", "--verify", f"refs/heads/{branch_name}"],
		capture_output=True,
		text=True,
		check=False
	)
	return result.returncode == 0


def _get_upstream(branch_name: str) -> str:
	result = subprocess.run(
		["git", "for-each-ref", "--format=%(upstream:short)", f"refs/heads/{branch_name}"],
		capture_output=True,
		text=True,
		check=False
	)
	return result.stdout.strip()


def _get_ahead_behind(upstream: str, branch_name: str) -> tuple[int, int]:
	result = subprocess.run(
		["git", "rev-list", "--left-right", "--count", f"{upstream}...{branch_name}"],
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
