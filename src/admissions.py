# ============================================================
# MIMIC PATIENT ANALYTICS
# ADMISSIONS MODULE
# ============================================================

import pandas as pd


# ============================================================
# ADMISSION TYPE DISTRIBUTION
# ============================================================

def admission_type_distribution(admissions):
    """
    Count admissions by admission type.
    """

    return (
        admissions["admission_type"]
        .value_counts()
        .rename_axis("admission_type")
        .reset_index(name="admission_count")
    )


# ============================================================
# ADMISSION LOCATION DISTRIBUTION
# ============================================================

def admission_location_distribution(admissions):
    """
    Count admissions by admission location.
    """

    return (
        admissions["admission_location"]
        .value_counts(dropna=False)
        .rename_axis("admission_location")
        .reset_index(
            name="admission_count"
        )
    )


# ============================================================
# DISCHARGE LOCATION DISTRIBUTION
# ============================================================

def discharge_location_distribution(admissions):
    """
    Count admissions by discharge location.
    """

    return (
        admissions["discharge_location"]
        .value_counts(dropna=False)
        .rename_axis("discharge_location")
        .reset_index(
            name="admission_count"
        )
    )


# ============================================================
# HOSPITAL LENGTH OF STAY
# ============================================================

def calculate_hospital_los(admissions):
    """
    Calculate hospital length of stay in days.
    """

    df = admissions.copy()

    df["admittime"] = pd.to_datetime(
        df["admittime"]
    )

    df["dischtime"] = pd.to_datetime(
        df["dischtime"]
    )

    df["los_days"] = (
        df["dischtime"]
        - df["admittime"]
    ).dt.total_seconds() / (
        24 * 60 * 60
    )

    return df


# ============================================================
# HOSPITAL LOS SUMMARY
# ============================================================

def hospital_los_summary(admissions):
    """
    Summarize hospital length of stay.
    """

    df = calculate_hospital_los(
        admissions
    )

    los = df["los_days"]

    return {
        "mean_los_days": los.mean(),
        "median_los_days": los.median(),
        "min_los_days": los.min(),
        "max_los_days": los.max(),
        "std_los_days": los.std()
    }


# ============================================================
# ADMISSIONS PER PATIENT
# ============================================================

def admissions_per_patient(admissions):
    """
    Calculate number of admissions per patient.
    """

    return (
        admissions
        .groupby("subject_id")
        .size()
        .rename("admission_count")
        .reset_index()
        .sort_values(
            "admission_count",
            ascending=False
        )
    )


# ============================================================
# ADMISSION OVERVIEW
# ============================================================

def admission_overview(admissions):
    """
    Generate high-level admission statistics.
    """

    return {
        "total_admissions": len(admissions),

        "unique_patients": (
            admissions["subject_id"]
            .nunique()
        ),

        "average_admissions_per_patient": (
            len(admissions)
            / admissions["subject_id"].nunique()
        )
    }
