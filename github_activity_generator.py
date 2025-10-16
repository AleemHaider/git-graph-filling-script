#!/usr/bin/env python3
"""
GitHub Activity Generator
Creates backdated commits to fill GitHub contribution graph
"""

import os
import subprocess
import random
from datetime import datetime, timedelta
import argparse


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
    # Create or modify a file
    file_path = os.path.join(repo_path, "activity.txt")
    with open(file_path, "a") as f:
        f.write(f"Commit on {date.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Set the date for the commit
    date_str = date.strftime('%Y-%m-%d %H:%M:%S')

    # Add and commit with backdated timestamp
    run_command("git add .", cwd=repo_path)

    date_formatted = date.strftime('%Y-%m-%d')
    commit_command = f'GIT_AUTHOR_DATE="{date_str}" GIT_COMMITTER_DATE="{date_str}" git commit -m "Activity: {date_formatted}"'
    run_command(commit_command, cwd=repo_path)


def generate_activity(repo_path, start_date, end_date, min_commits=1, max_commits=5, frequency=0.7, skip_weekends=True):
    """
    Generate commits for a date range

    Args:
        repo_path: Path to the git repository
        start_date: Start date for commits
        end_date: End date for commits
        min_commits: Minimum commits per day
        max_commits: Maximum commits per day
        frequency: Probability of having commits on a given day (0.0 to 1.0)
        skip_weekends: Skip Saturday and Sunday if True
    """
    current_date = start_date
    total_commits = 0

    while current_date <= end_date:
        # Skip weekends if enabled (Saturday=5, Sunday=6)
        if skip_weekends and current_date.weekday() in [5, 6]:
            current_date += timedelta(days=1)
            continue

        # Randomly decide if we commit on this day
        if random.random() < frequency:
            # Random number of commits for this day
            num_commits = random.randint(min_commits, max_commits)

            for i in range(num_commits):
                # Random time during the day
                hour = random.randint(9, 22)
                minute = random.randint(0, 59)
                commit_time = current_date.replace(hour=hour, minute=minute)

                create_commit(repo_path, commit_time, i)
                total_commits += 1

            print(f"Created {num_commits} commit(s) for {current_date.strftime('%Y-%m-%d')}")

        current_date += timedelta(days=1)

    print(f"\nTotal commits created: {total_commits}")


def setup_repository(repo_path, repo_name):
    """Initialize or use existing repository"""
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)
        print(f"Created directory: {repo_path}")

    # Initialize git repo if not already initialized
    if not os.path.exists(os.path.join(repo_path, ".git")):
        run_command("git init", cwd=repo_path)
        print("Initialized git repository")

        # Create initial README
        readme_path = os.path.join(repo_path, "README.md")
        with open(readme_path, "w") as f:
            f.write(f"# {repo_name}\n\nActivity tracking repository\n")

        run_command("git add README.md", cwd=repo_path)
        run_command('git commit -m "Initial commit"', cwd=repo_path)
    else:
        print("Using existing git repository")


def main():
    parser = argparse.ArgumentParser(
        description="Generate GitHub activity with backdated commits",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fill last 6 months with activity
  python github_activity_generator.py --days 180

  # Fill specific date range
  python github_activity_generator.py --start-date 2021-01-01 --end-date 2025-10-14

  # More aggressive activity pattern
  python github_activity_generator.py --days 365 --min-commits 3 --max-commits 10 --frequency 0.9

  # Include weekends
  python github_activity_generator.py --days 365 --include-weekends

  # After generating commits, push to GitHub:
  cd github-activity
  git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
  git branch -M main
  git push -u origin main --force
        """
    )

    parser.add_argument("--repo-path", default="./github-activity",
                        help="Path for the repository (default: ./github-activity)")
    parser.add_argument("--repo-name", default="github-activity",
                        help="Repository name (default: github-activity)")
    parser.add_argument("--days", type=int,
                        help="Number of days back from today to generate activity")
    parser.add_argument("--start-date", type=str,
                        help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=str,
                        help="End date (YYYY-MM-DD, default: today)")
    parser.add_argument("--min-commits", type=int, default=1,
                        help="Minimum commits per day (default: 1)")
    parser.add_argument("--max-commits", type=int, default=5,
                        help="Maximum commits per day (default: 5)")
    parser.add_argument("--frequency", type=float, default=0.7,
                        help="Probability of activity on a given day, 0.0-1.0 (default: 0.7)")
    parser.add_argument("--include-weekends", action="store_true",
                        help="Include Saturday and Sunday (default: skip weekends)")

    args = parser.parse_args()

    # Determine date range
    end_date = datetime.now().replace(hour=23, minute=59, second=59)
    if args.end_date:
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

    if args.start_date:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    elif args.days:
        start_date = end_date - timedelta(days=args.days)
    else:
        # Default to last 365 days
        start_date = end_date - timedelta(days=365)

    print(f"GitHub Activity Generator")
    print(f"========================")
    print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"Commits per day: {args.min_commits}-{args.max_commits}")
    print(f"Activity frequency: {args.frequency * 100}%")
    print(f"Skip weekends: {not args.include_weekends}")
    print(f"Repository: {args.repo_path}\n")

    # Setup repository
    setup_repository(args.repo_path, args.repo_name)

    # Generate activity
    generate_activity(
        args.repo_path,
        start_date,
        end_date,
        args.min_commits,
        args.max_commits,
        args.frequency,
        skip_weekends=not args.include_weekends
    )

    print(f"\n{'='*60}")
    print("NEXT STEPS:")
    print(f"{'='*60}")
    print(f"1. Create a new repository on GitHub named '{args.repo_name}'")
    print(f"2. Run these commands:")
    print(f"   cd {args.repo_path}")
    print(f"   git remote add origin https://github.com/YOUR_USERNAME/{args.repo_name}.git")
    print(f"   git branch -M main")
    print(f"   git push -u origin main --force")
    print(f"\nYour GitHub contribution graph will be updated shortly after pushing!")


if __name__ == "__main__":
    main()
