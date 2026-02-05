# Surakshita SOS Real-Time Reporting System

## 🚨 Overview

The SOS Real-Time Reporting System enables users to quickly send emergency alerts with their exact location. The system features instant notification, real-time polling, and a dedicated admin dashboard for monitoring critical incidents.

## ✨ Key Features

### 1. **Emergency SOS Button**
- **Location**: Fixed button in bottom-right corner of dashboard
- **Visibility**: Prominent red button with pulsing animation
- **Accessibility**: Always visible, one-click access
- **Mobile Responsive**: Adapts size for mobile devices

### 2. **Automatic Geolocation Capture**
- **Browser API**: Uses HTML5 Geolocation API
- **High Accuracy**: Requests precise GPS coordinates
- **Permission Handling**: Clear user prompts for location access
- **Error Handling**: Graceful fallback if location unavailable

### 3. **Quick Report Modal**
- **Incident Type Selection**: Pre-defined emergency categories
- **Optional Description**: User can add brief details
- **Visual Feedback**: Real-time status updates
- **One-Click Submit**: Streamlined for emergency situations

### 4. **High Alert Status**
- **Database Priority**: SOS incidents marked as "Critical"
- **Status**: Automatically set to "High Alert"
- **Flagging**: `is_sos` boolean field for quick filtering
- **Visibility**: Clearly distinguished in all views

### 5. **Real-Time Updates**
- **Polling Interval**: Every 5 seconds
- **User Dashboard**: Checks for new incidents
- **Admin Dashboard**: Monitors all SOS alerts
- **Notifications**: Toast notifications for new alerts

## 🛠️ Technical Implementation

### Database Schema Updates

```sql
-- New columns added to incidents table
ALTER TABLE incidents ADD COLUMN priority TEXT DEFAULT 'Normal';
ALTER TABLE incidents ADD COLUMN is_sos BOOLEAN DEFAULT 0;

-- Updated status CHECK constraint
CHECK (status IN ('Pending', 'Resolved', 'High Alert'))

-- Priority levels
CHECK (priority IN ('Normal', 'High', 'Critical'))
```

### API Endpoints

#### POST /api/report
**Purpose**: Submit emergency SOS alert

**Request Body**:
```json
{
    "latitude": 28.6139,
    "longitude": 77.2090,
    "incident_type": "SOS Emergency",
    "description": "Emergency situation description"
}
```

**Response**:
```json
{
    "success": true,
    "message": "SOS alert sent successfully",
    "incident_id": 123
}
```

**Features**:
- Requires authentication
- Validates GPS coordinates
- Sets status to "High Alert"
- Sets priority to "Critical"
- Marks `is_sos` as true

#### GET /api/poll/incidents
**Purpose**: Poll for new user incidents

**Parameters**:
- `last_id` (integer): Last known incident ID

**Response**:
```json
{
    "incidents": [...],
    "count": 2
}
```

#### GET /api/admin/poll/alerts
**Purpose**: Poll for new high-priority alerts (admin)

**Parameters**:
- `last_id` (integer): Last known alert ID

**Response**:
```json
{
    "alerts": [...],
    "count": 1
}
```

### Frontend Components

#### SOS Button (HTML/CSS)
```html
<div class="sos-button" id="sosButton">
    <i class="fas fa-exclamation-triangle"></i>
    <div>SOS</div>
</div>
```

**Styling**:
- Fixed position (bottom-right)
- Red gradient background
- Pulsing animation
- Box shadow with glow effect
- Hover scale effect

#### SOS Modal
**Features**:
- Fullscreen overlay (dark background)
- Centered modal dialog
- Incident type dropdown
- Description textarea
- Real-time status updates
- Submit and Cancel buttons

#### JavaScript Functions

**sendSOS()**
```javascript
function sendSOS() {
    // 1. Get user location
    navigator.geolocation.getCurrentPosition(...)
    
    // 2. Collect form data
    // 3. Send POST to /api/report
    // 4. Show success/error feedback
    // 5. Reload page to show new incident
}
```

**pollForNewIncidents()**
```javascript
function pollForNewIncidents() {
    // 1. Fetch from /api/poll/incidents
    // 2. Check for new incidents
    // 3. Show notifications
    // 4. Update UI
}
```

