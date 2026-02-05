# Surakshita - Quick Start Guide

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- PowerShell (Windows)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Step-by-Step Setup

#### 1. Navigate to Project Directory
```powershell
cd "c:\Users\Dev\OneDrive\Documents\Womens Safety"
```

#### 2. Create Virtual Environment
```powershell
python -m venv venv
```

#### 3. Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

**Note**: If you encounter an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 4. Install Dependencies
```powershell
pip install -r requirements.txt
```

#### 5. Initialize Database
```powershell
python database.py
```

Expected output:
```
Database initialized successfully!
```

#### 6. (Optional) Create Test Data
```powershell
# First, run the app and register a user named 'testuser'
# Then run this to populate test data:
python test_dashboard.py
```

#### 7. Run the Application
```powershell
python app.py
```

Expected output:
```
Database initialized successfully!
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://[your-local-ip]:5000
Press CTRL+C to quit
```

#### 8. Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## 📝 First Time Usage

### 1. Register an Account
- Click "Register here" on the login page
- Enter:
  - Username (unique)
  - Email (unique)
  - Password
  - Confirm Password
- Click "Create Account"

### 2. Login
- Enter your username and password
- Click "Sign in"

### 3. Explore the Dashboard

You'll see:

**Statistics Cards:**
- Total Incidents
- Pending Incidents
- Resolved Incidents

**Interactive Map:**
- Dark theme with clustered markers
- Red markers = Pending incidents
- Green markers = Resolved incidents
- Click markers for details
- Heatmap showing incident density

**Analytics Charts:**
- Bar Chart: Incidents by Category
- Line Chart: Reports Over Time (30 days)

**Recent Incidents Table:**
- Type, Description, Location, Status, Date

### 4. Report Your First Incident

1. Click "Report" button in navigation
2. Fill in the form:
   - **Incident Type**: Select from dropdown
   - **Description**: Detailed information
   - **Latitude**: GPS coordinate (or click "Use Current Location")
   - **Longitude**: GPS coordinate
3. Click "Submit Incident"

### 5. Manage Incidents

1. Navigate to "Incidents" page
2. Filter by status: All / Pending / Resolved
3. Actions available:
   - **Mark Resolved/Pending**: Toggle status
   - **Delete**: Remove incident (with confirmation)

## 🎨 Dashboard Features Overview

### Map Interactions
- **Zoom**: Mouse wheel or +/- buttons
- **Pan**: Click and drag map
- **Cluster Click**: Zoom into clustered area
- **Marker Click**: View incident popup

### Chart Features
- **Hover**: See exact values
- **Responsive**: Auto-adjusts to screen size
- **Dark Theme**: Consistent UI

### Navigation
- **Dashboard**: Analytics overview
- **Incidents**: Full incident list
- **Report**: Create new incident
- **Logout**: End session

## 🔧 Troubleshooting

### Issue: Virtual Environment Won't Activate
**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Module Not Found
**Solution**:
```powershell
pip install -r requirements.txt
```

### Issue: Database Error
**Solution**:
```powershell
# Reinitialize database
python database.py
```

### Issue: Port Already in Use
**Solution**:
Edit `app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

### Issue: Map Not Displaying
**Causes**:
1. No incidents reported yet
2. Browser blocking CDN resources
3. JavaScript errors

**Solution**:
1. Report at least one incident
2. Check browser console (F12) for errors
3. Verify internet connection (CDN resources required)

### Issue: Charts Not Rendering
**Solution**:
1. Clear browser cache
2. Hard refresh (Ctrl + Shift + R)
3. Check browser console for errors

## 📊 Sample Data Generation

To quickly test dashboard features with realistic data:

```powershell
# 1. Register a user with username: testuser
# 2. Login with that user
# 3. Run the test script
python test_dashboard.py
```

This creates:
- 25 sample incidents
- Various incident types
- Distribution over last 30 days
- Random locations near Delhi, India
- Mix of Pending and Resolved statuses

## 🌐 API Testing

### Using Browser
Navigate to (while logged in):
```
http://localhost:5000/api/incidents
http://localhost:5000/api/analytics
```

### Using PowerShell
```powershell
# Get incidents (requires session cookie)
Invoke-WebRequest -Uri "http://localhost:5000/api/incidents" -UseBasicParsing
```

### Using Python
```python
import requests

# Login first
session = requests.Session()
login_data = {
    'username': 'testuser',
    'password': 'yourpassword'
}
session.post('http://localhost:5000/login', data=login_data)

# Get incidents
response = session.get('http://localhost:5000/api/incidents')
incidents = response.json()
print(incidents)
```

## 🔒 Security Notes

### Development vs Production

**Current Setup (Development)**:
- `debug=True` (shows detailed errors)
- `host='0.0.0.0'` (accessible on network)
- Random secret key (changes on restart)

**For Production**:
1. Set `debug=False`
2. Use environment variables for secrets
3. Use proper WSGI server (Gunicorn, uWSGI)
4. Enable HTTPS
5. Add rate limiting
6. Use PostgreSQL instead of SQLite

### Secure Secret Key

For production, use a fixed secret key:

```python
import os
app.secret_key = os.environ.get('SECRET_KEY') or 'your-secure-secret-key-here'
```

Generate secure key:
```python
import secrets
print(secrets.token_hex(32))
```

## 📱 Mobile Access

Access from mobile devices on same network:

1. Find your computer's IP address:
```powershell
ipconfig
```

2. Look for "IPv4 Address" (e.g., 192.168.1.100)

3. On mobile browser, navigate to:
```
http://192.168.1.100:5000
```

## 🎓 Learning Resources

### Understanding the Code
- `app.py`: Flask routes and logic
- `database.py`: SQLite schema
- `templates/dashboard.html`: Frontend visualization
- `static/styles.css`: Custom styling

### Technologies Used
- **Flask**: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- **Leaflet.js**: [https://leafletjs.com/](https://leafletjs.com/)
- **Chart.js**: [https://www.chartjs.org/](https://www.chartjs.org/)
- **Tailwind CSS**: [https://tailwindcss.com/](https://tailwindcss.com/)

## 📞 Support

For issues or questions:
1. Check `DASHBOARD_FEATURES.md` for detailed documentation
2. Review error messages in terminal
3. Check browser console (F12) for JavaScript errors
4. Verify all dependencies are installed

## ✅ Quick Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed from requirements.txt
- [ ] Database initialized (surakshita.db exists)
- [ ] Application running on port 5000
- [ ] Can access login page at localhost:5000
- [ ] Can register and login successfully
- [ ] Dashboard displays statistics
- [ ] Map loads with dark theme
- [ ] Charts render properly
- [ ] Can create new incidents
- [ ] Can view incidents list
- [ ] Can update incident status
- [ ] Can delete incidents

---

**Version**: 2.0.0  
**Last Updated**: February 6, 2026  
**Status**: Production Ready ✓
