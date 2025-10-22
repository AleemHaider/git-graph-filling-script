#!/usr/bin/env python3
"""
Realistic Commit Generator
Creates authentic-looking commits with varied messages and file changes
"""

import os
import subprocess
import random
import argparse
from datetime import datetime, timedelta

# Realistic commit message templates
COMMIT_TYPES = {
    'feat': [
        'add user authentication',
        'implement search functionality',
        'add pagination support',
        'create dashboard view',
        'add export feature',
        'implement notification system',
        'add user profile page',
        'create admin panel',
        'add file upload support',
        'implement dark mode',
    ],
    'fix': [
        'resolve memory leak issue',
        'correct validation logic',
        'handle edge case in parser',
        'resolve race condition',
        'fix null pointer exception',
        'correct timezone handling',
        'fix broken link',
        'resolve authentication bug',
        'fix responsive layout',
        'correct data formatting',
    ],
    'refactor': [
        'improve code structure',
        'optimize database queries',
        'clean up unused imports',
        'extract reusable components',
        'simplify conditional logic',
        'improve error handling',
        'reorganize project structure',
        'optimize algorithm performance',
        'update deprecated methods',
        'improve naming conventions',
    ],
    'docs': [
        'update README',
        'add API documentation',
        'improve code comments',
        'update installation guide',
        'add usage examples',
        'create contributing guide',
        'update changelog',
        'add architecture diagrams',
        'document configuration options',
        'improve inline documentation',
    ],
    'style': [
        'format code with prettier',
        'update color scheme',
        'improve button styling',
        'fix layout alignment',
        'update font styles',
        'improve responsive design',
        'add loading animations',
        'update UI components',
        'improve accessibility',
        'refine spacing and margins',
    ],
    'test': [
        'add unit tests for auth',
        'improve test coverage',
        'add integration tests',
        'fix failing tests',
        'add e2e tests',
        'update test fixtures',
        'add performance tests',
        'mock external services',
        'add validation tests',
        'improve test assertions',
    ],
    'chore': [
        'update dependencies',
        'configure CI/CD pipeline',
        'update build scripts',
        'clean up temporary files',
        'update gitignore',
        'configure linting rules',
        'update environment variables',
        'optimize bundle size',
        'update package versions',
        'configure docker setup',
    ],
}

# File types and realistic content
FILE_TYPES = {
    'src': ['index.js', 'App.js', 'utils.js', 'config.js', 'api.js', 'routes.js', 'middleware.js'],
    'components': ['Header.js', 'Footer.js', 'Sidebar.js', 'Card.js', 'Button.js', 'Modal.js'],
    'styles': ['main.css', 'variables.css', 'theme.css', 'responsive.css'],
    'tests': ['app.test.js', 'utils.test.js', 'api.test.js', 'integration.test.js'],
    'docs': ['README.md', 'CONTRIBUTING.md', 'API.md', 'CHANGELOG.md'],
    'config': ['.env.example', 'package.json', 'webpack.config.js', '.eslintrc.js'],
}


def run_command(command, cwd=None):
    """Execute a shell command"""
    result = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result


def create_realistic_file_structure(repo_path):
    """Create a realistic project structure"""
    for folder, files in FILE_TYPES.items():
        folder_path = os.path.join(repo_path, folder)
        os.makedirs(folder_path, exist_ok=True)

        for file in files:
            file_path = os.path.join(folder_path, file)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    f.write(f"// {file}\n// Created for project\n\n")


def get_random_commit_message():
    """Generate a realistic commit message"""
    commit_type = random.choice(list(COMMIT_TYPES.keys()))
    message = random.choice(COMMIT_TYPES[commit_type])
    return f"{commit_type}: {message}"


def modify_random_files(repo_path):
    """Modify random files to simulate real work"""
    num_files = random.randint(1, 4)
    modified_files = []

    for _ in range(num_files):
        folder = random.choice(list(FILE_TYPES.keys()))
        file = random.choice(FILE_TYPES[folder])
        file_path = os.path.join(repo_path, folder, file)

        # Ensure file exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Append realistic content
        with open(file_path, 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"\n// Updated: {timestamp}\n")
            f.write(f"// Changes: {random.choice(['Bug fix', 'Enhancement', 'Refactor', 'New feature'])}\n")

        modified_files.append(file_path)

    return modified_files


