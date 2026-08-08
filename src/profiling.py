# ============================================================
# MIMIC PATIENT ANALYTICS
# DATA PROFILING MODULE
# ============================================================

import pandas as pd


# ============================================================
# BASIC DATASET PROFILE
# ============================================================

def profile_dataset(df, dataset_name):
    """
    Generate basic structural information
    about a dataset.
    """

    return {
        "dataset": dataset_name,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_cells": int(
            df.isna().sum().sum()
        ),
        "duplicate_rows": int(
            df.duplicated().sum()
        ),
    }


# ============================================================
# MISSINGNESS REPORT
# ============================================================

def missingness_report(df):
    """
    Calculate missing-value counts and percentages
    for every column.
    """

    report = pd.DataFrame({
        "missing_count": df.isna().sum(),
        "total_rows": len(df)
    })

    report["missing_pct"] = (
        report["missing_count"]
        / report["total_rows"]
        * 100
    )

    report = report.sort_values(
        "missing_pct",
        ascending=False
    )

    return report


# ============================================================
# COLUMN PROFILE
# ============================================================

def column_profile(df):
    """
    Generate a column-level structural profile.
    """

    report = pd.DataFrame({
        "column": df.columns,
        "dtype": df.dtypes.astype(str).values,
        "missing_count": df.isna().sum().values,
        "unique_values": df.nunique(
            dropna=True
        ).values
    })

    report["missing_pct"] = (
        report["missing_count"]
        / len(df)
        * 100
    )

    return report


# ============================================================
# DUPLICATE REPORT
# ============================================================

def duplicate_report(df):
    """
    Report duplicate rows in a dataset.
    """

    duplicate_count = int(
        df.duplicated().sum()
    )

    duplicate_pct = (
        duplicate_count / len(df) * 100
        if len(df) > 0
        else 0
    )

    return {
        "duplicate_rows": duplicate_count,
        "duplicate_pct": duplicate_pct
    }
