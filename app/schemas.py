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
