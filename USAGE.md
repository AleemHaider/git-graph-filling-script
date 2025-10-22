# Simple Usage Guide

## Quick Start

I've created a simple one-command script for you: `simple_run.sh`

### Basic Usage (Commits Only)

```bash
cd /home/haider/Desktop/github-activity-generator

./simple_run.sh \
  --repo YourUsername/your-repo \
  --start 2024-01-01 \
  --end 2024-12-31
```

### With Custom Commit Frequency

```bash
./simple_run.sh \
  --repo YourUsername/your-repo \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --min-commits 2 \
  --max-commits 8
```

### Include Weekends

```bash
./simple_run.sh \
  --repo YourUsername/your-repo \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --include-weekends
```

### With GitHub Features (Issues + PRs)

First, set your GitHub token:

```bash
export GITHUB_TOKEN='your_github_token_here'
```

Then run:

```bash
./simple_run.sh \
  --repo YourUsername/your-repo \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --min-commits 3 \
  --max-commits 7
```

## Parameters

### Required
- `--repo` - Your GitHub repository (format: `username/repository`)
- `--start` - Start date (format: `YYYY-MM-DD`)
- `--end` - End date (format: `YYYY-MM-DD`)

### Optional
- `--min-commits` - Minimum commits per day (default: 1)
- `--max-commits` - Maximum commits per day (default: 5)
- `--include-weekends` - Include Saturday and Sunday (default: skip weekends)
- `--token` - GitHub token (or use `GITHUB_TOKEN` environment variable)

## Complete Example

```bash
# 1. Create repository on GitHub first
# Go to https://github.com/new and create a repository

# 2. Run the generator
cd /home/haider/Desktop/github-activity-generator

./simple_run.sh \
  --repo AleemHaider/my-project \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --min-commits 2 \
  --max-commits 6

# 3. The script will:
#    - Generate commits with backdated timestamps
#    - Ask for confirmation before pushing
#    - Push to your GitHub repository
#    - Show you the results

# 4. Wait 30-60 minutes for your contribution graph to update
```

## With GitHub Token (for Issues/PRs)

```bash
# 1. Create token at https://github.com/settings/tokens
#    - Select "repo" permission
#    - Copy the token

# 2. Set the token
export GITHUB_TOKEN='ghp_your_token_here'

# 3. Run with all features
./simple_run.sh \
  --repo AleemHaider/my-project \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --min-commits 3 \
  --max-commits 8 \
  --include-weekends
```

## What Each Parameter Does

- **`--repo YourUsername/your-repo`** - Where to push the code on GitHub
- **`--start 2024-01-01`** - When to start backdated commits
- **`--end 2024-12-31`** - When to end backdated commits
- **`--min-commits 2`** - At least 2 commits on active days
- **`--max-commits 6`** - At most 6 commits on active days
- **No weekends by default** - Automatically skips Saturday/Sunday (use `--include-weekends` to include them)

## Local Repository Location

The script creates repositories in:
```
~/Desktop/github-activity-repos/your-repo-name/
```

## Help

View all options:
```bash
./simple_run.sh --help
```

## Educational Use Only

⚠️ **Important**: This tool is for educational purposes to understand:
- How git timestamps work
- How GitHub contribution graphs are calculated
- GitHub API usage

**Do not use this to misrepresent your work history.**
