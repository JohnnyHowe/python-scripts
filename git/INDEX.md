This file was generated using the output of each script with "--help"
# check

## check_gh_auth.py
```text
usage: check_gh_auth.py [-h]

Check GitHub CLI availability and login status.

options:
  -h, --help  show this help message and exit
```

# delete

## delete_branches_already_merged.py
```text
usage: delete_branches_already_merged.py [-h] [--remote] [--ignore IGNORE]
                                         base_branch

Delete git branches already merged into a base branch.

positional arguments:
  base_branch      Base branch to check merged status against, e.g. dev or
                   main.

options:
  -h, --help       show this help message and exit
  --remote         Also delete merged remote branches.
  --ignore IGNORE  Branch name to ignore (can be repeated).
```

# ensure

## ensure_github_cli_is_authenticated.py
```text
usage: ensure_github_cli_is_authenticated.py [-h] [--verbose]

Check GitHub CLI availability and login status.

options:
  -h, --help  show this help message and exit
  --verbose   Print success details.
```

# get

## get_all_branches.py
```text
usage: get_all_branches.py [-h] [--local-only] [--keep-origin]

List all local and remote branches.

options:
  -h, --help     show this help message and exit
  --local-only   Only include local branches.
  --keep-origin  Keep the origin/ prefix on remote branches.
```

## get_branch_tidy_status.py
```text
usage: get_branch_tidy_status.py [-h]

Print branch tidy status as comma-separated rows.

options:
  -h, --help  show this help message and exit
```

## get_branch_tidy_status_pretty.py
```text
usage: get_branch_tidy_status_pretty.py [-h]

Summarize local git branches with merge and push status.

options:
  -h, --help  show this help message and exit
```

## get_branches_already_merged.py
```text
usage: get_branches_already_merged.py [-h] [--remotes] [--all] base_branch

List git branches already merged into a base branch.

positional arguments:
  base_branch  Base branch to check merged status against, e.g. dev or main.

options:
  -h, --help   show this help message and exit
  --remotes    Include remote branches.
  --all        Include both local and remote branches.
```

## get_branches_in_pull_request.py
```text
usage: get_branches_in_pull_request.py [-h]

Get branches relevant to the current pull request context.

options:
  -h, --help  show this help message and exit
```

## get_merge_status.py
```text
usage: get_merge_status.py [-h] branch_name

Compute ahead/behind status for a branch against its upstream.

positional arguments:
  branch_name  Local branch name to check.

options:
  -h, --help   show this help message and exit
```

## get_push_status.py
```text
usage: get_push_status.py [-h] branch_name

Compute ahead/behind status for a branch against its upstream.

positional arguments:
  branch_name  Local branch name to check.

options:
  -h, --help   show this help message and exit
```

## get_repo_root.py
```text
usage: get_repo_root.py [-h]

Get the root directory of the current git repository.

options:
  -h, --help  show this help message and exit
```

# git

## git_script_config.py
```text
usage: git_script_config.py [-h]

Print git script configuration as JSON.

options:
  -h, --help  show this help message and exit
```

# has

## has_merge_conflicts.py
```text
usage: has_merge_conflicts.py [-h] [--verbose] target source

Check whether merging a source branch into a target would cause conflicts.

positional arguments:
  target      Target branch to merge into.
  source      Source branch to merge from.

options:
  -h, --help  show this help message and exit
  --verbose   Print progress details.
```

# print

## print_table.py
```text
usage: print_table.py [-h] --headers HEADERS [--row ROW]

Print a simple text table.

options:
  -h, --help         show this help message and exit
  --headers HEADERS  Comma-separated header names.
  --row ROW          Comma-separated row values (repeatable).
```

# pull

## pull_all_remote_branches.py
```text
usage: pull_all_remote_branches.py [-h]

Fetch all remotes and create local tracking branches for any remote branches
that do not yet exist locally.

options:
  -h, --help  show this help message and exit
```

# remove

## remove_tracked_files_in_gitignore.py
```text
usage: remove_tracked_files_in_gitignore.py [-h] [--dry-run]

Remove tracked files that are ignored by .gitignore (keeps files on disk).

options:
  -h, --help  show this help message and exit
  --dry-run   List files but do not untrack them.
```
