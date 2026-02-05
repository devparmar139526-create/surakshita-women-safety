"""
Security Testing Script for Surakshita
Tests all security controls and generates a report
"""

import sqlite3
import re
import os
from typing import List, Tuple

class SecurityTester:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.results = []
    
    def test(self, name: str, condition: bool, details: str = ""):
        """Record test result"""
        if condition:
            self.tests_passed += 1
            status = "✅ PASS"
        else:
            self.tests_failed += 1
            status = "❌ FAIL"
        
        result = f"{status} - {name}"
        if details:
            result += f"\n     {details}"
        
        self.results.append(result)
        print(result)
    
    def report(self):
        """Print final report"""
        total = self.tests_passed + self.tests_failed
        percentage = (self.tests_passed / total * 100) if total > 0 else 0
        
        print("\n" + "="*70)
        print("🔐 SECURITY TEST REPORT")
        print("="*70)
        print(f"Total Tests: {total}")
        print(f"Passed: {self.tests_passed} ✅")
        print(f"Failed: {self.tests_failed} ❌")
        print(f"Success Rate: {percentage:.1f}%")
        print("="*70)
        
        if self.tests_failed == 0:
            print("\n🎉 ALL SECURITY TESTS PASSED!")
            print("✅ Application is production-ready from security perspective")
        else:
            print("\n⚠️  SECURITY ISSUES DETECTED")
            print("❌ Review failed tests before deployment")
        
        return self.tests_failed == 0


def test_sql_injection_protection():
    """Test SQL injection vulnerabilities"""
    tester = SecurityTester()
    print("\n🔍 Testing SQL Injection Protection...")
    print("-" * 70)
    
    # Check app.py for parameterized queries
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for dangerous patterns
        dangerous_patterns = [
            (r'execute\(["\'].*%s.*["\']', "String formatting in SQL"),
            (r'execute\(f["\']', "F-string in SQL"),
            (r'execute\(["\'].*\+.*["\']', "String concatenation in SQL"),
            (r'execute\(["\'].* format\(', ".format() in SQL"),
        ]
        
        for pattern, description in dangerous_patterns:
            matches = re.findall(pattern, content)
            tester.test(
                f"No {description}",
                len(matches) == 0,
                f"Found {len(matches)} instances" if matches else ""
            )
        
        # Check for parameterized queries
        param_queries = re.findall(r'execute\([^)]*\?[^)]*\)', content)
        tester.test(
            "Parameterized queries used",
            len(param_queries) > 0,
            f"Found {len(param_queries)} parameterized queries"
        )
    
    except FileNotFoundError:
        tester.test("app.py exists", False, "File not found")
    
    return tester.report()


