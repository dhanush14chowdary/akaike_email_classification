# PII Masking Script for Akaike Email Classification
# Masks names, phone numbers, and emails in the 'email' column using Spacy and regex
# Optimized for speed with disabled Spacy components and tqdm progress bar
# Fixed phone number masking for all formats with error logging
# Author: Dhanush
# Date: April 18, 2025

import spacy
import pandas as pd
import re
import logging
from tqdm import tqdm

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load Spacy model
try:
    nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger"])
    logger.info("Spacy model loaded successfully")
except Exception as e:
    logger.error(f"Error loading Spacy model: {e}")
    exit(1)

def mask_pii(text):
    try:
        # Ensure text is a string
        if not isinstance(text, str):
            logger.warning(f"Non-string input: {text}")
            return str(text)
        masked_text = text

        # Regex for names after "My name is" or similar
        name_pattern = r'(?i)(my name is|ich heiße|name is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'
        masked_text = re.sub(name_pattern, r'\1 [NAME]', masked_text)

             # Additional regex for standalone names
        standalone_name_pattern = r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'
        masked_text = re.sub(standalone_name_pattern, '[NAME]', masked_text)

             # Regex for phone numbers (simplified for US and international)
        phone_pattern = r'\b(?:\+?\d{1,4})?[-. ]?(?:\(\d{1,4}\)|\d{1,4})?[-. ]?\d{1,4}[-. ]?\d{1,4}[-. ]?\d{1,9}\b|\b\d{7,12}\b'
        try:
            masked_text = re.sub(phone_pattern, "[PHONE]", masked_text)
        except Exception as e:
            logger.error(f"Phone regex error: {e}")
            return masked_text

             # Process text with Spacy
        try:
            doc = nlp(masked_text)
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    masked_text = masked_text.replace(ent.text, "[NAME]")
                elif ent.label_ in ["PHONE", "EMAIL"]:
                    masked_text = masked_text.replace(ent.text, f"[{ent.label_}]")
        except Exception as e:
            logger.error(f"Spacy processing error: {e}")

        # Regex for emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        masked_text = re.sub(email_pattern, "[EMAIL]", masked_text)

        # Mask "[Your Name]" placeholders
        masked_text = re.sub(r'\[Your Name\]', '[NAME]', masked_text)

        return masked_text
    except Exception as e:
        logger.error(f"Error masking text: {e}")
        return text

     # Load dataset (subset for testing)
try:
    df = pd.read_csv("emails.csv")
    logger.info(f"Dataset loaded successfully. Shape: {df.shape}")
except Exception as e:
    logger.error(f"Error loading dataset: {e}")
    exit(1)

     # Apply PII masking
try:
    tqdm.pandas()
    df["email_masked"] = df["email"].progress_apply(mask_pii)
    logger.info("PII masking applied")
except Exception as e:
    logger.error(f"Error applying PII masking: {e}")
    exit(1)

     # Save masked dataset
try:
    df.to_csv("emails_masked.csv", index=False)
    logger.info("Saved emails_masked.csv")
except Exception as e:
    logger.error(f"Error saving masked dataset: {e}")
    exit(1)

     # Print sample
try:
    with pd.option_context('display.max_colwidth', None):
        print("Sample Masked Data:\n", df[["email", "email_masked", "type"]].head())
except Exception as e:
    logger.error(f"Error printing sample: {e}")