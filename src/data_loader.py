# ============================================================
# MIMIC PATIENT ANALYTICS
# DATA LOADING MODULE
# ============================================================

import pandas as pd


# ============================================================
# GITHUB CONFIGURATION
# ============================================================

GITHUB_RAW_BASE = (
    "https://raw.githubusercontent.com/"
    "Abdurrehman-9/mimic-patient-analytics/"
    "main/data/"
)


# ============================================================
# DATASET REGISTRY
# ============================================================

DATASETS = {

    # Core patient / hospital data
    "patients": "patients.csv",
    "admissions": "admissions.csv",
    "transfers": "transfers.csv",
    "services": "services.csv",
    "icustays": "icustays.csv",

    # Clinical events
    "chartevents": "chartevents.csv",
    "datetimeevents": "datetimeevents.csv",
    "outputevents": "outputevents.csv",
    "inputevents": "inputevents.csv",
    "ingredientevents": "ingredientevents.csv",
    "procedureevents": "procedureevents.csv",

    # Laboratory / microbiology
    "labevents": "labevents.csv",
    "microbiologyevents": "microbiologyevents.csv",

    # Medications
    "pharmacy": "pharmacy.csv",
    "prescriptions": "prescriptions.csv",
    "emar": "emar.csv",
    "emar_detail": "emar_detail.csv",

    # Diagnoses / procedures
    "diagnoses_icd": "diagnoses_icd.csv",
    "procedures_icd": "procedures_icd.csv",
    "drgcodes": "drgcodes.csv",
    "hcpcsevents": "hcpcsevents.csv",

    # Reference tables
    "d_items": "d_items.csv",
    "d_labitems": "d_labitems.csv",
    "d_icd_diagnoses": "d_icd_diagnoses.csv",
    "d_icd_procedures": "d_icd_procedures.csv",
    "d_hcpcs": "d_hcpcs.csv",

    # Administrative
    "caregiver": "caregiver.csv",
    "provider": "provider.csv",
    "poe": "poe.csv",
    "poe_detail": "poe_detail.csv",
    "omr": "omr.csv",
}


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset(dataset_name):
    """
    Load a registered dataset directly from GitHub.

    Parameters
    ----------
    dataset_name : str
        Dataset name from DATASETS.

    Returns
    -------
    pandas.DataFrame
        Loaded dataset.
    """

    if dataset_name not in DATASETS:

        available = ", ".join(DATASETS.keys())

        raise ValueError(
            f"Unknown dataset '{dataset_name}'. "
            f"Available datasets: {available}"
        )

    filename = DATASETS[dataset_name]

    url = GITHUB_RAW_BASE + filename

    df = pd.read_csv(url)

    return df


# ============================================================
# DATASET PROFILE
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
