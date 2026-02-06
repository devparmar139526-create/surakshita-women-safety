"""
Test script for the new Dispatch feature
Run this to verify the dispatch endpoint works correctly
"""

import requests
import json

# Test configuration
BASE_URL = "http://localhost:5000"
TEST_ALERT_ID = 1  # Change this to a valid incident ID

def test_dispatch_endpoint():
    """Test the dispatch API endpoint"""
    
    print("=" * 60)
    print("DISPATCH FEATURE TEST")
    print("=" * 60)
    
    # Test 1: Dispatch Police Patrol
    print("\n[TEST 1] Dispatching Police Patrol...")
    response = requests.post(
        f"{BASE_URL}/api/dispatch",
        json={
            "alert_id": TEST_ALERT_ID,
            "unit_type": "police"
        }
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 2: Dispatch Ambulance
    print("\n[TEST 2] Dispatching Ambulance...")
    response = requests.post(
        f"{BASE_URL}/api/dispatch",
        json={
            "alert_id": TEST_ALERT_ID,
            "unit_type": "ambulance"
        }
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 3: Invalid unit type
    print("\n[TEST 3] Testing invalid unit type...")
    response = requests.post(
        f"{BASE_URL}/api/dispatch",
        json={
            "alert_id": TEST_ALERT_ID,
            "unit_type": "invalid_unit"
        }
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 4: Missing data
    print("\n[TEST 4] Testing missing data...")
    response = requests.post(
        f"{BASE_URL}/api/dispatch",
        json={}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 5: Test polling endpoint
    print("\n[TEST 5] Testing polling endpoint...")
    response = requests.get(
        f"{BASE_URL}/api/admin/poll/alerts",
        params={"last_id": 0}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Alert Count: {response.json().get('count', 0)}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_dispatch_endpoint()
    except Exception as e:
        print(f"\n[ERROR] Test failed: {str(e)}")
        print("Make sure the Flask app is running on http://localhost:5000")
        print("And you're logged in as admin in the browser")
