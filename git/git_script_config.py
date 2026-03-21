"""Local configuration for git helper scripts."""
import argparse
import json

MERGE_CHECK_TARGET = "dev"
ALWAYS_KEEP_BRANCHES = ["main", "dev"]


def git_script_config() -> dict[str, object]:
	return {
		"merge_check_target": MERGE_CHECK_TARGET,
		"always_keep_branches": list(ALWAYS_KEEP_BRANCHES),
	}


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Print git script configuration as JSON.")
	parser.parse_args()
	print(json.dumps(git_script_config(), indent=2))
