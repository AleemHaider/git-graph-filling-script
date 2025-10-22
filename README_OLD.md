# GitHub Activity Generator

A Python script to generate GitHub contribution activity with backdated commits to fill your GitHub activity graph.

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Command-Line Options](#command-line-options)
- [Examples](#examples)
- [Complete Workflow](#complete-workflow)
- [Troubleshooting](#troubleshooting)
- [Important Notes](#important-notes)
- [FAQ](#faq)
- [License](#license)

## ✨ Features

- 🎯 Generate commits for any date range
- 📊 Customize commit frequency and intensity
- 🎲 Randomized commit patterns for natural-looking activity
- 📅 Option to skip weekends (Monday-Friday only)
- ⚙️ Simple command-line interface
- 🚀 Fast and efficient commit generation

## 📦 Requirements

- Python 3.6 or higher
- Git installed and configured
- GitHub account
- SSH key configured with GitHub (or use HTTPS with personal access token)

## 🔧 Installation

1. **Clone or download this repository**

```bash
cd /home/haider/Desktop/github-activity-generator
```

2. **Make the script executable (optional)**

```bash
chmod +x github_activity_generator.py
```

3. **Verify Git is configured**

```bash
git config --global user.name "Your Name"
git config --global user.email "your-github-email@example.com"
```

**⚠️ IMPORTANT:** The email MUST match a verified email on your GitHub account, or commits won't appear on your profile.

## 🚀 Quick Start

### Basic Usage (Last Year)

```bash
python3 github_activity_generator.py --days 365
```

### Specific Date Range

```bash
python3 github_activity_generator.py --start-date 2021-01-01 --end-date 2025-10-14
```

### Custom Activity Pattern

```bash
# More aggressive activity (90% of days, 3-10 commits per day)
python3 github_activity_generator.py --days 365 --min-commits 3 --max-commits 10 --frequency 0.9

# Light activity (50% of days, 1-2 commits per day)
python3 github_activity_generator.py --days 365 --min-commits 1 --max-commits 2 --frequency 0.5
```

## 📖 Usage

The script generates commits in a local git repository, which you then push to GitHub.

```bash
python3 github_activity_generator.py [OPTIONS]
```

## ⚙️ Command-Line Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--repo-path` | string | `./github-activity` | Path for the repository |
| `--repo-name` | string | `github-activity` | Repository name |
| `--days` | int | 365 | Number of days back from today |
| `--start-date` | string | - | Start date (YYYY-MM-DD) |
| `--end-date` | string | Today | End date (YYYY-MM-DD) |
| `--min-commits` | int | 1 | Minimum commits per active day |
| `--max-commits` | int | 5 | Maximum commits per active day |
| `--frequency` | float | 0.7 | Activity probability (0.0-1.0) |
| `--include-weekends` | flag | False | Include Saturday and Sunday |

## 💡 Examples

### Example 1: Fill Last 6 Months (Weekdays Only)

```bash
python3 github_activity_generator.py --days 180
```

**Result:** ~90 days of activity with 1-5 commits per weekday

### Example 2: Specific Date Range (2021-2025)

```bash
python3 github_activity_generator.py --start-date 2021-01-01 --end-date 2025-10-14
```

**Result:** ~1,700 commits over 4 years, 10 months (weekdays only)

### Example 3: Very Active Pattern

```bash
python3 github_activity_generator.py \
  --days 365 \
  --min-commits 5 \
  --max-commits 15 \
  --frequency 0.95 \
  --include-weekends
```

**Result:** Heavy activity pattern with 5-15 commits on 95% of days, including weekends

### Example 4: Minimal Activity Pattern

```bash
python3 github_activity_generator.py \
  --days 365 \
  --min-commits 1 \
  --max-commits 2 \
  --frequency 0.3
```

**Result:** Light activity with 1-2 commits on only 30% of weekdays

### Example 5: Custom Repository Path

```bash
python3 github_activity_generator.py \
  --days 180 \
  --repo-path ~/my-activity \
  --repo-name my-github-activity
```

**Result:** Creates repository in custom location

## 🔄 Complete Workflow

### Step 1: Generate Commits

```bash
python3 github_activity_generator.py --start-date 2021-01-01 --end-date 2025-10-14
```

**Output:**
```
GitHub Activity Generator
========================
Date range: 2021-01-01 to 2025-10-14
Commits per day: 1-5
Activity frequency: 70.0%
Skip weekends: True
Repository: ./github-activity

Created directory: ./github-activity
Initialized git repository
Created 3 commit(s) for 2021-01-04
Created 2 commit(s) for 2021-01-05
...
Total commits created: 1700
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository named `github-activity` (or your chosen name)
3. **Do NOT** initialize with README, .gitignore, or license

### Step 3: Push to GitHub

```bash
cd github-activity
git remote add origin git@github.com:YOUR_USERNAME/github-activity.git
git branch -M main
git push -u origin main --force
```

**Or with HTTPS:**

```bash
cd github-activity
git remote add origin https://github.com/YOUR_USERNAME/github-activity.git
git branch -M main
git push -u origin main --force
```

### Step 4: Verify

- Visit your GitHub profile: `https://github.com/YOUR_USERNAME`
- Check the repository: `https://github.com/YOUR_USERNAME/github-activity`
- Your contribution graph should update within 10-60 minutes

## 🛠️ Troubleshooting

### Commits Not Showing on GitHub Profile

**Problem:** Commits appear in repository but not on contribution graph

**Solutions:**

1. **Check email configuration:**
   ```bash
   cd github-activity
   git log -1 --format='%ae'
   ```

   This email MUST match a verified email in your GitHub account settings.

2. **Fix email if incorrect:**
   ```bash
   cd github-activity

   # Rewrite all commits with correct email
   git filter-branch -f --env-filter '
   export GIT_AUTHOR_EMAIL="your-github-email@example.com"
   export GIT_COMMITTER_EMAIL="your-github-email@example.com"
   ' -- --all

   # Force push again
   git push -u origin main --force
   ```

3. **Verify email on GitHub:**
   - Go to GitHub Settings → Emails
   - Make sure your email is listed and verified
   - Add email if needed and mark as verified

### Repository Already Exists

**Problem:** Error when adding remote

**Solution:**
```bash
cd github-activity
git remote remove origin
git remote add origin git@github.com:YOUR_USERNAME/github-activity.git
git push -u origin main --force
```

### Permission Denied When Pushing

**Solutions:**

**Option 1: Use SSH (Recommended)**
```bash
# Generate SSH key if you don't have one
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
cat ~/.ssh/id_ed25519.pub
```

**Option 2: Use Personal Access Token**
```bash
# Generate token at: GitHub Settings → Developer settings → Personal access tokens
# Use token as password when pushing via HTTPS
```

### Want to Regenerate Activity

```bash
# Delete old repository and start fresh
rm -rf github-activity
python3 github_activity_generator.py --start-date 2021-01-01 --end-date 2025-10-14
```

## 📌 Important Notes

### Ethics and Transparency

- ✅ These are **real git commits** with backdated timestamps (a standard git feature)
- ✅ Backdating commits is **allowed by GitHub** and is a legitimate git feature
- ⚠️ Anyone can inspect the repository and see these are generated commits
- ⚠️ Consider the implications for professional profiles and job applications
- ⚠️ Be transparent about your actual coding experience

### Technical Details

- **How it works:** Uses `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` environment variables to set commit dates
- **File modified:** Creates/appends to `activity.txt` for each commit
- **Commit messages:** Format is "Activity: YYYY-MM-DD"
- **Repository:** Creates a standard git repository that can be hosted anywhere
- **Graph update time:** 10-60 minutes after pushing, depending on commit volume

### Best Practices

1. **Use for personal/learning repositories** - Not recommended for misrepresenting professional work
2. **Match patterns to reality** - Use realistic commit frequencies
3. **Skip weekends** - More believable activity pattern (default behavior)
4. **Vary commit counts** - Script already randomizes this
5. **Be honest** - If asked, be transparent about using automation

## ❓ FAQ

### Q: Is this against GitHub's Terms of Service?

**A:** No. Backdating commits is a standard git feature. However, using it to misrepresent your work history could be considered misleading.

### Q: Will this help me get a job?

**A:** Contribution graphs are just one small factor. Real projects, code quality, and skills matter much more. Many employers look at actual repositories, not just green squares.

### Q: Can I get banned for this?

**A:** No, you cannot be banned for backdating commits. It's a git feature. However, ethical considerations apply.

### Q: How long does the graph take to update?

**A:** Usually 10-30 minutes, sometimes up to 1 hour for large commit volumes (1000+).

### Q: Can I delete the repository after pushing?

**A:** Yes, but your contribution graph will be recalculated and the commits will disappear from it.

### Q: Does this work with private repositories?

**A:** Commits to private repositories show on your graph only if you enable "Private contributions" in your GitHub settings.

### Q: Can I add to existing commits?

**A:** Yes, just run the script with a different date range or repository path, then push to a different repository.

### Q: What if I want commits on weekends too?

**A:** Use the `--include-weekends` flag.

### Q: How many commits should I generate?

**A:** For realistic patterns:
- Light user: 200-500 per year
- Active user: 500-1500 per year
- Very active: 1500-3000 per year

## 📄 License

This project is provided as-is for educational purposes. Use responsibly.

## 🤝 Contributing

Feel free to fork, modify, and use this script. If you find bugs or have improvements, contributions are welcome.

## ⚠️ Disclaimer

This tool is for educational and personal use only. Users are responsible for using this tool ethically and in compliance with GitHub's policies. The authors do not endorse misrepresenting work history or experience.

---

**Made with ❤️ for learning and experimentation**

**Last Updated:** October 2025
