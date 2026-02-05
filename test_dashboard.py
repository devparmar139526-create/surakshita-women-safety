"""
Test Script for Surakshita Dashboard Features
This script tests the enhanced dashboard functionality
"""

import sqlite3
import json
from datetime import datetime, timedelta
import random

def create_test_data():
    """Create sample test data for dashboard visualization"""
    
    print("Creating test data for Surakshita dashboard...")
    
    # Connect to database
    conn = sqlite3.connect('surakshita.db')
    cursor = conn.cursor()
    
    # Check if test user exists
    cursor.execute("SELECT id FROM users WHERE username = 'testuser'")
    user = cursor.fetchone()
    
    if not user:
        print("⚠️  No test user found. Please register a user first.")
        conn.close()
        return
    
    user_id = user[0]
    print(f"✓ Found test user with ID: {user_id}")
    
    # Incident types
    incident_types = [
        'Harassment',
        'Stalking',
        'Assault',
        'Theft',
        'Suspicious Activity',
        'Unsafe Area'
    ]
    
    descriptions = [
        'Witnessed suspicious behavior in the area.',
        'Encountered harassment while commuting.',
        'Reported unsafe lighting in parking lot.',
        'Experienced verbal abuse near workplace.',
        'Noticed individual following at distance.',
        'Found area lacking security presence.',
        'Observed concerning activity late at night.',
        'Felt unsafe due to poor visibility.'
    ]
    
    # Generate incidents over last 30 days
    base_lat = 28.6139  # Delhi, India
    base_lng = 77.2090
    
    incidents_created = 0
    
    for i in range(25):  # Create 25 test incidents
        # Random date in last 30 days
        days_ago = random.randint(0, 30)
        incident_date = datetime.now() - timedelta(days=days_ago)
        
        # Random location within ~5km radius
        lat_offset = random.uniform(-0.05, 0.05)
        lng_offset = random.uniform(-0.05, 0.05)
        
        incident_type = random.choice(incident_types)
        description = random.choice(descriptions)
        latitude = base_lat + lat_offset
        longitude = base_lng + lng_offset
        status = random.choice(['Pending', 'Pending', 'Resolved'])  # 2/3 pending
        
        try:
            cursor.execute('''
                INSERT INTO incidents 
                (user_id, incident_type, description, latitude, longitude, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, 
                incident_type, 
                description, 
                latitude, 
                longitude, 
                status,
                incident_date.strftime('%Y-%m-%d %H:%M:%S'),
                incident_date.strftime('%Y-%m-%d %H:%M:%S')
            ))
            incidents_created += 1
        except Exception as e:
            print(f"✗ Error creating incident: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"✓ Created {incidents_created} test incidents")
    print("\nTest data generation complete!")
    print("\nYou can now:")
    print("1. Run 'python app.py' to start the application")
    print("2. Login with your test user credentials")
    print("3. View the enhanced dashboard with:")
    print("   - Interactive map with clustered markers")
    print("   - Heatmap visualization")
    print("   - Bar chart (Incidents by Category)")
    print("   - Line chart (Reports Over Time)")

def verify_database():
    """Verify database schema and structure"""
    print("\nVerifying database structure...")
    
    conn = sqlite3.connect('surakshita.db')
    cursor = conn.cursor()
    
    # Check users table
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"✓ Users table: {user_count} users")
    
    # Check incidents table
    cursor.execute("SELECT COUNT(*) FROM incidents")
    incident_count = cursor.fetchone()[0]
    print(f"✓ Incidents table: {incident_count} incidents")
    
    # Check incident types distribution
    cursor.execute("""
        SELECT incident_type, COUNT(*) as count 
        FROM incidents 
        GROUP BY incident_type 
        ORDER BY count DESC
    """)
    
    print("\nIncident distribution:")
    for row in cursor.fetchall():
        print(f"  - {row[0]}: {row[1]}")
    
    conn.close()

if __name__ == '__main__':
    print("=" * 60)
    print("Surakshita Dashboard Test Data Generator")
    print("=" * 60)
    
    try:
        create_test_data()
        verify_database()
        
        print("\n" + "=" * 60)
        print("✓ All tests completed successfully!")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("Make sure the database exists. Run 'python database.py' first.")
