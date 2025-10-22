#!/bin/bash

###############################################################################
# GitHub Activity Generator - Educational Tool
###############################################################################
#
# ⚠️  EDUCATIONAL PURPOSE ONLY ⚠️
# This tool demonstrates git internals and GitHub API usage.
# Using this to misrepresent your work history is unethical and may violate
# GitHub's Terms of Service.
#
# Use responsibly and transparently.
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() { echo -e "${BLUE}ℹ${NC} $1"; }
print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }

# Print header
echo ""
echo "=============================================="
echo "  GitHub Activity Generator"
echo "  Educational Tool"
echo "=============================================="
echo ""

# Parse command line arguments
GITHUB_REPO=""
START_DATE=""
END_DATE=""
MIN_COMMITS="1"
MAX_COMMITS="5"
SKIP_WEEKENDS="true"
USE_REALISTIC="false"
SOURCE_REPO=""

# Show usage
usage() {
    echo "Usage: $0 --repo <username/repo> --start <YYYY-MM-DD> --end <YYYY-MM-DD> [options]"
    echo ""
    echo "Required:"
    echo "  --repo          GitHub repository (format: username/repository)"
    echo "  --start         Start date (YYYY-MM-DD)"
    echo "  --end           End date (YYYY-MM-DD)"
    echo ""
    echo "Optional:"
    echo "  --min-commits   Minimum commits per day (default: 1)"
    echo "  --max-commits   Maximum commits per day (default: 5)"
    echo "  --include-weekends  Include Saturday and Sunday"
    echo "  --realistic     Use realistic commit messages and file changes"
    echo "  --source-repo   Clone code from existing GitHub repo (URL)"
    echo "  --token         GitHub token (or use GITHUB_TOKEN env var)"
    echo ""
    echo "Examples:"
    echo "  # Clone existing repo and rewrite history (BEST)"
    echo "  $0 --repo username/myrepo --start 2024-01-01 --end 2024-12-31 \\"
    echo "     --source-repo https://github.com/someone/cool-project.git"
    echo ""
    echo "  # Realistic commits with generated code"
    echo "  $0 --repo username/myrepo --start 2024-01-01 --end 2024-12-31 --realistic"
    echo ""
    echo "  # Simple commits"
    echo "  $0 --repo username/myrepo --start 2024-01-01 --end 2024-12-31"
    echo ""
    exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --repo)
            GITHUB_REPO="$2"
            shift 2
            ;;
        --start)
            START_DATE="$2"
            shift 2
            ;;
        --end)
            END_DATE="$2"
            shift 2
            ;;
        --min-commits)
            MIN_COMMITS="$2"
            shift 2
            ;;
        --max-commits)
            MAX_COMMITS="$2"
            shift 2
            ;;
        --include-weekends)
            SKIP_WEEKENDS="false"
            shift
            ;;
        --realistic)
            USE_REALISTIC="true"
            shift
            ;;
        --source-repo)
            SOURCE_REPO="$2"
            shift 2
            ;;
        --token)
            GITHUB_TOKEN="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            print_error "Unknown option: $1"
            usage
            ;;
    esac
done

# Validate required arguments
if [ -z "$GITHUB_REPO" ] || [ -z "$START_DATE" ] || [ -z "$END_DATE" ]; then
    print_error "Missing required arguments"
    echo ""
    usage
fi

