from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_NAME = "bert-base-uncased"

LABELS = [
    "frontend_ui",
    "backend_api",
    "database",
    "authentication",
    "performance",
    "infrastructure",
]


class BERTTriageEngine:
    def __init__(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_NAME,
            num_labels=len(LABELS),
        )
        self.model.eval()

    def classify_issue(self, text: str) -> dict:
        inputs = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt",
        )

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1)[0]

        best_idx = int(torch.argmax(probs))

        return {
            "predicted_label": LABELS[best_idx],
            "confidence": float(probs[best_idx]),
        }
