#!/usr/bin/env python3
"""
Custom Security Check Script for Pre-commit Hook

This script performs additional security validations beyond standard tools.
It checks for common security vulnerabilities and patterns in Python and JavaScript files.
"""

import re
import sys
import os
import json
import hashlib
from typing import List, Dict, Any, Tuple
import argparse


class SecurityChecker:
    """Custom security checker for various file types"""
    
    def __init__(self):
        self.issues = []
        self.critical_patterns = self._load_critical_patterns()
        self.warning_patterns = self._load_warning_patterns()
    
    def _load_critical_patterns(self) -> Dict[str, List[Dict[str, str]]]:
        """Load critical security patterns that should fail the commit"""
        return {
            'python': [
                {
                    'pattern': r'subprocess\.(call|run|Popen|check_output|check_call)\([^)]*shell\s*=\s*True',
                    'message': 'Command injection vulnerability: shell=True with subprocess',
                    'severity': 'CRITICAL'
                },
                {
                    'pattern': r'os\.system\s*\(',
                    'message': 'Command injection vulnerability: os.system usage',
                    'severity': 'CRITICAL'
                },
                {
                    'pattern': r'eval\s*\(',
                    'message': 'Code injection vulnerability: eval() usage',
                    'severity': 'CRITICAL'
                },
                {
                    'pattern': r'exec\s*\(',
                    'message': 'Code injection vulnerability: exec() usage',
                    'severity': 'CRITICAL'
                },
                {
                    'pattern': r'pickle\.load\s*\(',
                    'message': 'Deserialization vulnerability: pickle.load usage',
                    'severity': 'CRITICAL'
                },
                {
                    'pattern': r'\.decode\s*\(\s*[\'"]base64[\'"]',
                    'message': 'Potential obfuscated code or data',
                    'severity': 'HIGH'
                },
                {
                    'pattern': r'[\'"]?(?:password|pwd|secret|token|key|api_key|private_key|secret_key)[\'"]?\s*[=:]\s*[\'"][^\'"\s]{8,}[\'"]',
                    'message': 'Hardcoded secret detected',
                    'severity': 'CRITICAL'
                },
                {
                    'pattern': r'requests\.(get|post|put|delete|patch|head|options)\([^)]*verify\s*=\s*False',
                    'message': 'SSL/TLS verification disabled',
                    'severity': 'HIGH'
                },
                {
                    'pattern': r'urllib3\.disable_warnings',
                    'message': 'SSL/TLS warnings disabled',
                    'severity': 'HIGH'
                },
                {
                    'pattern': r'jwt\.decode\([^)]*verify\s*=\s*False',
                    'message': 'JWT signature verification disabled',
                    'severity': 'CRITICAL'
                },
                {
                    'pattern': r'django\.conf\.settings\.DEBUG\s*=\s*True',
                    'message': 'Django debug mode enabled in production',
                    'severity': 'HIGH'
                },
                {
                    'pattern': r'app\.config\[[\'"](DEBUG|TESTING)[\'"]\]\s*=\s*True',
                    'message': 'Flask debug/testing mode enabled',
                    'severity': 'HIGH'
                },
                {
                    'pattern': r'\.format\s*\([^)]*\{[^}]*\}',
                    'message': 'Potential format string vulnerability',
                    'severity': 'MEDIUM'
                },
                {
                    'pattern': r'%\s*[^%\s]+\s*%',
                    'message': 'Potential SQL injection with string formatting',
                    'severity': 'HIGH'
                }
            ],
            'javascript': [
                {
                    'pattern': r'eval\s*\(',
                    'message': 'Code injection vulnerability: eval() usage',
                    'severity': 'CRITICAL'
                },
                {
                    'pattern': r'innerHTML\s*=\s*[^;]*\+',
                    'message': 'Potential XSS vulnerability: innerHTML with concatenation',
                    'severity': 'HIGH'
                },
                {
                    'pattern': r'document\.write\s*\(',
                    'message': 'Potential XSS vulnerability: document.write usage',
                    'severity': 'HIGH'
                },
                {
                    'pattern': r'\.html\s*\([^)]*\+',
                    'message': 'Potential XSS vulnerability: jQuery .html() with concatenation',
                    'severity': 'HIGH'
                },
                {
                    'pattern': r'[\'"]?(?:password|pwd|secret|token|key|api_key|private_key|secret_key)[\'"]?\s*[=:]\s*[\'"][^\'"\s]{8,}[\'"]',
                    'message': 'Hardcoded secret detected',
                    'severity': 'CRITICAL'
                },
                {
                    'pattern': r'Math\.random\s*\(\s*\)',
                    'message': 'Cryptographically insecure random number generation',
                    'severity': 'MEDIUM'
                },
                {
                    'pattern': r'XMLHttpRequest\s*\(\s*\)',
                    'message': 'Consider using fetch() instead of XMLHttpRequest',
                    'severity': 'LOW'
                },
                {
                    'pattern': r'localStorage\.(setItem|getItem)',
                    'message': 'Sensitive data in localStorage may be accessible to XSS',
                    'severity': 'MEDIUM'
                },
                {
                    'pattern': r'sessionStorage\.(setItem|getItem)',
                    'message': 'Sensitive data in sessionStorage may be accessible to XSS',
                    'severity': 'MEDIUM'
                },
                {
                    'pattern': r'window\.location\s*=\s*[^;]*\+',
                    'message': 'Potential open redirect vulnerability',
                    'severity': 'HIGH'
                },
                {
                    'pattern': r'postMessage\s*\(',
                    'message': 'Ensure postMessage usage validates origin',
                    'severity': 'MEDIUM'
                }
            ]
        }
    
    def _load_warning_patterns(self) -> Dict[str, List[Dict[str, str]]]:
        """Load warning patterns that should be flagged but not fail the commit"""
        return {
            'python': [
                {
                    'pattern': r'# TODO.*(?:security|auth|password|token)',
                    'message': 'Security-related TODO comment found',
                    'severity': 'INFO'
                },
                {
                    'pattern': r'print\s*\([^)]*(?:password|secret|token|key)',
                    'message': 'Potential information disclosure: printing sensitive data',
                    'severity': 'MEDIUM'
                },
                {
                    'pattern': r'logging\..*\([^)]*(?:password|secret|token|key)',
                    'message': 'Potential information disclosure: logging sensitive data',
                    'severity': 'MEDIUM'
                }
            ],
            'javascript': [
                {
                    'pattern': r'console\.log\s*\([^)]*(?:password|secret|token|key)',
                    'message': 'Potential information disclosure: console logging sensitive data',
                    'severity': 'MEDIUM'
                },
                {
                    'pattern': r'alert\s*\([^)]*(?:password|secret|token|key)',
                    'message': 'Potential information disclosure: alert with sensitive data',
                    'severity': 'MEDIUM'
                }
            ]
        }
    
    def check_file(self, filepath: str) -> List[Dict[str, Any]]:
        """Check a single file for security issues"""
        if not os.path.exists(filepath):
            return []
        
        file_extension = os.path.splitext(filepath)[1].lower()
        file_type = self._get_file_type(filepath, file_extension)
        
        if file_type not in self.critical_patterns:
            return []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return [{'filepath': filepath, 'error': f'Failed to read file: {str(e)}'}]
        
        issues = []
        
        # Check critical patterns
        for pattern_info in self.critical_patterns[file_type]:
            matches = re.finditer(pattern_info['pattern'], content, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                issues.append({
                    'filepath': filepath,
                    'line': line_num,
                    'message': pattern_info['message'],
                    'severity': pattern_info['severity'],
                    'matched_text': match.group(0)[:100],  # Truncate for readability
                    'type': 'security'
                })
        
        # Check warning patterns
        for pattern_info in self.warning_patterns.get(file_type, []):
            matches = re.finditer(pattern_info['pattern'], content, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                issues.append({
                    'filepath': filepath,
                    'line': line_num,
                    'message': pattern_info['message'],
                    'severity': pattern_info['severity'],
                    'matched_text': match.group(0)[:100],
                    'type': 'warning'
                })
        
        return issues
    
    def _get_file_type(self, filepath: str, extension: str) -> str:
        """Determine file type based on extension and content"""
        if extension in ['.py', '.pyw']:
            return 'python'
        elif extension in ['.js', '.jsx', '.ts', '.tsx']:
            return 'javascript'
        elif extension in ['.html', '.htm']:
            # Check if HTML file contains JavaScript
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if '<script' in content.lower():
                        return 'javascript'
            except:
                pass
        return 'unknown'
    
    def check_files(self, filepaths: List[str]) -> Tuple[List[Dict[str, Any]], bool]:
        """Check multiple files and return issues and whether to fail"""
        all_issues = []
        has_critical = False
        
        for filepath in filepaths:
            issues = self.check_file(filepath)
            all_issues.extend(issues)
            
            # Check if any critical issues found
            for issue in issues:
                if issue.get('severity') == 'CRITICAL':
                    has_critical = True
        
        return all_issues, has_critical
    
    def format_output(self, issues: List[Dict[str, Any]]) -> str:
        """Format issues for output"""
        if not issues:
            return "✅ No security issues found!"
        
        output = []
        output.append("🔒 Security Issues Found:")
        output.append("=" * 50)
        
        # Group by severity
        severity_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']
        severity_symbols = {
            'CRITICAL': '🚨',
            'HIGH': '⚠️',
            'MEDIUM': '⚡',
            'LOW': '💡',
            'INFO': 'ℹ️'
        }
        
        for severity in severity_order:
            severity_issues = [issue for issue in issues if issue.get('severity') == severity]
            if severity_issues:
                output.append(f"\n{severity_symbols.get(severity, '❓')} {severity} ({len(severity_issues)} issues)")
                output.append("-" * 30)
                for issue in severity_issues:
                    output.append(f"  📁 {issue['filepath']}:{issue.get('line', '?')}")
                    output.append(f"  💬 {issue['message']}")
                    if 'matched_text' in issue:
                        output.append(f"  🔍 Code: {issue['matched_text']}")
                    output.append("")
        
        return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='Custom security checker for pre-commit')
    parser.add_argument('files', nargs='*', help='Files to check')
    parser.add_argument('--config', help='Configuration file (unused for now)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if not args.files:
        print("✅ No files to check")
        sys.exit(0)
    
    checker = SecurityChecker()
    issues, has_critical = checker.check_files(args.files)
    
    if issues:
        print(checker.format_output(issues))
        
        # Print summary
        critical_count = len([i for i in issues if i.get('severity') == 'CRITICAL'])
        high_count = len([i for i in issues if i.get('severity') == 'HIGH'])
        
        print(f"\n📊 Summary: {len(issues)} total issues found")
        print(f"   🚨 Critical: {critical_count}")
        print(f"   ⚠️  High: {high_count}")
        print(f"   ⚡ Medium: {len([i for i in issues if i.get('severity') == 'MEDIUM'])}")
        print(f"   💡 Low: {len([i for i in issues if i.get('severity') == 'LOW'])}")
        print(f"   ℹ️  Info: {len([i for i in issues if i.get('severity') == 'INFO'])}")
        
        if has_critical:
            print("\n🛑 COMMIT BLOCKED: Critical security issues must be fixed!")
            sys.exit(1)
        else:
            print("\n⚠️  WARNING: Security issues found but commit allowed")
            sys.exit(0)
    else:
        print("✅ No security issues found!")
        sys.exit(0)


if __name__ == "__main__":
    main()