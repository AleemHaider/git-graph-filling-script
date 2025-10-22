# Windows Usage Guide

## ✅ Yes, It Works on Windows!

This project works on Windows using either:
1. **Batch Script** (`.bat`) - Works on all Windows versions
2. **PowerShell** (`.ps1`) - Recommended for Windows 10/11

## 🚀 Quick Start (Windows)

### Method 1: Using Batch File (Easiest)

Open **Command Prompt** and run:

```cmd
cd %USERPROFILE%\Desktop\github-activity-generator

simple_run.bat ^
  --repo YourUsername/your-repo ^
  --start 2024-01-01 ^
  --end 2024-12-31 ^
  --realistic
```

### Method 2: Using PowerShell (Recommended)

Open **PowerShell** and run:

```powershell
cd $env:USERPROFILE\Desktop\github-activity-generator

.\simple_run.ps1 `
  -Repo YourUsername/your-repo `
  -Start 2024-01-01 `
  -End 2024-12-31 `
  -Realistic
```

## 📦 Prerequisites

### 1. Install Python

Download from: https://www.python.org/downloads/

**Important:** Check "Add Python to PATH" during installation

Verify installation:
```cmd
python --version
```

### 2. Install Git

Download from: https://git-scm.com/download/win

Verify installation:
```cmd
git --version
```

### 3. Install Dependencies

```cmd
pip install PyGithub requests
```

## 💻 Command Prompt Usage

### Basic Command

```cmd
simple_run.bat --repo username/repo --start 2024-01-01 --end 2024-12-31
```

### Clone Existing Repo (Best Method)

```cmd
simple_run.bat ^
  --repo username/my-project ^
  --start 2024-01-01 ^
  --end 2024-12-31 ^
  --source-repo https://github.com/vercel/next.js.git
```

### Realistic Generated Code

```cmd
simple_run.bat ^
  --repo username/my-project ^
  --start 2024-01-01 ^
  --end 2024-12-31 ^
  --realistic
```

### More Commits Per Day

```cmd
simple_run.bat ^
  --repo username/my-project ^
  --start 2024-01-01 ^
  --end 2024-12-31 ^
  --realistic ^
  --min-commits 3 ^
  --max-commits 8
```

### Include Weekends

```cmd
simple_run.bat ^
  --repo username/my-project ^
  --start 2024-01-01 ^
  --end 2024-12-31 ^
  --realistic ^
  --include-weekends
```

### View Help

```cmd
simple_run.bat --help
```

## 🔷 PowerShell Usage

### Enable Script Execution (First Time Only)

Open PowerShell as Administrator:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Basic Command

```powershell
.\simple_run.ps1 -Repo username/repo -Start 2024-01-01 -End 2024-12-31
```

### Clone Existing Repo (Best Method)

```powershell
.\simple_run.ps1 `
  -Repo username/my-project `
  -Start 2024-01-01 `
  -End 2024-12-31 `
  -SourceRepo https://github.com/vercel/next.js.git
```

### Realistic Generated Code

```powershell
.\simple_run.ps1 `
  -Repo username/my-project `
  -Start 2024-01-01 `
  -End 2024-12-31 `
  -Realistic
```

### More Commits Per Day

```powershell
.\simple_run.ps1 `
  -Repo username/my-project `
  -Start 2024-01-01 `
  -End 2024-12-31 `
  -Realistic `
  -MinCommits 3 `
  -MaxCommits 8
```

### Include Weekends

```powershell
.\simple_run.ps1 `
  -Repo username/my-project `
  -Start 2024-01-01 `
  -End 2024-12-31 `
  -Realistic `
  -IncludeWeekends
```

### View Help

```powershell
.\simple_run.ps1 -Help
```

## 📁 File Locations (Windows)

Generated repositories are saved to:
```
C:\Users\YourUsername\Desktop\github-activity-repos\
```

View generated repo:
```cmd
cd %USERPROFILE%\Desktop\github-activity-repos\your-repo-name
git log --oneline
```

Or in PowerShell:
```powershell
cd $env:USERPROFILE\Desktop\github-activity-repos\your-repo-name
git log --oneline
```

## 📊 Complete Example (Command Prompt)

```cmd
REM 1. Navigate to project directory
cd %USERPROFILE%\Desktop\github-activity-generator

REM 2. Create GitHub repository at https://github.com/new

REM 3. Run the generator
simple_run.bat ^
  --repo YourUsername/my-project ^
  --start 2024-01-01 ^
  --end 2024-12-31 ^
  --source-repo https://github.com/tastejs/todomvc.git

REM 4. Type "yes" when prompted
REM 5. Wait 30-60 minutes and check GitHub
```

## 📊 Complete Example (PowerShell)

```powershell
# 1. Navigate to project directory
cd $env:USERPROFILE\Desktop\github-activity-generator

