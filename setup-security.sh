#!/bin/bash

# Security Tools Setup Script
# This script installs and configures all security tools for the pre-commit system

set -e  # Exit on any error

echo "🔒 Setting up Security Tools for Pre-commit System"
echo "================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "\n${BLUE}[STEP]${NC} $1"
}

# Check if we're in a Git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Not in a Git repository. Please run this script from the root of your Git repository."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if Node.js is installed (for JavaScript security checks)
if ! command -v node &> /dev/null; then
    print_warning "Node.js is not installed. Some JavaScript security checks will be skipped."
    NODE_AVAILABLE=false
else
    NODE_AVAILABLE=true
fi

print_step "1. Creating virtual environment for security tools"
if [ ! -d "venv-security" ]; then
    python3 -m venv venv-security
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
source venv-security/bin/activate

print_step "2. Installing Python security tools"
if [ -f "requirements-security.txt" ]; then
    pip install --upgrade pip
    pip install -r requirements-security.txt
    print_status "Security tools installed from requirements-security.txt"
else
    print_warning "requirements-security.txt not found. Installing essential tools..."
    pip install pre-commit bandit safety semgrep detect-secrets flake8 flake8-security
fi

print_step "3. Setting up pre-commit hooks"
if [ -f ".pre-commit-config.yaml" ]; then
    pre-commit install
    print_status "Pre-commit hooks installed"
else
    print_error ".pre-commit-config.yaml not found. Please create it first."
    exit 1
fi

print_step "4. Installing pre-commit hook environments"
print_status "This may take a few minutes..."
pre-commit install --install-hooks
print_status "Hook environments installed"

print_step "5. Setting up detect-secrets baseline"
if [ ! -f ".secrets.baseline" ]; then
    detect-secrets scan --all-files --baseline .secrets.baseline
    print_status "Secrets baseline created"
else
    print_status "Secrets baseline already exists"
fi

print_step "6. Creating ESLint configuration for JavaScript security"
if [ "$NODE_AVAILABLE" = true ]; then
    if [ ! -f ".eslintrc.json" ]; then
        cat > .eslintrc.json << 'EOF'
{
    "env": {
        "browser": true,
        "es6": true,
        "node": true
    },
    "extends": [
        "eslint:recommended"
    ],
    "plugins": [
        "security"
    ],
    "rules": {
        "security/detect-unsafe-regex": "error",
        "security/detect-buffer-noassert": "error",
        "security/detect-child-process": "error",
        "security/detect-disable-mustache-escape": "error",
        "security/detect-eval-with-expression": "error",
        "security/detect-no-csrf-before-method-override": "error",
        "security/detect-non-literal-fs-filename": "error",
        "security/detect-non-literal-regexp": "error",
        "security/detect-non-literal-require": "error",
        "security/detect-object-injection": "error",
        "security/detect-possible-timing-attacks": "error",
        "security/detect-pseudoRandomBytes": "error",
        "security/detect-new-buffer": "error",
        "no-eval": "error",
        "no-implied-eval": "error",
        "no-new-func": "error"
    }
}
EOF
        print_status "ESLint security configuration created"
    else
        print_status "ESLint configuration already exists"
    fi
    
    # Initialize package.json if it doesn't exist
    if [ ! -f "package.json" ]; then
        cat > package.json << 'EOF'
{
    "name": "security-demo",
    "version": "1.0.0",
    "description": "Demo project with security tools",
    "scripts": {
        "security-audit": "npm audit --audit-level=high",
        "lint": "eslint . --ext .js,.jsx,.ts,.tsx"
    },
    "devDependencies": {
        "eslint": "^8.57.0",
        "eslint-plugin-security": "^1.7.1",
        "eslint-plugin-node": "^11.1.0"
    }
}
EOF
        print_status "Package.json created"
    fi
    
    # Install npm dependencies
    if command -v npm &> /dev/null; then
        print_status "Installing Node.js security dependencies..."
        npm install
        print_status "Node.js dependencies installed"
    else
        print_warning "npm not found. JavaScript security checks may not work fully."
    fi
else
    print_warning "Skipping Node.js setup (Node.js not available)"
fi

print_step "7. Setting up Git hooks"
# Make sure the security-check.py script is executable
if [ -f "security-check.py" ]; then
    chmod +x security-check.py
    print_status "security-check.py made executable"
fi

print_step "8. Creating security configuration files"

# Create .gitignore entries for security tools
if [ -f ".gitignore" ]; then
    if ! grep -q "venv-security" .gitignore; then
        echo "" >> .gitignore
        echo "# Security tools" >> .gitignore
        echo "venv-security/" >> .gitignore
        echo ".secrets.baseline" >> .gitignore
        echo "bandit-report.json" >> .gitignore
        echo "security-report.json" >> .gitignore
        print_status "Added security tool entries to .gitignore"
    fi
fi

# Create a simple security policy file
if [ ! -f "SECURITY.md" ]; then
    cat > SECURITY.md << 'EOF'
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it to us privately.
Do not create a public issue for security vulnerabilities.

## Security Measures

This project uses automated security scanning tools:

- **Bandit**: Python security scanner
- **Safety**: Python dependency vulnerability checker
- **Semgrep**: Static analysis for security patterns
- **detect-secrets**: Hardcoded secret detection
- **ESLint Security**: JavaScript security linting
- **Custom security checks**: Additional pattern matching

All commits are automatically scanned for security issues.
EOF
    print_status "Security policy created"
fi

print_step "9. Running initial security scan"
print_status "Testing the security setup..."

# Run a test of the pre-commit hooks
if pre-commit run --all-files > /dev/null 2>&1; then
    print_status "Pre-commit hooks test passed"
else
    print_warning "Pre-commit hooks found issues (this is expected with the demo vulnerable code)"
fi

# Deactivate virtual environment
deactivate

print_step "10. Setup complete!"
echo
echo "🎉 Security tools have been successfully installed and configured!"
echo
echo "📋 Next steps:"
echo "   1. Review the security findings in your code"
echo "   2. Fix any critical security issues"
echo "   3. Commit your changes (security hooks will run automatically)"
echo "   4. Read README-SECURITY.md for detailed usage instructions"
echo
echo "🔍 To run security checks manually:"
echo "   • Full scan: pre-commit run --all-files"
echo "   • Specific tool: bandit -r . -f json"
echo "   • Custom checks: python security-check.py <files>"
echo
echo "⚠️  Note: The pre-commit hooks will now run automatically before each commit."
echo "   Critical security issues will block commits until fixed."
echo
echo "🔗 For more information, see: README-SECURITY.md"

# Add the virtual environment to .gitignore if not already there
if [ -f ".gitignore" ] && ! grep -q "venv-security" .gitignore; then
    echo "venv-security/" >> .gitignore
fi

print_status "Setup script completed successfully!"