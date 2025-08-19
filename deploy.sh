#!/bin/bash

# ArtifAI Git Deployment Script for CapRover

echo "🚀 Starting ArtifAI deployment..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Check if Git LFS is installed
if ! command -v git-lfs &> /dev/null; then
    echo "❌ Error: Git LFS is not installed"
    echo "Please install Git LFS: https://git-lfs.github.io/"
    exit 1
fi

# Verify Git LFS files
echo "📦 Checking Git LFS files..."
git lfs ls-files

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Found uncommitted changes. Adding to git..."
    git add .
    
    # Prompt for commit message
    read -p "Enter commit message (or press Enter for default): " commit_msg
    if [ -z "$commit_msg" ]; then
        commit_msg="Deploy to production $(date '+%Y-%m-%d %H:%M:%S')"
    fi
    
    git commit -m "$commit_msg"
else
    echo "✅ No uncommitted changes found"
fi

# Push to origin
echo "🔄 Pushing to origin..."
git push origin main

# Push LFS files
echo "📤 Pushing LFS files..."
git lfs push origin main

echo "✅ Deployment initiated!"
echo "🌐 Check your CapRover dashboard for build status"
echo "🔗 App will be available at: https://artifa.apps.austinjiang.com"
echo "❤️  Health check: https://artifa.apps.austinjiang.com/health"