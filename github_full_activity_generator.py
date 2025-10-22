#!/usr/bin/env python3
"""
GitHub Full Activity Generator
Generates commits, issues, pull requests, and code reviews with backdated timestamps
"""

import os
import subprocess
import random
import argparse
from datetime import datetime, timedelta
from github import Github, GithubException
import time


def run_command(command, cwd=None):
    """Execute a shell command"""
    result = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    if result.returncode != 0 and "nothing to commit" not in result.stderr:
        print(f"Warning: {result.stderr}")
    return result


def create_commit(repo_path, date, commit_number):
    """Create a commit with a specific date"""
    file_path = os.path.join(repo_path, "activity.txt")
    with open(file_path, "a") as f:
        f.write(f"Commit on {date.strftime('%Y-%m-%d %H:%M:%S')}\n")

    date_str = date.strftime('%Y-%m-%d %H:%M:%S')
    run_command("git add .", cwd=repo_path)

    date_formatted = date.strftime('%Y-%m-%d')
    commit_command = f'GIT_AUTHOR_DATE="{date_str}" GIT_COMMITTER_DATE="{date_str}" git commit -m "Activity: {date_formatted}"'
    run_command(commit_command, cwd=repo_path)


def create_issue(github_client, repo_name, date, issue_number):
    """Create an issue (GitHub API doesn't support backdating, but we can create them)"""
    try:
        repo = github_client.get_repo(repo_name)

        titles = [
            f"Feature request: Add new functionality #{issue_number}",
            f"Bug: Fix issue in module #{issue_number}",
            f"Enhancement: Improve performance #{issue_number}",
            f"Documentation: Update README #{issue_number}",
            f"Refactor: Clean up code #{issue_number}",
        ]

        bodies = [
            f"Created on {date.strftime('%Y-%m-%d')}\n\nThis issue needs attention.",
            f"Issue details for {date.strftime('%Y-%m-%d')}.\n\nSteps to reproduce:\n1. Step one\n2. Step two",
            f"Suggested improvement for {date.strftime('%Y-%m-%d')}.",
        ]

        title = random.choice(titles)
        body = random.choice(bodies)

        issue = repo.create_issue(title=title, body=body)
        print(f"Created issue #{issue.number}: {title}")

        # Close some issues randomly
        if random.random() > 0.5:
            issue.edit(state='closed')
            print(f"  ↳ Closed issue #{issue.number}")

        return issue
    except GithubException as e:
        print(f"Error creating issue: {e}")
        return None


def create_pull_request(github_client, repo_name, repo_path, date, pr_number):
    """Create a pull request with commits"""
    try:
        repo = github_client.get_repo(repo_name)

        # Create a new branch
        branch_name = f"feature/update-{date.strftime('%Y%m%d')}-{pr_number}"

        # Create some commits in the branch
        run_command(f"git checkout -b {branch_name}", cwd=repo_path)

        # Make a change
        file_path = os.path.join(repo_path, f"feature_{pr_number}.txt")
        with open(file_path, "w") as f:
            f.write(f"Feature added on {date.strftime('%Y-%m-%d')}\n")

        date_str = date.strftime('%Y-%m-%d %H:%M:%S')
        run_command("git add .", cwd=repo_path)
        commit_command = f'GIT_AUTHOR_DATE="{date_str}" GIT_COMMITTER_DATE="{date_str}" git commit -m "Add feature {pr_number}"'
        run_command(commit_command, cwd=repo_path)

        # Push the branch
        run_command(f"git push origin {branch_name}", cwd=repo_path)

        # Create PR
        titles = [
            f"Feature: Add new functionality #{pr_number}",
            f"Fix: Resolve issue #{pr_number}",
            f"Update: Improve component #{pr_number}",
        ]

        title = random.choice(titles)
        body = f"Pull request created on {date.strftime('%Y-%m-%d')}\n\nChanges:\n- Added feature {pr_number}\n- Updated documentation"

        pr = repo.create_pull(
            title=title,
            body=body,
            head=branch_name,
            base="main"
        )
        print(f"Created PR #{pr.number}: {title}")

        # Merge some PRs randomly
        if random.random() > 0.3:
            time.sleep(2)  # Wait a bit before merging
            pr.merge()
            print(f"  ↳ Merged PR #{pr.number}")

        # Go back to main branch
        run_command("git checkout main", cwd=repo_path)

        return pr
    except GithubException as e:
        print(f"Error creating PR: {e}")
        run_command("git checkout main", cwd=repo_path)
        return None


