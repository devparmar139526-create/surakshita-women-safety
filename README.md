# Surakshita - Women Safety Analytics

A production-ready web application for tracking and managing women's safety incidents with advanced analytics, real-time SOS reporting, and visualization.

## ✨ Features

### Core Features
- **User Authentication**: Secure registration and login with bcrypt password hashing
- **Incident Management**: Report, track, and manage safety incidents
- **Location Tracking**: Incidents include GPS coordinates (latitude/longitude)
- **Status Management**: Mark incidents as Pending, Resolved, or High Alert
- **Mobile Responsive**: Professional UI built with Tailwind CSS

### 🎯 Enhanced Dashboard Features (v2.0)
- **Interactive Map**: Leaflet.js with dark theme, clustered markers, and heatmap visualization
- **Real-time Analytics**: Chart.js powered bar and line charts
- **Dark Admin Theme**: Professional dark UI for better focus and reduced eye strain
- **Category Analysis**: Bar chart showing incidents by type
- **Trend Analysis**: Line chart displaying reports over the last 30 days
- **API Endpoints**: RESTful API for data export and integration

### 🚨 Real-Time SOS System (v2.1) NEW!
- **Emergency SOS Button**: One-click emergency alert with GPS location capture
- **Instant Geolocation**: Automatic GPS coordinate capture using browser API
- **High Alert Status**: SOS incidents marked as "Critical" priority
- **Real-Time Polling**: 5-second polling for instant dashboard updates
- **Admin Monitoring**: Dedicated admin dashboard for all SOS alerts
- **Notifications**: Toast notifications and sound alerts for new emergencies
- **Quick Response**: Direct links to Google Maps and emergency services

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite with High Alert support
- **Frontend**: Tailwind CSS, Font Awesome
- **Mapping**: Leaflet.js, Leaflet.markercluster, Leaflet.heat
- **Analytics**: Chart.js
- **Real-Time**: JavaScript polling (5-second intervals)
- **Geolocation**: HTML5 Geolocation API
- **Security**: bcrypt password hashing, session management

## 📁 Project Structure

```
Womens Safety/
├── app.py                       # Main Flask application with API routes
├── database.py                  # Database initialization script
├── requirements.txt             # Python dependencies
├── README.md                    # Main documentation
├── DASHBOARD_FEATURES.md        # Enhanced dashboard documentation
├── static/                      # Static files
│   ├── styles.css              # Custom dark theme styles
│   └── dashboard.js            # Dashboard utilities
├── templates/                   # HTML templates
│   ├── base.html               # Base template with dark nav
│   ├── login.html              # User login
│   ├── register.html           # User registration
│   ├── dashboard.html          # Enhanced analytics dashboard
│   ├── incidents.html          # Incidents list
│   └── new_incident.html       # Report new incident
└── surakshita.db               # SQLite database (created on first run)
```

## 📊 Database Schema

### Users Table
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- created_at

### Incidents Table
- id (Primary Key)
- user_id (Foreign Key)
- incident_type
- description
- latitude
- longitude
- status (Pending/Resolved)
- created_at
- updated_at

## Setup Instructions

### 1. Create Virtual Environment

```powershell
# Navigate to project directory
cd "c:\Users\Dev\OneDrive\Documents\Womens Safety"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
# Install required packages
pip install -r requirements.txt
```

### 3. Run the Application

```powershell
# Run the Flask application
python app.py
```

The application will be available at: `http://localhost:5000`

## 🎮 Usage

1. **Register**: Create a new account with username, email, and password
2. **Login**: Sign in with your credentials
3. **Dashboard**: 
   - View real-time statistics (Total, Pending, Resolved)
   - Explore interactive map with clustered markers and heatmap
   - Analyze incident trends with Chart.js visualizations
   - Review recent incidents table
4. **Report Incident**: Submit new safety incidents with location data (GPS coordinates)
5. **Manage Incidents**: Update status (Pending/Resolved) or delete incidents
6. **Filter**: View incidents by status (All/Pending/Resolved)

## 🔒 Security Features

- Passwords are hashed using bcrypt before storage
- Session-based authentication with secure secret key
- Login required for all incident-related operations
- User can only access their own incidents (data isolation)
- CSRF protection through Flask sessions

## 🌐 API Endpoints

### Public Endpoints
- `GET /` - Home (redirects to login or dashboard)
- `GET/POST /register` - User registration
- `GET/POST /login` - User login

### Protected Endpoints (Require Authentication)
- `GET /logout` - User logout
- `GET /dashboard` - Enhanced analytics dashboard
- `GET /incidents` - View all incidents (with filters)
- `GET/POST /incidents/new` - Report new incident
- `POST /incidents/<id>/update` - Update incident status
- `POST /incidents/<id>/delete` - Delete incident

### API Endpoints (JSON)
- `GET /api/incidents` - Get all user incidents (full details)
- `GET /api/analytics` - Get analytics data (categories & timeline)

## 🎨 Dashboard Visualization

### Interactive Map Features:
- **Dark Theme Basemap**: Professional CARTO dark tiles
- **Clustered Markers**: Automatic grouping of nearby incidents
- **Heatmap Layer**: Color-coded density visualization
- **Status-based Markers**: Red (Pending) / Green (Resolved)
- **Interactive Popups**: Click markers for incident details
- **Auto-zoom**: Fits bounds to show all incidents

### Chart Analytics:
- **Bar Chart**: Incidents by Category (Harassment, Stalking, Assault, etc.)
- **Line Chart**: Reports Over Time (30-day trend analysis)
- **Dark Theme**: Consistent with admin portal aesthetic
- **Responsive**: Adapts to mobile and desktop screens

## 🚀 Advanced Features

### Data Export:
Use the JavaScript utility to export incidents:
```javascript
exportToCSV() // Downloads all incidents as CSV
```

### Custom Styling:
- Dark admin theme with gradient backgrounds
- Professional color palette (Purple, Blue, Green, Yellow, Red)
- Smooth animations and transitions
- Responsive design for all devices

## 🔧 Configuration

### Map Customization:
Edit tile layer in `templates/dashboard.html`:
```javascript
// Change to light theme
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')
```

### Theme Colors:
Modify CSS variables in `static/styles.css`:
```css
:root {
    --dark-bg-primary: #0f172a;
    --accent-purple: #8b5cf6;
}
```

## 📱 Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## 🎯 Future Enhancements

- ✅ Interactive map visualization using Leaflet.js (Completed)
- ✅ Heat maps for incident concentration (Completed)
- ✅ Chart.js analytics (Completed)
- Email notifications
- SMS alerts for nearby incidents
- Admin panel for monitoring
- Export incidents to CSV/PDF
- Multi-language support

## License

This project is created for educational and safety awareness purposes.

## Support

For issues or questions, please contact the development team.
