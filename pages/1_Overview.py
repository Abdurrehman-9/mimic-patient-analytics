import streamlit as st

from src.streamlit_data import load_core_data


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Overview | MIMIC Analytics",
    page_icon="🏥",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

data = load_core_data()

patients = data["patients"]
admissions = data["admissions"]
icustays = data["icustays"]
labevents = data["labevents"]
chartevents = data["chartevents"]
prescriptions = data["prescriptions"]
microbiology = data["microbiologyevents"]


# ============================================================
# HEADER
# ============================================================

st.title("🏥 MIMIC Patient Analytics")

st.markdown(
    """
    ### Executive Overview

    High-level view of the patient population, hospital utilization,
    ICU activity, clinical events, laboratory testing, and medications.
    """
)

st.divider()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_patients = patients["subject_id"].nunique()

total_admissions = admissions["hadm_id"].nunique()

total_icu_stays = icustays["stay_id"].nunique()

total_lab_events = len(labevents)

total_chart_events = len(chartevents)

total_prescriptions = len(prescriptions)

total_micro_events = len(microbiology)


# ============================================================
# KPI ROW 1
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Patients",
        f"{total_patients:,}"
    )

with col2:
    st.metric(
        "Admissions",
        f"{total_admissions:,}"
    )

with col3:
    st.metric(
        "ICU Stays",
        f"{total_icu_stays:,}"
    )

with col4:
    st.metric(
        "Lab Events",
        f"{total_lab_events:,}"
    )


# ============================================================
# KPI ROW 2
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Chart Events",
        f"{total_chart_events:,}"
    )

with col2:
    st.metric(
        "Prescriptions",
        f"{total_prescriptions:,}"
    )

with col3:
    st.metric(
        "Microbiology Events",
        f"{total_micro_events:,}"
    )

with col4:
    st.metric(
        "Average Age",
        f"{patients['anchor_age'].mean():.1f}"
    )


# ============================================================
# DATASET COVERAGE
# ============================================================

st.divider()

st.subheader("Dataset Coverage")

coverage = {
    "Patients": total_patients,
    "Admissions": total_admissions,
    "ICU Stays": total_icu_stays,
    "Laboratory Events": total_lab_events,
    "Clinical Chart Events": total_chart_events,
    "Prescriptions": total_prescriptions,
    "Microbiology Events": total_micro_events,
}

coverage_df = (
    __import__("pandas")
    .DataFrame(
        list(coverage.items()),
        columns=["Dataset", "Records"]
    )
)

st.bar_chart(
    coverage_df.set_index("Dataset")
)
