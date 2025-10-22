# GitHub Activity Generator - Complete Guide

## 🚀 Quick Start - Choose Your Method

### Method 1: Clone Existing Repo (BEST - Most Authentic)
```bash
./simple_run.sh \
  --repo YourUsername/your-repo \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --source-repo https://github.com/someone/cool-project.git
```

### Method 2: Realistic Generated Commits (Good)
```bash
./simple_run.sh \
  --repo YourUsername/your-repo \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --realistic
```

### Method 3: Simple Commits (Basic)
```bash
./simple_run.sh \
  --repo YourUsername/your-repo \
  --start 2024-01-01 \
  --end 2024-12-31
```

## 📋 All Available Options

```bash
./simple_run.sh \
  --repo <username/repository>     # Required: Your GitHub repo
  --start <YYYY-MM-DD>             # Required: Start date
  --end <YYYY-MM-DD>               # Required: End date
  --source-repo <URL>              # Optional: Clone from existing repo
  --realistic                      # Optional: Use realistic commits
  --min-commits <number>           # Optional: Min commits/day (default: 1)
  --max-commits <number>           # Optional: Max commits/day (default: 5)
  --include-weekends               # Optional: Include Sat/Sun
  --token <github_token>           # Optional: For issues/PRs
```

## 🎯 Complete Workflow

### Step 1: Create GitHub Repository
1. Go to https://github.com/new
2. Create repository (e.g., `my-project`)
3. **Don't** initialize it
4. Copy repo name: `YourUsername/my-project`

### Step 2: Choose Your Method

**For Most Authentic Results:**
```bash
cd /home/haider/Desktop/github-activity-generator

./simple_run.sh \
  --repo YourUsername/my-project \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --source-repo https://github.com/vercel/next.js.git
```

### Step 3: Confirm and Push
- Script asks for confirmation
- Type `yes` to agree
- Script generates commits
- Type `yes` to push to GitHub

### Step 4: Verify Results
- Wait 30-60 minutes
- Check: https://github.com/YourUsername
- View repo: https://github.com/YourUsername/my-project

## 📊 Method Comparison

| Feature | Clone Repo | Realistic | Simple |
|---------|-----------|-----------|--------|
| Real Code | ✅ Actual project | ✅ Generated | ❌ activity.txt only |
| Commit Messages | ✅ Professional | ✅ Professional | ❌ Generic |
| File Variety | ✅ Many files | ✅ Multiple types | ❌ One file |
| Reviewable | ✅ Yes | ✅ Yes | ❌ No |
| Authenticity | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |

## 💡 Recommended Usage

### Single Project
```bash
./simple_run.sh \
  --repo YourUsername/web-app \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --source-repo https://github.com/vercel/nextjs-blog-starter.git
```

### Multiple Projects (Best Strategy)
```bash
# Project 1: Frontend (6 months)
./simple_run.sh \
  --repo YourUsername/react-dashboard \
  --start 2024-01-01 \
  --end 2024-06-30 \
  --source-repo https://github.com/creativetimofficial/material-dashboard-react.git

# Project 2: Backend (4 months)
./simple_run.sh \
  --repo YourUsername/api-server \
  --start 2024-05-01 \
  --end 2024-08-31 \
  --source-repo https://github.com/tiangolo/fastapi.git

# Project 3: Full-Stack (6 months)
./simple_run.sh \
  --repo YourUsername/ecommerce \
  --start 2024-07-01 \
  --end 2024-12-31 \
  --source-repo https://github.com/vercel/commerce.git
```

## 🎨 Popular Source Repositories

### React/Frontend
```bash
https://github.com/vercel/next.js.git
https://github.com/facebook/create-react-app.git
https://github.com/tastejs/todomvc.git
```

### Node.js/Backend
```bash
https://github.com/expressjs/express.git
https://github.com/nestjs/nest.git
https://github.com/tiangolo/fastapi.git
```