def create_realistic_commit(repo_path, date):
    """Create a commit that looks authentic"""
    # Modify random files
    modify_random_files(repo_path)

    # Get realistic commit message
    message = get_random_commit_message()

    # Add files
    run_command("git add .", cwd=repo_path)

    # Create commit with backdated timestamp
    date_str = date.strftime('%Y-%m-%d %H:%M:%S')
    commit_command = f'GIT_AUTHOR_DATE="{date_str}" GIT_COMMITTER_DATE="{date_str}" git commit -m "{message}"'
    result = run_command(commit_command, cwd=repo_path)

    return message, result.returncode == 0


def generate_realistic_activity(repo_path, start_date, end_date, min_commits=1,
                               max_commits=5, frequency=0.7, skip_weekends=True):
    """Generate realistic-looking activity"""
    current_date = start_date
    total_commits = 0

    print(f"\n{'='*60}")
    print("Generating Realistic Activity")
    print(f"{'='*60}")
    print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"Commits per day: {min_commits}-{max_commits}")
    print(f"Activity frequency: {frequency*100}%")
    print(f"Skip weekends: {skip_weekends}")
    print(f"{'='*60}\n")

    # Create realistic file structure
    print("Creating project structure...")
    create_realistic_file_structure(repo_path)
    run_command("git add .", cwd=repo_path)
    run_command('git commit -m "chore: initial project setup"', cwd=repo_path)
    print("✓ Project structure created\n")

    print("Generating commits...\n")

    while current_date <= end_date:
        # Skip weekends if enabled
        if skip_weekends and current_date.weekday() in [5, 6]:
            current_date += timedelta(days=1)
            continue

        # Randomly decide if we have activity on this day
        if random.random() < frequency:
            num_commits = random.randint(min_commits, max_commits)
            day_commits = []

            for i in range(num_commits):
                # Random time during work hours
                hour = random.randint(9, 20)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                commit_time = current_date.replace(hour=hour, minute=minute, second=second)

                message, success = create_realistic_commit(repo_path, commit_time)
                if success:
                    total_commits += 1
                    day_commits.append(message)

            if day_commits:
                print(f"[{current_date.strftime('%Y-%m-%d')}] {len(day_commits)} commit(s)")
                for msg in day_commits:
                    print(f"  • {msg}")

        current_date += timedelta(days=1)

    print(f"\n{'='*60}")
    print(f"✓ Created {total_commits} realistic commits")
    print(f"{'='*60}\n")


def setup_repository(repo_path, repo_name):
    """Initialize repository"""
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)

    if not os.path.exists(os.path.join(repo_path, ".git")):
        run_command("git init", cwd=repo_path)

        # Create README
        readme_path = os.path.join(repo_path, "README.md")
        with open(readme_path, "w") as f:
            f.write(f"# {repo_name}\n\n")
            f.write("A modern web application built with best practices.\n\n")
            f.write("## Features\n\n")
            f.write("- User authentication\n")
            f.write("- Responsive design\n")
            f.write("- RESTful API\n")
            f.write("- Unit tests\n\n")
            f.write("## Installation\n\n")
            f.write("```bash\nnpm install\nnpm start\n```\n")

        run_command("git add README.md", cwd=repo_path)
        run_command('git commit -m "docs: initial commit"', cwd=repo_path)


def main():
    parser = argparse.ArgumentParser(description="Generate realistic-looking GitHub activity")
    parser.add_argument("--repo-path", required=True, help="Local repository path")
    parser.add_argument("--repo-name", required=True, help="Repository name")
    parser.add_argument("--start-date", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument("--min-commits", type=int, default=1, help="Min commits per day")
    parser.add_argument("--max-commits", type=int, default=5, help="Max commits per day")
    parser.add_argument("--frequency", type=float, default=0.7, help="Activity frequency (0.0-1.0)")
    parser.add_argument("--include-weekends", action="store_true", help="Include weekends")

    args = parser.parse_args()

    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

    setup_repository(args.repo_path, args.repo_name)

    generate_realistic_activity(
        args.repo_path,
        start_date,
        end_date,
        args.min_commits,
        args.max_commits,
        args.frequency,
        skip_weekends=not args.include_weekends
    )


if __name__ == "__main__":
    main()
