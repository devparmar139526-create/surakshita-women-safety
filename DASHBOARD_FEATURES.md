# Surakshita Dashboard - Enhanced Features Documentation

## Overview
The enhanced dashboard provides real-time analytics, interactive mapping, and comprehensive incident visualization using a professional dark admin theme.

## New Features

### 1. Interactive Map with Leaflet.js

**Features:**
- **Dark Theme Map**: Uses CARTO dark basemap for professional appearance
- **Clustered Markers**: Groups nearby incidents to prevent map clutter
- **Heatmap Layer**: Visualizes incident concentration areas
- **Custom Markers**: 
  - 🔴 Red markers = Pending incidents
  - 🟢 Green markers = Resolved incidents
- **Interactive Popups**: Click markers to view incident details
- **Auto-Fit Bounds**: Automatically zooms to show all incidents

**Technical Implementation:**
```javascript
// Map initialization with dark theme
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png')

// Marker clustering for better visualization
L.markerClusterGroup()

// Heatmap layer with custom gradient
L.heatLayer(heatData, {
    gradient: {
        0.0: '#3b82f6',  // Blue (low)
        0.5: '#f59e0b',  // Orange (medium)
        1.0: '#ef4444'   // Red (high)
    }
})
```

### 2. Chart.js Analytics

**Bar Chart - Incidents by Category:**
- Visualizes incident distribution across categories
- Color-coded bars for easy identification
- Shows: Harassment, Stalking, Assault, Theft, Suspicious Activity, etc.

**Line Chart - Reports Over Time:**
- Displays incident trends over the last 30 days
- Smooth curve with gradient fill
- Helps identify patterns and peak reporting times

**Chart Configuration:**
- Dark theme with custom colors
- Responsive design (adapts to screen size)
- Interactive tooltips on hover
- Grid lines for better readability

### 3. Enhanced API Endpoints

**`/api/incidents`** (GET)
- Returns all user incidents with full details
- Used by map and export features
- Response format:
```json
[
    {
        "id": 1,
        "incident_type": "Harassment",
        "description": "Incident details...",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "status": "Pending",
        "created_at": "2026-02-06T10:30:00"
    }
]
```

**`/api/analytics`** (GET)
- Provides aggregated analytics data
- Used for charts and statistics
- Response format:
```json
{
    "categories": [
        {"type": "Harassment", "count": 5},
        {"type": "Stalking", "count": 3}
    ],
    "timeline": [
        {"date": "2026-02-01", "count": 2},
        {"date": "2026-02-02", "count": 1}
    ]
}
```

### 4. Dark Admin Theme

**Design Elements:**
- **Background**: Deep navy (#0f172a)
- **Cards**: Gradient slate (#1e293b to #334155)
- **Accent Colors**:
  - Purple (#8b5cf6) - Primary actions
  - Blue (#3b82f6) - Information
  - Green (#10b981) - Success/Resolved
  - Yellow (#f59e0b) - Warning/Pending
  - Red (#ef4444) - Critical/Delete

**UI Components:**
- Glassmorphic stat cards with icons
- Smooth hover transitions
- Consistent border styling
- Professional shadows and spacing

### 5. Responsive Design

**Mobile Optimization:**
- Map height: 300px on mobile, 500px on desktop
- Chart height: 250px on mobile, 300px on desktop
- Stacked grid layouts on small screens
- Touch-friendly controls

**Breakpoints:**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## File Structure

```
Womens Safety/
├── app.py                          # Enhanced Flask routes
├── templates/
│   ├── base.html                   # Updated with dark nav
│   └── dashboard.html              # Complete dashboard redesign
├── static/
│   ├── styles.css                  # Custom dark theme styles
│   └── dashboard.js                # Dashboard utilities
└── README.md                       # Updated documentation
```

## Key Dependencies

### CDN Resources:
- **Leaflet.js** (v1.9.4): Base mapping library
- **Leaflet.markercluster** (v1.5.3): Marker clustering
- **Leaflet.heat** (v0.2.0): Heatmap visualization
- **Chart.js** (v4.4.0): Charts and analytics
- **Tailwind CSS**: Utility-first styling
- **Font Awesome** (v6.4.0): Icons

## Usage Guide

### Viewing the Dashboard:

1. **Login** to your account
2. Navigate to **Dashboard** (automatic redirect after login)
3. **Explore Features**:
   - View statistics in the top cards
   - Interact with the map (zoom, pan, click markers)
   - Analyze charts for patterns
   - Review recent incidents in the table

### Map Interactions:

- **Zoom**: Mouse wheel or +/- buttons
- **Pan**: Click and drag
- **View Details**: Click any marker
- **Cluster Info**: Click cluster to zoom in

### Chart Insights:

- **Hover** over bars/points to see exact values
- **Category Chart**: Identifies most common incident types
- **Timeline Chart**: Shows reporting trends

### Exporting Data:

Use the JavaScript utility function:
```javascript
exportToCSV() // Downloads incidents as CSV file
```

## Customization Options

### Changing Map Style:
Edit the tile layer URL in `dashboard.html`:
```javascript
// Light theme example
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')

// Satellite view example
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}')
```

### Adjusting Chart Colors:
Modify the `backgroundColor` and `borderColor` arrays in chart configurations.

### Customizing Theme:
Edit CSS variables in `static/styles.css`:
```css
:root {
    --dark-bg-primary: #your-color;
    --accent-purple: #your-color;
}
```

## Performance Considerations

- **Map Performance**: Clustering prevents rendering thousands of individual markers
- **Lazy Loading**: Charts render only when dashboard is accessed
- **API Caching**: Consider implementing Redis for high-traffic scenarios
- **Database Indexing**: Add indexes on `user_id` and `created_at` columns

## Security Notes

- All API endpoints require authentication (`@login_required`)
- Users can only access their own incidents
- Session-based security prevents unauthorized access
- No sensitive data exposed in API responses

## Future Enhancements

- [ ] Real-time updates with WebSockets
- [ ] Advanced filtering (date range, radius search)
- [ ] PDF report generation
- [ ] Email alerts for nearby incidents
- [ ] Admin dashboard for system-wide analytics
- [ ] Multi-language support
- [ ] Push notifications
- [ ] Incident collaboration features

## Troubleshooting

### Map Not Displaying:
1. Check browser console for errors
2. Verify CDN resources are loading
3. Ensure at least one incident exists
4. Check latitude/longitude values are valid

### Charts Not Rendering:
1. Verify Chart.js is loaded
2. Check data is being passed from Flask
3. Inspect browser console for JavaScript errors
4. Ensure canvas elements have proper IDs

### Dark Theme Issues:
1. Clear browser cache
2. Verify `styles.css` is loaded
3. Check for CSS conflicts
4. Use browser DevTools to inspect styles

## Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ⚠️ IE 11 (limited support)

## API Rate Limiting

Currently no rate limiting implemented. For production:
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: session.get('user_id'))

@app.route('/api/incidents')
@limiter.limit("100 per hour")
def api_incidents():
    # ...
```

## Contact & Support

For issues or feature requests, please contact the development team.

---

**Last Updated**: February 6, 2026  
**Version**: 2.0.0  
**Author**: Surakshita Development Team
