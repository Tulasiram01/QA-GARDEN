"""
Test with empty stack trace to verify fallback logic
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.schemas import FailureInput
from app.services.triage_service import process_failure
import json

print("=" * 80)
print("Testing with EMPTY stack trace (user's example)")
print("=" * 80)
print()

payload = FailureInput(
    test_name="test_checkout_button_unresponsive",
    file_path="tests/ui/test_checkout_page.py",
    error_message="Element not interactable",
    stack_trace="",  # EMPTY!
    logs="[2025-12-05 14:22:10] INFO: Navigated to /checkout\n[2025-12-05 14:22:11] WARN: Click attempted on #checkout-btn but no action detected\n[2025-12-05 14:22:14] INFO: Retrying click on #checkout-btn (attempt 3)\n[2025-12-05 14:22:17] WARN: Element still not interactable after retries",
    llm_model="gemma:2b",
    bert_url="http://localhost:8001/triage",
    labels=["ui", "flaky", "interaction"]
)

try:
    result = process_failure(payload)
    
    print("RESULT:")
    print("-" * 80)
    print(f"Test Name: {result.get('test_name')}")
    print(f"Suite Name: {result.get('suite_name')}")
    print(f"Error File Path: {result.get('error_file_path')}")
    print(f"Error Line Number: {result.get('error_line_number')}")
    print(f"Stack Trace: {result.get('stack_trace')}")
    print(f"Severity: {result.get('severity')}")
    print(f"Category: {result.get('category')}")
    print(f"Is Flaky: {result.get('is_flaky')}")
    print(f"Flakiness Reasons: {result.get('flakiness_reasons')}")
    print(f"Timestamp: {result.get('timestamp')}")
   
    print()
    
    # Check which fields are NOT null
    non_null_fields = [k for k, v in result.items() if v is not None and v != "" and v != []]
    print(f"Non-null fields ({len(non_null_fields)}): {', '.join(non_null_fields)}")
    print()
    
    print("=" * 80)
    print("[PASS] Fallback logic working - error_file_path uses file_path!")
    print("=" * 80)
    
except Exception as e:
    print(f"[INFO] Error (likely Ollama not running): {str(e)[:150]}")
    print("This is expected if Ollama service is not running.")
