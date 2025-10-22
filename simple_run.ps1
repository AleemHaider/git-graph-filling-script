# GitHub Activity Generator - PowerShell Version
# Educational Tool

param(
    [Parameter(Mandatory=$false)]
    [string]$Repo,

    [Parameter(Mandatory=$false)]
    [string]$Start,

    [Parameter(Mandatory=$false)]
    [string]$End,

    [Parameter(Mandatory=$false)]
    [int]$MinCommits = 1,

    [Parameter(Mandatory=$false)]
    [int]$MaxCommits = 5,

    [Parameter(Mandatory=$false)]
    [switch]$IncludeWeekends,

    [Parameter(Mandatory=$false)]
    [switch]$Realistic,

    [Parameter(Mandatory=$false)]
    [string]$SourceRepo,

    [Parameter(Mandatory=$false)]
    [string]$Token,

    [Parameter(Mandatory=$false)]
    [switch]$Help
)

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Show-Help {
    Write-Host ""
    Write-Host "Usage: .\simple_run.ps1 -Repo <username/repo> -Start <YYYY-MM-DD> -End <YYYY-MM-DD> [options]"
    Write-Host ""
    Write-Host "Required:"
    Write-Host "  -Repo          GitHub repository (format: username/repository)"
    Write-Host "  -Start         Start date (YYYY-MM-DD)"
    Write-Host "  -End           End date (YYYY-MM-DD)"
    Write-Host ""
    Write-Host "Optional:"
    Write-Host "  -MinCommits    Minimum commits per day (default: 1)"
    Write-Host "  -MaxCommits    Maximum commits per day (default: 5)"
    Write-Host "  -IncludeWeekends   Include Saturday and Sunday"
    Write-Host "  -Realistic     Use realistic commit messages and file changes"
    Write-Host "  -SourceRepo    Clone code from existing GitHub repo (URL)"
    Write-Host "  -Token         GitHub token"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  # Clone existing repo (BEST)"
    Write-Host "  .\simple_run.ps1 -Repo username/myrepo -Start 2024-01-01 -End 2024-12-31 ``"
    Write-Host "     -SourceRepo https://github.com/someone/cool-project.git"
    Write-Host ""
    Write-Host "  # Realistic commits"
    Write-Host "  .\simple_run.ps1 -Repo username/myrepo -Start 2024-01-01 -End 2024-12-31 -Realistic"
    Write-Host ""
    Write-Host "  # Simple commits"
    Write-Host "  .\simple_run.ps1 -Repo username/myrepo -Start 2024-01-01 -End 2024-12-31"
    Write-Host ""
    exit
}

# Show help if requested or missing required params
if ($Help -or -not $Repo -or -not $Start -or -not $End) {
    Show-Help
}

# Print header
Write-Host ""
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "  GitHub Activity Generator" -ForegroundColor Cyan
Write-Host "  Educational Tool - PowerShell Version" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

# Extract username and repo name
$parts = $Repo -split '/'
$GitHubUser = $parts[0]
$RepoName = $parts[1]

# Set local repository path
$RepoPath = Join-Path $env:USERPROFILE "Desktop\github-activity-repos\$RepoName"

# Display configuration
Write-Host ""
Write-ColorOutput "Configuration:" "Blue"
Write-Host "  Repository: $Repo"
Write-Host "  Date Range: $Start to $End"
if ($SourceRepo) {
    Write-Host "  Mode: Clone from source repo"
    Write-Host "  Source: $SourceRepo"
} elseif ($Realistic) {
    Write-Host "  Mode: Realistic generated commits"
    Write-Host "  Commits/Day: $MinCommits-$MaxCommits"
} else {
    Write-Host "  Mode: Simple commits"
    Write-Host "  Commits/Day: $MinCommits-$MaxCommits"
}
$skipWeekends = -not $IncludeWeekends
Write-Host "  Skip Weekends: $skipWeekends"
Write-Host "  Local Path: $RepoPath"
Write-Host ""

# Warning
Write-ColorOutput "WARNING: EDUCATIONAL USE ONLY" "Yellow"
Write-Host "  This tool is for learning about git internals and GitHub API."
Write-Host "  Do not use this to misrepresent your work history."
Write-Host ""
$agree = Read-Host "Do you understand and agree? (yes/no)"
if ($agree -ne "yes") {
    Write-ColorOutput "Aborted by user" "Red"
    exit 1
}

