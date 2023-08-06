import json
from argparse import ArgumentParser
from collections import defaultdict
from subprocess import run


def main() -> None:
    # Parse the arguments
    parser = ArgumentParser()
    parser.add_argument(
        "--repo", type=str, default=".", help="the path to the Git repository"
    )
    parser.add_argument(
        "--max", type=int, default=5, help="the max number of branches per contributor"
    )
    args = parser.parse_args()

    # Run the Git command and process the output
    run(
        "git fetch -p",
        check=True,
        shell=True,
        cwd=args.repo,
    )
    completed_process = run(
        'git for-each-ref --sort=authorname --format "%(authorname) %(refname)"',
        check=True,
        shell=True,
        cwd=args.repo,
        capture_output=True,
    )
    git_output = completed_process.stdout.decode().split("\n")

    # Filter the branches
    branch_lines = filter(lambda l: "refs/remotes" in l, git_output)
    branch_lines = filter(lambda l: "HEAD" not in l, branch_lines)
    branch_lines = filter(lambda l: "master" not in l, branch_lines)
    branch_lines = filter(lambda l: "release-" not in l, branch_lines)

    # Build the results map
    full_branch_map = defaultdict(list)
    for line in branch_lines:
        author, branch = line.split(" refs/remotes/origin/")
        full_branch_map[author].append(branch)
    branch_map = {
        author: branches
        for author, branches in full_branch_map.items()
        if len(branches) >= args.max
    }

    print(json.dumps(branch_map, indent=4, ensure_ascii=False))
