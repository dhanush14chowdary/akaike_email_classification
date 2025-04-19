# validate_pii.py
# Validates PII masking in emails_masked.csv, checking for unmasked names, emails, phone numbers
# Added 'Book Air' to exclusion list to fix false positives, aligned with mask_pii.py
# Author: Dhanush
# Date: April 19, 2025

import pandas as pd
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define regex patterns
phone_pattern = r'\b(?:\+?\d{1,4}[-.\s]?)?(?:\(\d{1,4}\)|[\d-]{1,4})?[-.\s]?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,9}\b|\b\d{10,12}\b|<tel_num>'
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
name_pattern = r'\b[A-Z][a-z]{2,} [A-Z][a-z]{2,}\b'  # Stricter: 3+ letters per name part

def validate_pii(text, row_idx):
    issues = []
    if not isinstance(text, str):
        return issues

    # Remove masked tokens before validation
    text_clean = re.sub(r'\[PHONE\]|\[EMAIL\]|\[NAME\]|\[\[NAME\]\]', '', text)

    # Check for phone numbers
    phone_matches = re.finditer(phone_pattern, text_clean)
    for match in phone_matches:
        issues.append(f"Phone not masked in row {row_idx}: {match.group()}")

    # Check for emails
    email_matches = re.finditer(email_pattern, text_clean)
    for match in email_matches:
        issues.append(f"Email not masked in row {row_idx}: {match.group()}")

    # Check for names
    name_matches = re.finditer(name_pattern, text_clean)
    for match in name_matches:
        # Exclude common false positives
        if match.group() not in ["Customer Support", "Dear Customer", "Concerns About", "Securing Medical", "Book Air"]:
            issues.append(f"Name not masked in row {row_idx}: {match.group()}")

    return issues

def main():
    # Load dataset
    try:
        df = pd.read_csv("emails_masked.csv")
        logger.info(f"Validating PII masking for {len(df)} rows")
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        exit(1)

    # Validate PII
    issues = []
    for idx, row in df.iterrows():
        row_issues = validate_pii(row["email_masked"], idx)
        issues.extend(row_issues)

    # Log results
    if issues:
        for issue in issues[:10]:  # Log first 10 issues
            logger.warning(issue)
        logger.info(f"Validation complete. {len(issues)} potential PII issues found.")
    else:
        logger.info("Validation complete. 0 potential PII issues found.")

if __name__ == "__main__":
    main()