**showNotification()**
```javascript
function showNotification(title, message, type) {
    // Creates toast notification
    // Auto-dismisses after 5 seconds
    // Positioned top-right
}
```

## 📱 User Experience Flow

### Sending an SOS Alert

1. **User clicks SOS button** (bottom-right corner)
2. **Modal opens** with emergency form
3. **Browser requests location permission**
4. **User optionally selects incident type**
5. **User clicks "Send SOS Alert"**
6. **System captures GPS coordinates**
7. **Alert sent to backend**
8. **Confirmation shown to user**
9. **Page reloads with new incident**
10. **Admin dashboard updated in real-time**

### Receiving SOS Notifications (Dashboard)

1. **User's dashboard polls every 5 seconds**
2. **New incidents detected**
3. **Toast notification appears** (top-right)
4. **If SOS**: Red "High Alert" notification
5. **Dashboard auto-refreshes after 2 seconds**
6. **New incident appears on map and in list**

## 🔧 Admin Dashboard Features

### Real-Time Monitoring

**Access**: `/admin/dashboard`

**Features**:
- View all SOS alerts system-wide
- Real-time polling (5-second intervals)
- Visual distinction for active alerts
- Pulsing animation on critical alerts
- Auto-refresh when new alerts arrive

### Statistics Cards

1. **Total SOS Alerts**: All-time count
2. **Active Alerts**: Currently unresolved
3. **Resolved**: Successfully handled

### Alert Cards

**Information Displayed**:
- Incident type with SOS badge
- Description
- User details (username, email)
- Timestamp
- GPS coordinates
- Priority level
- Active status indicator

**Actions Available**:
- **View on Map**: Google Maps link
- **Call Emergency**: Tel link (911)
- **Mark Resolved**: Update status

### Notifications

- **Visual**: Toast notification (top-right)
- **Audio**: Beep sound on new alert
- **Animation**: Pulsing red border
- **Auto-dismiss**: 8 seconds

## 🎨 Visual Design

### Color Coding

