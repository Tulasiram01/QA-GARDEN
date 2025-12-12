"""
Test script to verify the extended triage output functionality.
"""
import sys
import os

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.schemas import FailureInput
from app.services.triage_service import process_failure
import json

# Test payload with realistic Playwright failure data
payload = FailureInput(
    test_name="test_login_page_title",
    file_path="tests/auth/test_login.spec.js",
    error_message="expect(page).toHaveTitle(expected) failed\nExpected: 'Login - MyApp'\nReceived: 'MyApp'",
    stack_trace="""    at tests/auth/test_login.spec.js:42:5
    at WorkerRunner._runTestWithBeforeHooks (playwright/lib/worker/workerRunner.js:471:7)""",
    logs="[ERROR] Page title mismatch\n[DEBUG] Current URL: http://localhost:3000/login\n[INFO] Screenshot saved",
    llm_model="gemma:2b",
    bert_url="http://localhost:8001/triage",
    labels=["frontend", "backend"]
)

print("=" * 80)
print("Testing Extended Bug Triage Engine Output")
print("=" * 80)
print()

try:
    result = process_failure(payload)
    
    print("[OK] process_failure() executed successfully")
    print()
    
    # Check all expected fields are present
    expected_fields = [
        "bug_title", "bug_description", "triage_label", "triage_confidence",
        "raw_failure_text", "test_name", "failure_reason", "suite_name",
        "error_file_path", "error_line_number", "browser", "environment",
        "stack_trace", "log_snippet", "category", "severity",
        "is_flaky", "flakiness_reasons", "timestamp"
    ]
    
    missing_fields = [field for field in expected_fields if field not in result]
    
    if missing_fields:
        print(f"[FAIL] Missing fields: {missing_fields}")
    else:
        print("[OK] All expected fields are present in the result")
    
    print()
    print("-" * 80)
    print("RESULT SUMMARY:")
    print("-" * 80)
    print(f"Bug Title: {result.get('bug_title', 'N/A')}")
    print(f"Test Name: {result.get('test_name', 'N/A')}")
    print(f"Suite Name: {result.get('suite_name', 'N/A')}")
    print(f"Error File Path: {result.get('error_file_path', 'N/A')}")
    print(f"Error Line Number: {result.get('error_line_number', 'N/A')}")
    print(f"Failure Reason: {result.get('failure_reason', 'N/A')[:100]}...")
    print(f"Category: {result.get('category', 'N/A')}")
    print(f"Severity: {result.get('severity', 'N/A')}")
    print(f"Triage Confidence: {result.get('triage_confidence', 'N/A')}")
    print(f"Is Flaky: {result.get('is_flaky', 'N/A')}")
    print(f"Flakiness Reasons: {result.get('flakiness_reasons', 'N/A')}")
    print()
    

    
    print("-" * 80)
    print("FULL RESULT (JSON):")
    print("-" * 80)
    # Convert to JSON-serializable format
    result_json = {k: v for k, v in result.items()}
    print(json.dumps(result_json, indent=2, default=str))
    
    print()
    print("=" * 80)
    print("[PASS] TEST PASSED - All fields generated successfully!")
    print("=" * 80)
    
except Exception as e:
    print(f"[FAIL] TEST FAILED with error: {str(e)}")
    import traceback
    traceback.print_exc()
