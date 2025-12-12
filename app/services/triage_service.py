from typing import Any, Dict, Optional, List, Tuple

from app.services.ollama_service import generate_bug_report
from app.schemas import FailureInput


def _extract_error_message(failure_text: str) -> str:
    for line in failure_text.splitlines():
        if line.startswith("Error Message:"):
            return line.split("Error Message:", 1)[1].strip()
    return ""


def _rule_based_category(failure_text: str) -> str:
    """
    Basic rule-based triage using keywords in the failure text.
    Returns one of: 'frontend_ui', 'backend_api', 'database',
    'performance', 'infrastructure', 'authentication', 'unknown'
    """
    em = _extract_error_message(failure_text).lower()
    full = failure_text.lower()

    # Frontend / UI (Selenium, Playwright, React UI)
    if (
        "noselementexception" in em
        or "unable to locate element" in em
        or "selenium" in full
        or "playwright" in full
        or ("button" in full and "click" in full)
        or "#edit-" in full
        or "component" in full and ("render" in full or "props" in full)
        or "cannot read properties of undefined" in em
        or "cannot read property" in em
    ):
        return "frontend_ui"

    # Database
    if (
        "psycopg2" in em
        or "sql" in em
        or "database" in em
        or "connection timed out" in em
        or ("timeout" in em and "query" in full)
        or "deadlock" in full
    ):
        return "database"

    # Authentication / auth
    if (
        "unauthorized" in em
        or "forbidden" in em
        or "authentication" in full
        or "jwt" in full
        or "token expired" in full
    ):
        return "authentication"

    # Performance / timeout
    if (
        "timeout" in em
        or "took too long" in full
        or "slow response" in full
        or "latency" in full
    ):
        return "performance"

    # Backend / API
    if (
        "internal server error" in em
        or "status code 500" in em
        or "status code 5" in em
        or "500" in em
        or "api" in full
        or "endpoint" in full
        or "response code" in full
    ):
        return "backend_api"

    # Infrastructure / network
    if (
        "connection refused" in em
        or "host unreachable" in em
        or "dns" in full
        or "gateway" in full
        or "service unavailable" in em
    ):
        return "infrastructure"

    return "unknown"


def _map_category_to_labels(category: str, labels: Optional[List[str]]) -> str:
    """
    Map the internal category to one of the user-provided labels (if any).
    If no labels match, fallback to the first label or the category itself.
    """
    if not labels or len(labels) == 0:
        return category

    cat = category.lower()

    # direct match
    for lab in labels:
        if lab.lower() == cat:
            return lab

    # fuzzy mapping
    for lab in labels:
        l = lab.lower()
        if cat == "frontend_ui" and ("ui" in l or "front" in l or "view" in l):
            return lab
        if cat == "backend_api" and ("api" in l or "back" in l or "service" in l):
            return lab
        if cat == "database" and ("db" in l or "data" in l or "sql" in l):
            return lab
        if cat == "performance" and ("perf" in l or "latency" in l or "timeout" in l):
            return lab
        if cat == "infrastructure" and ("infra" in l or "network" in l or "server" in l):
            return lab
        if cat == "authentication" and ("auth" in l or "login" in l or "token" in l):
            return lab

    # fallback: just return the first candidate
    return labels[0]


import json
import os
from typing import Optional, Tuple, Dict, List

# Default (hardcoded) values — will be used if config file is missing or faulty
DEFAULT_CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "frontend_ui": [
        "selector", "click", "visible", "xpath", "css", "button", "input",
        "ui", "element", "text not found", "locate"
    ],
    "backend_api": [
        "500", "404", "401", "timeout", "connection refused", "bad request",
        "response", "request", "endpoint", "api", "jsondecode", "serialization"
    ],
    "network": [
        "timeout", "dns", "connection reset", "connection refused",
        "host unreachable", "network", "ssl", "certificate", "proxy"
    ],
    "data_issue": [
        "null", "none", "nan", "constraint", "foreign key", "primary key",
        "index", "schema", "mismatch", "deserialization", "data"
    ],
    "env_config": [
        "env", "environment", "config", "configuration", "variable",
        "missing dependency", "version mismatch", "path", "not found"
    ],
    "test_code": [
        "assert", "fixture", "mock", "stub", "test setup", "teardown",
        "flaky", "race condition", "test code"
    ],
    "unknown": []
}

DEFAULT_BASE_SCORES: Dict[str, float] = {
    "frontend_ui": 0.82,
    "backend_api": 0.80,
    "network": 0.76,
    "data_issue": 0.78,
    "env_config": 0.72,
    "test_code": 0.68,
    "unknown": 0.40,
}

