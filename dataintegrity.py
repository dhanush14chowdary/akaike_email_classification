import pandas as pd
masked = pd.read_csv("emails_masked.csv")
print("Shape:", masked.shape)
print("Type counts:\n", masked["type"].value_counts())
original = pd.read_csv("emails.csv")
print("Original type counts:\n", original["type"].value_counts())
print("Type columns match:", (original["type"] == masked["type"]).all())