def test_xss_protection():
    """Test XSS protection"""
    tester = SecurityTester()
    print("\n🔍 Testing XSS Protection...")
    print("-" * 70)
    
    # Check templates for safe filters
    import os
    template_dir = 'templates'
    
    if os.path.exists(template_dir):
        safe_filter_found = False
        autoescape_disabled = False
        
        for filename in os.listdir(template_dir):
            if filename.endswith('.html'):
                filepath = os.path.join(template_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for | safe filter (dangerous)
                if '| safe' in content or '|safe' in content:
                    safe_filter_found = True
                    tester.test(
                        f"No '| safe' filter in {filename}",
                        False,
                        "Found unsafe filter - review manually"
                    )
                
                # Check for autoescape disabled
                if 'autoescape' in content and 'false' in content.lower():
                    autoescape_disabled = True
        
        if not safe_filter_found:
            tester.test("No '| safe' filters in templates", True)
        
        tester.test(
            "Autoescape not disabled",
            not autoescape_disabled,
            "Jinja2 autoescape should be enabled"
        )
        
        # Check for CSP headers in app.py
        try:
            with open('app.py', 'r', encoding='utf-8') as f:
                app_content = f.read()
            
            has_csp = 'Content-Security-Policy' in app_content
            tester.test(
                "Content-Security-Policy header configured",
                has_csp,
                "Adds defense-in-depth against XSS"
            )
        except:
            pass
    else:
        tester.test("Templates directory exists", False)
    
    return tester.report()


def test_admin_authorization():
    """Test admin role authorization"""
    tester = SecurityTester()
    print("\n🔍 Testing Admin Authorization...")
    print("-" * 70)
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for admin_required decorator
        has_admin_decorator = 'def admin_required' in content
        tester.test(
            "admin_required decorator exists",
            has_admin_decorator,
            "Decorator function defined"
        )
        
        # Check if admin routes are protected
        admin_routes = [
            r"@app\.route\('/admin/dashboard'\).*?@admin_required",
            r"@app\.route\('/api/admin/poll/alerts'\).*?@admin_required",
        ]
        
        for pattern in admin_routes:
            is_protected = bool(re.search(pattern, content, re.DOTALL))
            route_name = pattern.split("'")[1]
            tester.test(
                f"Route {route_name} protected",
                is_protected,
                "Should have @admin_required decorator"
            )
        
        # Check database schema
        if os.path.exists('surakshita.db'):
            conn = sqlite3.connect('surakshita.db')
            cursor = conn.cursor()
            
            # Check if is_admin column exists
            columns = cursor.execute("PRAGMA table_info(users)").fetchall()
            has_admin_column = any(col[1] == 'is_admin' for col in columns)
            
            tester.test(
                "is_admin column in users table",
                has_admin_column,
                "Database schema updated"
            )
            
            conn.close()
        else:
            tester.test("Database exists", False, "Run database.py first")
    
    except FileNotFoundError:
        tester.test("app.py exists", False)
    
    return tester.report()


def test_csrf_protection():
    """Test CSRF protection"""
    tester = SecurityTester()
    print("\n🔍 Testing CSRF Protection...")
    print("-" * 70)
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for Flask-WTF import
        has_wtf_import = 'flask_wtf' in content.lower() or 'CSRFProtect' in content
        tester.test(
            "Flask-WTF imported",
            has_wtf_import,
            "CSRF protection library loaded"
        )
        
        # Check for CSRFProtect initialization
        has_csrf_init = 'CSRFProtect' in content and 'csrf = CSRFProtect' in content
        tester.test(
            "CSRFProtect initialized",
            has_csrf_init,
            "CSRF protection active"
        )
        
        # Check templates for CSRF tokens
        template_dir = 'templates'
        forms_with_csrf = 0
        forms_without_csrf = 0
        
        if os.path.exists(template_dir):
            for filename in os.listdir(template_dir):
                if filename.endswith('.html'):
                    filepath = os.path.join(template_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        template_content = f.read()
                    
                    # Count forms
                    forms = re.findall(r'<form[^>]*method=["\']post["\'][^>]*>', template_content, re.IGNORECASE)
                    csrf_tokens = re.findall(r'csrf_token\(\)', template_content)
                    
                    if len(forms) > 0:
                        if len(csrf_tokens) > 0:
                            forms_with_csrf += len(forms)
                        else:
                            forms_without_csrf += len(forms)
            
            tester.test(
                "POST forms have CSRF tokens",
                forms_without_csrf == 0,
                f"{forms_with_csrf} protected, {forms_without_csrf} unprotected"
            )
    
    except FileNotFoundError:
        tester.test("app.py exists", False)
    
    return tester.report()


def test_rate_limiting():
    """Test rate limiting configuration"""
    tester = SecurityTester()
    print("\n🔍 Testing Rate Limiting...")
    print("-" * 70)
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for Flask-Limiter
        has_limiter_import = 'flask_limiter' in content.lower() or 'Limiter' in content
        tester.test(
            "Flask-Limiter imported",
            has_limiter_import,
            "Rate limiting library loaded"
        )
        
        has_limiter_init = 'limiter = Limiter' in content
        tester.test(
            "Limiter initialized",
            has_limiter_init,
            "Rate limiter configured"
        )
        
        # Check for rate limits on critical endpoints
        critical_endpoints = [
            ('api_report_sos', 'SOS endpoint'),
            ('login', 'Login endpoint'),
            ('register', 'Registration endpoint'),
        ]
        
        for func_name, description in critical_endpoints:
            # Look for @limiter.limit decorator before function
            pattern = rf'@limiter\.limit.*?def {func_name}'
            has_limit = bool(re.search(pattern, content, re.DOTALL))
            tester.test(
                f"{description} rate limited",
                has_limit,
                "Should have @limiter.limit decorator"
            )
    
    except FileNotFoundError:
        tester.test("app.py exists", False)
    
    return tester.report()


def test_session_security():
    """Test session security configuration"""
    tester = SecurityTester()
    print("\n🔍 Testing Session Security...")
    print("-" * 70)
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for secure secret key
        has_env_secret = 'os.getenv' in content and 'SECRET_KEY' in content
        tester.test(
            "SECRET_KEY from environment",
            has_env_secret,
            "Secret key should be loaded from .env"
        )
        
        not_using_urandom = 'os.urandom(24)' not in content or 'os.getenv' in content
        tester.test(
            "Not using os.urandom directly",
            not_using_urandom,
            "Should use persistent secret key"
        )
        
        # Check for session security flags
        security_configs = [
            ('SESSION_COOKIE_SECURE', 'HTTPS-only cookies'),
            ('SESSION_COOKIE_HTTPONLY', 'No JavaScript access'),
            ('SESSION_COOKIE_SAMESITE', 'CSRF mitigation'),
            ('PERMANENT_SESSION_LIFETIME', 'Session timeout'),
        ]
        
        for config, description in security_configs:
            has_config = config in content
            tester.test(
                f"{config} configured",
                has_config,
                description
            )
    
    except FileNotFoundError:
        tester.test("app.py exists", False)
    
    return tester.report()


def test_input_validation():
    """Test input validation"""
    tester = SecurityTester()
    print("\n🔍 Testing Input Validation...")
    print("-" * 70)
    
    # Check if validators.py exists
    validators_exists = os.path.exists('validators.py')
    tester.test(
        "validators.py module exists",
        validators_exists,
        "Input validation functions"
    )
    
    if validators_exists:
        try:
            from validators import (
                validate_coordinates,
                validate_description,
                validate_incident_type,
                validate_email,
                validate_username,
                validate_password
            )
            
            # Test coordinate validation
            valid, _ = validate_coordinates(28.6139, 77.2090)
            tester.test("Valid coordinates accepted", valid)
            
            valid, _ = validate_coordinates(999, 999)
            tester.test("Invalid coordinates rejected", not valid)
            
            # Test description validation
            valid, _ = validate_description("Normal description")
            tester.test("Valid description accepted", valid)
            
            valid, _ = validate_description("<script>alert('xss')</script>")
            tester.test("XSS in description rejected", not valid)
            
            valid, _ = validate_description("A" * 501)
            tester.test("Long description rejected", not valid)
            
            # Test incident type validation
            valid, _ = validate_incident_type("Harassment")
            tester.test("Valid incident type accepted", valid)
            
            valid, _ = validate_incident_type("InvalidType")
            tester.test("Invalid incident type rejected", not valid)
            
        except ImportError as e:
            tester.test("Import validators", False, str(e))
    
    return tester.report()


def test_security_headers():
    """Test security headers configuration"""
    tester = SecurityTester()
    print("\n🔍 Testing Security Headers...")
    print("-" * 70)
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for after_request handler
        has_after_request = '@app.after_request' in content
        tester.test(
            "after_request handler exists",
            has_after_request,
            "For adding security headers"
        )
        
        # Check for specific headers
        headers = [
            ('Content-Security-Policy', 'XSS protection'),
            ('X-Frame-Options', 'Clickjacking protection'),
            ('X-Content-Type-Options', 'MIME sniffing protection'),
            ('Strict-Transport-Security', 'HTTPS enforcement'),
            ('Referrer-Policy', 'Privacy protection'),
        ]
        
        for header, description in headers:
            has_header = header in content
            tester.test(
                f"{header} configured",
                has_header,
                description
            )
    
    except FileNotFoundError:
        tester.test("app.py exists", False)
    
    return tester.report()


def test_dependency_security():
    """Test for secure dependencies"""
    tester = SecurityTester()
    print("\n🔍 Testing Dependency Security...")
    print("-" * 70)
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
        
        # Check for security packages
        security_packages = [
            ('Flask-WTF', 'CSRF protection'),
            ('Flask-Limiter', 'Rate limiting'),
            ('bcrypt', 'Password hashing'),
            ('python-dotenv', 'Environment management'),
        ]
        
        for package, purpose in security_packages:
            has_package = package in requirements
            tester.test(
                f"{package} installed",
                has_package,
                purpose
            )
    
    except FileNotFoundError:
        tester.test("requirements.txt exists", False)
    
    return tester.report()


def main():
    """Run all security tests"""
    import os
    
    print("="*70)
    print("🔐 SURAKSHITA SECURITY TESTING SUITE")
    print("="*70)
    print("\nRunning comprehensive security tests...\n")
    
    all_passed = True
    
    # Run all tests
    all_passed &= test_sql_injection_protection()
    all_passed &= test_xss_protection()
    all_passed &= test_admin_authorization()
    all_passed &= test_csrf_protection()
    all_passed &= test_rate_limiting()
    all_passed &= test_session_security()
    all_passed &= test_input_validation()
    all_passed &= test_security_headers()
    all_passed &= test_dependency_security()
    
    print("\n" + "="*70)
    if all_passed:
        print("🎉 ALL SECURITY TEST SUITES PASSED!")
        print("✅ Application meets security requirements")
        print("\nRecommendation: ✅ APPROVED FOR PRODUCTION")
    else:
        print("⚠️  SOME SECURITY TESTS FAILED")
        print("❌ Review failures and implement fixes")
        print("\nRecommendation: ⚠️  IMPLEMENT SECURITY HARDENING")
        print("See SECURITY_HARDENING.md for implementation guide")
    print("="*70)
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
