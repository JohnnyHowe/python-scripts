"""Summarize local git branches with merge and push status."""
import argparse
from pathlib import Path
import re
import sys

sys.path.append(str(Path(__file__).parent))
from get_merge_status import MergeStatus
from get_branch_tidy_status import BranchStatus, get_branch_tidy_status
from get_branch_tidy_status import MERGE_CHECK_TARGET
from get_all_branches import get_all_branches


def _colorize(text, color):
	return f"{_COLORS.get(color, '')}{text}{_COLORS['reset']}"


_COLORS = {
	"green": "\033[32m",
	"red": "\033[31m",
	"yellow": "\033[33m",
	"reset": "\033[0m",
}


_BRANCH_STATUS_STRINGS = {
	BranchStatus.ALWAYS_KEEP: _colorize("", "green"),
	BranchStatus.IN_PR: _colorize("Open PR", "green"),
	BranchStatus.MERGED: _colorize(f"Merged into {MERGE_CHECK_TARGET}", "yellow"),
	BranchStatus.READY_FOR_MERGE: _colorize(f"Ready for merge into {MERGE_CHECK_TARGET}", "yellow"),
	BranchStatus.MERGE_CONFLICTS: _colorize(f"Conflicts with {MERGE_CHECK_TARGET}", "red"),
	BranchStatus.UNKNOWN: _colorize("Unknown", "red"),
}


_MERGE_STATUS_STRINGS = {
	MergeStatus.REMOTE_UP_TO_DATE: _colorize("Up to date", "green"),
	MergeStatus.LOCAL_BEHIND: _colorize("Local behind remote", "red"),
	MergeStatus.REMOTE_BEHIND: _colorize("Remote behind local", "red"),
	MergeStatus.NOT_PUSHED: _colorize("Not pushed", "yellow"),
}

_SPACING = 1

HEADERS = ["Branch", "Status", "Remote"]

_ansi_re = re.compile(r'\x1b\[[0-9;]*m')


def get_git_tidy_status_pretty() -> int:
	column_widths = _get_column_widths()

	print(_render_row(HEADERS, column_widths))
	print(_render_row(["-" * width for width in column_widths], column_widths))

	for (branch, branch_status, merge_status) in get_branch_tidy_status():
		print(_render_row([branch, _BRANCH_STATUS_STRINGS.get(branch_status, branch_status.name), _MERGE_STATUS_STRINGS.get(merge_status, merge_status.name)], column_widths))


def _get_column_widths() -> list[int]:
	return [
		max([len(name) for name in get_all_branches()]),
		_get_max_len(BranchStatus, _BRANCH_STATUS_STRINGS),
		_get_max_len(MergeStatus, _MERGE_STATUS_STRINGS),
	]


def _get_max_len(enum, display_dict: dict) -> int:
	result = 0
	for item in enum:
		result = max(result, len(item.name))
	for item in display_dict.values():
		result = max(result, _get_visible_len(item))
	return result


def _render_row(row: list[str], column_widths: list[int]) -> str:
	if len(row) != len(column_widths):
		raise Exception("row length and colum_widths length differ!")

	items = []
	for i in range(len(row)):
		item: str = row[i]
		target_width = column_widths[i]
		padded = _pad_ansi_str(item, target_width)
		items.append(padded)

	spacer = " " * _SPACING

	inner = f"{spacer}|{spacer}".join(items)
	return f"|{spacer}{inner}{spacer}|"


def _pad_ansi_str(s: str, width: int) -> str:
    return s + ' ' * max(0, width - _get_visible_len(s))


def _get_visible_len(s: str) -> int:
	return len(_ansi_re.sub('', s))


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Summarize local git branches with merge and push status.")
	parser.parse_args()

	raise SystemExit(get_git_tidy_status_pretty())
