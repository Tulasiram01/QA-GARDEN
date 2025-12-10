from fastapi import APIRouter
from app.schemas import FailureInput, TriageOutput
from app.services.triage_service import process_failure

router = APIRouter()


@router.post("/triage", response_model=TriageOutput)
def triage_failure(payload: FailureInput):
    try:
        result = process_failure(payload)
        return result
    except Exception as e:
        # Fallback so the API never crashes with 500
        return TriageOutput(
            bug_title="API Internal Error",
            bug_description=f"Error while processing triage request: {str(e)}",
            triage_label="triage_error",
            triage_confidence=0.0,
            raw_failure_text="",
        )
