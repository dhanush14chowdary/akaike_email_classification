import pandas as pd
pd.set_option('display.max_colwidth', None)  # Show full column content
df = pd.read_csv("emails_masked.csv")
print("Row 64:\n", df.loc[64, ["email", "email_masked"]])
print("Row 23778:\n", df.loc[23778, ["email", "email_masked"]])
print("Row 23818:\n", df.loc[23818, ["email", "email_masked"]])
print("Row 5:\n", df.loc[5, ["email", "email_masked"]])