"""
Test script to verify GET endpoints work correctly
"""
import requests
import json

BASE_URL = "http://192.168.1.51:8000/api"

print("=" * 80)
print("Testing Triage Engine GET Endpoints")
print("=" * 80)
print()

# Test 1: POST a triage request
print("Test 1: Creating a triage result via POST...")
print("-" * 40)

payload = {
    "test_name": "test_login_button",
    "file_path": "tests/login.spec.js",
    "error_message": "Button not found",
    "stack_trace": "    at tests/login.spec.js:42:5",
    "logs": "[ERROR] Element not found",
    "llm_model": "gemma:2b",
    "bert_url": "http://localhost:8001/triage",
    "labels": ["frontend", "ui"]
}

try:
    response = requests.post(f"{BASE_URL}/triage", json=payload)
    response.raise_for_status()
    result = response.json()
    
    result_id = result.get("id")
    print(f"✓ POST successful!")
    print(f"  Result ID: {result_id}")
    print(f"  Bug Title: {result.get('bug_title')}")
    print(f"  Created At: {result.get('created_at')}")
    print()
    
    # Test 2: GET the specific result
    print("Test 2: Retrieving the result via GET...")
    print("-" * 40)
    
    response = requests.get(f"{BASE_URL}/triage/{result_id}")
    response.raise_for_status()
    retrieved = response.json()
    
    print(f"✓ GET successful!")
    print(f"  Retrieved ID: {retrieved.get('id')}")
    print(f"  Bug Title: {retrieved.get('bug_title')}")
    print(f"  Severity: {retrieved.get('severity')}")
    print(f"  Error Line: {retrieved.get('error_line_number')}")
    print()
    
    # Test 3: GET all results
    print("Test 3: Listing all results...")
    print("-" * 40)
    
    response = requests.get(f"{BASE_URL}/triage")
    response.raise_for_status()
    all_results = response.json()
    
    print(f"✓ GET all successful!")
    print(f"  Total results: {all_results.get('total')}")
    print(f"  Results count: {len(all_results.get('results', []))}")
    print()
    
    # Test 4: GET non-existent result (should fail)
    print("Test 4: Testing 404 for non-existent ID...")
    print("-" * 40)
    
    response = requests.get(f"{BASE_URL}/triage/invalid-id-12345")
    if response.status_code == 404:
        print(f"✓ Correctly returned 404 for invalid ID")
    else:
        print(f"✗ Expected 404, got {response.status_code}")
    print()
    
    print("=" * 80)
    print("ALL TESTS PASSED!")
    print("=" * 80)
    print()
    print("You can now share results with others using:")
    print(f"  GET {BASE_URL}/triage/{result_id}")
    print()
    
except requests.exceptions.ConnectionError:
    print("✗ ERROR: Could not connect to the API server.")
    print(f"  Make sure the server is running at {BASE_URL}")
    print("  Run: python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
except Exception as e:
    print(f"✗ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
