
    # clean_data.py
# A complete, VS Code friendly data-cleaning script
# - If messy_data.csv is missing, it will create a sample file with Indian names.
# - Then it reads, cleans, and writes cleaned_data.csv

import os
import pandas as pd
import numpy as np
from datetime import datetime

CSV_NAME = "messy_data.csv"
CLEANED_CSV = "cleaned_data.csv"

SAMPLE_CSV_CONTENT = """Name, Age ,salary , join_date ,Department
rahul sharma,25,50000,2022/01/10,hr
Priya   Singh, ,55000,10-02-2021,Finance
Amit,30, ,2021/5/7,IT
rahul sharma,25,50000,2022/01/10,hr
Ananya,,62000,2022/11/15, finance
Ravi Kumar,28,45000,15-08-2020,operations
Sakshi Gupta, ,48000,03-03-2021,HR
Deepak,27, ,2021/12/01, it
"""

def ensure_sample_csv():
    """Create a sample messy CSV if one doesn't exist."""
    if not os.path.exists(CSV_NAME):
        print(f"'{CSV_NAME}' not found — creating a sample file for you.")
        with open(CSV_NAME, "w", encoding="utf-8") as f:
            f.write(SAMPLE_CSV_CONTENT)
        print(f"Sample '{CSV_NAME}' created. You can edit it in VS Code and re-run the script.\n")

def read_csv_safe(path):
    """Read CSV robustly; return DataFrame or raise friendly error."""
    try:
        # read as strings first to avoid parsing errors
        df = pd.read_csv(path, dtype=str)
        return df
    except pd.errors.EmptyDataError:
        raise SystemExit(f"Error: '{path}' is empty. Open the file and add data.")
    except FileNotFoundError:
        raise SystemExit(f"Error: '{path}' not found. Make sure it's in the same folder as this script.")
    except Exception as e:
        raise SystemExit(f"Error reading '{path}': {e}")

def standardize_column_names(df):
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

def clean_names(s: pd.Series) -> pd.Series:
    # collapse multiple spaces, strip, title case
    s = s.fillna("").astype(str)
    s = s.str.strip().str.replace(r"\s+", " ", regex=True)
    s = s.str.title()
    s = s.replace("", np.nan)  # empty -> NaN
    return s

def clean_departments(s: pd.Series) -> pd.Series:
    s = s.fillna("").astype(str)
    s = s.str.strip().str.replace(r"\s+", " ", regex=True)
    s = s.str.lower().str.title()
    s = s.replace("", np.nan)
    return s

def to_numeric(series, how="median"):
    """Convert to numeric and fill missing with median (or mean)"""
    num = pd.to_numeric(series, errors="coerce")
    if num.isna().all():
        return num  # nothing to fill
    if how == "median":
        fill = int(num.median()) if not np.isnan(num.median()) else 0
    else:
        fill = int(num.mean()) if not np.isnan(num.mean()) else 0
    return num.fillna(fill).astype(int)

def parse_dates(series):
    # dayfirst=True helps for formats like 10-02-2021 (10 Feb 2021)
    parsed = pd.to_datetime(series, errors="coerce", dayfirst=True)
    return parsed

def main():
    # 1) Ensure sample file exists (helps beginners)
    ensure_sample_csv()

    # 2) Show current directory and files (helpful debug info)
    print("Current working directory:", os.getcwd())
    print("Files in the current directory:")
    for fname in sorted(os.listdir()):
        print("-", fname)
    print()

    # 3) Read CSV
    df = read_csv_safe(CSV_NAME)
    print("Original data (first 10 rows):")
    print(df.head(10).to_string(index=False))
    print("\n--- Starting cleaning steps ---\n")

    # 4) Standardize column names
    df = standardize_column_names(df)

    # normalize expected column names (handle tiny differences)
    # map probable alternatives to our expected names
    expected_map = {
        "name": "name",
        "age": "age",
        "salary": "salary",
        "join_date": "join_date",
        "date": "join_date",
        "department": "department",
    }
    # attempt to rename columns based on keywords
    rename_map = {}
    for col in df.columns:
        k = col.lower().replace("-", "_")
        if k in expected_map:
            rename_map[col] = expected_map[k]
    if rename_map:
        df = df.rename(columns=rename_map)

    # 5) Clean name column
    if "name" in df.columns:
        df["name"] = clean_names(df["name"])
    else:
        print("Warning: 'name' column not found.")

    # 6) Clean department column
    if "department" in df.columns:
        df["department"] = clean_departments(df["department"])
    else:
        print("Warning: 'department' column not found.")

    # 7) Age and salary -> numeric and fill missing
    if "age" in df.columns:
        df["age"] = to_numeric(df["age"], how="median")
    if "salary" in df.columns:
        df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
        # fill salary with median of available salaries
        if df["salary"].notna().any():
            median_sal = int(df["salary"].median(skipna=True))
            df["salary"] = df["salary"].fillna(median_sal).astype(int)
        else:
            df["salary"] = df["salary"].fillna(0).astype(int)

    # 8) Parse dates
    if "join_date" in df.columns:
        df["join_date"] = parse_dates(df["join_date"])

    # 9) Trim whitespace in all string columns (final pass)
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip().replace("nan", np.nan)

    # 10) Remove exact duplicates (after cleaning)
    before = len(df)
    df = df.drop_duplicates(keep="first").reset_index(drop=True)
    after = len(df)
    print(f"Removed {before - after} duplicate rows.")

    # 11) Reorder columns if you want a canonical order
    cols_order = ["name", "age", "salary", "join_date", "department"]
    cols_present = [c for c in cols_order if c in df.columns]
    other_cols = [c for c in df.columns if c not in cols_present]
    df = df[cols_present + other_cols]

    # 12) Show summary and save
    print("\nCleaned data (first 10 rows):")
    print(df.head(10).to_string(index=False))
    print("\nData types and missing counts:")
    print(df.info())
    print("\nMissing values per column:")
    print(df.isna().sum())

    # 13) Export cleaned CSV
    df.to_csv(CLEANED_CSV, index=False, date_format="%Y-%m-%d")
    print(f"\nCleaned file written to '{CLEANED_CSV}'. You're ready to analyze it!")

if __name__ == "__main__":
    main()
