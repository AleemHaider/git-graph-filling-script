# GitHub Activity Generator

Generate authentic GitHub contribution history with **one simple command**.

## 🎯 What This Does

Creates realistic GitHub activity with backdated commits that appear on your contribution graph.

**Three modes:**
1. 🏆 **Clone existing repos** - Most authentic (real code)
2. ⭐ **Realistic commits** - Professional-looking (generated code)
3. ⚡ **Simple commits** - Basic activity (minimal code)

## 💻 Platform Support

✅ **Linux** - Use `simple_run.sh`
✅ **Mac** - Use `simple_run.sh`
✅ **Windows** - Use `simple_run.bat` or `simple_run.ps1`

All features work on all platforms!

## 🚀 Quick Start

### 1. Create GitHub Repository
Go to https://github.com/new and create a repository (don't initialize it)

### 2. Run One Command

**Linux/Mac:**

**Best method (clones real code):**
```bash
cd /home/haider/Desktop/github-activity-generator

./simple_run.sh \
  --repo YourUsername/your-repo \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --source-repo https://github.com/vercel/next.js.git
```

**Alternative (generates realistic code):**
```bash
./simple_run.sh \
  --repo YourUsername/your-repo \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --realistic
```

**Windows (Command Prompt):**
```cmd
cd %USERPROFILE%\Desktop\github-activity-generator

simple_run.bat ^
  --repo YourUsername/your-repo ^
  --start 2024-01-01 ^
  --end 2024-12-31 ^
  --source-repo https://github.com/vercel/next.js.git
```

**Windows (PowerShell):**
```powershell
cd $env:USERPROFILE\Desktop\github-activity-generator

.\simple_run.ps1 `
  -Repo YourUsername/your-repo `
  -Start 2024-01-01 `
  -End 2024-12-31 `
  -SourceRepo https://github.com/vercel/next.js.git
```

### 3. Done!
- Wait 30-60 minutes for contribution graph to update
- Check your profile: https://github.com/YourUsername

## ✨ Features

✅ **One command** - Everything automated
✅ **Skips weekends** - Looks natural (automatic)
✅ **Realistic patterns** - Random times, varied frequency
✅ **Real code** - Clone actual projects or generate realistic code
✅ **Professional commits** - Uses conventional commit format
✅ **Multiple files** - Creates actual project structure
✅ **Safe** - Asks before pushing

## 📋 All Options

```bash
./simple_run.sh \
  --repo <username/repository>     # Where to push (required)
  --start <YYYY-MM-DD>             # Start date (required)
  --end <YYYY-MM-DD>               # End date (required)
  --source-repo <URL>              # Clone from existing repo (optional)
  --realistic                      # Use realistic commits (optional)
  --min-commits <number>           # Min commits/day (default: 1)
  --max-commits <number>           # Max commits/day (default: 5)
  --include-weekends               # Include Saturday/Sunday
```

## 📖 Examples

### Clone a Real Project
```bash
./simple_run.sh \
  --repo YourUsername/my-app \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --source-repo https://github.com/tastejs/todomvc.git
```

### Generate Realistic Code
```bash
./simple_run.sh \
  --repo YourUsername/my-app \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --realistic
```

### More Active Developer
```bash
./simple_run.sh \
  --repo YourUsername/my-app \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --realistic \
  --min-commits 3 \
  --max-commits 8 \
  --include-weekends
```

### Multiple Projects (Best Strategy)
```bash
# Project 1
./simple_run.sh --repo user/frontend-app --start 2024-01-01 --end 2024-06-30 --realistic

# Project 2
./simple_run.sh --repo user/backend-api --start 2024-05-01 --end 2024-09-30 --realistic

# Project 3
./simple_run.sh --repo user/mobile-app --start 2024-08-01 --end 2024-12-31 --realistic
```

## 🎨 Popular Source Repositories

### Frontend
- https://github.com/vercel/next.js.git
- https://github.com/facebook/create-react-app.git
- https://github.com/tastejs/todomvc.git