def load_triage_config(config_path: str = "triage_config.json") -> Tuple[Dict[str, List[str]], Dict[str, float]]:
    """
    Attempts to load category keywords and base scores from the specified JSON config file.
    If loading fails, returns the hardcoded defaults.
    """
    if os.path.isfile(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                cat_kw = data.get("CATEGORY_KEYWORDS", DEFAULT_CATEGORY_KEYWORDS)
                bs = data.get("base_scores", DEFAULT_BASE_SCORES)
                return cat_kw, bs
        except Exception as e:
            print(f"Warning: Could not load {config_path} ({e}), using defaults.")
    return DEFAULT_CATEGORY_KEYWORDS, DEFAULT_BASE_SCORES

CATEGORY_KEYWORDS, BASE_SCORES = load_triage_config()


def _normalize(text: str) -> str:
    return (text or "").lower()


def _detect_keyword_coverage(category: str, error_message: str, stack_trace: str) -> Tuple[int, int]:
    cat = (category or "").lower().strip()
    text = _normalize(error_message) + " " + _normalize(stack_trace)
    keywords = CATEGORY_KEYWORDS.get(cat, [])
    if not keywords:
        keywords = [
            "timeout", "null", "none", "500", "404", "failed", "exception",
            "not found", "crash", "connection"
        ]
    hits = sum(1 for kw in keywords if kw in text)
    return hits, len(keywords)


def _is_flaky_pattern(error_message: str, stack_trace: str) -> bool:
    text = _normalize(error_message) + " " + _normalize(stack_trace)
    flaky_tokens = [
        "sometimes", "intermittent", "occasionally", "randomly",
        "flaky", "sporadic", "non-deterministic", "timing issue"
    ]
    timeout_tokens = ["timeout", "timed out"]
    if any(tok in text for tok in flaky_tokens):
        return True
    timeout_count = sum(text.count(tok) for tok in timeout_tokens)
    return timeout_count >= 2


def compute_triage_confidence(
    category: str,
    error_message: str = "",
    stack_trace: str = "",
    model_probability: Optional[float] = None,
    has_similar_past_bug: bool = False
) -> float:
    cat = (category or "").lower().strip()
    base = BASE_SCORES.get(cat, 0.60)
    if model_probability is not None:
        p = max(0.0, min(float(model_probability), 1.0))
        base = 0.5 * base + 0.5 * p
    hits, total = _detect_keyword_coverage(cat, error_message, stack_trace)
    if total > 0:
        coverage = hits / total
        effect = (coverage - 0.5) * 2
        base += 0.15 * effect
    if has_similar_past_bug:
        base += 0.07
    if _is_flaky_pattern(error_message, stack_trace):
        base -= 0.10
    base = max(0.05, min(base, 0.97))
    return round(base, 2)


def classify_issue_rule_based(failure_text: str, labels: Optional[List[str]]) -> Dict[str, Any]:
    category = _rule_based_category(failure_text)
    confidence = compute_triage_confidence(
        category=category,
        error_message=_extract_error_message(failure_text),
        stack_trace=failure_text
    )
    chosen_label = _map_category_to_labels(category, labels)
    return {
        "label": chosen_label,
        "confidence": confidence,
    }


def process_failure(payload: FailureInput) -> Dict[str, Any]:
    failure_text = f"""
Test Name: {payload.test_name}
File Path: {payload.file_path}
Error Message: {payload.error_message}
Stack Trace: {payload.stack_trace}
Logs: {payload.logs}
""".strip()

    # 1) Bug report via Ollama
    try:
        bug = generate_bug_report(payload.llm_model, failure_text)
    except Exception as e:
        bug = {
            "title": "Bug Generation Error",
            "description": f"Bug generator crashed: {str(e)}",
        }

    # 2) Triage via rule-based classifier
    triage = classify_issue_rule_based(failure_text, payload.labels)

    # 3) Extract extra structured fields INLINE (no new helper functions)
    
    # Extract failure_reason (first line or truncated to ~150 chars)
    failure_reason = payload.error_message.split('\n')[0][:150] if payload.error_message else None
    
    # Extract suite_name from file_path (basename without extension)
    import os
    suite_name = os.path.splitext(os.path.basename(payload.file_path))[0] if payload.file_path else None
    
    # Extract error_line_number from stack trace using regex
    import re
    error_line_number = None
    if payload.stack_trace:
        # Try patterns: "line XXX", ":XXX:", ":XXX)", "at file.py:XXX"
        line_match = re.search(r'line\s+(\d+)', payload.stack_trace, re.IGNORECASE)
        if not line_match:
            line_match = re.search(r':(\d+)[:)]', payload.stack_trace)
        if not line_match:
            line_match = re.search(r'at\s+[^\s]+:(\d+)', payload.stack_trace)
        if line_match:
            error_line_number = int(line_match.group(1))
    
    # Extract error_file_path from stack trace
    error_file_path = None
    if payload.stack_trace:
        # Look for patterns like "at file.py:line" or "File \"file.py\""
        file_match = re.search(r'at\s+([^\s:]+\.(?:py|js|ts|spec\.js|spec\.ts))', payload.stack_trace)
        if not file_match:
            file_match = re.search(r'File\s+"([^"]+)"', payload.stack_trace)
        if file_match:
            error_file_path = file_match.group(1)
    
    # FALLBACK: If stack trace is empty or didn't contain file path, use file_path from payload
    if not error_file_path and payload.file_path:
        error_file_path = payload.file_path
    
    # Truncate stack_trace to max 3000 characters
    stack_trace_truncated = payload.stack_trace[:3000] if payload.stack_trace else None
    
    # Extract log_snippet (first 1000 characters)
    log_snippet = payload.logs[:1000] if payload.logs else None
    
    # Extract timestamp from logs if available
    timestamp = None
    if payload.logs:
        # Try to find timestamp patterns like [2025-12-05 14:22:10] or 2025-12-05T14:22:10
        ts_match = re.search(r'\[?(\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2})\]?', payload.logs)
        if ts_match:
            timestamp = ts_match.group(1)
    
    # Get internal category for severity computation
    category = _rule_based_category(failure_text)
    
    # Compute severity INLINE based on category and test_name patterns
    severity = "Medium"  # default
    test_name_lower = payload.test_name.lower() if payload.test_name else ""
    category_lower = category.lower()
    
    # Critical/High severity patterns
    if any(keyword in test_name_lower for keyword in ["login", "checkout", "payment", "auth", "critical", "security"]):
        severity = "Critical"
    elif any(keyword in test_name_lower for keyword in ["purchase", "transaction", "order", "signup"]):
        severity = "High"
    elif category_lower in ["authentication", "backend_api"] and "500" in payload.error_message:
        severity = "High"
    # Low severity patterns
    elif any(keyword in test_name_lower for keyword in ["visual", "ui", "style", "css", "color"]):
        severity = "Low"
    elif category_lower == "frontend_ui" and "button" in test_name_lower:
        severity = "Low"
    # Medium severity patterns (network, timeout, infrastructure)
    elif category_lower in ["performance", "infrastructure", "database"]:
        severity = "Medium"
    elif "timeout" in payload.error_message.lower():
        severity = "Medium"
    
    # Detect flakiness INLINE
    is_flaky = False
    flakiness_reasons = []
    
    error_msg_lower = payload.error_message.lower() if payload.error_message else ""
    stack_lower = payload.stack_trace.lower() if payload.stack_trace else ""
    combined_text = error_msg_lower + " " + stack_lower
    
    if "timeout" in combined_text or "timed out" in combined_text:
        is_flaky = True
        flakiness_reasons.append("Timeout detected")
    if "retry" in combined_text or "retrying" in combined_text:
        is_flaky = True
        flakiness_reasons.append("Retry pattern detected")
    if any(word in combined_text for word in ["intermittent", "occasionally", "sometimes", "randomly", "sporadic"]):
        is_flaky = True
        flakiness_reasons.append("Intermittent failure keywords detected")
    if "race condition" in combined_text or "timing" in combined_text:
        is_flaky = True
        flakiness_reasons.append("Timing/race condition pattern detected")
    
    # Extract bug title and description for return
    bug_title = bug.get("title", "No title")
    bug_description = bug.get("description", "No description")

    return {
        "bug_title": bug_title,
        "bug_description": bug_description,
        "triage_label": triage["label"],
        "triage_confidence": triage["confidence"],
        "raw_failure_text": failure_text,
        # Extra structured fields
        "test_name": payload.test_name,
        "failure_reason": failure_reason,
        "suite_name": suite_name,
        "error_file_path": error_file_path,
        "stack_trace": stack_trace_truncated,
        "error_line_number": error_line_number,
        "browser": None,
        "environment": None,
        "log_snippet": log_snippet,
        "category": category,
        "severity": severity,
        "is_flaky": is_flaky,
        "flakiness_reasons": flakiness_reasons,
        "timestamp": timestamp,
    }
