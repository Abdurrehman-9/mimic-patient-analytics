import streamlit as st
import pandas as pd

from src.data_loader import load_dataset
from src.demographics import (
    demographic_summary,
    gender_distribution,
    age_distribution,
)

st.set_page_config(page_title="Demographics", layout="wide")

st.title("👥 Patient Demographics")
st.caption("Demographic profile of the MIMIC-IV patient cohort")

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

patients = load_dataset("patients")

# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

summary = demographic_summary(patients)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Patients", summary["total_patients"])
col2.metric("Male Patients", summary["male_patients"])
col3.metric("Female Patients", summary["female_patients"])
col4.metric("Average Age", f"{summary['average_age']:.1f}")

st.divider()

# ------------------------------------------------------------
# GENDER
# ------------------------------------------------------------

st.subheader("Gender Distribution")

gender_df = gender_distribution(patients)

if isinstance(gender_df, pd.Series):
    gender_df = gender_df.reset_index()
    gender_df.columns = ["Gender", "Patients"]

st.bar_chart(
    gender_df.set_index(gender_df.columns[0])
)

# ------------------------------------------------------------
# AGE
# ------------------------------------------------------------

st.subheader("Age Distribution")

age_df = age_distribution(patients)

if isinstance(age_df, pd.Series):
    age_df = age_df.reset_index()
    age_df.columns = ["Age", "Patients"]

st.bar_chart(
    age_df.set_index(age_df.columns[0])
)

# ------------------------------------------------------------
# RAW SUMMARY
# ------------------------------------------------------------

with st.expander("View demographic summary"):
    st.json(summary)
