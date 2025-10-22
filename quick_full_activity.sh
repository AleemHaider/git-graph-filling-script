#!/bin/bash

# Quick Full Activity Generator
# Generates commits, issues, PRs, and code reviews

echo "=============================================="
echo "GitHub Full Activity Generator"
echo "=============================================="
echo ""

# Configuration
START_DATE="2021-01-01"
END_DATE="2025-10-14"
REPO_PATH="/home/haider/Desktop/github-activity"
GITHUB_USER="AleemHaider"
GITHUB_REPO="inventory-app"
REPO_FULL_NAME="$GITHUB_USER/$GITHUB_REPO"

echo "📅 Date Range: $START_DATE to $END_DATE"
echo "📁 Repository: $REPO_FULL_NAME"
echo ""

# Check if token is provided
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  No GITHUB_TOKEN environment variable found"
    echo ""
    echo "To create issues and PRs, you need a GitHub token:"
    echo "1. Create token at: https://github.com/settings/tokens"
    echo "2. Select 'repo' permission"
    echo "3. Export it: export GITHUB_TOKEN='your_token_here'"
    echo ""
    echo "Continuing with COMMITS ONLY..."
    echo ""
    read -p "Press Enter to continue..."

    # Run without GitHub features
    python3 /home/haider/Desktop/github-activity-generator/github_full_activity_generator.py \
        --start-date "$START_DATE" \
        --end-date "$END_DATE" \
        --repo-path "$REPO_PATH" \
        --min-commits 1 \
        --max-commits 5 \
        --frequency 0.7

else
    echo "✅ GitHub token found!"
    echo ""
    echo "Will generate:"
    echo "  ✓ Commits (backdated)"
    echo "  ✓ Issues"
    echo "  ✓ Pull Requests"
    echo "  ✓ Code Reviews"
    echo ""
    read -p "Press Enter to start..."

    # Check dependencies
    echo ""
    echo "Checking dependencies..."
    pip3 list | grep -q PyGithub
    if [ $? -ne 0 ]; then
        echo "Installing PyGithub..."
        pip3 install PyGithub requests
    else
        echo "✓ Dependencies installed"
    fi

    # Run with full features
    python3 /home/haider/Desktop/github-activity-generator/github_full_activity_generator.py \
        --start-date "$START_DATE" \
        --end-date "$END_DATE" \
        --repo-path "$REPO_PATH" \
        --github-token "$GITHUB_TOKEN" \
        --repo-name "$REPO_FULL_NAME" \
        --enable-issues-prs \
        --min-commits 1 \
        --max-commits 5 \
        --frequency 0.7
fi

# Check if generation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "=============================================="
    echo "Pushing to GitHub..."
    echo "=============================================="

    cd "$REPO_PATH"

    # Configure git
    git config user.name "$GITHUB_USER"
    git config user.email "aleemhaider111@gmail.com"

    # Add remote and push
    git remote add origin git@github.com:$REPO_FULL_NAME.git 2>/dev/null || \
        git remote set-url origin git@github.com:$REPO_FULL_NAME.git

    git branch -M main
    git push -u origin main --force

    if [ $? -eq 0 ]; then
        echo ""
        echo "=============================================="
        echo "✅ SUCCESS!"
        echo "=============================================="
        echo ""
        echo "🎉 Your GitHub activity has been generated!"
        echo ""
        echo "📊 Check your profile:"
        echo "   https://github.com/$GITHUB_USER"
        echo ""
        echo "📁 Repository:"
        echo "   https://github.com/$REPO_FULL_NAME"
        echo ""
        echo "⏱️  Contribution graph will update in 30-60 minutes"
        echo ""
        echo "💡 Make sure your email is verified:"
        echo "   https://github.com/settings/emails"
        echo ""
    else
        echo ""
        echo "❌ Push failed. Check the error above."
    fi
else
    echo ""
    echo "❌ Generation failed. Check the error above."
fi
