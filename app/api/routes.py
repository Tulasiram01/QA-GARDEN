from fastapi import APIRouter, HTTPException
from app.schemas import FailureInput, TriageOutput, TriageResultList
from app.services.triage_service import process_failure
from app.services import storage_service

router = APIRouter()


@router.post("/triage", response_model=TriageOutput)
def triage_failure(payload: FailureInput):
    """
    Process a test failure and return triage results.
    The result is automatically stored and can be retrieved later via GET endpoints.
    """
    try:
        result = process_failure(payload)
        
        # Store the result and add the ID to the response
        result_id = storage_service.store_result(result)
        result["id"] = result_id
        
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


@router.get("/triage/{result_id}", response_model=TriageOutput)
def get_triage_result(result_id: str):
    """
    Retrieve a specific triage result by its ID.
    """
    result = storage_service.get_result(result_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Triage result with ID '{result_id}' not found")
    return result


@router.get("/triage", response_model=TriageResultList)
def list_triage_results():
    """
    List all stored triage results.
    Returns results sorted by creation time (newest first).
    """
    results = storage_service.get_all_results()
    return TriageResultList(
        total=len(results),
        results=results
    )


@router.delete("/triage/{result_id}")
def delete_triage_result(result_id: str):
    """
    Delete a specific triage result by its ID.
    """
    deleted = storage_service.delete_result(result_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Triage result with ID '{result_id}' not found")
    return {"message": f"Triage result '{result_id}' deleted successfully"}

