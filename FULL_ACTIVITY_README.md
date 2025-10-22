# GitHub Full Activity Generator

Generate complete GitHub activity including **commits**, **issues**, **pull requests**, and **code reviews** to fill all contribution graphs!

## 🎯 What This Does

This enhanced script creates:

1. ✅ **Commits** - Backdated commits (like the original script)
2. ✅ **Issues** - Opens and closes issues
3. ✅ **Pull Requests** - Creates and merges PRs
4. ✅ **Code Reviews** - Adds review comments to PRs

All of these will appear on your GitHub contribution graphs!

## 📦 Installation

### Step 1: Install Python Dependencies

```bash
cd /home/haider/Desktop/github-activity-generator
pip3 install -r requirements.txt
```

Or install manually:
```bash
pip3 install PyGithub requests
```

### Step 2: Create GitHub Personal Access Token

**You need a token to create issues and PRs via the GitHub API.**

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `Activity Generator`
4. Select scopes:
   - ✅ **repo** (full control of private repositories)
5. Click **"Generate token"**
6. **Copy the token** (you won't see it again!)

## 🚀 Usage

### Option 1: Commits Only (No Token Needed)

```bash
python3 github_full_activity_generator.py \
  --start-date 2021-01-01 \
  --end-date 2025-10-14 \
  --repo-path /home/haider/Desktop/github-activity
```

### Option 2: Full Activity (Issues + PRs + Reviews)

```bash
python3 github_full_activity_generator.py \
  --start-date 2021-01-01 \
  --end-date 2025-10-14 \
  --repo-path /home/haider/Desktop/github-activity \
  --github-token YOUR_GITHUB_TOKEN_HERE \
  --repo-name AleemHaider/inventory-app \
  --enable-issues-prs
```

**Replace:**
- `YOUR_GITHUB_TOKEN_HERE` with your actual token
- `AleemHaider/inventory-app` with your GitHub username/repository

## 📋 Command-Line Options

| Option | Required | Description |
|--------|----------|-------------|
| `--start-date` | ✅ | Start date (YYYY-MM-DD) |
| `--end-date` | ✅ | End date (YYYY-MM-DD) |
| `--repo-path` | No | Local repo path (default: ./github-activity) |
| `--repo-name-local` | No | Local repo name (default: github-activity) |
| `--repo-name` | For issues/PRs | GitHub repo (format: username/repo) |
| `--github-token` | For issues/PRs | GitHub Personal Access Token |
| `--enable-issues-prs` | No | Enable issues and PRs creation |
| `--min-commits` | No | Min commits per day (default: 1) |
| `--max-commits` | No | Max commits per day (default: 5) |
| `--frequency` | No | Activity probability 0-1 (default: 0.7) |
| `--include-weekends` | No | Include Saturday/Sunday |

## 💡 Complete Example

### Step 1: Install dependencies

```bash
pip3 install PyGithub requests
```

### Step 2: Create repository on GitHub

1. Go to https://github.com/new
2. Create repository named `github-activity` (or any name)
3. **Do NOT** initialize with README

### Step 3: Run the generator

```bash
cd /home/haider/Desktop/github-activity-generator

# With full activity (issues, PRs, reviews)
python3 github_full_activity_generator.py \
  --start-date 2021-01-01 \
  --end-date 2025-10-14 \
  --repo-path /home/haider/Desktop/github-activity \
  --github-token ghp_your_token_here \
  --repo-name AleemHaider/github-activity \
  --enable-issues-prs \
  --min-commits 1 \
  --max-commits 5 \
  --frequency 0.7
```

### Step 4: Push to GitHub

```bash
cd /home/haider/Desktop/github-activity
git remote add origin git@github.com:AleemHaider/github-activity.git
git branch -M main
git push -u origin main --force
```

### Step 5: Wait

- **Commits**: Show immediately in repository
- **Issues/PRs**: Show immediately
- **Contribution graph**: Updates in 30-60 minutes

## 📊 What Gets Created

### Commits (Always)
- Backdated commits with your authorship
- Random patterns throughout the day (9 AM - 10 PM)
- Weekdays only by default

### Issues (Optional - with token)
- Random issue types: features, bugs, enhancements
- Some closed, some open
- Created randomly (~30% of active days)

### Pull Requests (Optional - with token)
- Feature branches with commits
- PRs created and many auto-merged
- Created randomly (~20% of active days)

### Code Reviews (Optional - with token)
- Review comments on PRs
- Approval reviews
- Added to ~50% of PRs

## 🎯 Expected Results

For date range 2021-01-01 to 2025-10-14 (default settings):

- **~1,700 commits** (weekdays, 70% frequency)
- **~250 issues** (if enabled)
- **~150 pull requests** (if enabled)
- **~75 code reviews** (if enabled)

## ⚠️ Important Notes

### GitHub API Rate Limits

- **Authenticated**: 5,000 requests/hour
- **Unauthenticated**: 60 requests/hour

Creating issues and PRs counts towards your rate limit. The script includes delays to avoid hitting limits.

### Backdating Limitations

- ❌ **Issues cannot be backdated** - GitHub API doesn't support this
- ❌ **PRs cannot be backdated** - Created with current timestamp
- ✅ **Commits CAN be backdated** - This works perfectly

**Result:** Issues and PRs will show as created "today" but commits will show for the date range you specify.

### What Shows on Contribution Graph

✅ **Commits** - Show on the date you specify (backdated)
✅ **Issues opened** - Show on day created
✅ **Pull requests opened** - Show on day created
✅ **Code reviews** - Show on day created
✅ **Issues closed** - Counts as contribution

## 🔒 Security

**Keep your token safe!**

```bash
# Store token in environment variable
export GITHUB_TOKEN="ghp_your_token_here"

# Then use it
python3 github_full_activity_generator.py \
  --start-date 2021-01-01 \
  --end-date 2025-10-14 \
  --github-token $GITHUB_TOKEN \
  --repo-name AleemHaider/github-activity \
  --enable-issues-prs
```

**Never commit your token to a repository!**

## 🐛 Troubleshooting

### Error: "Bad credentials"

- Your GitHub token is invalid or expired
- Create a new token at https://github.com/settings/tokens

### Error: "Not Found" when creating issues

- Make sure repository name is correct format: `username/repo`
- Repository must exist on GitHub
- Token must have `repo` permissions

### Issues/PRs not showing

- They should appear immediately in the repository
- Check: https://github.com/YOUR_USERNAME/YOUR_REPO/issues
- Check: https://github.com/YOUR_USERNAME/YOUR_REPO/pulls

### Rate limit exceeded

- Wait 1 hour for rate limit to reset
- Use `--frequency 0.5` to create fewer items
- Reduce date range

### Commits show wrong author

- Set git config before running:
  ```bash
  git config --global user.name "AleemHaider"
  git config --global user.email "aleemhaider111@gmail.com"
  ```

## 📈 Maximizing Your Contribution Graph

### Strategy 1: Commits Only (Safest)

```bash
# Just commits, looks most natural
python3 github_full_activity_generator.py \
  --start-date 2021-01-01 \
  --end-date 2025-10-14
```

### Strategy 2: Moderate Activity

```bash
# Commits + occasional issues/PRs
python3 github_full_activity_generator.py \
  --start-date 2021-01-01 \
  --end-date 2025-10-14 \
  --github-token $GITHUB_TOKEN \
  --repo-name AleemHaider/github-activity \
  --enable-issues-prs \
  --frequency 0.6
```

### Strategy 3: Very Active

```bash
# Maximum activity
python3 github_full_activity_generator.py \
  --start-date 2021-01-01 \
  --end-date 2025-10-14 \
  --github-token $GITHUB_TOKEN \
  --repo-name AleemHaider/github-activity \
  --enable-issues-prs \
  --min-commits 3 \
  --max-commits 10 \
  --frequency 0.9 \
  --include-weekends
```

## ❓ FAQ

**Q: Can I backdate issues and PRs?**
A: No, GitHub API doesn't support this. They'll be created with today's date.

**Q: Will issues show on my contribution graph?**
A: Yes! Opening and closing issues counts as contributions.

**Q: Can I use this on a private repository?**
A: Yes, but you need to enable "Private contributions" in your GitHub settings.

**Q: Is this against GitHub's Terms of Service?**
A: Backdating commits is a standard git feature. However, ethical considerations apply.

**Q: Can others see this is automated?**
A: Yes, if they inspect the repository they'll see the pattern.

## 📄 License

MIT License - Use responsibly and ethically.

## ⚠️ Disclaimer

This tool is for educational purposes. Be transparent about your experience and don't misrepresent your work history.

---

**Made for learning and experimentation**
**Last Updated:** October 2025
