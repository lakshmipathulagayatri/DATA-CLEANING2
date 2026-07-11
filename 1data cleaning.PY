

import pandas as pd
import numpy as np


def clean_data(filepath):
    df = pd.read_csv(filepath)

    # --- Handle missing values ---
    num_cols = df.select_dtypes(include=np.number).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    cat_cols = df.select_dtypes(include='object').columns
    for col in cat_cols:
        mode_val = df[col].mode()
        df[col] = df[col].fillna(mode_val[0] if not mode_val.empty else 'Unknown')

    # --- Remove duplicates ---
    before = len(df)
    df = df.drop_duplicates()
    print(f"Removed {before - len(df)} duplicate rows")

    # --- Fix inconsistent text formatting ---
    for col in cat_cols:
        df[col] = df[col].astype(str).str.strip().str.title()

    # --- Standardize date columns ---
    date_cols = [c for c in df.columns if 'date' in c.lower()]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # --- Remove outliers (IQR method) ---
    for col in num_cols:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]

    return df


if __name__ == "__main__":
    cleaned_df = clean_data("raw_data.csv")
    cleaned_df.to_csv("cleaned_data.csv", index=False)
    print("Data cleaning complete. Saved as cleaned_data.csv")