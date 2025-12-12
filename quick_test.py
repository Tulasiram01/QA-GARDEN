"""
Quick test to verify llm_prompt has been removed
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.schemas import FailureInput
from app.services.triage_service import process_failure

payload = FailureInput(
    test_name="test_login",
    file_path="tests/login.spec.js",
    error_message="Login failed",
    stack_trace="at tests/login.spec.js:42:5",
    logs="Error logs",
    llm_model="gemma:2b",
    bert_url="http://localhost:8001/triage",
    labels=["frontend"]
)

print("Testing without LLM prompt field...")
result = process_failure(payload)

print("\nFields in result:")
for key in result.keys():
    print(f"  - {key}")

if "llm_prompt" in result:
    print("\n[FAIL] llm_prompt is still in the result!")
else:
    print("\n[PASS] llm_prompt has been successfully removed!")

print(f"\nError Line Number: {result.get('error_line_number')}")
print(f"Severity: {result.get('severity')}")
print(f"Category: {result.get('category')}")
