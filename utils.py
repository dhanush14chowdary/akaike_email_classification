# utils.py
# Utility functions for PII masking
# Author: Dhanush
# Date: April 19, 2025

import spacy
import re
from typing import List, Dict

phone_pattern = r'\b(?:\+?\d{1,4}[-.\s]?)?(?:\(\d{3}\))?[-.\s]?\d{3}[-.\s]?\d{4}\b'
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
name_pattern = r'\b[A-Z][a-z]{2,}\s[A-Z][a-z]{2,}\b'
dob_pattern = r'\b(?:0[1-9]|1[0-2])[-/](?:0[1-9]|[12][0-9]|3[01])[-/](?:19|20)\d{2}\b'
aadhar_pattern = r'\b\d{4}\s\d{4}\s\d{4}\b'
credit_debit_pattern = r'\b\d{4}[- ]\d{4}[- ]\d{4}[- ]\d{4}\b'
cvv_pattern = r'(?<!\d)\b\d{3}\b(?!\d)'  # 3 digits, not part of larger number
expiry_pattern = r'\b(?:0[1-9]|1[0-2])/\d{2}\b'
placeholder_pattern = r'\b(?:<name>|<company_name>|<role>|<acc_num>|\[Ihr Name\])\b'

def mask_pii(text: str, nlp) -> tuple[str, List[Dict]]:
    if not isinstance(text, str):
        return text, []

    masked_entities = []
    
    def add_entity(start: int, end: int, entity_type: str, entity_value: str):
        masked_entities.append({
            "position": [start, end],
            "classification": entity_type,
            "entity": entity_value
        })

    # Initialize masked text
    masked_text = text
    offset = 0

    # Apply regex patterns in order of specificity
    patterns = [
        (email_pattern, '[email]', 'email'),
        (aadhar_pattern, '[aadhar_num]', 'aadhar_num'),
        (credit_debit_pattern, '[credit_debit_no]', 'credit_debit_no'),
        (dob_pattern, '[dob]', 'dob'),
        (phone_pattern, '[phone_number]', 'phone_number'),
        (expiry_pattern, '[expiry_no]', 'expiry_no'),
        (cvv_pattern, '[cvv_no]', 'cvv_no'),
        (placeholder_pattern, '[full_name]', 'full_name'),
    ]

    for pattern, placeholder, entity_type in patterns:
        matches = list(re.finditer(pattern, masked_text))
        replacements = []
        for match in matches:
            start, end = match.start(), match.end()
            entity_value = match.group()
            replacements.append((start, end, placeholder, entity_value))
            add_entity(start, end, entity_type, entity_value)
        # Apply replacements in reverse order to preserve positions
        replacements.sort(key=lambda x: x[0], reverse=True)
        for start, end, placeholder, _ in replacements:
            masked_text = masked_text[:start] + placeholder + masked_text[end:]

    # Apply name pattern, skip subjects
    matches = list(re.finditer(name_pattern, masked_text))
    replacements = []
    for match in matches:
        start, end = match.start(), match.end()
        entity_value = match.group()
        # Skip if in subject line or already masked
        if (not re.match(r'^Subject:.*$', masked_text[:start].split('\n')[-1]) and
            not re.search(r'\[(full_name|email|phone_number|dob|aadhar_num|credit_debit_no|cvv_no|expiry_no)\]', entity_value)):
            replacements.append((start, end, '[full_name]', entity_value))
            add_entity(start, end, 'full_name', entity_value)
    replacements.sort(key=lambda x: x[0], reverse=True)
    for start, end, placeholder, _ in replacements:
        masked_text = masked_text[:start] + placeholder + masked_text[end:]

    # Apply Spacy NER for names not caught by regex
    lines = masked_text.split('\n')
    masked_lines = []
    offset = 0
    for line in lines:
        original_line = line
        if not re.search(r'\[(full_name|email|phone_number|dob|aadhar_num|credit_debit_no|cvv_no|expiry_no)\]', line):
            doc = nlp(line)
            replacements = []
            for ent in doc.ents:
                if (ent.label_ == "PERSON" and len(ent.text.split()) >= 2 and
                    not re.match(r'^Subject:.*$', line) and
                    not re.match(r'\[(full_name|email|phone_number|dob|aadhar_num|credit_debit_no|cvv_no|expiry_no)\]', ent.text)):
                    start, end = ent.start_char, ent.end_char
                    replacements.append((start, end, '[full_name]', ent.text))
                    add_entity(offset + start, offset + end, 'full_name', ent.text)
            replacements.sort(key=lambda x: x[0], reverse=True)
            for start, end, placeholder, _ in replacements:
                line = line[:start] + placeholder + line[end:]
        masked_lines.append(line)
        offset += len(original_line) + 1

    masked_text = '\n'.join(masked_lines)
    return masked_text, masked_entities