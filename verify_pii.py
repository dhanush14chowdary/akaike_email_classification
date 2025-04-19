# verify_pii.py
# Verifies PII masking for specific rows and data integrity
# Author: Dhanush
# Date: April 19, 2025

import pandas as pd

pd.set_option('display.max_colwidth', None)

try:
    masked = pd.read_csv("emails_masked.csv")
    original = pd.read_csv("emails.csv")
except Exception as e:
    print(f"Error loading datasets: {e}")
    exit(1)

rows_to_check = [5, 64, 23778, 23818]
for row in rows_to_check:
    print(f"Row {row}:\n", masked.loc[row, ["email", "email_masked"]])
    print()

print("Shape:", masked.shape)
print("Type counts:\n", masked["type"].value_counts())
print("Original type counts:\n", original["type"].value_counts())
print("Type columns match:", (original["type"] == masked["type"]).all())