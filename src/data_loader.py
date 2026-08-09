# ============================================================
# MIMIC PATIENT ANALYTICS
# CENTRAL GITHUB DATA LOADER
# ============================================================

import pandas as pd
from functools import lru_cache


# ============================================================
# GITHUB DATA SOURCE
# ============================================================

GITHUB_RAW_BASE = (
    "https://raw.githubusercontent.com/"
    "Abdurrehman-9/"
    "mimic-patient-analytics/"
    "main/data/"
)


# ============================================================
# DATASET REGISTRY
# ============================================================

DATASETS = {

    # --------------------------------------------------------
    # CORE PATIENT / HOSPITAL DATA
    # --------------------------------------------------------

    "patients": "patients.csv",
    "admissions": "admissions.csv",
    "transfers": "transfers.csv",
    "services": "services.csv",
    "icustays": "icustays.csv",

    # --------------------------------------------------------
    # CLINICAL EVENTS
    # --------------------------------------------------------

    "chartevents": "chartevents.csv",
    "datetimeevents": "datetimeevents.csv",
    "outputevents": "outputevents.csv",
    "inputevents": "inputevents.csv",
    "ingredientevents": "ingredientevents.csv",
    "procedureevents": "procedureevents.csv",

    # --------------------------------------------------------
    # LABS / MICROBIOLOGY
    # --------------------------------------------------------

    "labevents": "labevents.csv",
    "microbiologyevents": "microbiologyevents.csv",

    # --------------------------------------------------------
    # MEDICATIONS
    # --------------------------------------------------------

    "pharmacy": "pharmacy.csv",
    "prescriptions": "prescriptions.csv",
    "emar": "emar.csv",
    "emar_detail": "emar_detail.csv",

    # --------------------------------------------------------
    # DIAGNOSES / PROCEDURES
    # --------------------------------------------------------

    "diagnoses_icd": "diagnoses_icd.csv",
    "procedures_icd": "procedures_icd.csv",
    "drgcodes": "drgcodes.csv",
    "hcpcsevents": "hcpcsevents.csv",

    # --------------------------------------------------------
    # REFERENCE / DICTIONARY TABLES
    # --------------------------------------------------------

    "d_items": "d_items.csv",
    "d_labitems": "d_labitems.csv",
    "d_icd_diagnoses": "d_icd_diagnoses.csv",
    "d_icd_procedures": "d_icd_procedures.csv",
    "d_hcpcs": "d_hcpcs.csv",

    # --------------------------------------------------------
    # ADMINISTRATIVE
    # --------------------------------------------------------

    "caregiver": "caregiver.csv",
    "provider": "provider.csv",
    "poe": "poe.csv",
    "poe_detail": "poe_detail.csv",
    "omr": "omr.csv",
}


# ============================================================
# BASIC DATA LOADING
# ============================================================

def load_csv_from_github(filename):
    """
    Load a CSV file directly from GitHub.

    This preserves the original loader used during
    the initial exploratory phase.
    """

    url = GITHUB_RAW_BASE + filename

    print(f"Loading: {filename}")

    df = pd.read_csv(url)

    print(
        f" Shape: "
        f"{df.shape[0]:,} rows × "
        f"{df.shape[1]} columns"
    )

    return df


# ============================================================
# CACHED DATASET LOADER
# ============================================================

@lru_cache(maxsize=None)
def load_dataset(dataset_name):
    """
    Load a registered dataset from GitHub.

    The result is cached in the current Python session,
    preventing repeated downloads.
    """

    if dataset_name not in DATASETS:

        raise ValueError(
            f"Unknown dataset: {dataset_name}. "
            f"Available datasets: "
            f"{list(DATASETS.keys())}"
        )

    filename = DATASETS[dataset_name]

    url = GITHUB_RAW_BASE + filename

    print(f"Loading {dataset_name}...")

    df = pd.read_csv(url)

    print(
        f"Loaded {dataset_name}: "
        f"{df.shape[0]:,} rows × "
        f"{df.shape[1]} columns"
    )

    return df


# ============================================================
# LOAD MULTIPLE DATASETS
# ============================================================

def load_datasets(dataset_names):
    """
    Load multiple registered datasets.

    Returns a dictionary:

        {
            "patients": DataFrame,
            "admissions": DataFrame,
            ...
        }
    """

    data = {}

    for dataset_name in dataset_names:

        data[dataset_name] = load_dataset(
            dataset_name
        )

    return data


# ============================================================
# DATASET PROFILING
# ============================================================

def profile_dataset(df, name):
    """
    Create a basic profile for a dataset.

    This function is intentionally kept here because
    the earlier Colab notebook imports it directly
    from src.data_loader.
    """

    profile = {

        "dataset": name,

        "rows": df.shape[0],

        "columns": df.shape[1],

        "missing_cells": int(
            df.isna().sum().sum()
        ),

        "duplicate_rows": int(
            df.duplicated().sum()
        ),
    }

    return profile
