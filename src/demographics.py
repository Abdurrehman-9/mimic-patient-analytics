# ============================================================
# MIMIC PATIENT ANALYTICS
# DEMOGRAPHICS MODULE
# ============================================================

import pandas as pd


# ============================================================
# PATIENT OVERVIEW
# ============================================================

def patient_overview(patients):
    """
    Calculate high-level patient demographics.
    """

    overview = {
        "total_patients": patients["subject_id"].nunique(),

        "male_patients": (
            patients["gender"]
            .eq("M")
            .sum()
        ),

        "female_patients": (
            patients["gender"]
            .eq("F")
            .sum()
        ),

        "average_age": (
            patients["anchor_age"]
            .mean()
        ),

        "median_age": (
            patients["anchor_age"]
            .median()
        )
    }

    return overview


# ============================================================
# GENDER DISTRIBUTION
# ============================================================

def gender_distribution(patients):
    """
    Return patient counts by gender.
    """

    return (
        patients["gender"]
        .value_counts()
        .rename_axis("gender")
        .reset_index(name="patient_count")
    )


# ============================================================
# AGE DISTRIBUTION
# ============================================================

def age_distribution(patients):
    """
    Return age information for distribution analysis.
    """

    return patients[
        [
            "subject_id",
            "anchor_age"
        ]
    ].copy()


# ============================================================
# AGE GROUPS
# ============================================================

def age_groups(patients):
    """
    Categorize patients into clinically interpretable
    age groups.
    """

    df = patients[
        [
            "subject_id",
            "anchor_age"
        ]
    ].copy()

    bins = [
        0,
        18,
        30,
        45,
        60,
        75,
        float("inf")
    ]

    labels = [
        "<18",
        "18–29",
        "30–44",
        "45–59",
        "60–74",
        "75+"
    ]

    df["age_group"] = pd.cut(
        df["anchor_age"],
        bins=bins,
        labels=labels,
        right=False
    )

    return (
        df["age_group"]
        .value_counts()
        .sort_index()
        .rename_axis("age_group")
        .reset_index(
            name="patient_count"
        )
    )


# ============================================================
# MORTALITY OVERVIEW
# ============================================================

def mortality_overview(admissions):
    """
    Calculate hospital mortality based on
    hospital_expire_flag.
    """

    total_admissions = len(admissions)

    deaths = (
        admissions["hospital_expire_flag"]
        .eq(1)
        .sum()
    )

    mortality_rate = (
        deaths / total_admissions * 100
        if total_admissions > 0
        else 0
    )

    return {
        "total_admissions": total_admissions,
        "hospital_deaths": int(deaths),
        "mortality_rate_pct": mortality_rate
    }
