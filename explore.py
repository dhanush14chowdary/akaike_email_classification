import pandas as pd

# Load dataset
df = pd.read_csv("emails.csv")
print("Dataset Shape:", df.shape)  # Number of rows and columns
print("\nColumns:", df.columns.tolist())  # Column names
print("\nCategories:", df["type"].unique())  # Unique categories
print("\nSample Data:\n", df.head())  # First 5 rows
print("\nCategory Counts:\n", df["type"].value_counts())  # Count of each category