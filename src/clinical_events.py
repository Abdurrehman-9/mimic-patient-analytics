# ============================================================
# MIMIC PATIENT ANALYTICS
# CLINICAL EVENTS MODULE
# ============================================================

import pandas as pd


# ============================================================
# LOAD CHARTEVENTS
# ============================================================

def load_chartevents(load_dataset):
    """
    Load the chartevents table through the central
    data loader.
    """

    return load_dataset("chartevents")


# ============================================================
# LOAD LABEVENTS
# ============================================================

def load_labevents(load_dataset):
    """
    Load the labevents table through the central
    data loader.
    """

    return load_dataset("labevents")


# ============================================================
# CHARTEVENT SUMMARY
# ============================================================

def chartevent_summary(chartevents):
    """
    Generate high-level statistics for chart events.
    """

    return {
        "total_events": len(chartevents),

        "unique_patients": (
            chartevents["subject_id"]
            .nunique()
        ),

        "unique_admissions": (
            chartevents["hadm_id"]
            .nunique()
        ),

        "unique_items": (
            chartevents["itemid"]
            .nunique()
        )
    }


# ============================================================
# CHART EVENTS BY ITEM
# ============================================================

def chartevents_by_item(chartevents):
    """
    Count chart events by item.
    """

    return (
        chartevents
        .groupby("itemid")
        .size()
        .rename("event_count")
        .reset_index()
        .sort_values(
            "event_count",
            ascending=False
        )
    )


# ============================================================
# LAB EVENT SUMMARY
# ============================================================

def lab_event_summary(labevents):
    """
    Generate high-level statistics for laboratory events.
    """

    return {
        "total_lab_events": len(labevents),

        "unique_patients": (
            labevents["subject_id"]
            .nunique()
        ),

        "unique_admissions": (
            labevents["hadm_id"]
            .nunique()
        ),

        "unique_lab_items": (
            labevents["itemid"]
            .nunique()
        )
    }


# ============================================================
# LAB EVENTS BY ITEM
# ============================================================

def lab_events_by_item(labevents):
    """
    Count laboratory events by item.
    """

    return (
        labevents
        .groupby("itemid")
        .size()
        .rename("event_count")
        .reset_index()
        .sort_values(
            "event_count",
            ascending=False
        )
    )


# ============================================================
# NUMERIC LABORATORY VALUES
# ============================================================

def numeric_lab_values(labevents):
    """
    Return laboratory observations with valid
    numeric values.
    """

    df = labevents.copy()

    df["valuenum"] = pd.to_numeric(
        df["valuenum"],
        errors="coerce"
    )

    return df[
        df["valuenum"].notna()
    ].copy()


# ============================================================
# LAB VALUE SUMMARY
# ============================================================

def lab_value_summary(labevents):
    """
    Calculate descriptive statistics for numeric
    laboratory measurements.
    """

    df = numeric_lab_values(
        labevents
    )

    return (
        df.groupby("itemid")["valuenum"]
        .agg([
            "count",
            "mean",
            "median",
            "std",
            "min",
            "max"
        ])
        .reset_index()
    )
