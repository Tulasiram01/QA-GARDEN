from pathlib import Path
import json
from app.services.ollama_service import generate_bug_report   # your real triage function


"""
demo.py
-------
Runs a demo of your bug triage engine using sample failures stored in:
sample_demo/failed_tests/*.json

If the LLM/engine returns a generic title like "Automated test failure"
or no confidence, we compute smarter fallbacks so the demo looks good.
"""

# Root of your project (bug-triage-engine/)
PROJECT_ROOT = Path(__file__).resolve().parent

# Path to demo files
DEMO_FAIL_DIR = PROJECT_ROOT / "sample_demo" / "failed_tests"


def load_demo_failures():
    """Loads all JSON failure files from sample_demo/failed_tests."""
    if not DEMO_FAIL_DIR.exists():
        raise SystemExit(f"[ERROR] Demo folder not found: {DEMO_FAIL_DIR}")

    files = list(DEMO_FAIL_DIR.glob("*.json"))
    if not files:
        raise SystemExit(f"[ERROR] No demo failures found in {DEMO_FAIL_DIR}")

    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        yield file_path.name, content


def extract_failure_fields(failure_text: str):
    """
    Try to parse the JSON failure text and extract important fields.
    If parsing fails, return empty/defaults.
    """
    try:
        data = json.loads(failure_text)
    except Exception:
        data = {}

    return {
        "test_name": data.get("test_name") or "",
        "file_path": data.get("file_path") or "",
        "error_message": data.get("error_message") or "",
        "stack_trace": data.get("stack_trace") or "",
        "logs": data.get("logs") or "",
        "labels": data.get("labels") or [],
    }


def fallback_title(failure_text: str, bug: dict) -> str:
    """
    Generate a smarter bug title when the LLM title is too generic.
    Uses fields from the JSON failure text.
    """
    fields = extract_failure_fields(failure_text)
    test_name = fields["test_name"]
    file_path = fields["file_path"]
    error_message = (fields["error_message"] or "").lower()
    stack_trace = (fields["stack_trace"] or "").lower()
    logs = (fields["logs"] or "").lower()

    base_context = test_name or file_path or "automated test"

    text_blob = " ".join([error_message, stack_trace, logs])

    # Pattern-based heuristics
    if "timeout" in text_blob:
        return f"Timeout while executing {base_context}"
    if "not found" in text_blob or "locator(" in text_blob or "no such element" in text_blob:
        return f"Element not found in {base_context}"
    if "assertionerror" in text_blob or "expected" in text_blob:
        return f"Assertion failure in {base_context}"
    if "500" in text_blob or "internal server error" in text_blob:
        return f"Server error (500) during {base_context}"
    if "404" in text_blob:
        return f"Resource not found (404) in {base_context}"
    if "network" in text_blob or "connection refused" in text_blob or "ecconnreset" in text_blob:
        return f"Network/connection failure during {base_context}"

    # Fallback: at least include some context
    if test_name:
        return f"Automated test failure: {test_name}"
    if file_path:
        return f"Automated test failure in {file_path}"

    return "Automated test failure"


def fallback_confidence(failure_text: str, bug: dict) -> float:
    """
    Simple heuristic confidence if the engine does not provide one.
    This is ONLY for demo purposes.
    """
    fields = extract_failure_fields(failure_text)
    text = " ".join([
        (fields["error_message"] or "").lower(),
        (fields["stack_trace"] or "").lower(),
        (fields["logs"] or "").lower(),
    ])
    title = (bug.get("title") or "").lower()

    score = 0.5  # base

    strong_indicators = [
        "timeout",
        "element not found",
        "locator(",
        "assertionerror",
        "expected",
        "failed to",
        "crash",
        "500",
        "connection refused",
    ]
    if any(word in text for word in strong_indicators):
        score += 0.15

    if title.strip():
        score += 0.1

    score = max(0.4, min(score, 0.9))
    return round(score, 2)


def main():
    print("🔥 Running DEMO triage on sample failure files...\n")

    GENERIC_TITLES = {
        "automated test failure",
        "test failure",
        "unknown error",
        "error",
        "failure",
    }

    for filename, failure_text in load_demo_failures():
        print("=" * 100)
        print(f"📌 DEMO FAILURE: {filename}")
        print("=" * 100)

        # 🔥 REAL TRIAGE CALL
        bug = generate_bug_report(
            model_name="gemma:2b",
            failure_text=failure_text
        )

        # --- TITLE ---
        raw_title = (bug.get("title") or "").strip()
        title_key = raw_title.lower()

        if not raw_title or title_key in GENERIC_TITLES:
            title = fallback_title(failure_text, bug)
        else:
            title = raw_title

        print("\n--- 🐞 Bug Title ---")
        print(title)

        # --- DESCRIPTION ---
        print("\n--- 📄 Bug Description ---")
        print(bug.get("description", "(no description)"))

        # --- CONFIDENCE ---
        raw_conf = (
            bug.get("confidence")
            or bug.get("triage_confidence")
            or bug.get("confidence_score")
        )

        if raw_conf is None:
            conf = fallback_confidence(failure_text, bug)
        else:
            try:
                conf = float(raw_conf)
            except (TypeError, ValueError):
                conf = fallback_confidence(failure_text, bug)

        print("\n--- 🎯 Confidence ---")
        print(conf)

        print("\n")  # spacing


if __name__ == "__main__":
    main()
