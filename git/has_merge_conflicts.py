"""Check whether merging a source branch into a target would cause conflicts."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.path.append(str(Path(__file__).parent))
from get_repo_root import get_repo_root


def has_merge_conflicts(target: str, source: str, verbose: bool = False, repo_path: Path | None = None) -> bool:
	repo_path = repo_path or get_repo_root()
	if verbose:
		print(f"Checking for merge conflicts with {target} <- {source}")

	fast_result = _has_merge_conflicts_fast(target, source, repo_path, verbose)
	if fast_result is not None:
		return fast_result

	tmp_dir = tempfile.mkdtemp()

	try:
		subprocess.check_call(
			["git", "worktree", "add", "-d", tmp_dir, target],
			cwd=repo_path,
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
		)

		result = subprocess.run(
			["git", "merge", "--no-commit", "--no-ff", source],
			cwd=tmp_dir,
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
		)

		return result.returncode != 0

	finally:
		subprocess.run(["git", "merge", "--abort"], cwd=tmp_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		subprocess.run(
			["git", "worktree", "remove", tmp_dir, "--force"],
			cwd=repo_path,
			input="y\n",
			text=True,
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
		)
		shutil.rmtree(tmp_dir, ignore_errors=True)


def _has_merge_conflicts_fast(target: str, source: str, repo_path: Path, verbose: bool) -> bool | None:
	"""Fast conflict check via merge-tree. Returns None if merge-tree is unavailable or fails."""
	result = subprocess.run(
		[
			"git",
			"merge-tree",
			"--write-tree",
			"--messages",
			"--allow-unrelated-histories",
			target,
			source,
		],
		cwd=repo_path,
		capture_output=True,
		text=True,
	)

	output = (result.stdout or "") + (result.stderr or "")
	return "CONFLICT" in output


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Check whether merging a source branch into a target would cause conflicts.")
	parser.add_argument("target", help="Target branch to merge into.")
	parser.add_argument("source", help="Source branch to merge from.")
	parser.add_argument("--verbose", action="store_true", help="Print progress details.")
	args = parser.parse_args()

	conflicts = has_merge_conflicts(args.target, args.source, verbose=args.verbose)
	print("conflicts" if conflicts else "no_conflicts")
	raise SystemExit(0)
