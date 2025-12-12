"""
In-memory storage service for triage results.
Results are stored with unique IDs and can be retrieved via GET endpoints.
"""
import uuid
from typing import Dict, List, Optional
from datetime import datetime


# In-memory storage: {result_id: result_data}
_storage: Dict[str, dict] = {}


def store_result(result: dict) -> str:
    """
    Store a triage result and return its unique ID.
    
    Args:
        result: The triage result dictionary to store
        
    Returns:
        The unique ID (UUID) assigned to this result
    """
    result_id = str(uuid.uuid4())
    
    # Add metadata
    result_with_metadata = {
        **result,
        "id": result_id,
        "created_at": datetime.now().isoformat()
    }
    
    _storage[result_id] = result_with_metadata
    return result_id


def get_result(result_id: str) -> Optional[dict]:
    """
    Retrieve a specific triage result by ID.
    
    Args:
        result_id: The unique ID of the result to retrieve
        
    Returns:
        The result dictionary if found, None otherwise
    """
    return _storage.get(result_id)


def get_all_results() -> List[dict]:
    """
    Retrieve all stored triage results.
    
    Returns:
        List of all stored results, sorted by creation time (newest first)
    """
    results = list(_storage.values())
    # Sort by created_at timestamp, newest first
    results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return results


def delete_result(result_id: str) -> bool:
    """
    Delete a specific triage result by ID.
    
    Args:
        result_id: The unique ID of the result to delete
        
    Returns:
        True if deleted, False if not found
    """
    if result_id in _storage:
        del _storage[result_id]
        return True
    return False


def get_result_count() -> int:
    """
    Get the total number of stored results.
    
    Returns:
        Count of stored results
    """
    return len(_storage)
