# main.py
# FastAPI endpoint for email PII masking and classification
# Author: Dhanush
# Date: April 19, 2025

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from pipeline import mask_pii, classify_email, nlp, model

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

class EmailInput(BaseModel):
    email: str

@app.post("/classify")
async def classify_email_endpoint(email_input: EmailInput):
    try:
        logger.info("Received email for classification")
        result = classify_email(email_input.email)
        return result
    except Exception as e:
        logger.error(f"Error processing email: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)