| Status | Color | Usage |
|--------|-------|-------|
| SOS/Critical | Red (#dc2626) | SOS button, alerts |
| High Alert | Yellow (#f59e0b) | Active monitoring |
| Resolved | Green (#10b981) | Completed alerts |
| Normal | Blue (#3b82f6) | Standard incidents |

### Animations

**Pulse Animation** (SOS Button):
```css
@keyframes pulse-sos {
    0%, 100% {
        box-shadow: 0 8px 20px rgba(220, 38, 38, 0.5),
                    0 0 0 0 rgba(220, 38, 38, 0.7);
    }
    50% {
        box-shadow: 0 8px 20px rgba(220, 38, 38, 0.5),
                    0 0 0 20px rgba(220, 38, 38, 0);
    }
}
```

**Alert Card Pulse**:
```css
@keyframes pulse-alert {
    0%, 100% {
        box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7);
    }
    50% {
        box-shadow: 0 0 0 15px rgba(220, 38, 38, 0);
    }
}
```

## 📊 Data Flow Diagram

```
┌─────────────┐
│   User      │
│  Dashboard  │
└──────┬──────┘
       │
       │ 1. Click SOS Button
       ▼
┌─────────────┐
│  SOS Modal  │
│  (Browser)  │
└──────┬──────┘
       │
       │ 2. Get Geolocation
       ▼
┌─────────────────┐
│ Geolocation API │
└──────┬──────────┘
       │
       │ 3. Return Coordinates
       ▼
┌───────────────┐
│  POST Request │
│  /api/report  │
└──────┬────────┘
       │
       │ 4. Save to Database
       ▼
┌──────────────────┐
│   SQLite DB      │
│  (High Alert)    │
└──────┬───────────┘
       │
       │ 5. Success Response
       ▼
┌────────────────┐
│  User Notified │
│  (Confirmation)│
└────────────────┘
       │
       │ 6. Auto-Refresh
       ▼
┌─────────────────────┐
│  Updated Dashboard  │
└─────────────────────┘

     ┌──────────────┐
     │   Polling    │
     │  (Every 5s)  │
     └──────┬───────┘
            │
            ▼
     ┌─────────────────┐
     │  Admin Dashboard│
     │  (Real-time)    │
     └─────────────────┘
```

## 🔒 Security Considerations

### Authentication
- All endpoints require login (`@login_required`)
- Session-based authentication
- User can only see their own incidents
- Admin sees all SOS alerts

### Location Privacy
- GPS coordinates only sent when user clicks SOS
- User explicitly grants location permission
- Coordinates used only for emergency response
- No background location tracking

### Data Validation
- Latitude/longitude validated as floats
- Required fields checked before insert
- SQL injection prevention (parameterized queries)
- Input sanitization on frontend

## 📱 Mobile Responsiveness

### SOS Button
```css
@media (max-width: 768px) {
    .sos-button {
        bottom: 1rem;
        right: 1rem;
        width: 70px;
        height: 70px;
    }
}
```

### Modal
- Full-screen on mobile
- Touch-friendly buttons
- Large tap targets (minimum 44x44px)
- Optimized for one-handed use

## 🧪 Testing

### Manual Testing Steps

1. **Test SOS Button**:
   ```
   ✓ Click SOS button
   ✓ Modal opens
   ✓ Select incident type
   ✓ Add description
   ✓ Grant location permission
   ✓ Click "Send SOS Alert"
   ✓ Verify success message
   ✓ Check dashboard shows new alert
   ```

2. **Test Real-Time Polling**:
   ```
   ✓ Open dashboard in two windows
   ✓ Send SOS from window 1
   ✓ Verify notification in window 2 (within 5s)
   ✓ Check auto-refresh occurs
   ```

3. **Test Admin Dashboard**:
   ```
   ✓ Navigate to /admin/dashboard
   ✓ Verify all SOS alerts shown
   ✓ Send new SOS
   ✓ Verify notification appears
   ✓ Check statistics update
   ✓ Click "Mark Resolved"
   ✓ Verify status changes
   ```

### Browser Compatibility

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| Geolocation | ✓ | ✓ | ✓ | ✓ |
| Fetch API | ✓ | ✓ | ✓ | ✓ |
| CSS Animations | ✓ | ✓ | ✓ | ✓ |
| Web Audio API | ✓ | ✓ | ✓ | ✓ |

## 🚀 Performance Optimization

### Polling Strategy
- **Interval**: 5 seconds (configurable)
- **Lightweight**: Only fetches new data
- **Efficient**: Uses `last_id` to filter
- **Scalable**: Minimal database queries

### Database Indexing
```sql
-- Recommended indexes for performance
CREATE INDEX idx_incidents_is_sos ON incidents(is_sos);
CREATE INDEX idx_incidents_status ON incidents(status);
CREATE INDEX idx_incidents_created_at ON incidents(created_at);
CREATE INDEX idx_incidents_user_id ON incidents(user_id);
```

## 📞 Emergency Integration

### Google Maps Integration
```javascript
https://www.google.com/maps?q=${latitude},${longitude}
```

### Emergency Call Link
```html
<a href="tel:911">Call Emergency</a>
```

### Future Enhancements
- [ ] SMS alerts to emergency contacts
- [ ] Email notifications
- [ ] Integration with local police API
- [ ] Automated dispatch system
- [ ] Two-way communication
- [ ] Live location tracking
- [ ] Emergency contact notifications

## 📝 Configuration

### Polling Interval
```javascript
// In dashboard.html
pollingInterval = setInterval(pollForNewIncidents, 5000); // 5 seconds
```

### Geolocation Options
```javascript
{
    enableHighAccuracy: true,  // Use GPS
    timeout: 10000,            // 10 second timeout
    maximumAge: 0              // No cache
}
```

### Notification Duration
```javascript
setTimeout(() => notification.remove(), 5000); // 5 seconds
```

## 🎯 Success Metrics

- **Response Time**: SOS sent within 2 seconds
- **Location Accuracy**: < 10 meters (high accuracy mode)
- **Notification Delay**: < 5 seconds (polling interval)
- **Uptime**: 99.9% availability
- **Error Rate**: < 0.1% failed SOS submissions

---

**Version**: 2.1.0  
**Last Updated**: February 6, 2026  
**Feature**: Real-Time SOS Reporting System  
**Status**: ✅ Production Ready
