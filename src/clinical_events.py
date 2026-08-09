# ============================================================
# MIMIC PATIENT ANALYTICS
# CLINICAL EVENTS & LABORATORY ANALYTICS
# ============================================================

import pandas as pd


# ============================================================
# CHARTEVENTS
# ============================================================

def load_chartevents(load_dataset):
    """
    Load chartevents using the central data loader.
    """

    return load_dataset("chartevents")


def chartevent_summary(chartevents):
    """
    Generate high-level statistics for chartevents.
    """

    return {

        "total_events": len(
            chartevents
        ),

        "unique_patients": (
            chartevents[
                "subject_id"
            ].nunique()
        ),

        "unique_admissions": (
            chartevents[
                "hadm_id"
            ].nunique()
        ),

        "unique_items": (
            chartevents[
                "itemid"
            ].nunique()
        )
    }


def chartevents_by_item(chartevents):
    """
    Count chart events by item ID.
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


def build_chart_catalog(
    chartevents,
    d_items
):
    """
    Create a human-readable chart-event catalog.

    Combines chartevent frequencies with
    metadata from d_items.
    """

    catalog = (
        chartevents
        .groupby("itemid")
        .agg(

            event_count=(
                "itemid",
                "size"
            ),

            unique_patients=(
                "subject_id",
                "nunique"
            ),

            unique_admissions=(
                "hadm_id",
                "nunique"
            )
        )
        .reset_index()
        .merge(

            d_items[
                [
                    "itemid",
                    "label",
                    "category",
                    "unitname",
                    "param_type"
                ]
            ],

            on="itemid",

            how="left",

            validate="many_to_one"
        )
        .sort_values(
            "event_count",
            ascending=False
        )
    )

    return catalog


# ============================================================
# LABEVENTS
# ============================================================

def load_labevents(load_dataset):
    """
    Load labevents using the central data loader.
    """

    return load_dataset("labevents")


def lab_event_summary(labevents):
    """
    Generate high-level statistics for laboratory events.
    """

    return {

        "total_lab_events": len(
            labevents
        ),

        "unique_patients": (
            labevents[
                "subject_id"
            ].nunique()
        ),

        "unique_admissions": (
            labevents[
                "hadm_id"
            ].nunique()
        ),

        "unique_lab_items": (
            labevents[
                "itemid"
            ].nunique()
        )
    }


def lab_events_by_item(labevents):
    """
    Count laboratory events by item ID.
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
# LABORATORY METADATA ENRICHMENT
# ============================================================

def enrich_labevents(
    labevents,
    d_labitems
):
    """
    Add human-readable laboratory metadata
    to every laboratory observation.
    """

    lab_dictionary = (
        d_labitems[
            [
                "itemid",
                "label",
                "fluid",
                "category"
            ]
        ]
        .drop_duplicates(
            subset=["itemid"]
        )
    )

    enriched = labevents.merge(

        lab_dictionary,

        on="itemid",

        how="left",

        validate="many_to_one"
    )

    return enriched


# ============================================================
# LAB TEST CATALOG
# ============================================================

def lab_test_catalog(
    labevents,
    d_labitems
):
    """
    Create a laboratory test catalog.

    Includes:
        - observation count
        - unique patients
        - numeric observations
        - laboratory metadata
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
                lambda x:
                    x.notna().sum()
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
# NUMERIC LABORATORY VALUES
# ============================================================

def numeric_lab_values(
    labevents
):
    """
    Return laboratory observations
    with valid numeric values.

    This function intentionally accepts either:

        labevents

    or:

        labs_with_labels

    because the original notebook passes
    the enriched laboratory table.
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
# ORIGINAL LAB VALUE SUMMARY
# ============================================================

def lab_value_summary(
    numeric_labs
):
    """
    Summarize numeric laboratory values.

    This preserves the original function expected
    by the earlier notebook.

    Statistics:
        count
        mean
        median
        standard deviation
        minimum
        maximum
    """

    group_columns = [
        "itemid"
    ]

    # Add metadata columns only if they exist.
    for column in [
        "label",
        "fluid",
        "category"
    ]:

        if column in numeric_labs.columns:

            group_columns.append(
                column
            )

    summary = (
        numeric_labs
        .groupby(
            group_columns
        )["valuenum"]
        .agg(
            [
                "count",
                "mean",
                "median",
                "std",
                "min",
                "max"
            ]
        )
        .reset_index()
    )

    return summary


# ============================================================
# COMPREHENSIVE LABORATORY TEST SUMMARY
# ============================================================

def laboratory_test_summary(
    labevents,
    d_labitems
):
    """
    Create a comprehensive summary of laboratory tests.

    Includes:
        - total observations
        - numeric observations
        - unique patients
        - abnormal observations
        - abnormal rate
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
                lambda x:
                    x.notna().sum()
            ),

            unique_patients=(
                "subject_id",
                "nunique"
            ),

            abnormal_observations=(
                "flag",
                lambda x:
                    (
                        x == "abnormal"
                    ).sum()
            )
        )
        .reset_index()
    )

    summary["abnormal_rate_pct"] = (
        summary[
            "abnormal_observations"
        ]
        / summary[
            "total_observations"
        ]
        * 100
    )

    return summary.sort_values(
        "total_observations",
        ascending=False
    )


# ============================================================
# PATIENT-LEVEL LABORATORY SUMMARY
# ============================================================

def patient_lab_summary(
    labevents
):
    """
    Create patient-level laboratory statistics.

    Only explicit 'abnormal' flags are counted
    as abnormal results.
    """

    df = numeric_lab_values(
        labevents
    )

    summary = (
        df
        .groupby("subject_id")
        .agg(

            total_lab_events=(
                "itemid",
                "count"
            ),

            unique_lab_tests=(
                "itemid",
                "nunique"
            ),

            abnormal_results=(
                "flag",
                lambda x:
                    (
                        x == "abnormal"
                    ).sum()
            )
        )
        .reset_index()
    )

    return summary


# ============================================================
# REFERENCE RANGE SUMMARY
# ============================================================

def reference_range_summary(
    labevents
):
    """
    Summarize reference-range availability.
    """

    has_lower = (
        labevents[
            "ref_range_lower"
        ].notna()
    )

    has_upper = (
        labevents[
            "ref_range_upper"
        ].notna()
    )

    has_range = (
        has_lower
        & has_upper
    )

    return {

        "with_reference_range": int(
            has_range.sum()
        ),

        "without_reference_range": int(
            (~has_range).sum()
        ),

        "reference_range_pct": (
            has_range.mean() * 100
        )
    }


# ============================================================
# LABORATORY FLAG SUMMARY
# ============================================================

def laboratory_flag_summary(
    labevents
):
    """
    Count observations by laboratory flag.
    """

    return (
        labevents[
            "flag"
        ]
        .value_counts(
            dropna=False
        )
        .rename_axis(
            "flag"
        )
        .reset_index(
            name="observation_count"
        )
    )
