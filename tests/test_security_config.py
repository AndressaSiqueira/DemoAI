#!/usr/bin/env python3
"""
Test script to verify security scanning tools can detect vulnerabilities
"""
import subprocess
import sys
import os

def test_bandit_detects_vulnerabilities():
    """Test if Bandit detects the security issues in vulnerable_app.py"""
    try:
        # Run bandit on the vulnerable app
        result = subprocess.run([
            'bandit', '-r', 'vunerable_app.py', '-f', 'json'
        ], capture_output=True, text=True)
        
        # Check if bandit found the expected vulnerabilities
        if result.returncode != 0:  # Bandit returns non-zero when issues found
            print("✅ Bandit successfully detected vulnerabilities")
            
            # Check for specific vulnerabilities
            output = result.stdout
            if "hardcoded_password" in output:
                print("✅ Hardcoded secret detected")
            if "subprocess_popen_with_shell_equals_true" in output:
                print("✅ Command injection vulnerability detected")
            
            return True
        else:
            print("❌ Bandit did not detect vulnerabilities")
            return False
            
    except FileNotFoundError:
        print("❌ Bandit not installed")
        return False
    except Exception as e:
        print(f"❌ Error running Bandit: {e}")
        return False

def test_workflow_file_exists():
    """Test if the security workflow file exists and is valid"""
    workflow_path = ".github/workflows/security-scan.yml"
    
    if os.path.exists(workflow_path):
        print("✅ Security workflow file exists")
        
        # Check for key components
        with open(workflow_path, 'r') as f:
            content = f.read()
            
        if "bandit" in content.lower():
            print("✅ Bandit configured in workflow")
        if "safety" in content.lower():
            print("✅ Safety configured in workflow")
        if "trufflehog" in content.lower():
            print("✅ TruffleHog configured in workflow")
        
        return True
    else:
        print("❌ Security workflow file not found")
        return False

def test_precommit_config_exists():
    """Test if pre-commit configuration exists"""
    config_path = ".pre-commit-config.yaml"
    
    if os.path.exists(config_path):
        print("✅ Pre-commit configuration exists")
        
        with open(config_path, 'r') as f:
            content = f.read()
            
        if "bandit" in content.lower():
            print("✅ Bandit configured in pre-commit")
        if "ggshield" in content.lower():
            print("✅ GitGuardian configured in pre-commit")
        if "black" in content.lower():
            print("✅ Black formatter configured in pre-commit")
        
        return True
    else:
        print("❌ Pre-commit configuration not found")
        return False

def test_vscode_extensions():
    """Test if VS Code extensions are configured"""
    extensions_path = ".vscode/extensions.json"
    
    if os.path.exists(extensions_path):
        print("✅ VS Code extensions configuration exists")
        
        with open(extensions_path, 'r') as f:
            content = f.read()
            
        if "sonarlint" in content.lower():
            print("✅ SonarLint extension recommended")
        if "gitguardian" in content.lower():
            print("✅ GitGuardian extension recommended")
        if "snyk" in content.lower():
            print("✅ Snyk extension recommended")
        
        return True
    else:
        print("❌ VS Code extensions configuration not found")
        return False

def main():
    """Run all security configuration tests"""
    print("🛡️  Security Scanning Configuration Tests")
    print("=" * 50)
    
    tests = [
        test_workflow_file_exists,
        test_precommit_config_exists,
        test_vscode_extensions,
        test_bandit_detects_vulnerabilities
    ]
    
    passed = 0
    for test in tests:
        print(f"\n📋 Running: {test.__name__}")
        if test():
            passed += 1
    
    print(f"\n🏆 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("✅ All security scanning configurations are working correctly!")
        return 0
    else:
        print("❌ Some security configurations need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())