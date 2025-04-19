# mask_pii.py
# Masks PII in emails.csv and saves to emails_masked.csv
# Fixed phone regex, stricter name regex, prevents nested masking
# Author: Dhanush
# Date: April 19, 2025

import spacy
import pandas as pd
import re
from tqdm import tqdm
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load Spacy model
try:
    nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger", "lemmatizer"])
    logger.info("Spacy model loaded successfully")
except Exception as e:
    logger.error(f"Error loading Spacy model: {e}")
    exit(1)

# Define regex patterns
phone_pattern = r'\b(?:\+?\d{1,4}[-.\s]?)?(?:\(\d{1,4}\)|[\d-]{1,4})?[-.\s]?\d{3,4}[-.\s]?\d{3,4}(?:[-.\s]?\d{3,4})?\b|\b\d{10,12}\b|<tel_num>'
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
name_pattern = r'\b[A-Z][a-z]{2,}\s[A-Z][a-z]{2,}\b'

def mask_pii(text, nlp):
    if not isinstance(text, str):
        return text

    # Replace placeholders
    text = re.sub(r'<tel_num>', '[PHONE]', text)
    text = re.sub(r'<name>|<company_name>|<role>|<acc_num>', '[NAME]', text)

    # Regex-based masking (phone first to avoid NER overlap)
    text = re.sub(phone_pattern, '[PHONE]', text)
    text = re.sub(email_pattern, '[EMAIL]', text)
    text = re.sub(name_pattern, '[NAME]', text)

    # Spacy NER only for unmasked text
    if not re.search(r'\[PHONE\]|\[EMAIL\]|\[NAME\]', text):
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON" and not re.match(r'\[(PHONE|EMAIL|NAME)\]', ent.text):
                text = text.replace(ent.text, "[NAME]")

    return text

def main():
    try:
        df = pd.read_csv("emails.csv")
        logger.info(f"Dataset loaded successfully. Shape: {df.shape}")
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        exit(1)

    tqdm.pandas()
    df["email_masked"] = df["email"].progress_apply(lambda x: mask_pii(x, nlp))
    logger.info("PII masking applied")

    try:
        df.to_csv("emails_masked.csv", index=False)
        logger.info("Saved emails_masked.csv")
    except Exception as e:
        logger.error(f"Error saving dataset: {e}")
        exit(1)

    logger.info("Sample Masked Data:")
    print(df[["email", "type", "email_masked"]].head())

if __name__ == "__main__":
    main()