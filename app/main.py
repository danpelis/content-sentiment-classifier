import logging
from fastapi import FastAPI, HTTPException

from app import classify_headline, ModelRequest, ModelResponse

app = FastAPI()
logging.basicConfig(level=logging.INFO)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/classify")
async def classify_headline_endpoint(request: ModelRequest):
    logging.info(f"Received request to classify -> {request.headline}")
    try:
        response = classify_headline(request.headline)
        logging.info(f"Model Response -> {response[0]} with confidence {response[1]}")
        return ModelResponse(sentiment=response[0], confidence=response[1])
    except Exception as e:
        logging.error(f"Error during classification: {e}")
        raise HTTPException(status_code=500, detail="Classification failed")