### Full-Stack
```bash
https://github.com/vercel/commerce.git
https://github.com/strapi/strapi.git
https://github.com/supabase/supabase.git
```

## ⚙️ Default Behavior

✅ **Automatically skips weekends** (realistic!)
✅ **Random commit times** (9 AM - 8 PM)
✅ **70% activity frequency** (some days no commits)
✅ **1-5 commits** per active day
✅ **Asks before pushing** (safe!)

## 🔧 Common Commands

### Include Weekends
```bash
./simple_run.sh \
  --repo YourUsername/my-repo \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --realistic \
  --include-weekends
```

### More Commits Per Day
```bash
./simple_run.sh \
  --repo YourUsername/my-repo \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --realistic \
  --min-commits 3 \
  --max-commits 8
```

### View Help
```bash
./simple_run.sh --help
```

## 📁 Files Created

After running, files are in:
```
~/Desktop/github-activity-repos/your-repo-name/
```

View locally:
```bash
cd ~/Desktop/github-activity-repos/your-repo-name
git log --oneline
ls -la
```

## 🛠️ Troubleshooting

### Script Not Executable
```bash
chmod +x /home/haider/Desktop/github-activity-generator/simple_run.sh
```

### Python Dependencies Missing
```bash
pip3 install PyGithub requests
```

### SSH Key Issues
Use HTTPS URL instead:
```bash
--source-repo https://github.com/user/repo.git
# NOT: git@github.com:user/repo.git
```

### Repository Already Exists
Delete it first:
```bash
rm -rf ~/Desktop/github-activity-repos/your-repo-name
```

### Contribution Graph Not Updating
- Wait 30-60 minutes
- Check email is verified: https://github.com/settings/emails
- Ensure repo is public or enable private contributions

## ⚠️ Important Notes

### What This Does
- ✅ Creates backdated commits
- ✅ Fills your contribution graph
- ✅ Shows realistic development patterns
- ✅ Uses real or generated code

### What to Remember
- 🎓 Educational purposes
- 🎓 Learn about git internals
- 🎓 Understand GitHub contributions
- ⚠️ Be transparent about experience

### Best Practices
- Use projects you understand
- Match your learning timeline
- Create multiple realistic projects
- Don't claim skills you don't have

## 📚 Documentation Files

- `FINAL_GUIDE.md` - This complete guide
- `CLONE_REPO_GUIDE.md` - Detailed clone method docs
- `REALISTIC_USAGE.md` - Realistic commit mode docs
- `USAGE.md` - Original usage guide

## 🎯 Example: Complete Setup

```bash
# 1. Navigate to directory
cd /home/haider/Desktop/github-activity-generator

# 2. Create GitHub repo at https://github.com/new
#    Name it: my-awesome-project

# 3. Run the generator
./simple_run.sh \
  --repo YourUsername/my-awesome-project \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --source-repo https://github.com/vercel/next.js.git

# 4. Confirm when prompted
# Type: yes (to agree)
# Type: yes (to push)

# 5. Wait 30-60 minutes and check:
# https://github.com/YourUsername
```

## 🚀 Ready to Start?

### Beginner (First Time)
```bash
./simple_run.sh \
  --repo YourUsername/test-repo \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --realistic
```

### Intermediate (Clone Real Code)
```bash
./simple_run.sh \
  --repo YourUsername/my-project \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --source-repo https://github.com/tastejs/todomvc.git
```

### Advanced (Multiple Projects)
Run the script 3-5 times with different repos and date ranges to create a realistic profile showing progression over time.

---

## ✨ Quick Reference

**Most Authentic Command:**
```bash
./simple_run.sh \
  --repo YourUsername/project \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --source-repo https://github.com/someone/project.git
```

**Quick Test:**
```bash
./simple_run.sh \
  --repo YourUsername/test \
  --start 2024-12-01 \
  --end 2024-12-31 \
  --realistic
```

**Help:**
```bash
./simple_run.sh --help
```

---

**Made for educational purposes - Use responsibly!** 🎓
