from fastapi import FastAPI
from pydantic import BaseModel
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_PATH = "bert-triage-system/classifier"  # output of train_bert_classifier.py

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

LABELS = [
    "UI Error",
    "Backend Error",
    "Assertion Failure",
    "Timeout Error",
    "Test Data Issue"
]
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()


app = FastAPI(title="BERT Bug Classifier")

class PredictRequest(BaseModel):
    text: str
    labels: list[str] | None = None

@app.post("/predict")
def predict(req: PredictRequest):
    inputs = tokenizer(
        req.text,
        return_tensors="pt",
        truncation=True,
        padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)[0]

    label_space = LABELS

    scores = {
        label_space[i]: float(probs[i])
        for i in range(len(label_space))
    }

    best_label = max(scores, key=scores.get)

    return {
        "label": best_label,
        "confidence": scores[best_label],
        "scores": scores
    }
