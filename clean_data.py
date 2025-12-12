import pandas as pd

# Load raw data
df = pd.read_csv("data_raw.csv")

# Remove duplicate rows
df = df.drop_duplicates()

# Fill missing marks with average
avg_marks = df["Marks"].mean()
df["Marks"] = df["Marks"].fillna(avg_marks)

# Correct outliers    
df.loc[df["Marks"] > 100, "Marks"] = 100

# Export cleaned CSV
df.to_csv("data_cleaned.csv", index=False)

print("Data cleaning completed! Cleaned file saved as data_cleaned.csv")
