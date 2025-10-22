#!/usr/bin/env python3
"""
Realistic Project History Generator
Takes an existing project and creates a realistic git history with backdated commits
Simulates natural development: initial setup, features, bug fixes, refactoring, etc.
"""

import os
import subprocess
import random
import argparse
import shutil
from datetime import datetime, timedelta
from pathlib import Path


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


def get_file_list(source_dir, exclude_patterns=None):
    """Get all files from source directory, excluding patterns"""
    if exclude_patterns is None:
        exclude_patterns = ['.git', 'node_modules', '__pycache__', '.env', 'venv', 'dist', 'build']

    files = []
    for root, dirs, filenames in os.walk(source_dir):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_patterns]

        for filename in filenames:
            file_path = os.path.join(root, filename)
            rel_path = os.path.relpath(file_path, source_dir)

            # Skip excluded patterns
            if any(pattern in rel_path for pattern in exclude_patterns):
                continue

            files.append((file_path, rel_path))

    return files


def categorize_files(files):
    """Categorize files by type for logical grouping"""
    categories = {
        'config': [],       # Config files
        'docs': [],         # Documentation
        'core': [],         # Core functionality
        'models': [],       # Models/schemas
        'views': [],        # Views/templates
        'controllers': [],  # Controllers/routes
        'api': [],          # API files
        'utils': [],        # Utilities
        'tests': [],        # Tests
        'assets': [],       # Static assets
        'styles': [],       # CSS/styling
        'other': []         # Everything else
    }

    for file_path, rel_path in files:
        lower_path = rel_path.lower()

        if any(x in lower_path for x in ['package.json', 'requirements.txt', 'setup.py', 'config', '.json', '.yaml', '.yml', '.env.example']):
            categories['config'].append((file_path, rel_path))
        elif any(x in lower_path for x in ['readme', 'docs/', 'documentation', '.md']):
            categories['docs'].append((file_path, rel_path))
        elif any(x in lower_path for x in ['model', 'schema', 'entity']):
            categories['models'].append((file_path, rel_path))
        elif any(x in lower_path for x in ['view', 'template', 'component', 'page']):
            categories['views'].append((file_path, rel_path))
        elif any(x in lower_path for x in ['controller', 'route', 'router', 'handler']):
            categories['controllers'].append((file_path, rel_path))
        elif any(x in lower_path for x in ['api', 'endpoint', 'service']):
            categories['api'].append((file_path, rel_path))
        elif any(x in lower_path for x in ['util', 'helper', 'lib']):
            categories['utils'].append((file_path, rel_path))
        elif any(x in lower_path for x in ['test', 'spec', '__tests__']):
            categories['tests'].append((file_path, rel_path))
        elif any(x in lower_path for x in ['.css', '.scss', '.sass', 'styles']):
            categories['styles'].append((file_path, rel_path))
        elif any(x in lower_path for x in ['static', 'public', 'assets', 'images', 'img']):
            categories['assets'].append((file_path, rel_path))
        elif any(x in lower_path for x in ['main', 'index', 'app', '__init__']):
            categories['core'].append((file_path, rel_path))
        else:
            categories['other'].append((file_path, rel_path))

    return categories


def create_commit(repo_path, date, message, files_to_add=None):
    """Create a commit with specific date and files"""
    if files_to_add:
        for file_src, file_rel in files_to_add:
            dest_path = os.path.join(repo_path, file_rel)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(file_src, dest_path)

    date_str = date.strftime('%Y-%m-%d %H:%M:%S')
    run_command("git add .", cwd=repo_path)

    commit_command = f'GIT_AUTHOR_DATE="{date_str}" GIT_COMMITTER_DATE="{date_str}" git commit -m "{message}"'
    result = run_command(commit_command, cwd=repo_path)

    return result.returncode == 0


