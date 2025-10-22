@echo off
REM GitHub Activity Generator - Windows Version
REM Educational Tool

setlocal EnableDelayedExpansion

echo.
echo ==============================================
echo   GitHub Activity Generator
echo   Educational Tool - Windows Version
echo ==============================================
echo.

REM Parse arguments
set "GITHUB_REPO="
set "START_DATE="
set "END_DATE="
set "MIN_COMMITS=1"
set "MAX_COMMITS=5"
set "SKIP_WEEKENDS=true"
set "USE_REALISTIC=false"
set "SOURCE_REPO="
set "GITHUB_TOKEN="

:parse_args
if "%~1"=="" goto end_parse
if "%~1"=="--repo" (
    set "GITHUB_REPO=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--start" (
    set "START_DATE=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--end" (
    set "END_DATE=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--min-commits" (
    set "MIN_COMMITS=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--max-commits" (
    set "MAX_COMMITS=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--include-weekends" (
    set "SKIP_WEEKENDS=false"
    shift
    goto parse_args
)
if "%~1"=="--realistic" (
    set "USE_REALISTIC=true"
    shift
    goto parse_args
)
if "%~1"=="--source-repo" (
    set "SOURCE_REPO=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--token" (
    set "GITHUB_TOKEN=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--help" (
    goto show_help
)
if "%~1"=="-h" (
    goto show_help
)
echo Error: Unknown option %~1
goto show_help

:end_parse

REM Validate required arguments
if "%GITHUB_REPO%"=="" (
    echo Error: --repo is required
    echo.
    goto show_help
)
if "%START_DATE%"=="" (
    echo Error: --start is required
    echo.
    goto show_help
)
if "%END_DATE%"=="" (
    echo Error: --end is required
    echo.
    goto show_help
)

REM Extract username and repo name
for /f "tokens=1,2 delims=/" %%a in ("%GITHUB_REPO%") do (
    set "GITHUB_USER=%%a"
    set "REPO_NAME=%%b"
)

REM Set local repository path
set "REPO_PATH=%USERPROFILE%\Desktop\github-activity-repos\%REPO_NAME%"

REM Display configuration
echo.
echo Configuration:
echo   Repository: %GITHUB_REPO%
echo   Date Range: %START_DATE% to %END_DATE%
if not "%SOURCE_REPO%"=="" (
    echo   Mode: Clone from source repo
    echo   Source: %SOURCE_REPO%
) else if "%USE_REALISTIC%"=="true" (
    echo   Mode: Realistic generated commits
    echo   Commits/Day: %MIN_COMMITS%-%MAX_COMMITS%
) else (
    echo   Mode: Simple commits
    echo   Commits/Day: %MIN_COMMITS%-%MAX_COMMITS%
)
echo   Skip Weekends: %SKIP_WEEKENDS%
echo   Local Path: %REPO_PATH%
echo.

REM Warning
echo WARNING: EDUCATIONAL USE ONLY
echo   This tool is for learning about git internals and GitHub API.
echo   Do not use this to misrepresent your work history.
echo.
set /p "AGREE=Do you understand and agree? (yes/no): "
if /i not "%AGREE%"=="yes" (
    echo Aborted by user
    exit /b 1
)

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Check dependencies
echo.
echo Checking dependencies...
python -c "import github" 2>nul
if errorlevel 1 (
    echo Installing PyGithub...
    pip install PyGithub requests
)
echo Dependencies OK
echo.

REM Prepare flags
set "SKIP_WEEKENDS_FLAG="
if "%SKIP_WEEKENDS%"=="false" (
    set "SKIP_WEEKENDS_FLAG=--include-weekends"
)

set "ENABLE_GITHUB_FEATURES="
if not "%GITHUB_TOKEN%"=="" (
    set "ENABLE_GITHUB_FEATURES=--enable-issues-prs --github-token %GITHUB_TOKEN% --repo-name %GITHUB_REPO%"
)

REM Get script directory
set "SCRIPT_DIR=%~dp0"

REM Run the appropriate generator
echo Running generator...
echo.

if not "%SOURCE_REPO%"=="" (
    REM Mode 1: Clone from existing repository
    echo Cloning and rewriting history from source repository...
    python "%SCRIPT_DIR%clone_and_rewrite.py" --source "%SOURCE_REPO%" --target-path "%REPO_PATH%" --repo-name "%REPO_NAME%" --start-date %START_DATE% --end-date %END_DATE% %SKIP_WEEKENDS_FLAG%
) else if "%USE_REALISTIC%"=="true" (
    REM Mode 2: Realistic generated commits
    echo Using realistic commit mode...
    python "%SCRIPT_DIR%realistic_commits.py" --repo-path "%REPO_PATH%" --repo-name "%REPO_NAME%" --start-date %START_DATE% --end-date %END_DATE% --min-commits %MIN_COMMITS% --max-commits %MAX_COMMITS% %SKIP_WEEKENDS_FLAG%
) else (
    REM Mode 3: Simple commits
    python "%SCRIPT_DIR%github_full_activity_generator.py" --start-date %START_DATE% --end-date %END_DATE% --repo-path "%REPO_PATH%" --repo-name-local "%REPO_NAME%" --min-commits %MIN_COMMITS% --max-commits %MAX_COMMITS% %SKIP_WEEKENDS_FLAG% %ENABLE_GITHUB_FEATURES%
)

if errorlevel 1 (
    echo.
    echo Error: Generation failed
    exit /b 1
)

echo.
echo Activity generated successfully
echo.

REM Ask if user wants to push
set /p "PUSH=Push to GitHub now? (yes/no): "
if /i not "%PUSH%"=="yes" (
    echo.
    echo Skipping push. You can push manually later:
    echo   cd "%REPO_PATH%"
    echo   git remote add origin git@github.com:%GITHUB_REPO%.git
    echo   git push -u origin main --force
    exit /b 0
)

REM Push to GitHub
echo.
echo Pushing to GitHub...
echo.

cd /d "%REPO_PATH%"

REM Configure git user
git config user.name "%GITHUB_USER%"
git config user.email "%GITHUB_USER%@users.noreply.github.com"

REM Add remote
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    git remote add origin git@github.com:%GITHUB_REPO%.git
) else (
    git remote set-url origin git@github.com:%GITHUB_REPO%.git
)

REM Push
git branch -M main
git push -u origin main --force

if errorlevel 1 (
    echo.
    echo Error: Push failed
    echo.
    echo Common issues:
    echo   1. Repository doesn't exist - create it at https://github.com/new
    echo   2. SSH key not configured - see https://docs.github.com/en/authentication
    echo   3. Wrong repository name - check format: username/repo
    exit /b 1
)

echo.
echo ==============================================
echo   SUCCESS!
echo ==============================================
echo.
echo View your activity:
echo   Profile: https://github.com/%GITHUB_USER%
echo   Repository: https://github.com/%GITHUB_REPO%
echo.
echo Contribution graph updates in 30-60 minutes
echo.

exit /b 0

:show_help
echo Usage: simple_run.bat --repo ^<username/repo^> --start ^<YYYY-MM-DD^> --end ^<YYYY-MM-DD^> [options]
echo.
echo Required:
echo   --repo          GitHub repository (format: username/repository)
echo   --start         Start date (YYYY-MM-DD)
echo   --end           End date (YYYY-MM-DD)
echo.
echo Optional:
echo   --min-commits   Minimum commits per day (default: 1)
echo   --max-commits   Maximum commits per day (default: 5)
echo   --include-weekends  Include Saturday and Sunday
echo   --realistic     Use realistic commit messages and file changes
echo   --source-repo   Clone code from existing GitHub repo (URL)
echo   --token         GitHub token (or use GITHUB_TOKEN env var)
echo.
echo Examples:
echo   REM Clone existing repo and rewrite history (BEST)
echo   simple_run.bat --repo username/myrepo --start 2024-01-01 --end 2024-12-31 ^
echo      --source-repo https://github.com/someone/cool-project.git
echo.
echo   REM Realistic commits with generated code
echo   simple_run.bat --repo username/myrepo --start 2024-01-01 --end 2024-12-31 --realistic
echo.
echo   REM Simple commits
echo   simple_run.bat --repo username/myrepo --start 2024-01-01 --end 2024-12-31
echo.
exit /b 1
