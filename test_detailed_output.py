"""
Detailed test showing ALL field values with proper data
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.schemas import FailureInput
from app.services.triage_service import process_failure
import json

print("=" * 80)
print("DETAILED BUG TRIAGE OUTPUT - ALL FIELDS WITH DATA")
print("=" * 80)
print()

# Realistic test failure with complete data
payload = FailureInput(
    test_name="test_login_page_title",
    file_path="tests/auth/test_login.spec.js",
    error_message="expect(page).toHaveTitle(expected) failed\nExpected: 'Login - MyApp'\nReceived: 'MyApp'",
    stack_trace="    at tests/auth/test_login.spec.js:42:5\n    at WorkerRunner._runTestWithBeforeHooks (playwright/lib/worker/workerRunner.js:471:7)",
    logs="[2025-12-11 10:30:15] INFO: Starting test_login_page_title\n[2025-12-11 10:30:16] DEBUG: Navigating to http://localhost:3000/login\n[2025-12-11 10:30:17] ERROR: Page title mismatch\n[2025-12-11 10:30:18] INFO: Screenshot saved to test-results/",
    llm_model="gemma:2b",
    bert_url="http://localhost:8001/triage",
    labels=["frontend", "ui", "regression"]
)

print("INPUT:")
print("-" * 80)
print(f"Test Name: {payload.test_name}")
print(f"File Path: {payload.file_path}")
print(f"Error Message: {payload.error_message[:80]}...")
print(f"Stack Trace: {payload.stack_trace[:80]}...")
print()

try:
    result = process_failure(payload)
    
    print("OUTPUT - ALL FIELDS WITH VALUES:")
    print("=" * 80)
    print()
    
    # Core fields
    print("📋 CORE FIELDS:")
    print(f"  Bug Title        : {result.get('bug_title')}")
    print(f"  Triage Label     : {result.get('triage_label')}")
    print(f"  Triage Confidence: {result.get('triage_confidence')}")
    print()
    
    # Test identification
    print("🔍 TEST IDENTIFICATION:")
    print(f"  Test Name        : {result.get('test_name')}")
    print(f"  Suite Name       : {result.get('suite_name')}")
    print(f"  File Path        : {result.get('error_file_path')}")
    print(f"  Line Number      : {result.get('error_line_number')}")
    print()
    
    # Classification
    print("📊 CLASSIFICATION:")
    print(f"  Category         : {result.get('category')}")
    print(f"  Severity         : {result.get('severity')}")
    print()
    
    # Flakiness analysis
    print("🔄 FLAKINESS ANALYSIS:")
    print(f"  Is Flaky         : {result.get('is_flaky')}")
    print(f"  Flaky Reasons    : {result.get('flakiness_reasons')}")
    print()
    
    # Context
    print("🌐 CONTEXT:")
    print(f"  Browser          : {result.get('browser')}")
    print(f"  Environment      : {result.get('environment')}")
    print(f"  Timestamp        : {result.get('timestamp')}")
    print()
    
    # Failure details
    print("❌ FAILURE DETAILS:")
    print(f"  Failure Reason   : {result.get('failure_reason')}")
    print()
    print("  Stack Trace (snippet):")
    stack = result.get('stack_trace', '')
    print(f"    {stack[:150]}...")
    print()
    print("  Log Snippet:")
    logs = result.get('log_snippet', '')
    print(f"    {logs[:150]}...")
    print()
    
    # Bug description
    print("📝 BUG DESCRIPTION:")
    print("-" * 80)
    desc = result.get('bug_description', '')
    print(desc[:500] + "..." if len(desc) > 500 else desc)
    print()
    
    # Full JSON
    print("=" * 80)
    print("COMPLETE JSON OUTPUT:")
    print("=" * 80)
    print(json.dumps(result, indent=2, default=str))
    
except Exception as e:
    print(f"ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
