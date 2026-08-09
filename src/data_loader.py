# ============================================================
# MIMIC PATIENT ANALYTICS
# CENTRAL DATA LOADER
# ============================================================

import pandas as pd
import streamlit as st


# ============================================================
# DATASET CONFIGURATION
# ============================================================

DATASET_FILES = {
    "admissions": "admissions.csv",
    "diagnoses_icd": "diagnoses_icd.csv",
    "drgcodes": "drgcodes.csv",
    "d_hcpcs": "d_hcpcs.csv",
    "d_icd_diagnoses": "d_icd_diagnoses.csv",
    "d_icd_procedures": "d_icd_procedures.csv",
    "d_labitems": "d_labitems.csv",
    "emar": "emar.csv",
    "emar_detail": "emar_detail.csv",
    "hcpcsevents": "hcpcsevents.csv",
    "labevents": "labevents.csv",
    "microbiologyevents": "microbiologyevents.csv",
    "omr": "omr.csv",
    "patients": "patients.csv",
    "pharmacy": "pharmacy.csv",
    "poe": "poe.csv",
    "poe_detail": "poe_detail.csv",
    "prescriptions": "prescriptions.csv",
    "procedures_icd": "procedures_icd.csv",
    "provider": "provider.csv",
    "services": "services.csv",
    "transfers": "transfers.csv",
    "caregiver": "caregiver.csv",
    "chartevents": "chartevents.csv",
    "datetimeevents": "datetimeevents.csv",
    "d_items": "d_items.csv",
    "icustays": "icustays.csv",
    "ingredientevents": "ingredientevents.csv",
    "inputevents": "inputevents.csv",
    "outputevents": "outputevents.csv",
    "procedureevents": "procedureevents.csv",
}


# ============================================================
# GITHUB CONFIGURATION
# ============================================================

# IMPORTANT:
# Replace this with your actual GitHub raw-data URL.
#
# Example:
# https://raw.githubusercontent.com/USERNAME/REPOSITORY/main/data/
#
# The final URL should point to the folder containing your CSVs.

GITHUB_RAW_BASE_URL = (
    "https://raw.githubusercontent.com/"
    "Abdurrehman-9/"
    "mimic-patient-analytics/"
    "main/data/"
)


# ============================================================
# LOAD DATASET
# ============================================================

@st.cache_data
def load_dataset(dataset_name):
    """
    Load a dataset from GitHub.

    Streamlit caches the returned DataFrame so that
    the CSV does not need to be downloaded and parsed
    every time the dashboard reruns.
    """

    if dataset_name not in DATASET_FILES:
        raise ValueError(
            f"Unknown dataset: {dataset_name}. "
            f"Available datasets: "
            f"{list(DATASET_FILES.keys())}"
        )

    filename = DATASET_FILES[dataset_name]

    url = (
        GITHUB_RAW_BASE_URL
        + filename
    )

    df = pd.read_csv(url)

    return df


# ============================================================
# LOAD MULTIPLE DATASETS
# ============================================================

@st.cache_data
def load_datasets(dataset_names):
    """
    Load multiple datasets and return them as a dictionary.

    Example:
        data = load_datasets(
            ["patients", "admissions", "icustays"]
        )

        patients = data["patients"]
    """

    data = {}

    for dataset_name in dataset_names:
        data[dataset_name] = load_dataset(
            dataset_name
        )

    return data
