# CI/CD Pipeline Guide

> **Purpose**: Automated continuous integration and deployment pipeline  
> **Status**: ✅ Active  
> **Last Updated**: 2025-11-14

This guide describes the CI/CD pipeline architecture that supports our Trunk-Based Development workflow.

## Table of Contents

- [Overview](#overview)
- [Pipeline Stages](#pipeline-stages)
- [Branch Workflows](#branch-workflows)
- [Quality Gates](#quality-gates)
- [Deployment Strategy](#deployment-strategy)
- [Monitoring](#monitoring)
- [Configuration](#configuration)

## Overview

Our CI/CD pipeline automates:

- ✅ **Code Quality**: Linting, formatting, type checking
- ✅ **Testing**: Unit, integration, contract tests
- ✅ **Security**: Vulnerability scanning, secrets detection
- ✅ **Building**: Docker images, artifacts
- ✅ **Deployment**: Automated to dev/staging, manual to production

### Pipeline Architecture

```
Code Push → GitHub Actions → Quality Gates → Build → Deploy
     ↓             ↓              ↓           ↓        ↓
  Webhook      Parallel       Pass/Fail   Artifacts  K8s/Cloud
              Checks
```

## Pipeline Stages

### Stage 1: Code Quality (Parallel)

Runs on every push to any branch:

#### Backend (Python)

```yaml
# .github/workflows/backend-ci.yml
name: Backend CI

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install ruff black mypy pytest pytest-cov
          pip install -r requirements.txt
      
      - name: Lint with ruff
        run: ruff check .
      
      - name: Format check with black
        run: black --check .
      
      - name: Type check with mypy
        run: mypy app/
```

#### Frontend (React/TypeScript)

```yaml
# .github/workflows/frontend-ci.yml
name: Frontend CI

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Lint
        run: npm run lint
      
      - name: Type check
        run: npm run type-check
      
      - name: Format check
        run: npm run format:check
```

### Stage 2: Testing (Parallel)

#### Unit Tests

```yaml
test-unit:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    
    - name: Run unit tests
      run: |
        pytest tests/unit \
          --cov=app \
          --cov-report=xml \
          --cov-report=html
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
```

#### Integration Tests

```yaml
test-integration:
  runs-on: ubuntu-latest
  services:
    postgres:
      image: postgres:15
      env:
        POSTGRES_PASSWORD: test
    rabbitmq:
      image: rabbitmq:3-management
  steps:
    - uses: actions/checkout@v4
    
    - name: Run integration tests
      run: pytest tests/integration
      env:
        DATABASE_URL: postgresql://postgres:test@localhost/test
        RABBITMQ_URL: amqp://guest:guest@localhost:5672
```

#### Contract Tests (Events)

```yaml
test-contracts:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    
    - name: Validate event schemas
      run: |
        python scripts/validate_event_schemas.py
    
    - name: Run contract tests
      run: pytest tests/contracts
```

### Stage 3: Security Scanning

```yaml
security:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
    
    - name: Check for secrets
      uses: trufflesecurity/trufflehog@main
      with:
        path: ./
        base: main
```

### Stage 4: Build

Only runs on `main` branch or tags:

```yaml
build:
  if: github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/')
  needs: [quality, test-unit, test-integration, security]
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Login to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: |
          ghcr.io/${{ github.repository }}/orders-api:latest
          ghcr.io/${{ github.repository }}/orders-api:${{ github.sha }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

### Stage 5: Deploy

#### Development (Automatic)

Deploys automatically on push to `main`:

```yaml
deploy-dev:
  if: github.ref == 'refs/heads/main'
  needs: [build]
  runs-on: ubuntu-latest
  environment: development
  steps:
    - name: Deploy to Dev
      run: |
        kubectl set image deployment/orders-api \
          orders-api=ghcr.io/${{ github.repository }}/orders-api:${{ github.sha }} \
          --namespace=dev
        kubectl rollout status deployment/orders-api -n dev
```

#### Staging (Manual Approval)

Requires manual approval:

```yaml
deploy-staging:
  if: github.ref == 'refs/heads/main'
  needs: [deploy-dev]
  runs-on: ubuntu-latest
  environment: staging
  steps:
    - name: Deploy to Staging
      run: |
        kubectl set image deployment/orders-api \
          orders-api=ghcr.io/${{ github.repository }}/orders-api:${{ github.sha }} \
          --namespace=staging
        kubectl rollout status deployment/orders-api -n staging
    
    - name: Run smoke tests
      run: |
        python scripts/smoke_tests.py --env staging
```

#### Production (Manual + Approvals)

Requires multiple approvals and is tag-based:

```yaml
deploy-production:
  if: startsWith(github.ref, 'refs/tags/v')
  needs: [build]
  runs-on: ubuntu-latest
  environment: 
    name: production
    url: https://api.production.example.com
  steps:
    - name: Deploy to Production
      run: |
        kubectl set image deployment/orders-api \
          orders-api=ghcr.io/${{ github.repository }}/orders-api:${{ github.ref_name }} \
          --namespace=production
        kubectl rollout status deployment/orders-api -n production
    
    - name: Run smoke tests
      run: |
        python scripts/smoke_tests.py --env production
    
    - name: Notify team
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        text: 'Deployed ${{ github.ref_name }} to production'
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

## Branch Workflows

### Feature Branch (feature/*)

```
On Push:
  ✓ Lint
  ✓ Format check
  ✓ Type check
  ✓ Unit tests
  ✓ Integration tests
  ✓ Security scan
  ✗ No build
  ✗ No deployment
```

### Main Branch

```
On Push to main:
  ✓ All quality checks
  ✓ All tests
  ✓ Security scan
  ✓ Build Docker image
  ✓ Deploy to Development (automatic)
  ⏸ Deploy to Staging (manual approval)
  ✗ No production deployment
```

### Release Tag (v*.*.*)

```
On Tag v*.*.*:
  ✓ All quality checks
  ✓ All tests
  ✓ Security scan
  ✓ Build Docker image (with version tag)
  ⏸ Deploy to Production (manual approval)
```

### Hotfix Branch (hotfix/*)

```
On Push:
  ✓ All quality checks
  ✓ All tests
  ✓ Security scan
  ⏸ Fast-track review (<1 hour)
  
After Merge to main:
  ✓ Build
  ✓ Deploy to Development
  ⏸ Deploy to Production (expedited approval)
```

## Quality Gates

All quality gates must pass before merge to `main`:

### Required Checks

1. ✅ **Linting**: Code style compliance
2. ✅ **Formatting**: Code formatting standards
3. ✅ **Type Checking**: Type safety validation
4. ✅ **Unit Tests**: >80% coverage, all passing
5. ✅ **Integration Tests**: Critical paths covered
6. ✅ **Security Scan**: No critical vulnerabilities
7. ✅ **Code Review**: At least 1 approval

### Optional Checks (Warnings)

1. ⚠️ **Performance Tests**: Degradation warnings
2. ⚠️ **Bundle Size**: Size increase warnings
3. ⚠️ **Dependency Updates**: Outdated dependencies

### Branch Protection Rules

Configure in GitHub:

```yaml
main:
  required_status_checks:
    strict: true
    contexts:
      - "Backend CI / quality"
      - "Backend CI / test-unit"
      - "Backend CI / test-integration"
      - "Backend CI / security"
      - "Frontend CI / quality"
      - "Frontend CI / test"
  required_pull_request_reviews:
    required_approving_review_count: 1
    dismiss_stale_reviews: true
  enforce_admins: false
  required_linear_history: true
  restrictions: null
```

## Deployment Strategy

### Blue-Green Deployment

For zero-downtime deployments:

```yaml
deploy:
  steps:
    - name: Deploy green environment
      run: kubectl apply -f k8s/green-deployment.yaml
    
    - name: Wait for green to be healthy
      run: kubectl wait --for=condition=available deployment/orders-api-green
    
    - name: Run smoke tests on green
      run: python scripts/smoke_tests.py --env green
    
    - name: Switch traffic to green
      run: kubectl patch service orders-api -p '{"spec":{"selector":{"version":"green"}}}'
    
    - name: Keep blue for rollback
      run: kubectl scale deployment/orders-api-blue --replicas=1
```

### Canary Deployment

For gradual rollout:

```yaml
deploy-canary:
  steps:
    - name: Deploy canary (10% traffic)
      run: |
        kubectl apply -f k8s/canary-deployment.yaml
        kubectl apply -f k8s/traffic-split-10.yaml
    
    - name: Monitor metrics for 10 minutes
      run: python scripts/monitor_canary.py --duration 600
    
    - name: Increase to 50% if healthy
      if: success()
      run: kubectl apply -f k8s/traffic-split-50.yaml
    
    - name: Monitor again
      run: python scripts/monitor_canary.py --duration 300
    
    - name: Full rollout
      if: success()
      run: kubectl apply -f k8s/traffic-split-100.yaml
```

### Rollback Procedure

Automated rollback on failure:

```yaml
deploy:
  steps:
    - name: Deploy
      id: deploy
      run: kubectl set image deployment/orders-api orders-api=new-version
    
    - name: Wait for rollout
      run: kubectl rollout status deployment/orders-api --timeout=5m
    
    - name: Smoke tests
      id: smoke
      run: python scripts/smoke_tests.py
    
    - name: Rollback on failure
      if: failure()
      run: |
        kubectl rollout undo deployment/orders-api
        kubectl rollout status deployment/orders-api
```

## Monitoring

### Pipeline Metrics

Track in GitHub Actions:

- **Build Success Rate**: % of successful builds
- **Build Duration**: Average time per pipeline run
- **Test Coverage**: Code coverage trend
- **Deployment Frequency**: Deploys per day
- **Lead Time**: Commit to production time
- **Mean Time to Recovery**: Time to fix failed deployments

### Application Metrics

Monitor post-deployment:

- **Error Rate**: 4xx/5xx responses
- **Response Time**: p50, p95, p99 latency
- **Throughput**: Requests per second
- **Resource Usage**: CPU, memory, disk
- **Custom Metrics**: Business metrics

### Alerts

Configure alerts for:

```yaml
alerts:
  - name: Build Failure
    condition: build_status == 'failure'
    notify: slack_channel, email
  
  - name: Test Coverage Drop
    condition: coverage < 80%
    notify: slack_channel
  
  - name: Deployment Failed
    condition: deployment_status == 'failed'
    notify: slack_channel, pagerduty
  
  - name: High Error Rate
    condition: error_rate > 5%
    notify: pagerduty
```

## Configuration

### Environment Variables

```bash
# .env.dev
ENVIRONMENT=development
DATABASE_URL=postgresql://...
RABBITMQ_URL=amqp://...
LOG_LEVEL=DEBUG
FEATURE_NEW_PAYMENT_FLOW=true

# .env.staging
ENVIRONMENT=staging
DATABASE_URL=postgresql://...
RABBITMQ_URL=amqp://...
LOG_LEVEL=INFO
FEATURE_NEW_PAYMENT_FLOW=true

# .env.production
ENVIRONMENT=production
DATABASE_URL=postgresql://...
RABBITMQ_URL=amqp://...
LOG_LEVEL=WARNING
FEATURE_NEW_PAYMENT_FLOW=false  # Gradual rollout
```

### Secrets Management

Store in GitHub Secrets or cloud provider:

```yaml
secrets:
  - DATABASE_PASSWORD
  - RABBITMQ_PASSWORD
  - JWT_SECRET_KEY
  - STRIPE_API_KEY
  - SLACK_WEBHOOK_URL
```

Access in workflows:

```yaml
env:
  DATABASE_PASSWORD: ${{ secrets.DATABASE_PASSWORD }}
  STRIPE_API_KEY: ${{ secrets.STRIPE_API_KEY }}
```

## Best Practices

### 1. Fast Feedback

- ✅ Run fast checks first (linting, formatting)
- ✅ Parallelize test suites
- ✅ Use caching for dependencies
- ✅ Fail fast on errors

### 2. Reproducible Builds

- ✅ Pin dependency versions
- ✅ Use same tools locally and in CI
- ✅ Docker for consistent environments
- ✅ Version everything

### 3. Secure Pipeline

- ✅ Scan for vulnerabilities
- ✅ Never log secrets
- ✅ Use minimal permissions
- ✅ Audit access logs

### 4. Observable Pipeline

- ✅ Log all steps
- ✅ Track metrics
- ✅ Set up alerts
- ✅ Visualize trends

## Related Documentation

- [Version Control Workflow](version-control-workflow.md)
- [Feature Flags Guide](feature-flags.md)
- [ADR-007: Trunk-Based Development](../adr/007-trunk-based-development.md)
- [Deployment Guide](deployment.md)
- [Monitoring Guide](monitoring.md)

---

**Questions?** Contact the DevOps Team on Slack #devops channel.