def generate_commit_messages(category, files):
    """Generate realistic commit messages for file category"""
    messages = {
        'config': [
            "chore: setup project configuration",
            "chore: add project dependencies",
            "chore: configure build system",
            "chore: update project settings",
        ],
        'docs': [
            "docs: add README and documentation",
            "docs: update project documentation",
            "docs: add API documentation",
            "docs: improve setup instructions",
        ],
        'core': [
            "feat: implement core functionality",
            "feat: add main application logic",
            "feat: setup application entry point",
            "refactor: improve core architecture",
        ],
        'models': [
            "feat: add data models",
            "feat: implement database schemas",
            "feat: add entity definitions",
            "refactor: improve data structures",
        ],
        'views': [
            "feat: add user interface components",
            "feat: implement view templates",
            "feat: add page layouts",
            "style: improve UI components",
        ],
        'controllers': [
            "feat: add route handlers",
            "feat: implement controllers",
            "feat: add request handling",
            "refactor: improve routing logic",
        ],
        'api': [
            "feat: add API endpoints",
            "feat: implement REST services",
            "feat: add API integration",
            "fix: improve API error handling",
        ],
        'utils': [
            "feat: add utility functions",
            "feat: implement helper methods",
            "refactor: extract common utilities",
            "chore: add utility libraries",
        ],
        'tests': [
            "test: add unit tests",
            "test: add integration tests",
            "test: improve test coverage",
            "test: add test fixtures",
        ],
        'styles': [
            "style: add styling",
            "style: improve CSS",
            "style: add responsive design",
            "style: update theme",
        ],
        'assets': [
            "chore: add static assets",
            "chore: add images and icons",
            "chore: update assets",
        ],
        'other': [
            "feat: add additional features",
            "chore: add miscellaneous files",
            "refactor: code improvements",
        ]
    }

    return random.choice(messages.get(category, messages['other']))


