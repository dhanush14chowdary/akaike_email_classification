# api.py
# API logic for email classification
# Author: Dhanush
# Date: April 19, 2025

from fastapi import HTTPException
from pydantic import BaseModel
import logging
from pipeline import classify_email

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EmailInput(BaseModel):
    email: str

async def classify_email_endpoint(email_input: EmailInput):
    try:
        logger.info("Received email for classification")
        result = classify_email(email_input.email)
        return result
    except Exception as e:
        logger.error(f"Error processing email: {e}")
        raise HTTPException(status_code=500, detail=str(e))