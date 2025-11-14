# Git Workflow Quick Reference Card

> **Quick commands for daily development with Trunk-Based Development**

## Daily Workflow

### Start New Feature

```bash
# 1. Update main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/TASK-123-add-payment-validation

# 3. Verify branch
git branch
```

### Work on Feature

```bash
# Make changes...

# Commit frequently (2-3 times per day)
git add .
git commit -m "feat(payments): add credit card validation"

# Push to remote
git push -u origin feature/TASK-123-add-payment-validation
# (subsequent pushes: just `git push`)
```

### Keep Branch Updated

```bash
# Option A: Rebase (recommended - clean history)
git checkout main && git pull origin main
git checkout feature/TASK-123-add-payment-validation
git rebase main
# If conflicts: fix → git add . → git rebase --continue
git push --force-with-lease

# Option B: Merge (simpler)
git merge origin/main
# If conflicts: fix → git add . → git commit
git push
```

### Create Pull Request

```bash
# Via GitHub CLI
gh pr create \
  --title "feat(payments): Add credit card validation" \
  --body "Implements validation as per TASK-123"

# Or via GitHub UI
# → "Pull requests" → "New pull request"
```

### After Merge

```bash
# Switch to main
git checkout main
git pull origin main

# Delete local branch
git branch -d feature/TASK-123-add-payment-validation

# Delete remote (if not auto-deleted)
git push origin --delete feature/TASK-123-add-payment-validation
```

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `refactor` - Code refactoring
- `test` - Tests
- `chore` - Maintenance

### Examples

```bash
feat(orders): add order cancellation endpoint
fix(payments): resolve timeout on card validation
docs(api): update payment API documentation
refactor(inventory): simplify stock reservation
test(orders): add integration tests for order flow
```

## Hotfix Workflow

```bash
# 1. Create hotfix from main
git checkout main && git pull origin main
git checkout -b hotfix/FIX-payment-timeout

# 2. Fix the issue (minimal changes)
# ...

# 3. Commit
git commit -m "hotfix(payments): fix timeout in validation"

# 4. Push and create urgent PR
git push -u origin hotfix/FIX-payment-timeout
gh pr create --title "hotfix: Fix payment timeout" --label "hotfix"

# 5. Fast-track review (< 1 hour)
# 6. Merge and deploy immediately
# 7. Create patch release tag
git tag -a v1.2.1 -m "Hotfix: Payment timeout"
git push origin v1.2.1
```

## Common Operations

### Update from Main

```bash
git fetch origin
git rebase origin/main
```

### Undo Last Commit (Not Pushed)

```bash
git reset --soft HEAD~1  # Keep changes staged
# or
git reset HEAD~1         # Keep changes unstaged
```

### Discard All Local Changes

```bash
git checkout .           # Discard unstaged
git reset --hard HEAD    # Discard all changes
```

### View Commit History

```bash
git log --oneline --graph --decorate -10
```

### Check Branch Status

```bash
git status
git diff                 # Unstaged changes
git diff --staged        # Staged changes
```

### Stash Changes

```bash
git stash                # Save changes
git stash list           # List stashes
git stash pop            # Apply and remove latest stash
git stash apply          # Apply without removing
```

### Cherry-Pick Commit

```bash
git cherry-pick <commit-hash>
```

## Resolving Conflicts

### During Rebase

```bash
# 1. Conflict detected
# 2. Open files and fix conflicts (look for <<<<<<< markers)
# 3. Stage resolved files
git add <resolved-files>

# 4. Continue rebase
git rebase --continue

# If too complex, abort
git rebase --abort
```

### During Merge

```bash
# 1. Conflict detected
# 2. Fix conflicts in files
# 3. Stage resolved files
git add <resolved-files>

# 4. Complete merge
git commit
```

## Branch Management

### List Branches

```bash
git branch              # Local branches
git branch -a           # All branches (local + remote)
git branch -r           # Remote branches
```

### Delete Branches

```bash
git branch -d feature/old-feature      # Delete local (safe)
git branch -D feature/old-feature      # Force delete local
git push origin --delete feature/old   # Delete remote
```

### Clean Up Merged Branches

```bash
# List merged branches
git branch --merged main

# Delete all merged branches (except main)
git branch --merged main | grep -v "\* main" | xargs -n 1 git branch -d
```

## Release Management

### Create Release Tag

```bash
git checkout main
git pull origin main

# Create annotated tag
git tag -a v1.2.0 -m "Release v1.2.0

Features:
- New payment retry mechanism
- Order notification system

Bug Fixes:
- Payment timeout issue resolved
"

# Push tag
git push origin v1.2.0
```

### List Tags

```bash
git tag                 # List all tags
git tag -l "v1.*"       # List specific pattern
git show v1.2.0         # Show tag details
```

## Useful Aliases

Add to `~/.gitconfig`:

```ini
[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = log --oneline --graph --decorate --all
    sync = !git checkout main && git pull origin main
    cleanup = !git branch --merged main | grep -v "\\* main" | xargs -n 1 git branch -d
    amend = commit --amend --no-edit
    undo = reset HEAD~1
```

Usage:
```bash
git sync              # Update main
git co -b feature/new # Create new branch
git st                # Status
git visual            # Pretty log
git cleanup           # Delete merged branches
```

## Pre-Commit Checks

Before committing:

- [ ] Code follows style guide
- [ ] All tests pass locally
- [ ] No console.log or debug statements
- [ ] No commented-out code
- [ ] Commit message follows format
- [ ] Changes are small and focused

## Pull Request Checklist

Before creating PR:

- [ ] Branch is up-to-date with main
- [ ] All tests passing
- [ ] Code coverage > 80%
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Descriptive PR title and description
- [ ] Related task/issue linked

## Emergency Procedures

### Revert Bad Merge

```bash
# Find merge commit
git log --oneline --graph -10

# Revert the merge
git revert -m 1 <merge-commit-hash>

# Push
git push origin main
```

### Recover Deleted Branch

```bash
# Find commit hash
git reflog

# Recreate branch
git checkout -b feature/recovered <commit-hash>
```

### Remove Sensitive Data

```bash
# From last commit
git rm --cached <sensitive-file>
git commit --amend

# From history (dangerous!)
git filter-branch --tree-filter 'rm -f <sensitive-file>' HEAD
```

## Getting Help

- **Full Documentation**: [Version Control Workflow](version-control-workflow.md)
- **Feature Flags**: [Feature Flags Guide](feature-flags.md)
- **Code Review**: [Code Review Guidelines](code-review.md)
- **Architecture**: [ADR-007](../adr/007-trunk-based-development.md)
- **Slack**: #architecture channel

## Quick Tips

💡 **Commit Early, Commit Often**: Small commits are easier to review and revert

💡 **Branch Lifetime**: Keep feature branches < 3 days to minimize conflicts

💡 **Use Feature Flags**: Merge incomplete work safely behind feature flags

💡 **Rebase Daily**: Keep your branch updated to avoid merge conflicts

💡 **Descriptive Messages**: Future you will thank present you for clear commit messages

💡 **Self-Review**: Review your own changes before requesting review from others

💡 **Ask Questions**: Don't hesitate to ask the team if unsure about workflow

---

**Print this page for quick desk reference!**