# Check Python
Write-Host ""
Write-ColorOutput "Checking dependencies..." "Blue"
try {
    $null = python --version
} catch {
    Write-ColorOutput "Error: Python is not installed or not in PATH" "Red"
    exit 1
}

# Check Python modules
try {
    python -c "import github" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-ColorOutput "Installing PyGithub..." "Yellow"
        pip install PyGithub requests
    }
} catch {
    Write-ColorOutput "Installing PyGithub..." "Yellow"
    pip install PyGithub requests
}
Write-ColorOutput "Dependencies OK" "Green"
Write-Host ""

# Prepare flags
$SkipWeekendsFlag = ""
if ($IncludeWeekends) {
    $SkipWeekendsFlag = "--include-weekends"
}

$EnableGitHubFeatures = ""
if ($Token) {
    $EnableGitHubFeatures = "--enable-issues-prs --github-token $Token --repo-name $Repo"
}

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Run the appropriate generator
Write-ColorOutput "Running generator..." "Blue"
Write-Host ""

if ($SourceRepo) {
    # Mode 1: Clone from existing repository
    Write-ColorOutput "Cloning and rewriting history from source repository..." "Blue"
    $cmd = "python `"$ScriptDir\clone_and_rewrite.py`" --source `"$SourceRepo`" --target-path `"$RepoPath`" --repo-name `"$RepoName`" --start-date $Start --end-date $End $SkipWeekendsFlag"
    Invoke-Expression $cmd
} elseif ($Realistic) {
    # Mode 2: Realistic generated commits
    Write-ColorOutput "Using realistic commit mode..." "Blue"
    $cmd = "python `"$ScriptDir\realistic_commits.py`" --repo-path `"$RepoPath`" --repo-name `"$RepoName`" --start-date $Start --end-date $End --min-commits $MinCommits --max-commits $MaxCommits $SkipWeekendsFlag"
    Invoke-Expression $cmd
} else {
    # Mode 3: Simple commits
    $cmd = "python `"$ScriptDir\github_full_activity_generator.py`" --start-date $Start --end-date $End --repo-path `"$RepoPath`" --repo-name-local `"$RepoName`" --min-commits $MinCommits --max-commits $MaxCommits $SkipWeekendsFlag $EnableGitHubFeatures"
    Invoke-Expression $cmd
}

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-ColorOutput "Error: Generation failed" "Red"
    exit 1
}

Write-Host ""
Write-ColorOutput "Activity generated successfully" "Green"
Write-Host ""

# Ask if user wants to push
$push = Read-Host "Push to GitHub now? (yes/no)"
if ($push -ne "yes") {
    Write-Host ""
    Write-ColorOutput "Skipping push. You can push manually later:" "Blue"
    Write-Host "  cd `"$RepoPath`""
    Write-Host "  git remote add origin git@github.com:$Repo.git"
    Write-Host "  git push -u origin main --force"
    exit 0
}

# Push to GitHub
Write-Host ""
Write-ColorOutput "Pushing to GitHub..." "Blue"
Write-Host ""

Push-Location $RepoPath

# Configure git user
git config user.name $GitHubUser
git config user.email "$GitHubUser@users.noreply.github.com"

# Add remote
git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0) {
    git remote add origin "git@github.com:$Repo.git"
} else {
    git remote set-url origin "git@github.com:$Repo.git"
}

# Push
git branch -M main
git push -u origin main --force

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-ColorOutput "Error: Push failed" "Red"
    Write-Host ""
    Write-ColorOutput "Common issues:" "Yellow"
    Write-Host "  1. Repository doesn't exist - create it at https://github.com/new"
    Write-Host "  2. SSH key not configured - see https://docs.github.com/en/authentication"
    Write-Host "  3. Wrong repository name - check format: username/repo"
    Pop-Location
    exit 1
}

Pop-Location

Write-Host ""
Write-Host "==============================================" -ForegroundColor Green
Write-Host "  SUCCESS!" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green
Write-Host ""
Write-Host "View your activity:"
Write-Host "  Profile: https://github.com/$GitHubUser"
Write-Host "  Repository: https://github.com/$Repo"
Write-Host ""
Write-ColorOutput "Contribution graph updates in 30-60 minutes" "Blue"
Write-Host ""
