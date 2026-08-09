import pandas as pd
import streamlit as st

from src.streamlit_data import load_core_data

from src.demographics import (
    patient_overview,
    gender_distribution,
    age_distribution,
    age_groups,
    mortality_overview
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Demographics | MIMIC Analytics",
    page_icon="🏥",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

data = load_core_data()

patients = data["patients"]
admissions = data["admissions"]


# ============================================================
# HEADER
# ============================================================

st.title("👥 Patient Demographics")

st.markdown(
    """
    Population-level view of patient gender, age, and
    in-hospital mortality.
    """
)

st.divider()


# ============================================================
# KPI ROW
# ============================================================

overview = patient_overview(patients)
mortality = mortality_overview(admissions)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Patients", f"{overview['total_patients']:,}")

with col2:
    st.metric("Male", f"{overview['male_patients']:,}")

with col3:
    st.metric("Female", f"{overview['female_patients']:,}")

with col4:
    st.metric("Average Age", f"{overview['average_age']:.1f}")

with col5:
    st.metric("Median Age", f"{overview['median_age']:.1f}")


# ============================================================
# GENDER & AGE GROUP DISTRIBUTION
# ============================================================

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Gender Distribution")

    gender_df = gender_distribution(patients)

    st.bar_chart(
        gender_df.set_index("gender")
    )

    st.dataframe(
        gender_df,
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.subheader("Age Group Distribution")

    age_group_df = age_groups(patients)

    st.bar_chart(
        age_group_df.set_index("age_group")
    )

    st.dataframe(
        age_group_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# AGE DISTRIBUTION (RAW)
# ============================================================

st.divider()

st.subheader("Age Distribution")

age_df = age_distribution(patients)

st.bar_chart(
    age_df.set_index("subject_id")["anchor_age"]
)

with st.expander("View age summary statistics"):
    st.dataframe(
        age_df["anchor_age"].describe().to_frame(name="anchor_age"),
        use_container_width=True
    )


# ============================================================
# MORTALITY OVERVIEW
# ============================================================

st.divider()

st.subheader("Hospital Mortality")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Admissions",
        f"{mortality['total_admissions']:,}"
    )

with col2:
    st.metric(
        "In-Hospital Deaths",
        f"{mortality['hospital_deaths']:,}"
    )

with col3:
    st.metric(
        "Mortality Rate",
        f"{mortality['mortality_rate_pct']:.2f}%"
    )


# ============================================================
# ADMISSION-LEVEL DEMOGRAPHICS
# (insurance / marital status / race / language)
# ============================================================

st.divider()

st.subheader("Admission-Level Demographics")

st.caption(
    "These fields live on the admissions table, since a patient's "
    "insurance, marital status, and race can vary across visits."
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Insurance**")

    insurance_df = (
        admissions["insurance"]
        .value_counts(dropna=False)
        .rename_axis("insurance")
        .reset_index(name="admission_count")
    )

    st.bar_chart(
        insurance_df.set_index("insurance")
    )

with col2:
    st.markdown("**Marital Status**")

    marital_df = (
        admissions["marital_status"]
        .value_counts(dropna=False)
        .rename_axis("marital_status")
        .reset_index(name="admission_count")
    )

    st.bar_chart(
        marital_df.set_index("marital_status")
    )

col3, col4 = st.columns(2)

with col3:
    st.markdown("**Race**")

    race_df = (
        admissions["race"]
        .value_counts(dropna=False)
        .rename_axis("race")
        .reset_index(name="admission_count")
    )

    st.dataframe(
        race_df,
        use_container_width=True,
        hide_index=True
    )

with col4:
    st.markdown("**Language**")

    language_df = (
        admissions["language"]
        .value_counts(dropna=False)
        .rename_axis("language")
        .reset_index(name="admission_count")
    )

    st.dataframe(
        language_df,
        use_container_width=True,
        hide_index=True
    )
