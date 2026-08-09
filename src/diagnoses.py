# ============================================================
# MIMIC PATIENT ANALYTICS
# DIAGNOSES & PROCEDURES ANALYTICS
# ============================================================

import pandas as pd


# ============================================================
# DIAGNOSES
# ============================================================

def load_diagnoses(load_dataset):
    """
    Load ICD diagnosis records.
    """
    return load_dataset("diagnoses_icd")


def enrich_diagnoses(
    diagnoses_icd,
    d_icd_diagnoses
):
    """
    Add human-readable ICD diagnosis descriptions.
    """

    dictionary = (
        d_icd_diagnoses[
            [
                "icd_code",
                "icd_version",
                "long_title"
            ]
        ]
        .drop_duplicates(
            subset=[
                "icd_code",
                "icd_version"
            ]
        )
    )

    enriched = diagnoses_icd.merge(
        dictionary,
        on=[
            "icd_code",
            "icd_version"
        ],
        how="left",
        validate="many_to_one"
    )

    return enriched


def diagnosis_summary(
    diagnoses_icd
):
    """
    High-level diagnosis statistics.
    """

    return {
        "total_diagnosis_records": len(
            diagnoses_icd
        ),

        "unique_patients": (
            diagnoses_icd[
                "subject_id"
            ].nunique()
        ),

        "unique_admissions": (
            diagnoses_icd[
                "hadm_id"
            ].nunique()
        ),

        "unique_diagnosis_codes": (
            diagnoses_icd[
                "icd_code"
            ].nunique()
        )
    }


def diagnoses_by_code(
    diagnoses_icd,
    d_icd_diagnoses
):
    """
    Rank diagnoses by frequency.
    """

    enriched = enrich_diagnoses(
        diagnoses_icd,
        d_icd_diagnoses
    )

    result = (
        enriched
        .groupby(
            [
                "icd_code",
                "icd_version",
                "long_title"
            ],
            dropna=False
        )
        .agg(
            diagnosis_count=(
                "icd_code",
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
            "diagnosis_count",
            ascending=False
        )
    )

    return result


def primary_diagnoses(
    diagnoses_icd,
    d_icd_diagnoses
):
    """
    Extract primary diagnoses using seq_num = 1.
    """

    primary = diagnoses_icd[
        diagnoses_icd["seq_num"] == 1
    ].copy()

    return enrich_diagnoses(
        primary,
        d_icd_diagnoses
    )


def primary_diagnosis_summary(
    diagnoses_icd,
    d_icd_diagnoses
):
    """
    Summarize primary diagnoses.
    """

    primary = primary_diagnoses(
        diagnoses_icd,
        d_icd_diagnoses
    )

    result = (
        primary
        .groupby(
            [
                "icd_code",
                "icd_version",
                "long_title"
            ],
            dropna=False
        )
        .agg(
            admissions=(
                "hadm_id",
                "nunique"
            ),

            patients=(
                "subject_id",
                "nunique"
            )
        )
        .reset_index()
        .sort_values(
            "admissions",
            ascending=False
        )
    )

    return result


# ============================================================
# PROCEDURES
# ============================================================

def load_procedures(load_dataset):
    """
    Load ICD procedure records.
    """

    return load_dataset(
        "procedures_icd"
    )


def enrich_procedures(
    procedures_icd,
    d_icd_procedures
):
    """
    Add human-readable procedure descriptions.
    """

    dictionary = (
        d_icd_procedures[
            [
                "icd_code",
                "icd_version",
                "long_title"
            ]
        ]
        .drop_duplicates(
            subset=[
                "icd_code",
                "icd_version"
            ]
        )
    )

    enriched = procedures_icd.merge(
        dictionary,
        on=[
            "icd_code",
            "icd_version"
        ],
        how="left",
        validate="many_to_one"
    )

    return enriched


def procedure_summary(
    procedures_icd
):
    """
    High-level procedure statistics.
    """

    return {
        "total_procedure_records": len(
            procedures_icd
        ),

        "unique_patients": (
            procedures_icd[
                "subject_id"
            ].nunique()
        ),

        "unique_admissions": (
            procedures_icd[
                "hadm_id"
            ].nunique()
        ),

        "unique_procedure_codes": (
            procedures_icd[
                "icd_code"
            ].nunique()
        )
    }


def procedures_by_code(
    procedures_icd,
    d_icd_procedures
):
    """
    Rank procedures by frequency.
    """

    enriched = enrich_procedures(
        procedures_icd,
        d_icd_procedures
    )

    result = (
        enriched
        .groupby(
            [
                "icd_code",
                "icd_version",
                "long_title"
            ],
            dropna=False
        )
        .agg(
            procedure_count=(
                "icd_code",
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
            "procedure_count",
            ascending=False
        )
    )

    return result


def primary_procedures(
    procedures_icd,
    d_icd_procedures
):
    """
    Extract primary procedures using seq_num = 1.
    """

    primary = procedures_icd[
        procedures_icd["seq_num"] == 1
    ].copy()

    return enrich_procedures(
        primary,
        d_icd_procedures
    )
