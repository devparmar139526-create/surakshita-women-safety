# Dispatch Feature - Backend Documentation

## Overview
The dispatch feature allows admin users to assign emergency response units to active incidents through the admin dashboard.

## Implementation Details

### 1. New API Endpoint: `/api/dispatch`

**Route:** `POST /api/dispatch`

**Authentication:** Admin only (`@admin_only` decorator)

**Security:** CSRF exempt (API endpoint)

**Request Body (JSON):**
```json
{
  "alert_id": 123,
  "unit_type": "police"
}
```

**Valid Unit Types:**
- `police` → Police Patrol
- `ambulance` → Ambulance
- `fire` → Fire Brigade
- `swat` → SWAT Team

**Success Response (200):**
```json
{
  "success": true,
  "message": "Police Patrol dispatched successfully",
  "alert_id": 123,
  "unit_type": "Police Patrol",
  "status": "Dispatched: Police Patrol"
}
```

**Error Responses:**

- **400 Bad Request** - Missing or invalid data:
```json
{
  "success": false,
  "message": "Missing alert_id or unit_type"
}
```

- **404 Not Found** - Incident doesn't exist:
```json
{
  "success": false,
  "message": "Incident not found"
}
```

- **500 Server Error** - Internal error:
```json
{
  "success": false,
  "message": "Server error: [error details]"
}
```

### 2. Updated Polling Endpoint: `/api/admin/poll/alerts`

**Improvements:**
1. **Strict Row-to-Dict Conversion:** Ensures SQLite Row objects are properly serialized
2. **DateTime Handling:** Converts all datetime objects to strings for JSON serialization
3. **Dispatch Status Inclusion:** Now includes incidents with `status LIKE 'Dispatched:%'` in the query
4. **Enhanced Query:**
```sql
SELECT i.*, u.username, u.email
FROM incidents i
JOIN users u ON i.user_id = u.id
WHERE (i.status = 'High Alert' OR i.status LIKE 'Dispatched:%' OR i.is_sos = 1) AND i.id > ?
ORDER BY i.id DESC
```

### 3. Database Schema Changes

**Status Field Enhancement:**
- Removed strict CHECK constraint to allow dynamic dispatch statuses
- Status can now contain values like:
  - `Pending`
  - `Resolved`
  - `High Alert`
  - `Dispatched: Police Patrol`
  - `Dispatched: Ambulance`
  - `Dispatched: Fire Brigade`
  - `Dispatched: SWAT Team`

**Updated Timestamp:**
- `updated_at` field is automatically set to `CURRENT_TIMESTAMP` when dispatch occurs

### 4. Security Features

**Admin Authentication:**
- Both new routes use `@admin_only` decorator
- Prevents unauthorized users from dispatching units
- Requires admin login through `/admin` portal

**Input Validation:**
- Unit type validated against whitelist
- Alert ID must exist in database
- Proper error handling for edge cases

**CSRF Protection:**
- Main app has CSRF enabled
- `/api/dispatch` is explicitly exempted for API access
- Still requires admin authentication

### 5. Frontend Integration

The dispatch feature integrates with `templates/admin_dashboard.html`:

**UI Elements:**
- Dropdown select with 5 options (Select Unit, Police, Ambulance, Fire, SWAT)
- "DISPATCH NOW" button with `.btn-swiss` styling
- Embedded in each active incident card

**JavaScript Function:**
```javascript
function dispatchUnit(alertId) {
    const selectElement = document.getElementById('dispatchUnit' + alertId);
    const unitType = selectElement.value;
    
    if (!unitType) {
        alert('Please select a unit type before dispatching.');
        return;
    }
    
    fetch('/api/dispatch', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            alert_id: alertId,
            unit_type: unitType
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`${unitType.toUpperCase()} unit dispatched successfully!`);
            selectElement.value = '';
        } else {
            alert('Dispatch failed: ' + (data.message || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error dispatching unit:', error);
        alert('Error dispatching unit. Please try again.');
    });
}
```

## Testing

**Test File:** `test_dispatch.py`

Run tests:
```bash
# 1. Start the Flask app
python app.py

# 2. In another terminal, run tests
python test_dispatch.py
```

**Note:** You must be logged in as admin in your browser for the tests to work (session-based authentication).

## Migration Guide

**No database migration required** - The status field is already TEXT type and can accept any value.

However, if you want to see the new feature in action:

1. Restart your Flask application
2. Log in to admin portal at `/admin` (username: admin, password: admin)
3. Navigate to Admin Dashboard
4. Find an active incident
5. Select a unit from the dropdown
6. Click "DISPATCH NOW"
7. Verify the status changes to "Dispatched: [Unit Name]"

## Monitoring & Logging

The dispatch action updates:
- `incidents.status` → "Dispatched: [Unit Name]"
- `incidents.updated_at` → Current timestamp

Future enhancement suggestion: Add a separate `dispatch_log` table to track:
- Dispatch timestamp
- Admin who dispatched
- Unit type dispatched
- Incident ID
- Response time

## Error Handling

All errors are gracefully handled and returned as JSON:
- Missing data → 400 Bad Request
- Invalid unit type → 400 Bad Request
- Non-existent incident → 404 Not Found
- Server errors → 500 Internal Server Error

All errors include descriptive messages for debugging.