def generate_realistic_history(source_dir, repo_path, start_date, end_date,
                               project_name, skip_weekends=True):
    """Generate realistic project history"""

    print(f"\n{'='*60}")
    print(f"Analyzing project: {source_dir}")
    print(f"{'='*60}")

    # Get and categorize files
    all_files = get_file_list(source_dir)
    print(f"Found {len(all_files)} files")

    categories = categorize_files(all_files)

    print("\nFile categories:")
    for cat, files in categories.items():
        if files:
            print(f"  {cat}: {len(files)} files")

    # Setup repository
    print(f"\n{'='*60}")
    print("Setting up repository")
    print(f"{'='*60}")

    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    os.makedirs(repo_path)

    run_command("git init", cwd=repo_path)
    print("✓ Initialized git repository")

    # Create commit plan
    commit_plan = []

    # Phase 1: Initial setup (Day 1)
    phase_date = start_date
    commit_plan.append({
        'date': phase_date,
        'message': f"feat: initial project setup for {project_name}",
        'files': categories['config'][:3] if categories['config'] else []
    })

    # Phase 2: Documentation (Day 2-3)
    phase_date += timedelta(days=random.randint(1, 2))
    if categories['docs']:
        commit_plan.append({
            'date': phase_date,
            'message': "docs: add project documentation",
            'files': categories['docs']
        })

    # Phase 3: Core structure (Week 1)
    phase_date += timedelta(days=random.randint(1, 3))
    if categories['models']:
        commit_plan.append({
            'date': phase_date,
            'message': "feat: add data models and schemas",
            'files': categories['models']
        })

    # Phase 4: Core functionality (Week 1-2)
    phase_date += timedelta(days=random.randint(2, 4))
    if categories['core']:
        for i in range(0, len(categories['core']), 3):
            batch = categories['core'][i:i+3]
            commit_plan.append({
                'date': phase_date,
                'message': "feat: implement core application logic",
                'files': batch
            })
            phase_date += timedelta(days=random.randint(1, 2))

    # Phase 5: Controllers/Routes (Week 2-3)
    if categories['controllers']:
        for i in range(0, len(categories['controllers']), 2):
            batch = categories['controllers'][i:i+2]
            commit_plan.append({
                'date': phase_date,
                'message': "feat: add route handlers and controllers",
                'files': batch
            })
            phase_date += timedelta(days=random.randint(1, 3))

    # Phase 6: API endpoints (Week 3-4)
    if categories['api']:
        for i in range(0, len(categories['api']), 2):
            batch = categories['api'][i:i+2]
            commit_plan.append({
                'date': phase_date,
                'message': "feat: implement API endpoints",
                'files': batch
            })
            phase_date += timedelta(days=random.randint(1, 2))

    # Phase 7: Views/UI (Week 4-6)
    if categories['views']:
        for i in range(0, len(categories['views']), 4):
            batch = categories['views'][i:i+4]
            commit_plan.append({
                'date': phase_date,
                'message': "feat: add user interface components",
                'files': batch
            })
            phase_date += timedelta(days=random.randint(2, 4))

    # Phase 8: Styling (Week 6-7)
    if categories['styles']:
        commit_plan.append({
            'date': phase_date,
            'message': "style: add styling and improve UI",
            'files': categories['styles']
        })
        phase_date += timedelta(days=random.randint(2, 3))

    # Phase 9: Assets (Week 7)
    if categories['assets']:
        commit_plan.append({
            'date': phase_date,
            'message': "chore: add static assets and resources",
            'files': categories['assets']
        })
        phase_date += timedelta(days=random.randint(1, 2))

    # Phase 10: Utils (Week 8)
    if categories['utils']:
        commit_plan.append({
            'date': phase_date,
            'message': "feat: add utility functions and helpers",
            'files': categories['utils']
        })
        phase_date += timedelta(days=random.randint(1, 3))

    # Phase 11: Tests (Week 9)
    if categories['tests']:
        commit_plan.append({
            'date': phase_date,
            'message': "test: add unit and integration tests",
            'files': categories['tests']
        })
        phase_date += timedelta(days=random.randint(2, 4))

    # Phase 12: Remaining files (Week 10)
    if categories['other']:
        for i in range(0, len(categories['other']), 5):
            batch = categories['other'][i:i+5]
            commit_plan.append({
                'date': phase_date,
                'message': "feat: add additional features and improvements",
                'files': batch
            })
            phase_date += timedelta(days=random.randint(1, 2))

    # Phase 13: Remaining config
    if len(categories['config']) > 3:
        commit_plan.append({
            'date': phase_date,
            'message': "chore: finalize project configuration",
            'files': categories['config'][3:]
        })
        phase_date += timedelta(days=1)

    # Phase 14: Bug fixes and refinements (spread over time)
    refinement_messages = [
        "fix: resolve bugs and issues",
        "refactor: improve code quality",
        "fix: enhance error handling",
        "refactor: optimize performance",
        "fix: address edge cases",
        "docs: update documentation",
        "chore: update dependencies",
    ]

    # Add refinement commits throughout the timeline
    while phase_date < end_date:
        phase_date += timedelta(days=random.randint(3, 7))
        if phase_date > end_date:
            break

        commit_plan.append({
            'date': phase_date,
            'message': random.choice(refinement_messages),
            'files': []  # Empty commits for fixes/refactoring
        })

    # Execute commit plan
    print(f"\n{'='*60}")
    print(f"Creating {len(commit_plan)} commits")
    print(f"{'='*60}\n")

    successful_commits = 0

    for i, commit_info in enumerate(commit_plan, 1):
        commit_date = commit_info['date']

        # Skip weekends if enabled
        if skip_weekends and commit_date.weekday() in [5, 6]:
            # Move to next Monday
            days_ahead = 7 - commit_date.weekday()
            commit_date += timedelta(days=days_ahead)

        # Add some time variation
        commit_date = commit_date.replace(
            hour=random.randint(9, 20),
            minute=random.randint(0, 59)
        )

        message = commit_info['message']
        files = commit_info['files']

        if create_commit(repo_path, commit_date, message, files):
            successful_commits += 1
            print(f"[{i}/{len(commit_plan)}] {commit_date.strftime('%Y-%m-%d')} - {message}")

    print(f"\n{'='*60}")
    print(f"✓ Created {successful_commits} commits successfully")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Generate realistic project history from existing code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  python realistic_project_history.py \\
    --source /path/to/your/project \\
    --output /home/haider/Desktop/my-project-history \\
    --start-date 2021-01-01 \\
    --end-date 2025-10-14 \\
    --project-name "My Awesome Project"
        """
    )

    parser.add_argument("--source", required=True,
                        help="Source project directory")
    parser.add_argument("--output", required=True,
                        help="Output repository path")
    parser.add_argument("--start-date", required=True,
                        help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", required=True,
                        help="End date (YYYY-MM-DD)")
    parser.add_argument("--project-name", required=True,
                        help="Project name for commit messages")
    parser.add_argument("--skip-weekends", action="store_true", default=True,
                        help="Skip weekend commits (default: True)")

    args = parser.parse_args()

    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

    if not os.path.exists(args.source):
        print(f"Error: Source directory does not exist: {args.source}")
        return

    generate_realistic_history(
        args.source,
        args.output,
        start_date,
        end_date,
        args.project_name,
        args.skip_weekends
    )

    print(f"\n{'='*60}")
    print("NEXT STEPS")
    print(f"{'='*60}")
    print("1. Review the generated history:")
    print(f"   cd {args.output}")
    print("   git log --oneline")
    print("")
    print("2. Push to GitHub:")
    print(f"   cd {args.output}")
    print("   git remote add origin git@github.com:YOUR_USERNAME/REPO.git")
    print("   git branch -M main")
    print("   git push -u origin main --force")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
