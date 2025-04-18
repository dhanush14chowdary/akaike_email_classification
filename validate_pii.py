import pandas as pd
import re
import logging
    
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
    
try:
    df = pd.read_csv("emails_masked.csv")
    logger.info(f"Validating PII masking for {df.shape[0]} rows")
except Exception as e:
    logger.error(f"Error loading emails_masked.csv: {e}")
    exit(1)
    
unmasked_count = 0
for idx, row in df.iterrows():
    email_masked = row["email_masked"]
        # Check for emails
    if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email_masked):
        logger.warning(f"Email not masked in row {idx}: {email_masked}")
        unmasked_count += 1
        # Check for phone numbers
    if re.search(r'\b(?:\+?\d{1,4})?[-. ]?(?:\(\d{1,4}\)|\d{1,4})?[-. ]?\d{1,4}[-. ]?\d{1,4}[-. ]?\d{1,9}\b|\b\d{7,12}\b', email_masked):
        logger.warning(f"Phone not masked in row {idx}: {email_masked}")
        unmasked_count += 1
        # Check for names after "My name is"
    if re.search(r'(?i)(?:my name is|ich heiße|name is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', email_masked):
        logger.warning(f"Name not masked in row {idx}: {email_masked}")
        unmasked_count += 1
        # Check for [Your Name]
    if re.search(r'\[Your Name\]', email_masked):
        logger.warning(f"[Your Name] not masked in row {idx}: {email_masked}")
        unmasked_count += 1
    
logger.info(f"Validation complete. {unmasked_count} potential PII issues found.")