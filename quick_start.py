#!/usr/bin/env python3
"""
Quick Start Script - Automated GitHub Activity Generator
Generates and pushes commits automatically
"""
import subprocess
import sys
import os

def run_command(cmd, cwd=None, show_output=True):
    """Run a command and print output"""
    if show_output:
        print(f"\n→ Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=not show_output, text=True)
    return result.returncode

def main():
    print("=" * 70)
    print("  GitHub Activity Generator - Quick Start")
    print("=" * 70)

    # Configuration
    START_DATE = "2021-01-01"
    END_DATE = "2025-10-14"
    REPO_PATH = "/home/haider/Desktop/github-activity"
    GITHUB_REMOTE = "git@github.com:AleemHaider/inventory-app.git"

    print(f"\n📅 Date Range: {START_DATE} to {END_DATE}")
    print(f"📁 Repository Path: {REPO_PATH}")
    print(f"🌐 GitHub Remote: {GITHUB_REMOTE}")

    # Step 1: Clean up
    print("\n" + "=" * 70)
    print("STEP 1: Cleaning up old repository")
    print("=" * 70)
    if os.path.exists(REPO_PATH):
        run_command(f'rm -rf {REPO_PATH}')
        print("✓ Old repository removed")
    else:
        print("✓ No old repository found")

    # Step 2: Generate commits
    print("\n" + "=" * 70)
    print("STEP 2: Generating commits")
    print("=" * 70)
    print("This will take approximately 5 minutes...")
    print("Please wait...\n")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    generator_script = os.path.join(script_dir, "github_activity_generator.py")

    cmd = [
        sys.executable,
        generator_script,
        '--start-date', START_DATE,
        '--end-date', END_DATE,
        '--min-commits', '1',
        '--max-commits', '5',
        '--frequency', '0.7',
        '--repo-path', REPO_PATH
    ]

    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("\n❌ ERROR: Failed to generate commits")
        sys.exit(1)

    print("\n✓ Commits generated successfully!")

    # Step 3: Push to GitHub
    print("\n" + "=" * 70)
    print("STEP 3: Pushing to GitHub")
    print("=" * 70)

    # Check if remote already exists
    check_remote = subprocess.run(
        'git remote get-url origin',
        shell=True,
        cwd=REPO_PATH,
        capture_output=True
    )

    if check_remote.returncode == 0:
        print("→ Removing existing remote...")
        run_command('git remote remove origin', cwd=REPO_PATH, show_output=False)

    # Add remote
    print(f"→ Adding remote: {GITHUB_REMOTE}")
    result = run_command(f'git remote add origin {GITHUB_REMOTE}', cwd=REPO_PATH, show_output=False)

    if result != 0:
        print("❌ Failed to add remote")
        sys.exit(1)

    # Set branch to main
    print("→ Setting branch to main")
    run_command('git branch -M main', cwd=REPO_PATH, show_output=False)

    # Force push
    print("→ Pushing to GitHub (this may take a minute)...")
    result = run_command('git push -u origin main --force', cwd=REPO_PATH)

    if result == 0:
        print("\n" + "=" * 70)
        print("✅ SUCCESS! All done!")
        print("=" * 70)
        print(f"\n📊 Generated commits from {START_DATE} to {END_DATE}")
        print("📈 Approximately 1,700+ commits (weekdays only)")
        print("\n🔗 Check your GitHub profile:")
        print("   https://github.com/AleemHaider")
        print("\n⏱️  Your contribution graph should update within 30-60 minutes!")
        print("\n💡 Tip: Hard refresh your browser (Ctrl+Shift+R) to see updates faster")
    else:
        print("\n" + "=" * 70)
        print("❌ ERROR: Failed to push to GitHub")
        print("=" * 70)
        print("\nYou can try pushing manually:")
        print(f"  cd {REPO_PATH}")
        print("  git push -u origin main --force")
        print("\nCommon issues:")
        print("  - SSH key not configured: https://docs.github.com/en/authentication")
        print("  - Repository doesn't exist: Create it first on GitHub")
        print("  - Permission denied: Check your SSH key or use HTTPS with token")

if __name__ == '__main__':
    main()
