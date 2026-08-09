import streamlit as st
import pandas as pd

from src.data_loader import load_dataset
from src.icu import (
    icu_summary,
    icu_careunit_distribution,
)

st.set_page_config(page_title="ICU Analysis", layout="wide")

st.title("🛏️ ICU Analysis")
st.caption("Intensive Care Unit utilization and stay characteristics")

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

icustays = load_dataset("icustays")

# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

summary = icu_summary(icustays)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total ICU Stays", summary["total_icu_stays"])
col2.metric("Unique ICU Patients", summary["unique_icu_patients"])
col3.metric(
    "Unique Admissions",
    summary["unique_hospital_admissions"]
)
col4.metric(
    "Average ICU LOS",
    f"{summary['average_icu_los']:.2f} days"
)

st.divider()

# ------------------------------------------------------------
# ICU LOS
# ------------------------------------------------------------

st.subheader("ICU Length of Stay")

col1, col2 = st.columns(2)

col1.metric(
    "Mean ICU LOS",
    f"{summary['average_icu_los']:.2f} days"
)

col2.metric(
    "Median ICU LOS",
    f"{summary['median_icu_los']:.2f} days"
)

# ------------------------------------------------------------
# CARE UNIT DISTRIBUTION
# ------------------------------------------------------------

st.subheader("ICU Care Unit Distribution")

careunit_df = icu_careunit_distribution(icustays)

if isinstance(careunit_df, pd.Series):
    careunit_df = careunit_df.reset_index()
    careunit_df.columns = ["Care Unit", "ICU Stays"]

st.bar_chart(
    careunit_df.set_index(careunit_df.columns[0])
)

with st.expander("View ICU summary"):
    st.json(summary)