# 2. Create GitHub repository at https://github.com/new

# 3. Run the generator
.\simple_run.ps1 `
  -Repo YourUsername/my-project `
  -Start 2024-01-01 `
  -End 2024-12-31 `
  -SourceRepo https://github.com/tastejs/todomvc.git

# 4. Type "yes" when prompted
# 5. Wait 30-60 minutes and check GitHub
```

## 🎯 All Options

### Command Prompt (Batch)

| Option | Description |
|--------|-------------|
| `--repo` | GitHub repository (username/repo) |
| `--start` | Start date (YYYY-MM-DD) |
| `--end` | End date (YYYY-MM-DD) |
| `--source-repo` | Clone from existing repo URL |
| `--realistic` | Use realistic commits |
| `--min-commits` | Min commits per day (default: 1) |
| `--max-commits` | Max commits per day (default: 5) |
| `--include-weekends` | Include Saturday/Sunday |
| `--token` | GitHub token |
| `--help` | Show help |

### PowerShell

| Option | Description |
|--------|-------------|
| `-Repo` | GitHub repository (username/repo) |
| `-Start` | Start date (YYYY-MM-DD) |
| `-End` | End date (YYYY-MM-DD) |
| `-SourceRepo` | Clone from existing repo URL |
| `-Realistic` | Use realistic commits |
| `-MinCommits` | Min commits per day (default: 1) |
| `-MaxCommits` | Max commits per day (default: 5) |
| `-IncludeWeekends` | Include Saturday/Sunday |
| `-Token` | GitHub token |
| `-Help` | Show help |

## ⚙️ Git Bash Alternative

If you have **Git Bash** installed, you can also use the Linux script:

```bash
cd ~/Desktop/github-activity-generator

./simple_run.sh \
  --repo username/repo \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --realistic
```

## 🐛 Windows Troubleshooting

### Python Not Found

**Error:** `'python' is not recognized`

**Solution:**
1. Reinstall Python from https://www.python.org/downloads/
2. Check "Add Python to PATH"
3. Restart Command Prompt/PowerShell

### Git Not Found

**Error:** `'git' is not recognized`

**Solution:**
1. Install Git from https://git-scm.com/download/win
2. Restart Command Prompt/PowerShell

### PowerShell Script Execution Error

**Error:** `cannot be loaded because running scripts is disabled`

**Solution:**
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Long Path Issues

**Error:** Path too long errors

**Solution:** Enable long paths:
```cmd
git config --global core.longpaths true
```

### SSH Key Issues

**Error:** Permission denied (publickey)

**Solution:** Generate SSH key:
```cmd
ssh-keygen -t ed25519 -C "your_email@example.com"
type %USERPROFILE%\.ssh\id_ed25519.pub
```

Add the key to GitHub: https://github.com/settings/keys

Or use HTTPS URLs instead:
```cmd
--source-repo https://github.com/user/repo.git
```

## 📝 Path Differences

### Linux/Mac
```bash
~/Desktop/github-activity-generator
```

### Windows (Command Prompt)
```cmd
%USERPROFILE%\Desktop\github-activity-generator
```

### Windows (PowerShell)
```powershell
$env:USERPROFILE\Desktop\github-activity-generator
```

## 🎨 Popular Source Repos (Windows Compatible)

All these work perfectly on Windows:

### Frontend
```
https://github.com/vercel/next.js.git
https://github.com/facebook/create-react-app.git
https://github.com/tastejs/todomvc.git
```

### Backend
```
https://github.com/expressjs/express.git
https://github.com/nestjs/nest.git
https://github.com/fastify/fastify.git
```

### Full-Stack
```
https://github.com/vercel/commerce.git
https://github.com/strapi/strapi.git
```

## ✅ Feature Compatibility

All features work on Windows:

✅ Clone existing repositories
✅ Realistic generated commits
✅ Simple commits
✅ Skip weekends (automatic)
✅ Custom commit frequency
✅ Backdated timestamps
✅ Push to GitHub

## 🚀 Recommended Windows Command

**Command Prompt:**
```cmd
simple_run.bat ^
  --repo YourUsername/my-project ^
  --start 2024-01-01 ^
  --end 2024-12-31 ^
  --source-repo https://github.com/vercel/next.js.git
```

**PowerShell:**
```powershell
.\simple_run.ps1 `
  -Repo YourUsername/my-project `
  -Start 2024-01-01 `
  -End 2024-12-31 `
  -SourceRepo https://github.com/vercel/next.js.git
```

Both work identically - choose whichever you prefer!

---

**Everything works on Windows!** 🎉