### Backend
- https://github.com/expressjs/express.git
- https://github.com/nestjs/nest.git
- https://github.com/tiangolo/fastapi.git

### Full-Stack
- https://github.com/vercel/commerce.git
- https://github.com/strapi/strapi.git
- https://github.com/supabase/supabase.git

## 📊 What Gets Created

### With --source-repo (Clone Mode)
```
✅ Actual project code from the source repository
✅ Professional commit messages based on file types
✅ Realistic development timeline (setup → features → tests)
✅ Multiple file types and proper structure
✅ Commits spread naturally over date range
```

### With --realistic (Generated Mode)
```
✅ Generated project structure (src/, components/, tests/)
✅ Professional commit messages (feat:, fix:, docs:, etc.)
✅ Multiple file changes per commit
✅ Realistic development patterns
✅ Natural time distribution
```

### Without flags (Simple Mode)
```
✅ Basic commits with timestamps
✅ Simple activity.txt file
✅ Quick and easy
```

## 🛠️ Installation

```bash
# Install Python dependencies
pip3 install PyGithub requests

# Make script executable
chmod +x simple_run.sh
```

## ⚙️ Default Behavior

- ✅ Skips weekends (Saturday/Sunday)
- ✅ Random commit times (9 AM - 8 PM)
- ✅ 70% activity frequency (some days no commits)
- ✅ 1-5 commits per active day
- ✅ Asks confirmation before pushing

## 💡 Tips

### For Most Authentic Results
1. Use `--source-repo` to clone real code
2. Choose projects you actually understand
3. Use realistic date ranges (3-12 months per project)
4. Create multiple projects over time
5. Keep weekends skipped (default)

### Choosing Source Repos
- Pick projects matching your skill level
- Use technologies you know
- Choose appropriate project sizes
- Find repos on GitHub Explore or Trending

## 📁 Where Files Are Created

```bash
~/Desktop/github-activity-repos/your-repo-name/
```

View locally:
```bash
cd ~/Desktop/github-activity-repos/your-repo-name
git log --oneline
ls -la
```

## 🔍 Verification

After pushing:
- Wait 30-60 minutes
- Check profile: https://github.com/YourUsername
- View repository: https://github.com/YourUsername/your-repo
- Check commits: https://github.com/YourUsername/your-repo/commits/main

## 🐛 Troubleshooting

### Script won't run
```bash
chmod +x simple_run.sh
```

### Missing dependencies
```bash
pip3 install PyGithub requests
```

### Contribution graph not updating
- Wait 30-60 minutes
- Verify email at https://github.com/settings/emails
- Check repo is public or enable private contributions

### SSH key issues
Use HTTPS URLs:
```bash
--source-repo https://github.com/user/repo.git
```

## 📚 Documentation

- **`FINAL_GUIDE.md`** - Complete comprehensive guide
- **`WINDOWS_GUIDE.md`** - Windows-specific instructions
- **`CLONE_REPO_GUIDE.md`** - Clone mode detailed docs
- **`REALISTIC_USAGE.md`** - Realistic mode detailed docs
- **`USAGE.md`** - Original usage documentation

## ❓ Help

```bash
./simple_run.sh --help
```

## ⚠️ Disclaimer

This tool is for **educational purposes** to learn about:
- Git internals and timestamps
- GitHub contribution calculation
- Repository structure and commits

Use responsibly and ethically. Be transparent about your experience.

## 🎓 Educational Use

Learn how:
- Git commits can be backdated
- GitHub calculates contributions
- Project structure is organized
- Commit messages should be written

## 📝 License

MIT License - See LICENSE file

---

## 🚀 Get Started Now

```bash
cd /home/haider/Desktop/github-activity-generator

./simple_run.sh \
  --repo YourUsername/my-project \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --source-repo https://github.com/vercel/next.js.git
```

**That's it!** One command creates authentic GitHub activity. 🎉

---

Made with ❤️ for learning git internals
