#!/usr/bin/env python3
"""
Clone an existing repository and rewrite its history with backdated commits
Makes it look like you developed the project gradually over time
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


def clone_repository(source_url, temp_path):
    """Clone the source repository"""
    print(f"Cloning repository from {source_url}...")

    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)

    result = run_command(f"git clone {source_url} {temp_path}")

    if result.returncode == 0:
        print("✓ Repository cloned successfully")
        return True
    else:
        print(f"✗ Failed to clone repository: {result.stderr}")
        return False


def get_file_list(source_dir, exclude_patterns=None):
    """Get all files from source directory"""
    if exclude_patterns is None:
        exclude_patterns = ['.git', 'node_modules', '__pycache__', '.env', 'venv',
                          'dist', 'build', '.DS_Store', 'package-lock.json',
                          'yarn.lock', '.pytest_cache', '.vscode', '.idea']

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
    """Categorize files by type for logical commit grouping"""
    categories = {
        'config': [],       # Config files (package.json, requirements.txt, etc.)
        'docs': [],         # Documentation
        'models': [],       # Models/schemas/database
        'api': [],          # API endpoints
        'routes': [],       # Routes/controllers
        'services': [],     # Services/business logic
        'components': [],   # UI components
        'pages': [],        # Pages/views
        'styles': [],       # CSS/styling
        'assets': [],       # Images/static files
        'tests': [],        # Tests
        'utils': [],        # Utilities
        'other': []         # Everything else
    }

    for file_path, rel_path in files:
        lower_path = rel_path.lower()

        # Config files
        if any(x in lower_path for x in ['package.json', 'requirements.txt', 'setup.py',
                                          'dockerfile', 'docker-compose', '.env.example',
                                          'config.', 'webpack', 'babel', 'tsconfig',
                                          '.json', '.yaml', '.yml', 'makefile']):
            categories['config'].append((file_path, rel_path))

        # Documentation
        elif any(x in lower_path for x in ['readme', 'docs/', 'documentation', '.md', 'license']):
            categories['docs'].append((file_path, rel_path))

        # Models and database
        elif any(x in lower_path for x in ['model', 'schema', 'entity', 'database', 'migration']):
            categories['models'].append((file_path, rel_path))

        # API
        elif any(x in lower_path for x in ['api/', 'endpoint', 'graphql', 'rest']):
            categories['api'].append((file_path, rel_path))

        # Routes and controllers
        elif any(x in lower_path for x in ['route', 'controller', 'handler']):
            categories['routes'].append((file_path, rel_path))

        # Services
        elif any(x in lower_path for x in ['service', 'business', 'logic', 'repository']):
            categories['services'].append((file_path, rel_path))

        # Components
        elif any(x in lower_path for x in ['component', 'widget', 'element']):
            categories['components'].append((file_path, rel_path))

        # Pages and views
        elif any(x in lower_path for x in ['page', 'view', 'template', 'screen']):
            categories['pages'].append((file_path, rel_path))

        # Styles
        elif any(x in lower_path for x in ['.css', '.scss', '.sass', '.less', 'style', 'theme']):
            categories['styles'].append((file_path, rel_path))

        # Assets
        elif any(x in lower_path for x in ['static', 'public', 'asset', 'image', 'img',
                                            '.png', '.jpg', '.svg', '.ico', 'font']):
            categories['assets'].append((file_path, rel_path))

        # Tests
        elif any(x in lower_path for x in ['test', 'spec', '__tests__', '.test.', '.spec.']):
            categories['tests'].append((file_path, rel_path))

        # Utils
        elif any(x in lower_path for x in ['util', 'helper', 'lib', 'common', 'shared']):
            categories['utils'].append((file_path, rel_path))

        # Main/index files
        elif any(x in lower_path for x in ['index.', 'main.', 'app.', '__init__']):
            categories['other'].insert(0, (file_path, rel_path))  # Put at beginning

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


def generate_realistic_commit_message(category, file_count):
    """Generate realistic commit messages based on file category"""
    messages = {
        'config': [
            'chore: setup project configuration',
            'chore: add project dependencies',
            'chore: configure build system',
            'chore: update project settings',
        ],
        'docs': [
            'docs: add project documentation',
            'docs: update README with usage instructions',
            'docs: add API documentation',
            'docs: improve setup guide',
        ],
        'models': [
            'feat: add database models',
            'feat: implement data schemas',
            'feat: create entity definitions',
            'refactor: improve data structures',
        ],
        'api': [
            'feat: add API endpoints',
            'feat: implement REST services',
            'feat: create GraphQL resolvers',
            'fix: improve API error handling',
        ],
        'routes': [
            'feat: add route handlers',
            'feat: implement controllers',
            'feat: setup routing system',
            'refactor: improve routing logic',
        ],
        'services': [
            'feat: add business logic services',
            'feat: implement core functionality',
            'refactor: extract service layer',
            'feat: add data processing services',
        ],
        'components': [
            'feat: add UI components',
            'feat: create reusable components',
            'style: improve component design',
            'refactor: optimize component structure',
        ],
        'pages': [
            'feat: add application pages',
            'feat: implement views',
            'style: improve page layouts',
            'feat: create user interface',
        ],
        'styles': [
            'style: add CSS styling',
            'style: implement theme',
            'style: improve responsive design',
            'style: update visual design',
        ],
        'assets': [
            'chore: add static assets',
            'chore: add images and icons',
            'chore: update assets',
            'style: add visual resources',
        ],
        'tests': [
            'test: add unit tests',
            'test: add integration tests',
            'test: improve test coverage',
            'test: add test utilities',
        ],
        'utils': [
            'feat: add utility functions',
            'feat: implement helpers',
            'refactor: extract common utilities',
            'chore: add utility libraries',
        ],
        'other': [
            'feat: add core functionality',
            'feat: implement features',
            'refactor: improve code structure',
            'chore: add project files',
        ]
    }

    return random.choice(messages.get(category, messages['other']))


def rewrite_history(source_path, target_path, start_date, end_date,
                   repo_name, skip_weekends=True):
    """Rewrite git history with backdated commits"""

    print(f"\n{'='*60}")
    print("Analyzing source repository...")
    print(f"{'='*60}")

    # Get and categorize files
    all_files = get_file_list(source_path)
    print(f"Found {len(all_files)} files")

    categories = categorize_files(all_files)

    print("\nFile categories:")
    for cat, files in categories.items():
        if files:
            print(f"  {cat}: {len(files)} files")

    # Setup target repository
    print(f"\n{'='*60}")
    print("Setting up new repository")
    print(f"{'='*60}")

    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    os.makedirs(target_path)

    run_command("git init", cwd=target_path)
    print("✓ Initialized git repository")

    # Create commit plan with realistic progression
    commit_plan = []
    current_date = start_date

    # Phase 1: Initial setup
    if categories['config']:
        commit_plan.append({
            'date': current_date,
            'message': 'chore: initial project setup',
            'files': categories['config'][:min(3, len(categories['config']))]
        })
        current_date += timedelta(days=random.randint(1, 2))

    # Phase 2: Documentation
    if categories['docs']:
        commit_plan.append({
            'date': current_date,
            'message': 'docs: add project documentation',
            'files': categories['docs']
        })
        current_date += timedelta(days=random.randint(1, 2))

    # Phase 3: Models and data structures
    if categories['models']:
        for i in range(0, len(categories['models']), 3):
            batch = categories['models'][i:i+3]
            commit_plan.append({
                'date': current_date,
                'message': generate_realistic_commit_message('models', len(batch)),
                'files': batch
            })
            current_date += timedelta(days=random.randint(1, 3))

    # Phase 4: Services and business logic
    if categories['services']:
        for i in range(0, len(categories['services']), 2):
            batch = categories['services'][i:i+2]
            commit_plan.append({
                'date': current_date,
                'message': generate_realistic_commit_message('services', len(batch)),
                'files': batch
            })
            current_date += timedelta(days=random.randint(1, 2))

    # Phase 5: API endpoints
    if categories['api']:
        for i in range(0, len(categories['api']), 2):
            batch = categories['api'][i:i+2]
            commit_plan.append({
                'date': current_date,
                'message': generate_realistic_commit_message('api', len(batch)),
                'files': batch
            })
            current_date += timedelta(days=random.randint(1, 3))

    # Phase 6: Routes
    if categories['routes']:
        for i in range(0, len(categories['routes']), 2):
            batch = categories['routes'][i:i+2]
            commit_plan.append({
                'date': current_date,
                'message': generate_realistic_commit_message('routes', len(batch)),
                'files': batch
            })
            current_date += timedelta(days=random.randint(1, 2))

    # Phase 7: UI Components
    if categories['components']:
        for i in range(0, len(categories['components']), 3):
            batch = categories['components'][i:i+3]
            commit_plan.append({
                'date': current_date,
                'message': generate_realistic_commit_message('components', len(batch)),
                'files': batch
            })
            current_date += timedelta(days=random.randint(2, 4))

    # Phase 8: Pages
    if categories['pages']:
        for i in range(0, len(categories['pages']), 2):
            batch = categories['pages'][i:i+2]
            commit_plan.append({
                'date': current_date,
                'message': generate_realistic_commit_message('pages', len(batch)),
                'files': batch
            })
            current_date += timedelta(days=random.randint(2, 3))

    # Phase 9: Styling
    if categories['styles']:
        commit_plan.append({
            'date': current_date,
            'message': 'style: add styling and improve UI',
            'files': categories['styles']
        })
        current_date += timedelta(days=random.randint(2, 3))

    # Phase 10: Assets
    if categories['assets']:
        commit_plan.append({
            'date': current_date,
            'message': 'chore: add static assets',
            'files': categories['assets']
        })
        current_date += timedelta(days=random.randint(1, 2))

    # Phase 11: Utils
    if categories['utils']:
        commit_plan.append({
            'date': current_date,
            'message': 'feat: add utility functions',
            'files': categories['utils']
        })
        current_date += timedelta(days=random.randint(1, 3))

    # Phase 12: Tests
    if categories['tests']:
        commit_plan.append({
            'date': current_date,
            'message': 'test: add unit and integration tests',
            'files': categories['tests']
        })
        current_date += timedelta(days=random.randint(2, 4))

    # Phase 13: Remaining files
    if categories['other']:
        for i in range(0, len(categories['other']), 5):
            batch = categories['other'][i:i+5]
            commit_plan.append({
                'date': current_date,
                'message': 'feat: add additional features',
                'files': batch
            })
            current_date += timedelta(days=random.randint(1, 2))

    # Remaining config
    if len(categories['config']) > 3:
        commit_plan.append({
            'date': current_date,
            'message': 'chore: finalize configuration',
            'files': categories['config'][3:]
        })
        current_date += timedelta(days=1)

    # Add refinement commits
    refinement_messages = [
        'fix: resolve bugs and issues',
        'refactor: improve code quality',
        'fix: enhance error handling',
        'docs: update documentation',
        'chore: update dependencies',
    ]

    while current_date < end_date:
        current_date += timedelta(days=random.randint(3, 7))
        if current_date > end_date:
            break

        commit_plan.append({
            'date': current_date,
            'message': random.choice(refinement_messages),
            'files': []
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
            days_ahead = 7 - commit_date.weekday()
            commit_date += timedelta(days=days_ahead)

        # Add time variation
        commit_date = commit_date.replace(
            hour=random.randint(9, 20),
            minute=random.randint(0, 59)
        )

        message = commit_info['message']
        files = commit_info['files']

        if create_commit(target_path, commit_date, message, files):
            successful_commits += 1
            file_info = f" ({len(files)} files)" if files else ""
            print(f"[{i}/{len(commit_plan)}] {commit_date.strftime('%Y-%m-%d')} - {message}{file_info}")

    print(f"\n{'='*60}")
    print(f"✓ Created {successful_commits} commits successfully")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Clone a repository and rewrite its history with backdated commits"
    )
    parser.add_argument("--source", required=True,
                       help="Source repository URL (GitHub, GitLab, etc.)")
    parser.add_argument("--target-path", required=True,
                       help="Target repository path")
    parser.add_argument("--repo-name", required=True,
                       help="Repository name")
    parser.add_argument("--start-date", required=True,
                       help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", required=True,
                       help="End date (YYYY-MM-DD)")
    parser.add_argument("--skip-weekends", action="store_true", default=True,
                       help="Skip weekend commits (default: True)")

    args = parser.parse_args()

    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

    # Clone to temp directory
    temp_path = "/tmp/github_activity_source"

    if not clone_repository(args.source, temp_path):
        return

    # Rewrite history
    rewrite_history(
        temp_path,
        args.target_path,
        start_date,
        end_date,
        args.repo_name,
        args.skip_weekends
    )

    # Cleanup
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)

    print(f"\n{'='*60}")
    print("NEXT STEPS")
    print(f"{'='*60}")
    print("1. Review the generated history:")
    print(f"   cd {args.target_path}")
    print("   git log --oneline")
    print("")
    print("2. Push to your GitHub repository:")
    print(f"   cd {args.target_path}")
    print("   git remote add origin git@github.com:YOUR_USERNAME/REPO.git")
    print("   git branch -M main")
    print("   git push -u origin main --force")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
