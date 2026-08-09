import streamlit as st
import pandas as pd

from src.data_loader import load_dataset, DATASETS


# ============================================================
# STREAMLIT DATA LOADING
# ============================================================

@st.cache_data(show_spinner=False)
def load_dashboard_dataset(dataset_name):

    if dataset_name not in DATASETS:
        raise ValueError(
            f"Unknown dataset: {dataset_name}"
        )

    return load_dataset(dataset_name)


# ============================================================
# LOAD CORE DATASETS
# ============================================================

@st.cache_data(show_spinner=False)
def load_core_data():

    data = {}

    core_datasets = [
        "patients",
        "admissions",
        "icustays",
        "diagnoses_icd",
        "procedures_icd",
        "drgcodes",
        "prescriptions",
        "pharmacy",
        "emar",
        "microbiologyevents",
        "labevents",
        "chartevents",
        "transfers",
        "services",
    ]

    for dataset_name in core_datasets:
        data[dataset_name] = load_dashboard_dataset(dataset_name)

    return data
