import pandas as pd
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    df = pd.read_csv("emails_masked.csv")
    logger.info("Spot-checking PII masking for specific rows")
except Exception as e:
    logger.error(f"Error loading emails_masked.csv: {e}")
    exit(1)

unmasked_count = 0
check_rows = [1, 2, 20, 21, 64, 67, 87, 99]
for idx in check_rows:
    email_masked = df.iloc[idx]["email_masked"]
    if re.search(r'\b(?:\+?\d{1,4})?[-. ]?(?:\(\d{1,4}\)|\d{1,4})?[-. ]?\d{1,4}[-. ]?\d{1,4}[-. ]?\d{1,9}\b|\b\d{7,12}\b', email_masked):
        logger.warning(f"Phone not masked in row {idx}: {email_masked}")
        unmasked_count += 1
    if re.search(r'(?i)(?:my name is|ich heiße|name is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', email_masked):
        logger.warning(f"Name not masked in row {idx}: {email_masked}")
        unmasked_count += 1
    if re.search(r'\[Your Name\]', email_masked):
        logger.warning(f"[Your Name] not masked in row {idx}: {email_masked}")
        unmasked_count += 1
logger.info(f"Spot-check complete. {unmasked_count} issues found.")