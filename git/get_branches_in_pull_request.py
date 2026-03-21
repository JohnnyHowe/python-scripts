"""
Get branches relevant to the current pull request context.
"""
import argparse
import os
from pathlib import Path
import subprocess
import json
import sys

sys.path.append(str(Path(__file__).parent))
from ensure_github_cli_is_authenticated import ensure_github_cli_is_authenticated
from get_repo_root import get_repo_root


def get_branches_in_pull_request() -> list[str]:
	if ensure_github_cli_is_authenticated() != 0:
		print("Cannot continue without being logged into github cli")
		raise SystemExit(1)

	branches = []

	# GitHub Actions
	branches.extend(_get_env_pair("GITHUB_BASE_REF", "GITHUB_HEAD_REF"))

	branches = _dedupe_keep_order([branch for branch in branches if branch])
	if branches:
		return branches

	branches = _get_github_open_pr_branches()
	if branches:
		return branches

	repo_root = get_repo_root()
	current_branch = _get_current_branch(repo_root)
	return [current_branch] if current_branch else []


def _get_env_pair(base_key: str, head_key: str, strip_refs: bool = False) -> list[str]:
	base = os.environ.get(base_key, "").strip()
	head = os.environ.get(head_key, "").strip()
	if strip_refs:
		base = _strip_ref_prefix(base)
		head = _strip_ref_prefix(head)
	return [base, head]


def _strip_ref_prefix(value: str) -> str:
	if not value:
		return value
	for prefix in ("refs/heads/", "refs/"):
		if value.startswith(prefix):
			return value[len(prefix):]
	return value


def _dedupe_keep_order(values: list[str]) -> list[str]:
	seen = set()
	result = []
	for value in values:
		if not value:
			continue
		if value in seen:
			continue
		seen.add(value)
		result.append(value)
	return result


def _get_github_open_pr_branches() -> list[str]:
	repo_root = get_repo_root()
	if not _is_github_repo(repo_root):
		return []

	prs = _get_github_open_prs()
	if not prs:
		return []

	branches = []
	for pr in prs:
		base = (pr.get("baseRefName") or "").strip()
		head = (pr.get("headRefName") or "").strip()
		if base:
			branches.append(base)
		if head:
			branches.append(head)
	return _dedupe_keep_order(branches)


def _is_github_repo(repo_root: Path) -> bool:
	result = subprocess.run(
		["git", "-C", str(repo_root), "config", "--get", "remote.origin.url"],
		capture_output=True,
		text=True,
		check=False
	)
	url = result.stdout.strip().lower()
	return "github.com" in url


def _get_github_open_prs() -> list[dict]:
	# Prefer gh CLI if available (auth required).
	result = subprocess.run(
		["gh", "pr", "list", "--state", "open", "--json", "baseRefName,headRefName"],
		capture_output=True,
		text=True,
		check=False
	)
	if result.returncode == 0 and result.stdout.strip():
		try:
			return json.loads(result.stdout)
		except json.JSONDecodeError:
			return []
	return []


def _get_current_branch(repo_root: Path) -> str:
	result = subprocess.run(
		["git", "-C", str(repo_root), "rev-parse", "--abbrev-ref", "HEAD"],
		capture_output=True,
		text=True,
		check=False
	)
	branch = result.stdout.strip()
	if not branch or branch == "HEAD":
		return ""
	return branch


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Get branches relevant to the current pull request context.")
	parser.parse_args()

	for branch in get_branches_in_pull_request():
		print(branch)
