import streamlit as st
import pandas as pd

from src.data_loader import load_dataset
from src.admissions import (
    admission_summary,
    admission_type_distribution,
    length_of_stay_summary,
)

st.set_page_config(page_title="Admissions", layout="wide")

st.title("🏥 Admissions Analysis")
st.caption("Hospital admission patterns and length of stay")

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

admissions = load_dataset("admissions")

# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

summary = admission_summary(admissions)

col1, col2, col3 = st.columns(3)

col1.metric("Total Admissions", summary["total_admissions"])
col2.metric("Unique Patients", summary["unique_patients"])
col3.metric(
    "Admissions / Patient",
    f"{summary['average_admissions_per_patient']:.2f}"
)

st.divider()

# ------------------------------------------------------------
# ADMISSION TYPES
# ------------------------------------------------------------

st.subheader("Admission Type Distribution")

type_df = admission_type_distribution(admissions)

if isinstance(type_df, pd.Series):
    type_df = type_df.reset_index()
    type_df.columns = ["Admission Type", "Admissions"]

st.bar_chart(
    type_df.set_index(type_df.columns[0])
)

# ------------------------------------------------------------
# LENGTH OF STAY
# ------------------------------------------------------------

st.subheader("Length of Stay")

los = length_of_stay_summary(admissions)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Mean LOS", f"{los['mean_los_days']:.2f} days")
col2.metric("Median LOS", f"{los['median_los_days']:.2f} days")
col3.metric("Minimum LOS", f"{los['min_los_days']:.2f} days")
col4.metric("Maximum LOS", f"{los['max_los_days']:.2f} days")

with st.expander("View LOS statistics"):
    st.json(los)
