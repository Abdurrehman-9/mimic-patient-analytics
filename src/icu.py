# ============================================================
# MIMIC PATIENT ANALYTICS
# ICU ANALYTICS MODULE
# ============================================================

import pandas as pd


# ============================================================
# ICU OVERVIEW
# ============================================================

def icu_overview(icustays):
    """
    Calculate high-level ICU statistics.
    """

    return {
        "total_icu_stays": (
            icustays["stay_id"].nunique()
        ),

        "unique_icu_patients": (
            icustays["subject_id"].nunique()
        ),

        "unique_hospital_admissions": (
            icustays["hadm_id"].nunique()
        ),

        "average_icu_los": (
            icustays["los"].mean()
        ),

        "median_icu_los": (
            icustays["los"].median()
        )
    }


# ============================================================
# ICU CARE UNIT DISTRIBUTION
# ============================================================

def care_unit_distribution(icustays):
    """
    Count ICU stays by first care unit.
    """

    return (
        icustays["first_careunit"]
        .value_counts()
        .rename_axis("care_unit")
        .reset_index(
            name="icu_stays"
        )
    )


# ============================================================
# ICU LOS SUMMARY
# ============================================================

def icu_los_summary(icustays):
    """
    Summarize ICU length of stay.
    """

    los = icustays["los"]

    return {
        "mean_los_days": los.mean(),
        "median_los_days": los.median(),
        "min_los_days": los.min(),
        "max_los_days": los.max(),
        "std_los_days": los.std()
    }


# ============================================================
# ICU STAYS PER PATIENT
# ============================================================

def icu_stays_per_patient(icustays):
    """
    Calculate ICU stays per patient.
    """

    return (
        icustays
        .groupby("subject_id")
        .size()
        .rename("icu_stay_count")
        .reset_index()
        .sort_values(
            "icu_stay_count",
            ascending=False
        )
    )


# ============================================================
# ICU STAYS PER ADMISSION
# ============================================================

def icu_stays_per_admission(icustays):
    """
    Calculate ICU stays per hospital admission.
    """

    return (
        icustays
        .groupby("hadm_id")
        .size()
        .rename("icu_stay_count")
        .reset_index()
        .sort_values(
            "icu_stay_count",
            ascending=False
        )
    )


# ============================================================
# ICU LOS VALIDATION
# ============================================================

def validate_icu_los(icustays):
    """
    Independently calculate ICU LOS from timestamps
    and compare it with the supplied LOS.
    """

    df = icustays.copy()

    df["intime"] = pd.to_datetime(
        df["intime"]
    )

    df["outtime"] = pd.to_datetime(
        df["outtime"]
    )

    df["calculated_los"] = (
        df["outtime"]
        - df["intime"]
    ).dt.total_seconds() / (
        24 * 60 * 60
    )

    df["los_difference"] = (
        df["los"]
        - df["calculated_los"]
    )

    return df
