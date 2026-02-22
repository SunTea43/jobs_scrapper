# GitHub Setup Guide

Your repository has been initialized locally! Follow these steps to push it to GitHub:

## Step 1: Create a GitHub Repository

1. Go to <https://github.com/new>
2. Repository name: `linkedinSearcher` (or your preferred name)
3. Description: "Job scraper for LinkedIn and Computrabajo with filtering by company ratings and salary"
4. Choose: **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Push Your Code

After creating the repository on GitHub, run these commands:

```bash
cd /Users/santiagoperez/linkedinSearcher

# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/linkedinSearcher.git

# Push your code
git push -u origin main
```

## Step 3: Verify

Visit your repository at: `https://github.com/YOUR_USERNAME/linkedinSearcher`

You should see:

- ✅ README.md with project documentation
- ✅ computrabajo_searcher.py
- ✅ linkedin_scrapper.py
- ✅ linkedin_searcher.py
- ✅ requirements.txt
- ✅ .gitignore

## Alternative: Using GitHub CLI

If you have GitHub CLI installed:

```bash
cd /Users/santiagoperez/linkedinSearcher
gh repo create linkedinSearcher --public --source=. --push
```

## Next Steps

### Update README

Edit the README.md to replace `YOUR_USERNAME` with your actual GitHub username in the clone command.

### Add Topics/Tags

On GitHub, add topics like:

- `web-scraping`
- `python`
- `playwright`
- `job-search`
- `linkedin`
- `computrabajo`

### Enable GitHub Actions (Optional)

You could add automated testing or linting in the future.

## Current Status

✅ Git repository initialized
✅ All files committed
✅ Branch renamed to 'main'
✅ Git config set with your email: <santipego0001@gmail.com>

Ready to push to GitHub! 🚀
