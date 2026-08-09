# ============================================================
# MIMIC PATIENT ANALYTICS
# DATA QUALITY ENGINE
# ============================================================

import pandas as pd


# ============================================================
# DATASET QUALITY SUMMARY
# ============================================================

def dataset_quality_summary(datasets):
    """
    Generate a standardized data-quality summary
    for multiple datasets.

    Parameters
    ----------
    datasets : dict
        Dictionary in the form:
        {
            "dataset_name": dataframe
        }

    Returns
    -------
    pandas.DataFrame
        Summary containing:
        - dataset name
        - number of rows
        - number of columns
        - total missing cells
        - duplicate rows
    """

    results = []

    for name, df in datasets.items():

        results.append({
            "dataset": name,
            "rows": len(df),
            "columns": len(df.columns),
            "missing_cells": int(
                df.isna().sum().sum()
            ),
            "duplicate_rows": int(
                df.duplicated().sum()
            )
        })

    return pd.DataFrame(results)


# ============================================================
# MISSINGNESS BY COLUMN
# ============================================================

def missingness_by_column(df):
    """
    Calculate missing-value statistics
    for every column in a DataFrame.

    Returns
    -------
    pandas.DataFrame
        Columns:
        - missing_count
        - total_rows
        - missing_pct
    """

    result = pd.DataFrame({
        "missing_count": df.isna().sum(),
        "total_rows": len(df)
    })

    result["missing_pct"] = (
        result["missing_count"]
        / result["total_rows"]
        * 100
    )

    return (
        result
        .sort_values(
            "missing_pct",
            ascending=False
        )
    )


# ============================================================
# KEY COVERAGE
# ============================================================

def key_coverage(df, key_column):
    """
    Measure completeness and uniqueness
    of a key column.

    Parameters
    ----------
    df : pandas.DataFrame
    key_column : str

    Returns
    -------
    dict
    """

    if key_column not in df.columns:
        raise ValueError(
            f"Column '{key_column}' not found in DataFrame."
        )

    return {
        "column": key_column,
        "total_rows": len(df),
        "missing_keys": int(
            df[key_column].isna().sum()
        ),
        "unique_keys": int(
            df[key_column].nunique()
        )
    }


# ============================================================
# DUPLICATE SUMMARY
# ============================================================

def duplicate_summary(df):
    """
    Summarize duplicate rows in a DataFrame.

    Returns
    -------
    dict
        - total rows
        - duplicate rows
        - duplicate percentage
    """

    duplicate_count = int(
        df.duplicated().sum()
    )

    return {
        "total_rows": len(df),
        "duplicate_rows": duplicate_count,
        "duplicate_pct": (
            duplicate_count / len(df) * 100
            if len(df) > 0
            else 0
        )
    }


# ============================================================
# REFERENTIAL INTEGRITY
# ============================================================

def unmatched_keys(
    child_df,
    parent_df,
    key_column
):
    """
    Check whether keys in a child DataFrame
    exist in a parent DataFrame.

    Example
    -------
    admissions -> patients

    Parameters
    ----------
    child_df : pandas.DataFrame
    parent_df : pandas.DataFrame
    key_column : str

    Returns
    -------
    dict
    """

    if key_column not in child_df.columns:
        raise ValueError(
            f"Column '{key_column}' not found "
            "in child DataFrame."
        )

    if key_column not in parent_df.columns:
        raise ValueError(
            f"Column '{key_column}' not found "
            "in parent DataFrame."
        )

    child_keys = set(
        child_df[key_column]
        .dropna()
        .unique()
    )

    parent_keys = set(
        parent_df[key_column]
        .dropna()
        .unique()
    )

    unmatched = child_keys - parent_keys

    return {
        "child_dataset_rows": len(child_df),
        "unique_child_keys": len(child_keys),
        "unmatched_keys": len(unmatched),
        "unmatched_key_values": sorted(
            unmatched
        )
    }


# ============================================================
# INVALID DATETIME COUNT
# ============================================================

def invalid_datetime_count(
    df,
    column
):
    """
    Count invalid datetime values in a column.

    Null values are not treated as invalid.
    Only non-null values that fail datetime
    conversion are counted as invalid.

    Returns
    -------
    dict or None
    """

    if column not in df.columns:
        return None

    original_non_null = df[column].notna().sum()

    parsed = pd.to_datetime(
        df[column],
        errors="coerce"
    )

    invalid_count = (
        original_non_null
        - parsed.notna().sum()
    )

    return {
        "column": column,
        "non_null_values": int(
            original_non_null
        ),
        "invalid_datetime_values": int(
            invalid_count
        )
    }
