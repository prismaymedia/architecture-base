# Version Control Workflow Guide

> **Strategy**: Trunk-Based Development with Short-Lived Feature Branches  
> **Status**: ✅ Active  
> **Last Updated**: 2025-11-14

This guide defines the version control workflow for all microservices in the architecture-base project.

## Table of Contents

- [Overview](#overview)
- [Core Principles](#core-principles)
- [Branch Strategy](#branch-strategy)
- [Workflow Steps](#workflow-steps)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Release Management](#release-management)
- [Hotfix Process](#hotfix-process)
- [Best Practices](#best-practices)
- [Common Scenarios](#common-scenarios)
- [Troubleshooting](#troubleshooting)
- [Git Flow Alternative](#git-flow-alternative)

## Overview

We use **Trunk-Based Development (TBD)** as our primary version control strategy. This approach:

- Keeps `main` branch always deployable
- Uses short-lived feature branches (1-3 days maximum)
- Integrates code frequently (at least daily)
- Relies on feature flags for incomplete work
- Enables continuous deployment

### Why Trunk-Based Development?

- ✅ **Faster Integration**: Merge conflicts detected and resolved early
- ✅ **Continuous Delivery**: Main branch always ready to deploy
- ✅ **Better Collaboration**: Team works from same codebase
- ✅ **Reduced Risk**: Small, frequent changes easier to review and rollback
- ✅ **Aligns with Kanban**: Continuous flow without batching

See [ADR-007](../adr/007-trunk-based-development.md) for the full decision rationale.

## Core Principles

### 1. Main Branch is Sacred

- **Always Deployable**: Main must pass all tests and quality checks
- **Protected**: Cannot push directly, only via approved pull requests
- **Single Source of Truth**: All releases come from main

### 2. Small, Frequent Commits

- Commit at least 2-3 times per day
- Each commit should be a logical, working unit
- Push to remote frequently to avoid conflicts

### 3. Short-Lived Branches

- **Maximum Lifetime**: 2-3 days
- **Target**: Merge within 24 hours if possible
- **If Exceeding**: Break work into smaller tasks

### 4. Feature Flags for Incomplete Work

- Use feature toggles for work-in-progress features
- Allows merging incomplete code safely
- Enables gradual rollout and A/B testing

### 5. Comprehensive Testing

- All tests must pass before merge
- Code coverage > 80% for new code
- Integration tests for critical paths

## Branch Strategy

### Branch Types

#### 1. `main` (Trunk)

- **Purpose**: Production-ready code
- **Protection**: Branch protection enabled
- **Testing**: All CI/CD checks must pass
- **Deployment**: Auto-deploy to staging, manual to production

#### 2. `feature/TASK-XXX-description`

- **Purpose**: Develop new features or enhancements
- **Naming**: `feature/TASK-{number}-{short-description}`
- **Lifetime**: 1-3 days maximum
- **Source**: Branch from `main`
- **Target**: Merge to `main`

**Examples:**
```bash
feature/TASK-001-add-order-validation
feature/TASK-042-implement-payment-retry
feature/US-005-order-history-endpoint
```

#### 3. `hotfix/FIX-description`

- **Purpose**: Critical production bugs
- **Naming**: `hotfix/FIX-{short-description}`
- **Lifetime**: < 1 day
- **Source**: Branch from `main`
- **Target**: Merge to `main` immediately

**Examples:**
```bash
hotfix/FIX-payment-timeout-issue
hotfix/FIX-inventory-race-condition
```

#### 4. `docs/description` (Optional)

- **Purpose**: Documentation-only changes
- **Naming**: `docs/{short-description}`
- **Lifetime**: 1-2 days
- **Note**: Use sparingly, prefer combining docs with feature changes

**Examples:**
```bash
docs/update-api-documentation
docs/add-deployment-guide
```

### Release Tags

Releases are **tags**, not branches:

```bash
v1.0.0    # Major release
v1.1.0    # Minor release (new features)
v1.1.1    # Patch release (bug fixes)
```

**Format**: Semantic Versioning (SemVer) - `vMAJOR.MINOR.PATCH`

## Workflow Steps

### Standard Feature Development Flow

```
┌─────────────────────────────────────────────────────────┐
│                    1. Create Branch                      │
│  git checkout main                                       │
│  git pull origin main                                    │
│  git checkout -b feature/TASK-123-my-feature             │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                  2. Develop & Commit                     │
│  # Make changes                                          │
│  git add .                                               │
│  git commit -m "feat(orders): add validation logic"      │
│  git push origin feature/TASK-123-my-feature             │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│              3. Keep Branch Up-to-Date                   │
│  git checkout main                                       │
│  git pull origin main                                    │
│  git checkout feature/TASK-123-my-feature                │
│  git rebase main   # Or: git merge main                  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                4. Create Pull Request                    │
│  # Via GitHub UI or CLI                                  │
│  gh pr create --title "feat: Add order validation"       │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   5. Code Review                         │
│  # Address feedback                                      │
│  git add .                                               │
│  git commit -m "refactor: apply review feedback"         │
│  git push origin feature/TASK-123-my-feature             │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                  6. Merge to Main                        │
│  # After approval + CI passes                            │
│  # Use "Squash and merge" for clean history              │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                  7. Delete Branch                        │
│  git checkout main                                       │
│  git pull origin main                                    │
│  git branch -d feature/TASK-123-my-feature               │
└─────────────────────────────────────────────────────────┘
```

### Detailed Steps

#### Step 1: Create Feature Branch

```bash
# 1. Ensure main is up-to-date
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/TASK-123-add-payment-validation

# 3. Verify you're on the right branch
git branch
```

#### Step 2: Develop and Commit

```bash
# Make your changes
# ... edit files ...

# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat(payments): add credit card validation"

# Push to remote (first time)
git push -u origin feature/TASK-123-add-payment-validation

# Subsequent pushes
git push
```

**Best Practices:**
- Commit 2-3 times per day minimum
- Write meaningful commit messages
- Keep commits small and focused
- Run tests before committing

#### Step 3: Keep Branch Updated

**Option A: Rebase (Recommended for clean history)**

```bash
# Update main
git checkout main
git pull origin main

# Return to feature branch
git checkout feature/TASK-123-add-payment-validation

# Rebase on top of main
git rebase main

# If conflicts, resolve them
# ... fix conflicts ...
git add .
git rebase --continue

# Force push (rebase rewrites history)
git push --force-with-lease
```

**Option B: Merge (Simpler, preserves history)**

```bash
# From your feature branch
git merge origin/main

# Resolve conflicts if any
# ... fix conflicts ...
git add .
git commit -m "merge: resolve conflicts with main"

# Push normally
git push
```

**When to Update:**
- Daily if main has new commits
- Before creating pull request
- When conflicts are detected

#### Step 4: Create Pull Request

**Via GitHub CLI:**

```bash
gh pr create \
  --title "feat(payments): Add credit card validation" \
  --body "Implements validation for payment data as per TASK-123" \
  --base main \
  --head feature/TASK-123-add-payment-validation
```

**Via GitHub UI:**
1. Navigate to repository
2. Click "Pull requests" → "New pull request"
3. Select base: `main`, compare: `feature/TASK-123-add-payment-validation`
4. Fill in title and description
5. Add reviewers
6. Link to task/issue
7. Create pull request

**Pull Request Template:**

```markdown
## Description
Brief description of changes

## Related Task
Closes #123 (or TASK-123 in ClickUp)

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally
```

#### Step 5: Code Review Process

**For Authors:**
- Respond to feedback within 24 hours
- Make requested changes promptly
- Mark conversations as resolved when addressed
- Keep PR scope focused

**For Reviewers:**
- Review within 4 hours during business hours
- Check code quality, tests, documentation
- Verify CI/CD checks pass
- Approve or request changes

**Review Checklist:**
- [ ] Code follows architectural patterns
- [ ] Tests are comprehensive
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed
- [ ] Error handling implemented
- [ ] Logging added appropriately

#### Step 6: Merge to Main

**Merge Strategy: Squash and Merge (Recommended)**

- Creates single commit on main
- Clean, linear history
- Easier to revert if needed

**Alternative: Rebase and Merge**

- Preserves individual commits
- Useful for tracking detailed history
- Use when commits are well-structured

**After Merge:**
- CI/CD automatically deploys to staging
- Monitor deployment
- Verify functionality in staging

#### Step 7: Cleanup

```bash
# Switch to main
git checkout main

# Pull latest changes
git pull origin main

# Delete local branch
git branch -d feature/TASK-123-add-payment-validation

# Delete remote branch (if not auto-deleted)
git push origin --delete feature/TASK-123-add-payment-validation
```

## Commit Guidelines

### Commit Message Format

We follow **Conventional Commits** specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only
- **style**: Formatting, missing semicolons, etc. (no code change)
- **refactor**: Code change that neither fixes bug nor adds feature
- **perf**: Performance improvement
- **test**: Adding or updating tests
- **chore**: Maintenance, dependencies, build config
- **ci**: CI/CD configuration changes
- **revert**: Reverts a previous commit

### Scopes

Use the microservice name or component:

- `orders`
- `payments`
- `inventory`
- `notifications`
- `shared`
- `frontend`
- `infra`

### Examples

```bash
# Good commit messages
feat(orders): add order cancellation endpoint
fix(payments): resolve timeout on card validation
docs(api): update payment API documentation
refactor(inventory): simplify stock reservation logic
test(orders): add integration tests for order flow
chore(deps): update FastAPI to 0.104.0

# With body
feat(payments): integrate Stripe payment gateway

Implement Stripe payment processing including:
- Card tokenization
- Payment intent creation
- Webhook handling for async confirmations

Closes TASK-042

# Breaking change
feat(orders)!: change order status enum values

BREAKING CHANGE: Order status values changed from numeric to string.
Clients must update to use new string values: 'pending', 'confirmed', 'cancelled'
```

### Commit Best Practices

1. **Write in Imperative Mood**: "add feature" not "added feature"
2. **Be Specific**: "fix null pointer in payment validation" not "fix bug"
3. **Keep Subject Under 50 Characters**: For better readability
4. **Capitalize Subject Line**: Start with capital letter
5. **No Period at End**: Of subject line
6. **Separate Subject from Body**: With blank line
7. **Wrap Body at 72 Characters**: For better formatting

## Pull Request Process

### PR Best Practices

1. **Small PRs**: Target 200-400 lines changed
2. **Single Purpose**: One feature/fix per PR
3. **Self-Review First**: Review your own changes before requesting review
4. **Descriptive Title**: Clear, concise, follows commit format
5. **Complete Description**: Context, changes, testing, screenshots
6. **Link Tasks**: Reference related tasks/issues
7. **Update Tests**: All new code has tests
8. **Update Docs**: Documentation reflects changes

### PR Review Guidelines

**Approval Requirements:**
- Minimum 1 approval (recommended 2 for critical changes)
- All CI/CD checks must pass
- No unresolved conversations

**What to Review:**

✅ **Code Quality**
- Follows coding standards
- DRY principle applied
- SOLID principles followed
- Proper error handling
- Appropriate logging

✅ **Architecture**
- Aligns with architectural patterns
- Uses appropriate design patterns
- Event schemas follow conventions
- Database changes are migration-based

✅ **Testing**
- Unit tests for business logic
- Integration tests for APIs
- Contract tests for events
- Test coverage > 80%

✅ **Security**
- No hardcoded secrets
- Input validation present
- SQL injection prevention
- Proper authentication/authorization

✅ **Performance**
- No N+1 queries
- Appropriate caching
- Async operations where applicable
- Database indexes considered

✅ **Documentation**
- Code comments for complex logic
- API documentation updated
- Event catalog updated
- README updated if needed

### Review Turnaround Time

- **Target**: 4 hours during business hours
- **Maximum**: 24 hours
- **Urgent/Hotfix**: 1 hour

## Release Management

### Versioning Strategy

We use **Semantic Versioning** (SemVer): `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (v2.0.0)
- **MINOR**: New features, backward compatible (v1.1.0)
- **PATCH**: Bug fixes, backward compatible (v1.0.1)

### Creating a Release

**1. Prepare Release**

```bash
# Ensure main is stable
git checkout main
git pull origin main

# Verify all tests pass
# Run build and integration tests
```

**2. Create Release Tag**

```bash
# Tag the release
git tag -a v1.2.0 -m "Release version 1.2.0

Features:
- Add payment retry mechanism
- Implement order notifications
- Add inventory low stock alerts

Bug Fixes:
- Fix race condition in payment processing
- Resolve timeout in order creation

See CHANGELOG.md for details"

# Push tag to remote
git push origin v1.2.0
```

**3. Generate Release Notes**

Use GitHub Releases or create CHANGELOG.md:

```markdown
# Changelog

## [1.2.0] - 2025-11-14

### Added
- Payment retry mechanism with exponential backoff
- Email notifications for order confirmations
- Low stock alerts in inventory service

### Fixed
- Race condition in concurrent payment processing
- Timeout issues during order creation peak times

### Changed
- Improved error messages in payment API
- Updated dependencies to latest stable versions
```

**4. Deploy to Production**

```bash
# Tag triggers CD pipeline
# Or manual deployment:
./scripts/deploy-production.sh v1.2.0
```

### Release Checklist

- [ ] All tests passing
- [ ] Security scan completed
- [ ] Performance tests passed
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Migration scripts tested
- [ ] Rollback plan documented
- [ ] Stakeholders notified
- [ ] Production deployment scheduled

## Hotfix Process

For **critical production bugs** that need immediate fix:

### Hotfix Workflow

```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/FIX-payment-timeout

# 2. Fix the issue
# ... make minimal, focused changes ...

# 3. Test thoroughly
# Run all relevant tests

# 4. Commit
git add .
git commit -m "hotfix(payments): fix timeout in card validation

Increased timeout from 5s to 15s and added retry logic
for transient network errors.

Critical fix for production issue affecting 15% of transactions."

# 5. Push and create PR
git push -u origin hotfix/FIX-payment-timeout
gh pr create --title "hotfix: Fix payment timeout" --label "hotfix,urgent"

# 6. Fast-track review
# Get immediate review and approval

# 7. Merge and deploy
# Squash merge to main
# Deploy immediately to production

# 8. Create patch release
git tag -a v1.2.1 -m "Hotfix: Payment timeout resolution"
git push origin v1.2.1

# 9. Cleanup
git checkout main
git pull origin main
git branch -d hotfix/FIX-payment-timeout
```

### Hotfix Guidelines

1. **Minimal Changes**: Fix only the critical issue
2. **Fast Review**: Target < 1 hour for review
3. **Comprehensive Testing**: Test affected area thoroughly
4. **Immediate Deployment**: Deploy as soon as merged
5. **Post-Mortem**: Document incident and learnings
6. **Root Cause**: Schedule proper fix if hotfix is workaround

## Best Practices

### 1. Commit Early, Commit Often

```bash
# Bad: One giant commit at end of day
git commit -m "implemented entire payment feature"  # 50 files, 2000+ lines

# Good: Multiple focused commits
git commit -m "feat(payments): add payment model and repository"
git commit -m "feat(payments): implement payment validation"
git commit -m "feat(payments): add payment API endpoints"
git commit -m "test(payments): add unit tests for payment service"
```

### 2. Keep Branches Updated

```bash
# Update main daily
git checkout main && git pull origin main

# Rebase feature branch daily
git checkout feature/my-feature
git rebase main
```

### 3. Use Feature Flags

**Example in Python (FastAPI):**

```python
from app.core.config import settings

@router.post("/orders")
async def create_order(order: OrderCreate):
    # New payment retry feature behind flag
    if settings.FEATURE_PAYMENT_RETRY_ENABLED:
        result = await payment_service.process_with_retry(order.payment)
    else:
        result = await payment_service.process(order.payment)
    
    return result
```

**Configuration:**

```python
# .env
FEATURE_PAYMENT_RETRY_ENABLED=false  # Default off

# Enable in production gradually
FEATURE_PAYMENT_RETRY_ENABLED=true
```

### 4. Write Descriptive PR Descriptions

**Bad:**
```
Updated payment stuff
```

**Good:**
```
## Description
Implements retry mechanism for payment processing to handle transient failures.

## Changes
- Add exponential backoff retry logic to payment service
- Implement circuit breaker pattern for payment gateway
- Add metrics for payment retry success/failure
- Update payment API documentation

## Testing
- Unit tests for retry logic (100% coverage)
- Integration tests with mock payment gateway
- Load tested with 1000 concurrent requests
- Manually tested failure scenarios

## Related
Closes TASK-042
Related to US-002 (Payment Processing)

## Screenshots
![Retry metrics dashboard](link-to-image)
```

### 5. Clean Up Branches Regularly

```bash
# List merged branches
git branch --merged main

# Delete local merged branches
git branch --merged main | grep -v "\* main" | xargs -n 1 git branch -d

# Delete remote merged branches (carefully!)
git remote prune origin
```

### 6. Use Git Aliases

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
```

### 7. Pre-Commit Hooks

Use pre-commit hooks to enforce quality:

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Run linter
echo "Running linter..."
ruff check .
if [ $? -ne 0 ]; then
    echo "Linting failed. Please fix errors before committing."
    exit 1
fi

# Run tests
echo "Running tests..."
pytest tests/unit
if [ $? -ne 0 ]; then
    echo "Tests failed. Please fix before committing."
    exit 1
fi

echo "Pre-commit checks passed!"
```

## Common Scenarios

### Scenario 1: Forgot to Branch from Main

```bash
# You're on feature/old-feature and made commits for new feature

# 1. Create correct branch from main
git checkout main
git pull origin main
git checkout -b feature/TASK-999-correct-feature

# 2. Cherry-pick the commits you need
git cherry-pick <commit-hash-1>
git cherry-pick <commit-hash-2>

# 3. Push new branch
git push -u origin feature/TASK-999-correct-feature
```

### Scenario 2: Need to Update PR with Main Changes

```bash
# Your PR has conflicts with main

# 1. Update main
git checkout main
git pull origin main

# 2. Update feature branch
git checkout feature/TASK-123-my-feature
git rebase main

# 3. Resolve conflicts
# ... fix conflicts in files ...
git add .
git rebase --continue

# 4. Force push (since history changed)
git push --force-with-lease
```

### Scenario 3: Accidentally Committed to Main

```bash
# Oh no! You committed directly to main

# 1. Create a feature branch with your changes
git checkout -b feature/TASK-123-my-accidental-work

# 2. Reset main to origin
git checkout main
git reset --hard origin/main

# 3. Now your work is safely on the feature branch
git checkout feature/TASK-123-my-accidental-work
# Create PR normally
```

### Scenario 4: Need to Split Large PR

```bash
# Your PR is too large (500+ lines)

# 1. Create multiple feature branches
git checkout main
git checkout -b feature/TASK-123-part1-models
git checkout -b feature/TASK-123-part2-services
git checkout -b feature/TASK-123-part3-api

# 2. Use interactive rebase or cherry-pick to organize commits
git checkout feature/TASK-123-part1-models
git cherry-pick <commits-for-models>

# 3. Create separate PRs for each part
# PR 1: Models and schemas
# PR 2: Business logic (depends on PR 1)
# PR 3: API endpoints (depends on PR 2)
```

### Scenario 5: Reverting a Bad Merge

```bash
# A merged PR caused production issues

# 1. Find the merge commit
git log --oneline --graph -10

# 2. Revert the merge
git revert -m 1 <merge-commit-hash>

# 3. Commit and push
git push origin main

# 4. Deploy reverted version
./scripts/deploy.sh

# 5. Fix the issue in a new branch
git checkout -b fix/TASK-xxx-fix-previous-pr
# Make proper fixes
```

## Troubleshooting

### Merge Conflicts

**Resolve During Rebase:**

```bash
# 1. Start rebase
git rebase main

# 2. Conflict detected - git shows conflicted files
# 3. Open files and resolve conflicts
# Look for conflict markers:
<<<<<<< HEAD
main branch code
=======
your code
>>>>>>> your-branch

# 4. Choose correct code or combine both
# 5. Stage resolved files
git add <resolved-files>

# 6. Continue rebase
git rebase --continue

# 7. If multiple conflicts, repeat steps 3-6

# 8. When done, force push
git push --force-with-lease
```

**Abort Rebase:**

```bash
# If conflicts are too complex
git rebase --abort

# Use merge instead
git merge main
# Resolve conflicts
git commit
```

### Diverged Branches

```bash
# Error: "Your branch and 'origin/feature' have diverged"

# Option 1: Force pull (lose local commits)
git reset --hard origin/feature

# Option 2: Rebase local on remote
git pull --rebase

# Option 3: Merge remote into local
git pull
```

### Accidentally Deleted Branch

```bash
# Find the commit hash
git reflog

# Recreate branch from commit
git checkout -b feature/TASK-123-recovered <commit-hash>
```

### Large Files Committed by Mistake

```bash
# Remove from last commit
git rm --cached <large-file>
git commit --amend

# Remove from history (be careful!)
git filter-branch --tree-filter 'rm -f <large-file>' HEAD
```

## Git Flow Alternative

While we recommend Trunk-Based Development, Git Flow remains a valid alternative for teams that prefer it.

### Git Flow Overview

Git Flow uses multiple long-lived branches:

```
main (production)
  │
  └── develop (integration)
        │
        ├── feature/xxx (new features)
        ├── release/x.y.z (release preparation)
        └── hotfix/xxx (emergency fixes)
```

### Git Flow Workflow

**1. Setup:**

```bash
git flow init
```

**2. Feature Development:**

```bash
# Start feature
git flow feature start TASK-123-my-feature

# Work on feature
# ... make changes ...
git commit -am "Add feature"

# Finish feature (merges to develop)
git flow feature finish TASK-123-my-feature
```

**3. Release:**

```bash
# Start release
git flow release start 1.2.0

# Prepare release (version bumps, changelog)
# ... make changes ...
git commit -am "Prepare release 1.2.0"

# Finish release (merges to main and develop, creates tag)
git flow release finish 1.2.0
```

**4. Hotfix:**

```bash
# Start hotfix from main
git flow hotfix start 1.2.1

# Fix issue
# ... make changes ...
git commit -am "Fix critical bug"

# Finish hotfix (merges to main and develop)
git flow hotfix finish 1.2.1
```

### When to Use Git Flow

Consider Git Flow if:
- ✅ You have scheduled releases (quarterly, monthly)
- ✅ Multiple versions in production simultaneously
- ✅ Large team with formal release process
- ✅ Desktop/mobile apps with approval delays
- ✅ Need explicit release preparation phase

Don't use Git Flow if:
- ❌ You want continuous deployment
- ❌ Team is small (<10 developers)
- ❌ Microservices releasing independently
- ❌ Need fast feedback cycles
- ❌ Working with Kanban methodology

### Comparison Table

| Aspect | Trunk-Based Development | Git Flow |
|--------|------------------------|----------|
| **Branch Complexity** | Low (1 main branch) | High (2+ long-lived branches) |
| **Integration Frequency** | Daily | Per release cycle |
| **Merge Conflicts** | Rare | More common |
| **Release Cadence** | Continuous | Scheduled |
| **Learning Curve** | Easy | Moderate |
| **CI/CD Friendly** | Excellent | Moderate |
| **Microservices** | Ideal | Works but complex |
| **Team Size** | Any | Better for large teams |
| **Ceremony** | Minimal | More structured |

## Tools and Resources

### Git Tools

- **GitHub CLI**: `gh` for PR management
- **Git Aliases**: Speed up common commands
- **Pre-commit Hooks**: Automated quality checks
- **GitLens (VS Code)**: Enhanced git visualization
- **Git Flow Extension**: If using Git Flow

### Recommended Reading

- [Trunk Based Development](https://trunkbaseddevelopment.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Git Best Practices](https://git-scm.com/book/en/v2)
- [Pro Git Book](https://git-scm.com/book/en/v2)

### Related Documentation

- [ADR-007: Trunk-Based Development](../adr/007-trunk-based-development.md)
- [CI/CD Pipeline Guide](cicd-pipeline.md)
- [Feature Flags Guide](feature-flags.md)
- [Code Review Guidelines](code-review.md)
- [Kanban Guide](kanban-guide.md)

## Quick Reference

### Essential Commands

```bash
# Daily workflow
git checkout main && git pull                    # Update main
git checkout -b feature/TASK-123-my-feature      # New feature
git add . && git commit -m "feat: add feature"   # Commit
git push -u origin feature/TASK-123-my-feature   # Push

# Update branch
git fetch origin                                 # Fetch latest
git rebase origin/main                           # Rebase on main
git push --force-with-lease                      # Force push safely

# Cleanup
git checkout main && git pull                    # Back to main
git branch -d feature/TASK-123-my-feature        # Delete local
git remote prune origin                          # Clean remote refs
```

### Commit Message Template

```bash
# ~/.gitmessage
<type>(<scope>): <subject>
# |<----  Use Maximum 50 Characters  ---->|

# Explain why this change is being made
# |<----   Try To Limit Each Line to a Maximum Of 72 Characters   ---->|

# Provide links or keys to any relevant tickets, articles or other resources
# Example: Closes TASK-123

# --- COMMIT END ---
# Type can be
#    feat     (new feature)
#    fix      (bug fix)
#    refactor (refactoring code)
#    style    (formatting, missing semi colons, etc; no code change)
#    docs     (changes to documentation)
#    test     (adding or refactoring tests; no production code change)
#    chore    (updating grunt tasks etc; no production code change)
# --------------------
# Remember to
#   - Capitalize the subject line
#   - Use the imperative mood in the subject line
#   - Do not end the subject line with a period
#   - Separate subject from body with a blank line
#   - Use the body to explain what and why vs. how
```

Configure:
```bash
git config --global commit.template ~/.gitmessage
```

---

**Questions?** Reach out to the architecture team on Slack #architecture channel.