def create_code_review(github_client, repo_name, pr):
    """Add review comments to a pull request"""
    try:
        if pr is None:
            return

        comments = [
            "LGTM! Great work on this.",
            "Looks good to me. Approved!",
            "Nice implementation. A few suggestions but overall good.",
            "This looks solid. Approved.",
        ]

        # Create a review
        pr.create_review(body=random.choice(comments), event='APPROVE')
        print(f"  ↳ Added code review to PR #{pr.number}")

    except GithubException as e:
        print(f"Error creating review: {e}")


def generate_full_activity(repo_path, github_client, repo_name, start_date, end_date,
                          min_commits=1, max_commits=5, frequency=0.7,
                          skip_weekends=True, create_issues_prs=True):
    """
    Generate full GitHub activity: commits, issues, PRs, and reviews
    """
    current_date = start_date
    total_commits = 0
    total_issues = 0
    total_prs = 0
    issue_counter = 1
    pr_counter = 1

    print(f"\nGenerating activity from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"Options: commits={min_commits}-{max_commits}, frequency={frequency*100}%, skip_weekends={skip_weekends}")
    print(f"GitHub features: issues & PRs = {create_issues_prs}\n")

    while current_date <= end_date:
        # Skip weekends if enabled
        if skip_weekends and current_date.weekday() in [5, 6]:
            current_date += timedelta(days=1)
            continue

        # Randomly decide if we have activity on this day
        if random.random() < frequency:
            day_str = current_date.strftime('%Y-%m-%d')

            # Create commits
            num_commits = random.randint(min_commits, max_commits)
            for i in range(num_commits):
                hour = random.randint(9, 22)
                minute = random.randint(0, 59)
                commit_time = current_date.replace(hour=hour, minute=minute)
                create_commit(repo_path, commit_time, i)
                total_commits += 1

            print(f"[{day_str}] Created {num_commits} commit(s)", end="")

            # Create issues (less frequently)
            if create_issues_prs and github_client and random.random() > 0.7:
                hour = random.randint(10, 18)
                minute = random.randint(0, 59)
                issue_time = current_date.replace(hour=hour, minute=minute)
                issue = create_issue(github_client, repo_name, issue_time, issue_counter)
                if issue:
                    total_issues += 1
                    issue_counter += 1
                    print(f", 1 issue", end="")

            # Create PRs (less frequently)
            if create_issues_prs and github_client and random.random() > 0.8:
                hour = random.randint(10, 18)
                minute = random.randint(0, 59)
                pr_time = current_date.replace(hour=hour, minute=minute)
                pr = create_pull_request(github_client, repo_name, repo_path, pr_time, pr_counter)
                if pr:
                    total_prs += 1
                    pr_counter += 1
                    print(f", 1 PR", end="")

                    # Add code review
                    if random.random() > 0.5:
                        create_code_review(github_client, repo_name, pr)

            print()  # New line

        current_date += timedelta(days=1)

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total commits: {total_commits}")
    print(f"Total issues: {total_issues}")
    print(f"Total PRs: {total_prs}")
    print(f"{'='*60}\n")


def setup_repository(repo_path, repo_name):
    """Initialize or use existing repository"""
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)
        print(f"Created directory: {repo_path}")

    if not os.path.exists(os.path.join(repo_path, ".git")):
        run_command("git init", cwd=repo_path)
        print("Initialized git repository")

        readme_path = os.path.join(repo_path, "README.md")
        with open(readme_path, "w") as f:
            f.write(f"# {repo_name}\n\nActivity tracking repository\n")

        run_command("git add README.md", cwd=repo_path)
        run_command('git commit -m "Initial commit"', cwd=repo_path)
    else:
        print("Using existing git repository")