# Validate date format
if ! [[ "$START_DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || ! [[ "$END_DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    print_error "Invalid date format. Use YYYY-MM-DD"
    exit 1
fi

# Extract username from repo
GITHUB_USER=$(echo "$GITHUB_REPO" | cut -d'/' -f1)
REPO_NAME=$(echo "$GITHUB_REPO" | cut -d'/' -f2)

# Set local repository path
REPO_PATH="$HOME/Desktop/github-activity-repos/$REPO_NAME"

# Display configuration
echo ""
print_info "Configuration:"
echo "  Repository: $GITHUB_REPO"
echo "  Date Range: $START_DATE to $END_DATE"
if [ -n "$SOURCE_REPO" ]; then
    echo "  Mode: Clone from source repo"
    echo "  Source: $SOURCE_REPO"
elif [ "$USE_REALISTIC" = "true" ]; then
    echo "  Mode: Realistic generated commits"
    echo "  Commits/Day: $MIN_COMMITS-$MAX_COMMITS"
else
    echo "  Mode: Simple commits"
    echo "  Commits/Day: $MIN_COMMITS-$MAX_COMMITS"
fi
echo "  Skip Weekends: $SKIP_WEEKENDS"
echo "  Local Path: $REPO_PATH"
echo ""

# Warning about ethical use
print_warning "EDUCATIONAL USE ONLY"
echo "  This tool is for learning about git internals and GitHub API."
echo "  Do not use this to misrepresent your work history."
echo ""
read -p "Do you understand and agree? (yes/no): " -r
echo ""
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    print_error "Aborted by user"
    exit 1
fi

# Check dependencies
print_info "Checking dependencies..."
if ! command -v python3 &> /dev/null; then
    print_error "python3 is not installed"
    exit 1
fi

if ! python3 -c "import github" 2>/dev/null; then
    print_warning "PyGithub not found. Installing..."
    pip3 install PyGithub requests
fi
print_success "Dependencies OK"
echo ""

# Determine if we should enable GitHub features
ENABLE_GITHUB_FEATURES=""
if [ -n "$GITHUB_TOKEN" ]; then
    print_info "GitHub token found - will create issues and PRs"
    ENABLE_GITHUB_FEATURES="--enable-issues-prs --github-token $GITHUB_TOKEN --repo-name $GITHUB_REPO"
else
    print_info "No GitHub token - commits only"
fi

# Run the generator
print_info "Running generator..."
echo ""

SKIP_WEEKENDS_FLAG=""
if [ "$SKIP_WEEKENDS" = "true" ]; then
    SKIP_WEEKENDS_FLAG=""
else
    SKIP_WEEKENDS_FLAG="--include-weekends"
fi

# Choose mode based on options
if [ -n "$SOURCE_REPO" ]; then
    # Mode 1: Clone from existing repository
    print_info "Cloning and rewriting history from source repository..."
    python3 "$(dirname "$0")/clone_and_rewrite.py" \
        --source "$SOURCE_REPO" \
        --target-path "$REPO_PATH" \
        --repo-name "$REPO_NAME" \
        --start-date "$START_DATE" \
        --end-date "$END_DATE" \
        $SKIP_WEEKENDS_FLAG
elif [ "$USE_REALISTIC" = "true" ]; then
    # Mode 2: Realistic generated commits
    print_info "Using realistic commit mode..."
    python3 "$(dirname "$0")/realistic_commits.py" \
        --repo-path "$REPO_PATH" \
        --repo-name "$REPO_NAME" \
        --start-date "$START_DATE" \
        --end-date "$END_DATE" \
        --min-commits "$MIN_COMMITS" \
        --max-commits "$MAX_COMMITS" \
        $SKIP_WEEKENDS_FLAG
else
    # Mode 3: Simple commits
    python3 "$(dirname "$0")/github_full_activity_generator.py" \
        --start-date "$START_DATE" \
        --end-date "$END_DATE" \
        --repo-path "$REPO_PATH" \
        --repo-name-local "$REPO_NAME" \
        --min-commits "$MIN_COMMITS" \
        --max-commits "$MAX_COMMITS" \
        $SKIP_WEEKENDS_FLAG \
        $ENABLE_GITHUB_FEATURES
fi

# Check if generation was successful
if [ $? -ne 0 ]; then
    print_error "Generation failed"
    exit 1
fi

echo ""
print_success "Activity generated successfully"
echo ""

# Ask if user wants to push
read -p "Push to GitHub now? (yes/no): " -r
echo ""
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    print_info "Skipping push. You can push manually later:"
    echo "  cd $REPO_PATH"
    echo "  git remote add origin git@github.com:$GITHUB_REPO.git"
    echo "  git push -u origin main --force"
    exit 0
fi

# Push to GitHub
print_info "Pushing to GitHub..."
echo ""

cd "$REPO_PATH"

# Configure git user
git config user.name "$GITHUB_USER"
git config user.email "${GITHUB_USER}@users.noreply.github.com"

# Add remote
if git remote get-url origin &>/dev/null; then
    git remote set-url origin "git@github.com:$GITHUB_REPO.git"
else
    git remote add origin "git@github.com:$GITHUB_REPO.git"
fi

# Push
git branch -M main
if git push -u origin main --force; then
    echo ""
    print_success "Successfully pushed to GitHub!"
    echo ""
    echo "📊 View your activity:"
    echo "   Profile: https://github.com/$GITHUB_USER"
    echo "   Repository: https://github.com/$GITHUB_REPO"
    echo ""
    print_info "Contribution graph updates in 30-60 minutes"
    echo ""
else
    print_error "Push failed. Check the error above."
    echo ""
    print_info "Common issues:"
    echo "  1. Repository doesn't exist - create it first at https://github.com/new"
    echo "  2. SSH key not configured - see https://docs.github.com/en/authentication"
    echo "  3. Wrong repository name - check the format: username/repo"
    exit 1
fi
