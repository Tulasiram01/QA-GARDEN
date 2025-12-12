from pydantic import BaseModel
from typing import List, Optional


class FailureInput(BaseModel):
    test_name: str
    file_path: str
    error_message: str
    stack_trace: str
    logs: Optional[str] = None

    # dynamic settings from frontend/client
    llm_model: str                       # e.g. "gemma:2b"
    bert_url: str                        # e.g. "http://localhost:8001/triage"
    labels: Optional[List[str]] = None   # optional list of labels


class TriageOutput(BaseModel):
    bug_title: str
    bug_description: str
    triage_label: str
    triage_confidence: float
    raw_failure_text: str
    # Extra structured fields
    test_name: Optional[str] = None
    failure_reason: Optional[str] = None
    suite_name: Optional[str] = None
    error_file_path: Optional[str] = None
    stack_trace: Optional[str] = None
    error_line_number: Optional[int] = None
    browser: Optional[str] = None
    environment: Optional[str] = None
    log_snippet: Optional[str] = None
    category: Optional[str] = None
    severity: Optional[str] = None
    is_flaky: Optional[bool] = None
    flakiness_reasons: Optional[List[str]] = None
    timestamp: Optional[str] = None
    # Metadata fields (added when stored)
    id: Optional[str] = None
    created_at: Optional[str] = None


class TriageResultList(BaseModel):
    """Response model for listing multiple triage results"""
    total: int
    results: List[TriageOutput]
