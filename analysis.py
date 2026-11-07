import pandas as pd

def prepare_data(df):
    data = df.copy()
    if "Attrition" not in data.columns:
        raise ValueError("Required column Attrition is missing.")
    if data["Attrition"].dtype == object:
        values = data["Attrition"].astype(str).str.strip().str.lower().map(
            {"yes": 1, "no": 0, "1": 1, "0": 0, "true": 1, "false": 0})
        if values.isna().any():
            raise ValueError("Attrition must be encoded as Yes/No or 1/0.")
        data["Attrition"] = values
    data["Attrition"] = pd.to_numeric(data["Attrition"], errors="coerce")
    data = data.dropna(subset=["Attrition"])
    data["Attrition"] = data["Attrition"].astype(int)
    if not set(data["Attrition"].unique()).issubset({0, 1}):
        raise ValueError("Attrition must be binary: 0=stayed, 1=left.")
    return data

def attrition_summary(df):
    n = len(df)
    left = int(df["Attrition"].sum())
    return {"employees": n, "attrition_count": left,
            "retained_count": n-left, "attrition_rate": left/n if n else 0,
            "missing_cells": int(df.isna().sum().sum())}

def attrition_by_category(df, column):
    return df.groupby(column, dropna=False)["Attrition"].mean().sort_values(ascending=False)
