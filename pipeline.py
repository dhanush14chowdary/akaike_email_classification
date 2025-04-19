# pipeline.py
# Integrates PII masking and classification
# Author: Dhanush
# Date: April 19, 2025

import spacy
import re
import joblib
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger", "lemmatizer"])
    logger.info("Spacy model loaded successfully")
except Exception as e:
    logger.error(f"Error loading Spacy model: {e}")
    exit(1)

try:
    model = joblib.load("rf_model.pkl")
    logger.info("Random Forest model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    exit(1)

phone_pattern = r'\b(?:\+?\d{1,4}[-.\s]?)?(?:\(\d{1,4}\)|[\d-]{1,4})?[-.\s]?\d{3,4}[-.\s]?\d{3,4}(?:[-.\s]?\d{3,4})?\b|\b\d{10,12}\b|<tel_num>'
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
name_pattern = r'\b[A-Z][a-z]{2,}\s[A-Z][a-z]{2,}\b'
placeholder_pattern = r'\b(?:<name>|<company_name>|<role>|<acc_num>|\[Ihr Name\])\b'

def mask_pii(text, nlp):
    if not isinstance(text, str):
        return text

    text = re.sub(r'<tel_num>', '[PHONE]', text)
    text = re.sub(placeholder_pattern, '[NAME]', text)
    text = re.sub(phone_pattern, '[PHONE]', text)
    text = re.sub(email_pattern, '[EMAIL]', text)
    text = re.sub(name_pattern, '[NAME]', text)

    if not re.search(r'\[PHONE\]|\[EMAIL\]|\[NAME\]', text):
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON" and len(ent.text.split()) >= 2 and not re.match(r'\[(PHONE|EMAIL|NAME)\]', ent.text):
                text = text.replace(ent.text, "[NAME]")

    return text

def classify_email(email):
    logger.info("Masking email...")
    masked_email = mask_pii(email, nlp)
    
    logger.info("Classifying email...")
    prediction = model.predict([masked_email])[0]
    
    return {"masked_email": masked_email, "category": prediction}

if __name__ == "__main__":
    test_email = """
    Subject: Test Email
    Hello, please contact me at john.doe@example.com or +82-2-3456-7890.
    My name is John Doe.
    """
    result = classify_email(test_email)
    print(result)