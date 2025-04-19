Akaike Email Classification Assignment
Overview
This project processes a dataset of 24,000 emails (emails.csv) to mask PII and classify emails into four categories: Incident, Request, Problem, and Change.

Task 1: Masks PII using regex and Spacy NER.
Task 2: Trains a Random Forest classifier.
Task 3: Integrates masking and classification in a pipeline.
Task 4: Deploys a FastAPI endpoint for email classification.

Project Structure
akaike_assignment/
├── emails.csv              # Input dataset
├── emails_masked.csv       # Masked dataset
├── mask_pii.py             # Masks PII
├── validate_pii.py         # Validates PII masking
├── spot_check_pii.py       # Spot-checks rows 5, 64, 23778, 23818
├── verify_pii.py           # Verifies rows and integrity
├── models.py               # Trains Random Forest
├── pipeline.py             # Integrates masking and classification
├── main.py                 # FastAPI endpoint
├── rf_model.pkl            # Trained model
├── README.md               # Documentation
├── .gitignore              # Ignores CSVs and model

Setup

Clone Repository:
git clone https://github.com/dhanush14chowdary/akaike_email_classification
cd akaike_email_classification


Install Dependencies:
pip install pandas spacy scikit-learn tqdm fastapi uvicorn joblib
python -m spacy download en_core_web_sm


Verify .gitignore:
emails.csv
emails_masked.csv
rf_model.pkl



Task 1: Data Collection & Preprocessing
Masks PII in emails.csv, saves to emails_masked.csv.
Scripts

mask_pii.py: Masks PII.
validate_pii.py: Checks all rows.
spot_check_pii.py: Verifies specific rows.
verify_pii.py: Displays rows and integrity.

Usage
python mask_pii.py
python validate_pii.py
python spot_check_pii.py
python verify_pii.py

Task 2: Model Selection & Training
Trains Random Forest to classify emails.
Script

models.py: Trains and saves model.

Usage
python models.py

Task 3: System Integration
Integrates masking and classification.
Script

pipeline.py: Processes emails.

Usage
python pipeline.py

Task 4: API Development & Deployment
FastAPI endpoint for email classification.
Script

main.py: API server.

Usage
python main.py

Test:
curl -X POST "http://localhost:8000/classify" -H "Content-Type: application/json" -d '{"email": "Subject: Test\nContact john.doe@example.com or +82-2-3456-7890. Name: John Doe"}'

GitHub

Repository: https://github.com/dhanush14chowdary/akaike_email_classification

Commit:
git add .
git commit -m "Complete Akaike assignment: All tasks"
git push origin main



Notes

Dataset includes Change type (2517 rows).
Class imbalance affects model performance (accuracy 0.74, low recall for Problem/Change).
Over-masking in Task 1 (e.g., "Concerns About") does not expose PII.
Share outputs for debugging.

Author
Dhanush
