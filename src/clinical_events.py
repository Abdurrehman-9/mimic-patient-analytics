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


# ============================================================
# LABORATORY METADATA ENRICHMENT
# ============================================================

def enrich_labevents(labevents, d_labitems):
    """
    Add human-readable laboratory metadata
    to laboratory events.
    """

    lab_dictionary = d_labitems[
        [
            "itemid",
            "label",
            "fluid",
            "category"
        ]
    ].drop_duplicates(
        subset=["itemid"]
    )

    enriched = labevents.merge(
        lab_dictionary,
        on="itemid",
        how="left",
        validate="many_to_one"
    )

    return enriched


# ============================================================
# LABORATORY TEST CATALOG
# ============================================================

def lab_test_catalog(labevents, d_labitems):
    """
    Create a catalog of laboratory tests with
    their metadata and observation counts.
    """

    enriched = enrich_labevents(
        labevents,
        d_labitems
    )

    catalog = (
        enriched
        .groupby(
            [
                "itemid",
                "label",
                "fluid",
                "category"
            ],
            dropna=False
        )
        .agg(
            observation_count=(
                "itemid",
                "size"
            ),

            unique_patients=(
                "subject_id",
                "nunique"
            ),

            numeric_observations=(
                "valuenum",
                lambda x: x.notna().sum()
            )
        )
        .reset_index()
        .sort_values(
            "observation_count",
            ascending=False
        )
    )

    return catalog


# ============================================================
# LABORATORY TEST SUMMARY (WITH ABNORMAL RATES)
# ============================================================

def laboratory_test_summary(
    labevents,
    d_labitems
):
    """
    Create a summary of laboratory tests including
    numeric statistics and abnormal observations.
    """

    df = enrich_labevents(
        labevents,
        d_labitems
    ).copy()

    df["valuenum"] = pd.to_numeric(
        df["valuenum"],
        errors="coerce"
    )

    summary = (
        df
        .groupby(
            [
                "itemid",
                "label",
                "fluid",
                "category"
            ],
            dropna=False
        )
        .agg(
            total_observations=(
                "itemid",
                "size"
            ),

            numeric_observations=(
                "valuenum",
                lambda x: x.notna().sum()
            ),

            unique_patients=(
                "subject_id",
                "nunique"
            ),

            abnormal_observations=(
                "flag",
                lambda x: (
                    x == "abnormal"
                ).sum()
            )
        )
        .reset_index()
    )

    summary["abnormal_rate_pct"] = (
        summary["abnormal_observations"]
        / summary["total_observations"]
        * 100
    )

    return summary.sort_values(
        "total_observations",
        ascending=False
    )
