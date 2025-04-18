Akaike Email Classification Assignment
This repository contains the implementation of the Akaike Data Science Internship assignment (April 2025). The goal is to process a dataset of 24,000 emails, mask personally identifiable information (PII), classify emails into support categories (e.g., Incident, Request), and deploy the solution via an API on Hugging Face Spaces.
Assignment Overview
The assignment consists of five tasks:

Data Collection & Preprocessing: Mask PII in emails using NER (Spacy), regex, or custom methods; store original data securely.
Model Selection & Training: Train a classification model (e.g., Random Forest, BERT) to categorize emails.
System Integration: Build a pipeline for PII masking and classification.
API Development & Deployment: Create an API to accept emails, mask PII, and classify them; deploy on Hugging Face Spaces.
Generate Output: Process the dataset, mask PII, classify emails, and return results.

Task 1: Data Collection & Preprocessing

Objective: Load emails.csv (24,000 rows, columns: email, type), mask PII (names, phone numbers, emails), and store original data securely.
Implementation:
Explored the dataset using explore.py to confirm:
Shape: 24,000 rows, 2 columns (email, type).
type distribution: Request (12,000), Incident (12,000).
Multilingual content (English, German) with PII in email (names, emails, phone numbers).


Developed mask_pii.py to mask PII:
Used Spacy (en_core_web_sm) for NER and regex for pattern matching.
Successfully masked:
Names after "My name is" or "ich heiße" (e.g., "My name is Elena Ivanova" → "My name is [NAME]").
Standalone names (e.g., "Elena Ivanova" → "[NAME]").
Emails (e.g., "user@example.com" → "[EMAIL]").
Placeholders (e.g., "[Your Name]" → "[NAME]").


Optimized with disabled Spacy components (parser, tagger) and tqdm (~4-5 minutes for 24,000 rows).
Issues:
Phone numbers (e.g., "+82-2-3456-7890", "1234567890") are not masked due to regex limitations.
Errors in mask_pii.py (under investigation, likely regex or execution issues).


Added logging to mask_pii.py for debugging (e.g., regex, file, Spacy errors).


Validation:
Created validate_pii.py to check for unmasked PII.
Validated 1,000 rows, initially reporting 0 issues (flawed phone regex).
Created spot_check_pii.py to inspect rows 1, 2, 20, 21, 64, 67, 87, 99, confirming names and emails are masked.
Updated regex in validate_pii.py; re-validation pending mask_pii.py fix.


Output:
Generated emails_masked.csv (24,000 rows, columns: email, type, email_masked), stored locally.
Status: Names and emails masked; phone numbers unmasked due to errors.


Secure Storage:
Excluded emails.csv and emails_masked.csv via .gitignore.




Next Steps:
Debug mask_pii.py errors (awaiting error traceback).
Fix phone number regex to mask all formats.
Re-run mask_pii.py and validate_pii.py to confirm 0 PII issues.



Task 2: Model Selection & Training

Objective: Train a model to classify emails by type using email_masked.
Status: Not started (waiting for Task 1 completion).
Planned Approach:
Evaluate models: Random Forest (scikit-learn), BERT (transformers).
Use email_masked as input, type as labels.



Task 3: System Integration

Objective: Build a pipeline for PII masking and classification.
Status: Not started.

Task 4: API Development & Deployment

Objective: Develop an API to mask PII and classify emails; deploy on Hugging Face Spaces.
Status: Not started.
Planned Approach:
Use FastAPI for API development.
Deploy via Hugging Face Spaces.



Task 5: Generate Output

Objective: Process emails.csv, mask PII, classify emails, and return results.
Status: In progress (masking incomplete due to phone number issue).

Repository Structure

.gitignore: Excludes emails.csv and emails_masked.csv.
README.md: Project documentation.
explore.py: Dataset exploration (Task 1).
mask_pii.py: PII masking script with logging (Task 1).
validate_pii.py: PII validation script (Task 1).
spot_check_pii.py: Targeted PII validation (Task 1).
Pending Files:
app.py: Main script for pipeline.
models.py: Model training functions.
utils.py: Utility functions.
api.py: API development.
requirements.txt: Dependencies.



Setup Instructions

Clone the repository:git clone https://github.com/dhanush14chowdary/akaike_email_classification


Install dependencies:pip install spacy tqdm pandas
python -m spacy download en_core_web_sm


Place emails.csv in the project directory.
Run scripts:python explore.py
python mask_pii.py
python validate_pii.py
python spot_check_pii.py



Current Status

Task 1: Partially complete (names/emails masked; phone number masking and mask_pii.py errors pending).
Task 2–5: Not started (dependent on Task 1).
Next Steps:
Fix mask_pii.py errors and phone number masking.
Finalize Task 1 and start Task 2 (model training).
Develop pipeline, API, and deploy solution.



Code Quality

Following PEP8 guidelines.
Code commented for clarity.
Logging added for debugging.
Sensitive data excluded via .gitignore.

Author

Dhanush
GitHub: dhanush14chowdary
Date: April 18, 2025