def main():
    parser = argparse.ArgumentParser(
        description="Generate full GitHub activity: commits, issues, PRs, and reviews",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic commits only
  python github_full_activity_generator.py --start-date 2021-01-01 --end-date 2025-10-14

  # Full activity with issues and PRs (requires GitHub token)
  python github_full_activity_generator.py \\
    --start-date 2021-01-01 \\
    --end-date 2025-10-14 \\
    --github-token YOUR_TOKEN \\
    --repo-name username/repository \\
    --enable-issues-prs

Note: To create issues and PRs, you need a GitHub Personal Access Token
Create one at: https://github.com/settings/tokens
Permissions needed: repo (full control)
        """
    )

    parser.add_argument("--repo-path", default="./github-activity",
                        help="Path for the repository")
    parser.add_argument("--repo-name-local", default="github-activity",
                        help="Local repository name")
    parser.add_argument("--start-date", type=str, required=True,
                        help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=str, required=True,
                        help="End date (YYYY-MM-DD)")
    parser.add_argument("--min-commits", type=int, default=1,
                        help="Minimum commits per day")
    parser.add_argument("--max-commits", type=int, default=5,
                        help="Maximum commits per day")
    parser.add_argument("--frequency", type=float, default=0.7,
                        help="Activity probability (0.0-1.0)")
    parser.add_argument("--include-weekends", action="store_true",
                        help="Include Saturday and Sunday")
    parser.add_argument("--github-token", type=str,
                        help="GitHub Personal Access Token")
    parser.add_argument("--repo-name", type=str,
                        help="GitHub repo name (format: username/repository)")
    parser.add_argument("--enable-issues-prs", action="store_true",
                        help="Enable creating issues and PRs (requires token)")

    args = parser.parse_args()

    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

    print(f"\n{'='*60}")
    print("GitHub Full Activity Generator")
    print(f"{'='*60}")
    print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"Commits per day: {args.min_commits}-{args.max_commits}")
    print(f"Activity frequency: {args.frequency * 100}%")
    print(f"Skip weekends: {not args.include_weekends}")

    # Setup GitHub client if token provided
    github_client = None
    if args.github_token and args.enable_issues_prs:
        if not args.repo_name:
            print("\nError: --repo-name is required when using --enable-issues-prs")
            return
        try:
            github_client = Github(args.github_token)
            user = github_client.get_user()
            print(f"Authenticated as: {user.login}")
            print(f"Target repository: {args.repo_name}")
            print("Will create: commits, issues, PRs, and reviews")
        except Exception as e:
            print(f"GitHub authentication failed: {e}")
            print("Continuing with commits only...")
    else:
        print("GitHub features: commits only")

    print(f"{'='*60}\n")

    # Setup repository
    setup_repository(args.repo_path, args.repo_name_local)

    # Generate activity
    generate_full_activity(
        args.repo_path,
        github_client,
        args.repo_name,
        start_date,
        end_date,
        args.min_commits,
        args.max_commits,
        args.frequency,
        skip_weekends=not args.include_weekends,
        create_issues_prs=args.enable_issues_prs
    )

    print(f"\n{'='*60}")
    print("NEXT STEPS")
    print(f"{'='*60}")
    print("1. Push commits to GitHub:")
    print(f"   cd {args.repo_path}")
    print(f"   git remote add origin git@github.com:{args.repo_name}.git")
    print("   git branch -M main")
    print("   git push -u origin main --force")
    print("\n2. Check your GitHub profile contribution graph")
    print("   It will update within 30-60 minutes")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
