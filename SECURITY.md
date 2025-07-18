# 🛡️ Security Scanning Guide

This document provides instructions for using the security scanning tools implemented in this repository.

## 🚀 Automated Security Scanning

### GitHub Actions Workflow
The security scanning runs automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` branch

The workflow includes:
- **Bandit**: Python security issue scanner
- **Safety**: Dependency vulnerability checker
- **Semgrep**: Multi-language static analysis
- **TruffleHog**: Secret detection

### Pre-commit Hooks
Pre-commit hooks run locally before each commit to catch issues early.

#### Setup
```bash
# Install pre-commit
pip install pre-commit

# Install the hooks
pre-commit install

# Run hooks manually on all files
pre-commit run --all-files
```

## 🔧 Manual Security Scanning

### Bandit (Python Security Scanner)
```bash
# Install
pip install bandit

# Basic scan
bandit -r .

# Generate JSON report
bandit -r . -f json -o bandit-report.json

# Skip test files
bandit -r . -x tests/
```

### Safety (Dependency Vulnerability Check)
```bash
# Install
pip install safety

# Check installed packages
safety check

# Check requirements.txt
safety check -r requirements.txt

# Generate JSON report
safety check --json
```

### Semgrep (Multi-language SAST)
```bash
# Install
pip install semgrep

# Auto-config scan
semgrep scan --config=auto

# Specific ruleset
semgrep scan --config=p/security-audit

# Generate JSON report
semgrep scan --config=auto --json
```

### TruffleHog (Secret Detection)
```bash
# Install
go install github.com/trufflesecurity/trufflehog/v3@latest

# Scan current directory
trufflehog filesystem .

# Scan git history
trufflehog git file:///path/to/repo
```

## 🎯 Current Vulnerabilities Detected

The security tools will detect these intentional vulnerabilities in `vunerable_app.py`:

1. **Hardcoded Secret (Line 11)**
   - Tool: TruffleHog, GitGuardian
   - Issue: Secret key hardcoded in source code

2. **Command Injection (Line 17)**
   - Tool: Bandit, Semgrep
   - Issue: Subprocess call with shell=True and user input

3. **JWT Without Validation (Line 23)**
   - Tool: Bandit, Semgrep
   - Issue: JWT decode without signature verification

## 📊 VS Code Extensions

Recommended extensions for real-time security scanning:

1. **SonarLint** - Real-time code quality and security
2. **GitGuardian** - Secret detection in IDE
3. **Snyk** - Vulnerability scanning for dependencies
4. **Bandit** - Python security linting

## 🚨 Security Policies

### Vulnerability Severity Levels
- **Critical**: Block deployment, immediate fix required
- **High**: Review required, fix within 24 hours
- **Medium**: Fix within 1 week
- **Low**: Fix within 1 month

### Remediation Guidelines
1. Never commit secrets to version control
2. Always validate and sanitize user input
3. Use parameterized queries for database operations
4. Implement proper authentication and authorization
5. Keep dependencies updated

## 📈 Monitoring and Metrics

Track security posture with:
- Zero critical vulnerabilities in production
- 100% security scan coverage on PRs
- Regular dependency updates
- Security training completion rates