# Developer Setup Guide

> **Quick start guide for new developers**  
> **Last Updated**: 2025-11-14

This guide helps you set up your development environment for contributing to the project.

## Prerequisites

### Required Software

- **Git**: Version 2.30 or higher
- **GitHub CLI** (optional but recommended): `gh`
- **Python**: 3.12 or higher (for backend)
- **Node.js**: 20.x or higher (for frontend)
- **Docker**: Latest stable version
- **Docker Compose**: Latest version

### Accounts

- GitHub account with repository access
- ClickUp account (for task management)

## Initial Setup

### 1. Clone Repository

```bash
# Clone the repository
git clone https://github.com/prismaymedia/architecture-base.git
cd architecture-base
```

### 2. Configure Git

```bash
# Set your name and email
git config user.name "Your Name"
git config user.email "your.email@company.com"

# Use the commit message template
git config commit.template .gitmessage

# Enable Git aliases (optional but recommended)
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.sync '!git checkout main && git pull origin main'
git config --global alias.cleanup '!git branch --merged main | grep -v "\\* main" | xargs -n 1 git branch -d'
```

### 3. Install GitHub CLI (Optional)

**macOS:**
```bash
brew install gh
```

**Linux:**
```bash
# See: https://github.com/cli/cli/blob/trunk/docs/install_linux.md
```

**Windows:**
```bash
# See: https://github.com/cli/cli/releases
```

**Authenticate:**
```bash
gh auth login
```

## Development Environment Setup

### Backend (Python)

```bash
# Navigate to service directory
cd services/orders-api

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Frontend (React)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Verify installation
npm run type-check
npm run lint
```

### Docker Environment

```bash
# Start all services (from project root)
docker-compose up -d

# Verify services are running
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## IDE Setup

### Visual Studio Code (Recommended)

**Install Extensions:**

```bash
# Install recommended extensions
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension eamodio.gitlens
code --install-extension GitHub.copilot
```

**Workspace Settings:**

Create `.vscode/settings.json`:

```json
{
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

### PyCharm / IntelliJ IDEA

1. Open project
2. Configure Python interpreter (virtual environment)
3. Enable "Format on save"
4. Configure code style to match Black
5. Install plugins: GitToolBox, .env files support

## Verification

### Verify Git Setup

```bash
# Check git configuration
git config --list | grep user
git config --list | grep commit.template

# Test commit template
git commit --allow-empty -m "test"
# Should show template
```

### Verify Backend Setup

```bash
cd services/orders-api

# Activate venv
source venv/bin/activate

# Run linter
ruff check .

# Run formatter check
black --check .

# Run type checker
mypy app/

# Run tests
pytest tests/
```

### Verify Frontend Setup

```bash
cd frontend

# Run linter
npm run lint

# Run type checker
npm run type-check

# Run tests
npm test

# Start dev server
npm run dev
```

## Daily Workflow

### Start of Day

```bash
# Update main branch
git sync  # Or: git checkout main && git pull

# Check for updates
git log --oneline -5
```

### Starting New Task

```bash
# Create feature branch
git checkout -b feature/TASK-123-description

# Verify you're on correct branch
git branch
```

### During Development

```bash
# Make changes...

# Check status frequently
git st  # Or: git status

# Stage changes
git add .

# Commit with template
git commit
# Template will open in editor

# Or quick commit
git commit -m "feat(scope): subject"

# Push to remote
git push -u origin feature/TASK-123-description
```

### Creating Pull Request

```bash
# Option 1: GitHub CLI
gh pr create --title "feat: Add feature" --body "Description"

# Option 2: GitHub UI
# Navigate to repository and create PR
```

### After PR is Merged

```bash
# Update main
git checkout main
git pull

# Delete feature branch
git branch -d feature/TASK-123-description
```

## Troubleshooting

### Git Issues

**Problem: Changes not staged**
```bash
git add .
```

**Problem: Wrong branch**
```bash
git stash
git checkout correct-branch
git stash pop
```

**Problem: Need to undo commit**
```bash
git reset --soft HEAD~1  # Keep changes
```

### Python Issues

**Problem: Import errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Problem: Tests failing**
```bash
# Clear cache
pytest --cache-clear
```

### Node Issues

**Problem: Module not found**
```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Problem: TypeScript errors**
```bash
# Restart TypeScript server in VS Code
# Cmd+Shift+P → "TypeScript: Restart TS Server"
```

## Getting Help

### Documentation

- [Version Control Workflow](docs/guides/version-control-workflow.md)
- [Git Quick Reference](docs/guides/git-quick-reference.md)
- [Code Review Guidelines](docs/guides/code-review.md)
- [Architecture Overview](docs/architecture/README.md)

### Team Communication

- **Slack Channels**:
  - `#architecture` - Architecture questions
  - `#development` - General development help
  - `#devops` - CI/CD and deployment

- **Office Hours**:
  - Tuesday 2-3pm: Architecture consultation
  - Thursday 10-11am: Code review sessions

### Pair Programming

Don't hesitate to ask for pair programming sessions when:
- Starting a new feature
- Stuck on a problem
- Learning new patterns
- Complex refactoring

## Best Practices Reminder

✅ **DO:**
- Commit early and often (2-3 times per day)
- Keep branches short-lived (< 3 days)
- Write meaningful commit messages
- Run tests before committing
- Use feature flags for incomplete work
- Ask questions when unsure

❌ **DON'T:**
- Commit directly to main
- Leave branches open for weeks
- Skip code review
- Push without running tests
- Hardcode secrets
- Leave commented-out code

## Quick Reference

### Common Commands

```bash
# Daily sync
git sync

# Create branch
git co -b feature/TASK-123-new-feature

# Check status
git st

# Commit
git commit

# Push
git push

# Create PR
gh pr create

# Update branch
git rebase main

# Cleanup
git cleanup
```

### Environment Variables

Create `.env` file (never commit this):

```bash
# Backend (.env)
DATABASE_URL=postgresql://localhost/dev_db
RABBITMQ_URL=amqp://localhost:5672
FEATURE_NEW_PAYMENT_FLOW=false

# Frontend (.env.local)
VITE_API_URL=http://localhost:8000
VITE_FEATURE_NEW_CHECKOUT=false
```

## Next Steps

1. ✅ Complete this setup guide
2. 📖 Read [Version Control Workflow](docs/guides/version-control-workflow.md)
3. 📋 Review [Code Review Guidelines](docs/guides/code-review.md)
4. 🏗️ Understand [Architecture](docs/architecture/README.md)
5. 🎯 Pick your first task from [BACKLOG.md](../BACKLOG.md)
6. 💬 Join team channels on Slack
7. 👥 Schedule onboarding call with team lead

## Cheat Sheet

Print or bookmark: [Git Quick Reference](docs/guides/git-quick-reference.md)

---

**Welcome to the team! 🎉**

Questions? Ask in `#development` channel or contact your team lead.
