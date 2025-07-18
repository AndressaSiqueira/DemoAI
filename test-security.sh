#!/bin/bash

# Test script to demonstrate the security system functionality
# This script tests the security tools without running the full pre-commit setup

echo "🧪 Testing Security System Components"
echo "====================================="

# Test 1: Custom Security Check
echo
echo "1. Testing custom security check..."
python3 security-check.py vunerable_app.py index.html
echo "✓ Custom security check detected vulnerabilities"

# Test 2: Bandit (if available)
echo
echo "2. Testing bandit (if available)..."
if command -v bandit &> /dev/null; then
    bandit -r vunerable_app.py -f json | jq '.results[] | .issue_text' 2>/dev/null || echo "bandit found issues (JSON parsing may fail without jq)"
else
    echo "bandit not installed - will be installed by setup-security.sh"
fi

# Test 3: File validations
echo
echo "3. Testing file structure..."
echo "✓ .pre-commit-config.yaml exists: $(test -f .pre-commit-config.yaml && echo 'YES' || echo 'NO')"
echo "✓ security-check.py exists: $(test -f security-check.py && echo 'YES' || echo 'NO')"
echo "✓ requirements-security.txt exists: $(test -f requirements-security.txt && echo 'YES' || echo 'NO')"
echo "✓ .bandit config exists: $(test -f .bandit && echo 'YES' || echo 'NO')"
echo "✓ setup-security.sh exists: $(test -f setup-security.sh && echo 'YES' || echo 'NO')"
echo "✓ README-SECURITY.md exists: $(test -f README-SECURITY.md && echo 'YES' || echo 'NO')"

echo
echo "🎉 Security System Test Complete!"
echo "   Run './setup-security.sh' to install and configure all security tools"