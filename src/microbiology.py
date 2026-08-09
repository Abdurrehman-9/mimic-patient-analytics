# ============================================================
# MIMIC PATIENT ANALYTICS
# MICROBIOLOGY ANALYTICS
# ============================================================

import pandas as pd


# ============================================================
# LOADER
# ============================================================

def load_microbiology(load_dataset):
    """Load microbiology events."""
    return load_dataset(
        "microbiologyevents"
    )


# ============================================================
# SUMMARY
# ============================================================

def microbiology_summary(
    microbiology
):
    """
    High-level microbiology statistics.
    """

    return {
        "total_microbiology_events": len(
            microbiology
        ),

        "unique_patients": microbiology[
            "subject_id"
        ].nunique(),

        "unique_admissions": microbiology[
            "hadm_id"
        ].nunique(),

        "unique_specimens": microbiology[
            "micro_specimen_id"
        ].nunique(),

        "unique_tests": microbiology[
            "test_name"
        ].nunique()
    }


# ============================================================
# SPECIMENS
# ============================================================

def microbiology_by_specimen(
    microbiology
):
    """
    Frequency of microbiology specimen types.
    """

    return (
        microbiology
        .groupby(
            "spec_type_desc",
            dropna=False
        )
        .size()
        .reset_index(
            name="event_count"
        )
        .sort_values(
            "event_count",
            ascending=False
        )
    )


# ============================================================
# TESTS
# ============================================================

def microbiology_by_test(
    microbiology
):
    """
    Rank microbiology tests by frequency.
    """

    result = (
        microbiology
        .groupby(
            "test_name",
            dropna=False
        )
        .agg(
            test_count=(
                "test_name",
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
        .sort_values(
            "test_count",
            ascending=False
        )
    )

    return result


# ============================================================
# ORGANISMS
# ============================================================

def organism_summary(
    microbiology
):
    """
    Summarize identified organisms.
    """

    organisms = microbiology[
        microbiology["org_name"].notna()
        & (
            microbiology["org_name"]
            .astype(str)
            .str.strip()
            != ""
        )
    ].copy()

    return (
        organisms
        .groupby(
            "org_name",
            dropna=False
        )
        .agg(
            occurrences=(
                "org_name",
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
        .sort_values(
            "occurrences",
            ascending=False
        )
    )


# ============================================================
# INTERPRETATIONS
# ============================================================

def microbiology_interpretations(
    microbiology
):
    """
    Summarize microbiology interpretation values.
    """

    return (
        microbiology
        .groupby(
            "interpretation",
            dropna=False
        )
        .size()
        .reset_index(
            name="event_count"
        )
        .sort_values(
            "event_count",
            ascending=False
        )
    )


# ============================================================
# PATIENT-LEVEL MICROBIOLOGY
# ============================================================

def microbiology_by_patient(
    microbiology
):
    """
    Summarize microbiology activity per patient.
    """

    return (
        microbiology
        .groupby("subject_id")
        .agg(
            microbiology_events=(
                "microevent_id",
                "count"
            ),

            unique_tests=(
                "test_name",
                "nunique"
            ),

            unique_specimens=(
                "micro_specimen_id",
                "nunique"
            ),

            unique_organisms=(
                "org_name",
                "nunique"
            )
        )
        .reset_index()
        .sort_values(
            "microbiology_events",
            ascending=False
        )
    )
