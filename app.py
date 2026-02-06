from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3
import bcrypt
from functools import wraps
from datetime import datetime
import os
from config import config
from validators import validate_coordinates

# Initialize Flask app
app = Flask(__name__)

# Load configuration based on FLASK_ENV
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize extensions
csrf = CSRFProtect(app)  # Initialize CSRF protection
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=app.config.get('RATELIMIT_STORAGE_URL', 'memory://')
)

# Database helper function
def get_db():
    conn = sqlite3.connect('surakshita.db')
    conn.row_factory = sqlite3.Row
    return conn

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin portal decorator - separate from user authentication
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin_logged_in'):
            flash('Admin access required.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        
        # Check if user is admin
        conn = get_db()
        cursor = conn.cursor()
        user = cursor.execute(
            'SELECT is_admin FROM users WHERE id = ?', 
            (session['user_id'],)
        ).fetchone()
        conn.close()
        
        if not user or not user['is_admin']:
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Admin Portal Login - Separate from user authentication
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    """Dedicated admin portal login with hardcoded credentials"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Hardcoded admin credentials
        if username == 'admin' and password == 'admin':
            session.clear()  # Clear any existing user sessions to avoid conflicts
            session['is_admin_logged_in'] = True
            session['admin_username'] = 'admin'
            flash('Admin Portal Accessed', 'success')
            return redirect(url_for('admin_dashboard'))  # Explicit return for redirect
        
        flash('Invalid Credentials', 'error')
        return redirect(url_for('admin_login'))  # Redirect back to login on failure
    
    return render_template('admin_login.html')

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("3 per hour")
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))
        
        # Hash password with bcrypt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
            conn.close()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists.', 'error')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db()
        cursor = conn.cursor()
        user = cursor.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = bool(user['is_admin']) if 'is_admin' in user.keys() else False
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    cursor = conn.cursor()
    
    # Get incident statistics
    stats = cursor.execute('''
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) as pending,
            SUM(CASE WHEN status = 'Resolved' THEN 1 ELSE 0 END) as resolved
        FROM incidents
        WHERE user_id = ?
    ''', (session['user_id'],)).fetchone()
    
    # Convert Row objects to dictionaries for JSON serialization
    incidents_by_category = [dict(row) for row in cursor.execute('''
        SELECT incident_type, COUNT(*) as count
        FROM incidents
        WHERE user_id = ?
        GROUP BY incident_type
        ORDER BY count DESC
    ''', (session['user_id'],)).fetchall()]
    
    # Get reports over time for line chart (last 30 days)
    reports_over_time = [dict(row) for row in cursor.execute('''
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM incidents
        WHERE user_id = ? AND created_at >= DATE('now', '-30 days')
        GROUP BY DATE(created_at)
        ORDER BY date ASC
    ''', (session['user_id'],)).fetchall()]
    
    # Get recent incidents
    recent_incidents = cursor.execute('''
        SELECT * FROM incidents 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT 10
    ''', (session['user_id'],)).fetchall()
    
    conn.close()
    
    return render_template(
        'dashboard.html', 
        stats=stats, 
        incidents=recent_incidents,
        incidents_by_category=incidents_by_category,
        reports_over_time=reports_over_time
    )

@app.route('/incidents')
@login_required
def incidents():
    conn = get_db()
    cursor = conn.cursor()
    
    # Get filter parameter
    status_filter = request.args.get('status', 'all')
    
    if status_filter == 'all':
        incidents_list = cursor.execute('''
            SELECT * FROM incidents 
            WHERE user_id = ? 
            ORDER BY created_at DESC
        ''', (session['user_id'],)).fetchall()
    else:
        incidents_list = cursor.execute('''
            SELECT * FROM incidents 
            WHERE user_id = ? AND status = ?
            ORDER BY created_at DESC
        ''', (session['user_id'], status_filter.capitalize())).fetchall()
    
    conn.close()
    
    return render_template('incidents.html', incidents=incidents_list, current_filter=status_filter)

@app.route('/incidents/new', methods=['GET', 'POST'])
@login_required
def new_incident():
    if request.method == 'POST':
        incident_type = request.form.get('incident_type')
        description = request.form.get('description')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        
        # Validation
        if not all([incident_type, description, latitude, longitude]):
            flash('All fields are required.', 'error')
            return redirect(url_for('new_incident'))
        
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            
            # Validate coordinates are within Indian territories
            is_valid, error_msg = validate_coordinates(latitude, longitude)
            if not is_valid:
                flash(error_msg, 'error')
                return redirect(url_for('new_incident'))
            
            # Privacy: Round to 4 decimal places (~11m accuracy)
            latitude = round(latitude, 4)
            longitude = round(longitude, 4)
        except ValueError:
            flash('Invalid latitude or longitude values.', 'error')
            return redirect(url_for('new_incident'))
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO incidents (user_id, incident_type, description, latitude, longitude, status)
            VALUES (?, ?, ?, ?, ?, 'Pending')
        ''', (session['user_id'], incident_type, description, latitude, longitude))
        conn.commit()
        conn.close()
        
        flash('Incident reported successfully!', 'success')
        return redirect(url_for('incidents'))
    
    return render_template('new_incident.html')

@app.route('/incidents/<int:incident_id>/update', methods=['POST'])
@login_required
def update_incident_status(incident_id):
    new_status = request.form.get('status')
    
    if new_status not in ['Pending', 'Resolved']:
        flash('Invalid status.', 'error')
        return redirect(url_for('incidents'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Verify ownership
    incident = cursor.execute(
        'SELECT * FROM incidents WHERE id = ? AND user_id = ?',
        (incident_id, session['user_id'])
    ).fetchone()
    
    if not incident:
        flash('Incident not found.', 'error')
        conn.close()
        return redirect(url_for('incidents'))
    
    cursor.execute('''
        UPDATE incidents 
        SET status = ?, updated_at = CURRENT_TIMESTAMP 
        WHERE id = ? AND user_id = ?
    ''', (new_status, incident_id, session['user_id']))
    conn.commit()
    conn.close()
    
    flash(f'Incident status updated to {new_status}.', 'success')
    return redirect(url_for('incidents'))

# API endpoint for dispatching emergency units (Admin only) - New Route Format
@app.route('/api/dispatch/<int:incident_id>', methods=['POST'])
@csrf.exempt  # Exempt from CSRF for API endpoint
@login_required
@admin_required
def dispatch_emergency_unit(incident_id):
    """Admin endpoint to dispatch emergency units to incidents"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        unit = data.get('unit')
        
        if not unit:
            return jsonify({'success': False, 'message': 'Missing unit parameter'}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Verify incident exists
        incident = cursor.execute(
            'SELECT * FROM incidents WHERE id = ?',
            (incident_id,)
        ).fetchone()
        
        if not incident:
            conn.close()
            return jsonify({'success': False, 'message': 'Incident not found'}), 404
        
        # Update incident status to 'Dispatched' with unit info
        new_status = 'Dispatched'
        dispatch_note = f'{unit} unit dispatched at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        
        cursor.execute('''
            UPDATE incidents 
            SET status = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        ''', (new_status, incident_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': f'{unit} dispatched successfully',
            'incident_id': incident_id,
            'unit': unit,
            'status': new_status,
            'note': dispatch_note
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500

# Legacy API endpoint for backward compatibility with admin dashboard
@app.route('/api/dispatch', methods=['POST'])
@csrf.exempt  # Exempt from CSRF for API endpoint
@admin_only
def dispatch_emergency_unit_legacy():
    """Legacy admin endpoint for dispatch (backward compatibility)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        alert_id = data.get('alert_id')
        unit_type = data.get('unit_type')
        
        if not alert_id or not unit_type:
            return jsonify({'success': False, 'message': 'Missing alert_id or unit_type'}), 400
        
        # Validate unit type
        valid_units = ['police', 'ambulance', 'fire', 'swat']
        if unit_type.lower() not in valid_units:
            return jsonify({'success': False, 'message': 'Invalid unit type'}), 400
        
        # Map unit types to display names
        unit_names = {
            'police': 'Police Patrol',
            'ambulance': 'Ambulance',
            'fire': 'Fire Brigade',
            'swat': 'SWAT Team'
        }
        
        unit_display_name = unit_names.get(unit_type.lower(), unit_type)
        new_status = f'Dispatched: {unit_display_name}'
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Verify incident exists
        incident = cursor.execute(
            'SELECT * FROM incidents WHERE id = ?',
            (alert_id,)
        ).fetchone()
        
        if not incident:
            conn.close()
            return jsonify({'success': False, 'message': 'Incident not found'}), 404
        
        # Update incident status with dispatch information
        cursor.execute('''
            UPDATE incidents 
            SET status = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        ''', (new_status, alert_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': f'{unit_display_name} dispatched successfully',
            'alert_id': alert_id,
            'unit_type': unit_display_name,
            'status': new_status
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500

@app.route('/incidents/<int:incident_id>/delete', methods=['POST'])
@login_required
def delete_incident(incident_id):
    conn = get_db()
    cursor = conn.cursor()
    
    # Verify ownership and delete
    cursor.execute(
        'DELETE FROM incidents WHERE id = ? AND user_id = ?',
        (incident_id, session['user_id'])
    )
    conn.commit()
    
    if cursor.rowcount > 0:
        flash('Incident deleted successfully.', 'success')
    else:
        flash('Incident not found.', 'error')
    
    conn.close()
    return redirect(url_for('incidents'))

# API endpoint for map data and analytics
@app.route('/api/incidents')
@login_required
def api_incidents():
    conn = get_db()
    cursor = conn.cursor()
    incidents_list = cursor.execute('''
        SELECT id, incident_type, description, latitude, longitude, status, priority, is_sos, created_at
        FROM incidents 
        WHERE user_id = ?
        ORDER BY created_at DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return jsonify([dict(incident) for incident in incidents_list])

@app.route('/api/analytics')
@login_required
def api_analytics():
    conn = get_db()
    cursor = conn.cursor()
    
    # Incidents by category
    category_data = cursor.execute('''
        SELECT incident_type, COUNT(*) as count
        FROM incidents
        WHERE user_id = ?
        GROUP BY incident_type
        ORDER BY count DESC
    ''', (session['user_id'],)).fetchall()
    
    # Reports over time (last 30 days)
    timeline_data = cursor.execute('''
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM incidents
        WHERE user_id = ? AND created_at >= DATE('now', '-30 days')
        GROUP BY DATE(created_at)
        ORDER BY date ASC
    ''', (session['user_id'],)).fetchall()
    
    conn.close()
    
    return jsonify({
        'categories': [{'type': row['incident_type'], 'count': row['count']} for row in category_data],
        'timeline': [{'date': row['date'], 'count': row['count']} for row in timeline_data]
    })

# SOS Emergency Reporting Endpoint
@app.route('/api/report', methods=['POST'])
@login_required
@limiter.limit("1 per minute")
def api_report_sos():
    """Quick SOS reporting endpoint for emergency situations"""
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        incident_type = data.get('incident_type', 'SOS Emergency')
        description = data.get('description', 'Emergency SOS alert triggered')
        
        # Validation
        if not latitude or not longitude:
            return jsonify({'success': False, 'error': 'Location required'}), 400
        
        # Validate coordinates are within Indian territories
        is_valid, error_msg = validate_coordinates(latitude, longitude)
        if not is_valid:
            return jsonify({'success': False, 'error': error_msg}), 400
        
        # Privacy: Round to 4 decimal places (~11m accuracy)
        latitude = round(float(latitude), 4)
        longitude = round(float(longitude), 4)
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Insert SOS incident with High Alert status
        cursor.execute('''
            INSERT INTO incidents 
            (user_id, incident_type, description, latitude, longitude, status, priority, is_sos)
            VALUES (?, ?, ?, ?, ?, 'High Alert', 'Critical', 1)
        ''', (session['user_id'], incident_type, description, latitude, longitude))
        
        incident_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        flash('SOS alert sent successfully! Help is on the way.', 'success')
        
        return jsonify({
            'success': True,
            'message': 'SOS alert sent successfully',
            'incident_id': incident_id
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Real-time polling endpoint for new incidents
@app.route('/api/poll/incidents')
@login_required
def api_poll_incidents():
    """Polling endpoint to check for new incidents"""
    last_id = request.args.get('last_id', 0, type=int)
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get incidents newer than last_id
    new_incidents = cursor.execute('''
        SELECT id, incident_type, description, latitude, longitude, status, priority, is_sos, created_at
        FROM incidents 
        WHERE user_id = ? AND id > ?
        ORDER BY id DESC
    ''', (session['user_id'], last_id)).fetchall()
    
    conn.close()
    
    return jsonify({
        'incidents': [dict(inc) for inc in new_incidents],
        'count': len(new_incidents)
    })

# Admin Dashboard - Secure Portal with Separate Authentication
@app.route('/admin/dashboard')
@admin_only
def admin_dashboard():
    """Admin dashboard - Central Dispatch Monitor showing ALL incidents"""
    # Audit log: Track admin portal access
    print(f"[AUDIT] Admin Portal Access: username={session.get('admin_username')}, timestamp={datetime.now().isoformat()}, action='VIEW_ADMIN_DASHBOARD'")
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Separate active alerts (not resolved) from resolved incidents
    active_alerts = cursor.execute('''
        SELECT i.*, u.username, u.email
        FROM incidents i
        JOIN users u ON i.user_id = u.id
        WHERE i.status != 'Resolved'
        ORDER BY i.created_at DESC
    ''').fetchall()
    
    resolved_incidents = cursor.execute('''
        SELECT i.*, u.username, u.email
        FROM incidents i
        JOIN users u ON i.user_id = u.id
        WHERE i.status = 'Resolved'
        ORDER BY i.created_at DESC
    ''').fetchall()
    
    # Get statistics for admin view
    stats = cursor.execute('''
        SELECT 
            COUNT(*) as total_alerts,
            SUM(CASE WHEN status != 'Resolved' THEN 1 ELSE 0 END) as active_alerts,
            SUM(CASE WHEN status = 'Resolved' THEN 1 ELSE 0 END) as resolved_alerts
        FROM incidents
    ''').fetchone()
    
    conn.close()
    
    return render_template('admin_dashboard.html', 
                         active_alerts=active_alerts, 
                         resolved_incidents=resolved_incidents, 
                         stats=stats)

# API endpoint for admin to poll new alerts
@app.route('/api/admin/poll/alerts')
@admin_only
def api_admin_poll_alerts():
    """Admin polling endpoint for new high alerts with dispatch status"""
    last_id = request.args.get('last_id', 0, type=int)
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Fetch new alerts with proper serialization, including dispatch status
    new_alerts = cursor.execute('''
        SELECT i.*, u.username, u.email
        FROM incidents i
        JOIN users u ON i.user_id = u.id
        WHERE (i.status = 'High Alert' OR i.status LIKE 'Dispatched%' OR i.status = 'Dispatched' OR i.is_sos = 1) AND i.id > ?
        ORDER BY i.id DESC
    ''', (last_id,)).fetchall()
    
    conn.close()
    
    # Strictly convert SQLite Row objects to dictionaries
    serialized_alerts = []
    for row in new_alerts:
        alert_dict = dict(row)
        # Ensure all datetime objects are converted to strings
        if 'created_at' in alert_dict and alert_dict['created_at']:
            alert_dict['created_at'] = str(alert_dict['created_at'])
        if 'updated_at' in alert_dict and alert_dict['updated_at']:
            alert_dict['updated_at'] = str(alert_dict['updated_at'])
        
        # Ensure dispatch status is included for UI sync
        alert_dict['is_dispatched'] = alert_dict.get('status', '').startswith('Dispatched')
        
        serialized_alerts.append(alert_dict)
    
    return jsonify({
        'alerts': serialized_alerts,
        'count': len(serialized_alerts)
    })

if __name__ == '__main__':
    # Initialize database on first run
    from database import init_db
    init_db()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
