"""
Verification Script for Surakshita Dashboard
Checks that all components are properly configured
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✓ {description}: Found")
        return True
    else:
        print(f"✗ {description}: Missing")
        return False

def verify_installation():
    """Verify all required files and structure"""
    
    print("=" * 60)
    print("Surakshita Dashboard Verification")
    print("=" * 60)
    print()
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    all_good = True
    
    print("Checking Core Files...")
    print("-" * 60)
    
    core_files = {
        "app.py": "Main Flask Application",
        "database.py": "Database Initialization",
        "requirements.txt": "Python Dependencies",
        ".gitignore": "Git Ignore File"
    }
    
    for filename, desc in core_files.items():
        filepath = os.path.join(base_path, filename)
        if not check_file_exists(filepath, desc):
            all_good = False
    
    print()
    print("Checking Templates...")
    print("-" * 60)
    
    template_files = {
        "templates/base.html": "Base Template",
        "templates/login.html": "Login Page",
        "templates/register.html": "Registration Page",
        "templates/dashboard.html": "Enhanced Dashboard",
        "templates/incidents.html": "Incidents List",
        "templates/new_incident.html": "Report Form"
    }
    
    for filepath, desc in template_files.items():
        full_path = os.path.join(base_path, filepath)
        if not check_file_exists(full_path, desc):
            all_good = False
    
    print()
    print("Checking Static Files...")
    print("-" * 60)
    
    static_files = {
        "static/styles.css": "Custom CSS Styles",
        "static/dashboard.js": "Dashboard JavaScript"
    }
    
    for filepath, desc in static_files.items():
        full_path = os.path.join(base_path, filepath)
        if not check_file_exists(full_path, desc):
            all_good = False
    
    print()
    print("Checking Documentation...")
    print("-" * 60)
    
    doc_files = {
        "README.md": "Main Documentation",
        "QUICKSTART.md": "Setup Guide",
        "DASHBOARD_FEATURES.md": "Feature Documentation",
        "DASHBOARD_DESIGN.md": "Design Guide",
        "IMPLEMENTATION_SUMMARY.md": "Summary"
    }
    
    for filename, desc in doc_files.items():
        filepath = os.path.join(base_path, filename)
        if not check_file_exists(filepath, desc):
            all_good = False
    
    print()
    print("Checking Python Dependencies...")
    print("-" * 60)
    
    try:
        import flask
        print("✓ Flask: Installed")
    except ImportError:
        print("✗ Flask: Not installed")
        all_good = False
    
    try:
        import bcrypt
        print("✓ bcrypt: Installed")
    except ImportError:
        print("✗ bcrypt: Not installed")
        all_good = False
    
    print()
    print("Checking Dashboard Features...")
    print("-" * 60)
    
    # Check dashboard.html for key features
    dashboard_path = os.path.join(base_path, "templates/dashboard.html")
    if os.path.exists(dashboard_path):
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            features = {
                "leaflet.js": "Leaflet.js (Mapping)",
                "markercluster": "Marker Clustering",
                "leaflet-heat": "Heatmap Layer",
                "chart.js": "Chart.js (Analytics)",
                "categoryChart": "Category Bar Chart",
                "timelineChart": "Timeline Line Chart",
                "dark-card": "Dark Theme Styling"
            }
            
            for key, desc in features.items():
                if key.lower() in content.lower():
                    print(f"✓ {desc}: Implemented")
                else:
                    print(f"✗ {desc}: Missing")
                    all_good = False
    
    print()
    print("Checking Flask Routes...")
    print("-" * 60)
    
    # Check app.py for required routes
    app_path = os.path.join(base_path, "app.py")
    if os.path.exists(app_path):
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            routes = {
                "@app.route('/dashboard')": "Dashboard Route",
                "@app.route('/api/incidents')": "Incidents API",
                "@app.route('/api/analytics')": "Analytics API",
                "incidents_by_category": "Category Analytics",
                "reports_over_time": "Timeline Analytics"
            }
            
            for key, desc in routes.items():
                if key in content:
                    print(f"✓ {desc}: Configured")
                else:
                    print(f"✗ {desc}: Missing")
                    all_good = False
    
    print()
    print("=" * 60)
    
    if all_good:
        print("✓ ALL CHECKS PASSED!")
        print()
        print("Your Surakshita Dashboard is ready to run!")
        print()
        print("Next steps:")
        print("1. Activate virtual environment: .\\venv\\Scripts\\Activate.ps1")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Run the app: python app.py")
        print("4. Open browser: http://localhost:5000")
    else:
        print("✗ SOME CHECKS FAILED")
        print()
        print("Please review the missing items above.")
        print("Refer to QUICKSTART.md for setup instructions.")
    
    print("=" * 60)
    
    return all_good

if __name__ == '__main__':
    success = verify_installation()
    sys.exit(0 if success else 1)
