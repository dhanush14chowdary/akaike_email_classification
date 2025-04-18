Akaike Email Classification Assignment
This repository contains the implementation of the Akaike Data Science Internship assignment (April 2025), focused on email classification with PII masking and model training. The project processes a dataset of 24,000 emails to mask personally identifiable information (PII) and classify emails by type (e.g., Incident, Request).
Task 1: Data Exploration

Objective: Explore the dataset to understand its structure, columns, and categories.
Implementation:
Used explore.py to load emails.csv (24,000 rows, columns: email, type).
Analyzed the dataset shape, column types, and distribution of type (e.g., Request: 12,000, Incident: 12,000).
Identified multilingual content (English, German) and PII (names, emails, phone numbers) in the email column.


Output: Summary statistics and insights stored locally (not uploaded due to .gitignore).

Task 2: PII Masking

Objective: Mask PII (names, phone numbers, emails) in the email column of emails.csv to ensure privacy compliance.
Implementation:
Developed mask_pii.py using Spacy (en_core_web_sm) and regex to mask PII in English and German emails.
Successfully masked:
Names after "My name is" or "ich heiße" (e.g., "My name is Elena Ivanova" → "My name is [NAME]").
Standalone names (e.g., "Elena Ivanova" → "[NAME]").
Emails (e.g., "user@example.com" → "[EMAIL]").
Placeholders (e.g., "[Your Name]" → "[NAME]").


Optimized with disabled Spacy components (parser, tagger) and tqdm progress bar (~4-5 minutes for 24,000 rows).
Encountered issues:
Phone numbers (e.g., "+82-2-3456-7890", "1234567890") are not masking due to regex limitations.
Errors in mask_pii.py (pending debugging, likely related to phone number regex or script execution).


Added logging to mask_pii.py to diagnose errors (e.g., regex, file handling, Spacy issues).


Validation:
Created validate_pii.py to check for unmasked PII (emails, phones, names, [Your Name]).
Validated 1,000 rows, initially reporting 0 issues due to a flawed phone number regex.
Created spot_check_pii.py to validate specific rows (1, 2, 20, 21, 64, 67, 87, 99), confirming names and emails are masked.
Updated regex in validate_pii.py to catch unmasked phone numbers; re-validation pending after fixing mask_pii.py.


Output:
Generated emails_masked.csv (24,000 rows, columns: email, type, email_masked), stored locally and excluded via .gitignore.
Current status: Names and emails masked correctly; phone numbers unmasked due to ongoing errors.


Files:
mask_pii.py: PII masking script with logging.
validate_pii.py: PII validation script.
spot_check_pii.py: Targeted validation for specific rows.
explore.py: Data exploration script (Task 1).


Next Steps:
Debug errors in mask_pii.py (e.g., phone number regex, execution issues).
Re-run mask_pii.py and validate_pii.py to ensure all phone numbers are masked.
Commit fixed scripts and finalize Task 2.



Repository Structure

.gitignore: Excludes emails.csv and emails_masked.csv to avoid uploading sensitive data.
README.md: Project documentation.
explore.py: Task 1 data exploration.
mask_pii.py: Task 2 PII masking script.
validate_pii.py: Task 2 validation script.
spot_check_pii.py: Task 2 spot-check script.

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

Task 1: Completed (data exploration).
Task 2: In progress (names and emails masked; phone number masking and script errors pending resolution).
Task 3: Not started (model training pending Task 2 completion).

Author

Dhanush
GitHub: dhanush14chowdary
Date: April 18, 2025

