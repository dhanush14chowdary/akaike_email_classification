import spacy

# Load Spacy model
nlp = spacy.load("en_core_web_sm")

# Test text with PII
text = "My name is Alice Smith. Call me at (555) 123-4567 or email alice.smith@example.com."
doc = nlp(text)

# Print detected entities
print("Detected Entities:")
for ent in doc.ents:
    print(f"Text: {ent.text}, Label: {ent.label_}")