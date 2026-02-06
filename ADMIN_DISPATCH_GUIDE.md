# Admin Dispatch Feature - Quick Reference

## How to Dispatch Emergency Units

### Step 1: Access Admin Dashboard
1. Navigate to `/admin`
2. Login with credentials:
   - **Username:** admin
   - **Password:** admin
3. Click on "Admin Dashboard"

### Step 2: View Active Incidents
- Active incidents are displayed in the "Active Alerts" tab
- Each incident card shows:
  - Incident type
  - Description
  - User information
  - Location coordinates
  - Priority level

### Step 3: Dispatch a Unit
1. **Select Unit Type** from dropdown:
   - Police Patrol
   - Ambulance
   - Fire Brigade
   - SWAT Team

2. **Click "DISPATCH NOW"** button

3. **Confirmation:** 
   - Success message appears
   - Incident status updates to "Dispatched: [Unit Name]"
   - Dropdown resets to "Select Unit"

### Step 4: Monitor Dispatched Incidents
- Dispatched incidents remain in "Active Alerts" tab
- Status shows which unit was dispatched
- Updated timestamp reflects dispatch time

## Status Meanings

| Status | Meaning |
|--------|---------|
| Pending | Incident reported, awaiting action |
| High Alert | Critical incident requiring immediate attention |
| Dispatched: Police Patrol | Police unit dispatched to scene |
| Dispatched: Ambulance | Medical unit dispatched to scene |
| Dispatched: Fire Brigade | Fire response dispatched to scene |
| Dispatched: SWAT Team | Special tactical unit dispatched to scene |
| Resolved | Incident has been resolved |

## Additional Actions

### View Location on Map
- Click "View on Map" link
- Opens Google Maps with incident coordinates

### Call Emergency Services
- Click "CALL EMERGENCY" button
- Initiates call to 911

### Mark as Resolved
- Click "MARK RESOLVED" button
- Moves incident to "Resolved Archives" tab

## Auto-Refresh
- Dashboard auto-refreshes every 5 seconds
- New incidents appear automatically
- Manual refresh available via "Refresh Now" button

## Troubleshooting

### "Please select a unit type before dispatching"
**Issue:** No unit selected from dropdown
**Solution:** Select a unit type before clicking DISPATCH NOW

### "Dispatch failed: Incident not found"
**Issue:** Incident was deleted or doesn't exist
**Solution:** Refresh the page to see updated incident list

### "Dispatch failed: Invalid unit type"
**Issue:** Invalid data sent to server
**Solution:** Contact system administrator

### Dispatch button not responding
**Issue:** JavaScript or network error
**Solution:** 
1. Check browser console for errors (F12)
2. Verify internet connection
3. Refresh the page
4. Try again

## Security Notes

⚠️ **IMPORTANT:**
- Only admin users can dispatch units
- All dispatch actions are logged
- Unauthorized access attempts are blocked
- Use strong passwords for admin account

## Best Practices

1. **Assess Priority:** Review incident details before dispatching
2. **Choose Appropriate Unit:** Match unit type to incident type
3. **Monitor Progress:** Check "Updated" timestamp to track response time
4. **Mark Resolved:** Update status once incident is handled
5. **Document Actions:** Consider adding notes in external system

## Emergency Contacts

- **Police:** 911
- **Medical:** 911
- **Fire:** 911
- **Crisis Hotline:** [Add local number]

---

**For technical support or feature requests, contact the development team.**
