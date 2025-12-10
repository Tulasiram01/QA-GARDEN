# C:\bug-triage-engine\bert_server.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn

# ---- Request/Response Models ----

class BertRequest(BaseModel):
    text: str
    labels: Optional[List[str]] = None


class BertResponse(BaseModel):
    label: str
    confidence: float
    scores: Dict[str, float]


# ---- FastAPI app ----

app = FastAPI(title="BERT Classification Server")


@app.get("/")
async def root():
    return {"status": "ok", "service": "bert_server", "message": "BERT server is running"}


@app.post("/predict", response_model=BertResponse)
async def predict(request: BertRequest):
    """
    Dummy/Baseline classifier.
    You can later plug your real BERT model here.
    """
    labels = request.labels or ["General"]

    # Simple logic: pick the first label as the "best"
    best_label = labels[0]
    score_each = 1.0 / len(labels) if labels else 1.0

    scores = {lbl: score_each for lbl in labels}

    return BertResponse(
        label=best_label,
        confidence=score_each,
        scores=scores,
    )


if __name__ == "__main__":
    # For direct "python bert_server.py" runs
    uvicorn.run("bert_server:app", host="127.0.0.1", port=8001, reload=True)
