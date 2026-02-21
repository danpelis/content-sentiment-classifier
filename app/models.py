from transformers import pipeline
from app.config import MODEL_NAME

pipeline = pipeline("zero-shot-classification", model=MODEL_NAME)
candidate_labels = ["negative", "neutral", "positive"]

def classify_headline(headline:str) -> str:
    result = pipeline(headline, candidate_labels)
    return (result['labels'][0], result['scores'][0])

if __name__ == "__main__":
    headline = "The stock market is crashing"
    result = classify_headline(headline)
    print(result)