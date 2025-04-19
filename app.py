# app.py
# Main FastAPI application for email classification
# Author: Dhanush
# Date: April 19, 2025

from fastapi import FastAPI
import uvicorn
from api import classify_email_endpoint

app = FastAPI()

app.post("/classify")(classify_email_endpoint)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)