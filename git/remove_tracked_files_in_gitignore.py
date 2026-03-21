"""
Removes all the tracked files from the repo that are caught by .gitignore.
Does not mess with submodules.
Keeps untracked files on disk.
"""

from __future__ import annotations

import argparse
import os
import subprocess
from typing import Iterable, List


def run_git(args: List[str], cwd: str, input_bytes: bytes | None = None) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace")
        raise RuntimeError(f"git {' '.join(args)} failed: {stderr.strip()}")
    return result.stdout


def run_git_allow_exit_codes(
    args: List[str], cwd: str, input_bytes: bytes | None, allowed_exit_codes: Iterable[int]
) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode not in allowed_exit_codes:
        stderr = result.stderr.decode("utf-8", errors="replace")
        raise RuntimeError(f"git {' '.join(args)} failed: {stderr.strip()}")
    return result


def get_repo_root() -> str:
    output = run_git(["rev-parse", "--show-toplevel"], cwd=os.getcwd())
    return output.decode("utf-8", errors="replace").strip()


def get_tracked_files(repo_root: str) -> List[str]:
    output = run_git(["ls-files", "-z"], cwd=repo_root)
    if not output:
        return []
    return [p for p in output.decode("utf-8", errors="replace").split("\0") if p]


def get_submodule_paths(repo_root: str) -> List[str]:
    gitmodules_path = os.path.join(repo_root, ".gitmodules")
    if not os.path.exists(gitmodules_path):
        return []

    try:
        output = run_git(["config", "-f", ".gitmodules", "--get-regexp", "path"], cwd=repo_root)
    except RuntimeError:
        # If git config fails, fall back to no submodules to avoid blocking.
        return []

    lines = output.decode("utf-8", errors="replace").splitlines()
    paths: List[str] = []
    for line in lines:
        # Format: "submodule.<name>.path <path>"
        parts = line.strip().split(None, 1)
        if len(parts) == 2:
            paths.append(parts[1])
    return paths


def filter_out_submodules(paths: Iterable[str], submodules: Iterable[str]) -> List[str]:
    submodule_prefixes = [p.rstrip("/") + "/" for p in submodules]
    filtered: List[str] = []
    for path in paths:
        if path in submodules:
            continue
        if any(path.startswith(prefix) for prefix in submodule_prefixes):
            continue
        filtered.append(path)
    return filtered


def get_ignored_tracked_files(repo_root: str) -> List[str]:
    # List tracked files that are ignored by standard ignore rules.
    output = run_git(["ls-files", "-ci", "--exclude-standard", "-z"], cwd=repo_root)
    if not output:
        return []
    return [p for p in output.decode("utf-8", errors="replace").split("\0") if p]


def chunked(items: List[str], size: int) -> Iterable[List[str]]:
    for i in range(0, len(items), size):
        yield items[i : i + size]


def remove_from_index(repo_root: str, paths: List[str], dry_run: bool) -> None:
    if dry_run:
        return
    for batch in chunked(paths, 200):
        run_git(["rm", "--cached", "--", *batch], cwd=repo_root)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remove tracked files that are ignored by .gitignore (keeps files on disk)."
    )
    parser.add_argument("--dry-run", action="store_true", help="List files but do not untrack them.")
    args = parser.parse_args()

    repo_root = get_repo_root()
    ignored = get_ignored_tracked_files(repo_root)
    submodules = get_submodule_paths(repo_root)
    ignored = filter_out_submodules(ignored, submodules)

    if not ignored:
        print("No tracked files are ignored by .gitignore.")
        return 0

    for path in ignored:
        print(path)

    remove_from_index(repo_root, ignored, args.dry_run)

    if args.dry_run:
        print(f"\nDry run: {len(ignored)} file(s) would be untracked.")
    else:
        print(f"\nUntracked {len(ignored)} file(s) (kept on disk).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
