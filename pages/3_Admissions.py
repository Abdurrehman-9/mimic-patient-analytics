import pandas as pd
import streamlit as st

from src.streamlit_data import load_core_data

from src.admissions import (
    admission_type_distribution,
    admission_location_distribution,
    discharge_location_distribution,
    calculate_hospital_los,
    hospital_los_summary,
    admissions_per_patient,
    admission_overview
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Admissions | MIMIC Analytics",
    page_icon="🏥",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

data = load_core_data()

admissions = data["admissions"]


# ============================================================
# HEADER
# ============================================================

st.title("🏨 Hospital Admissions")

st.markdown(
    """
    Admission volume, type, location flow, and length of stay
    across the hospitalization dataset.
    """
)

st.divider()


# ============================================================
# KPI ROW
# ============================================================

overview = admission_overview(admissions)
los_summary = hospital_los_summary(admissions)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Admissions",
        f"{overview['total_admissions']:,}"
    )

with col2:
    st.metric(
        "Unique Patients",
        f"{overview['unique_patients']:,}"
    )

with col3:
    st.metric(
        "Avg Admissions / Patient",
        f"{overview['average_admissions_per_patient']:.2f}"
    )

with col4:
    st.metric(
        "Median LOS (days)",
        f"{los_summary['median_los_days']:.2f}"
    )


# ============================================================
# ADMISSION TYPE / LOCATION
# ============================================================

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Admission Type")

    admission_types = admission_type_distribution(admissions)

    st.bar_chart(
        admission_types.set_index("admission_type")
    )

    st.dataframe(
        admission_types,
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.subheader("Admission Location")

    admission_locations = admission_location_distribution(admissions)

    st.bar_chart(
        admission_locations.set_index("admission_location")
    )

    st.dataframe(
        admission_locations,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# DISCHARGE LOCATION
# ============================================================

st.divider()

st.subheader("Discharge Location")

discharge_locations = discharge_location_distribution(admissions)

st.bar_chart(
    discharge_locations.set_index("discharge_location")
)

st.dataframe(
    discharge_locations,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# HOSPITAL LENGTH OF STAY
# ============================================================

st.divider()

st.subheader("Hospital Length of Stay")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Mean (days)", f"{los_summary['mean_los_days']:.2f}")

with col2:
    st.metric("Median (days)", f"{los_summary['median_los_days']:.2f}")

with col3:
    st.metric("Min (days)", f"{los_summary['min_los_days']:.2f}")

with col4:
    st.metric("Max (days)", f"{los_summary['max_los_days']:.2f}")

with col5:
    st.metric("Std Dev (days)", f"{los_summary['std_los_days']:.2f}")

los_df = calculate_hospital_los(admissions)

los_bins = [0, 1, 2, 3, 5, 7, 10, 14, 21, 30, float("inf")]
los_labels = [
    "0–1", "1–2", "2–3", "3–5", "5–7",
    "7–10", "10–14", "14–21", "21–30", "30+"
]

los_df["los_bucket"] = pd.cut(
    los_df["los_days"],
    bins=los_bins,
    labels=los_labels,
    right=False
)

los_histogram = (
    los_df["los_bucket"]
    .value_counts()
    .sort_index()
    .rename_axis("los_bucket")
    .reset_index(name="admission_count")
)

st.bar_chart(
    los_histogram.set_index("los_bucket")
)

with st.expander("View admissions with longest length of stay"):
    st.dataframe(
        los_df.sort_values("los_days", ascending=False)[
            [
                "subject_id",
                "hadm_id",
                "admission_type",
                "admittime",
                "dischtime",
                "los_days"
            ]
        ].head(20),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# ADMISSION TREND OVER TIME
# ============================================================

st.divider()

st.subheader("Admission Trend Over Time")

st.caption(
    "MIMIC-IV timestamps are date-shifted per patient for "
    "de-identification, so this reflects relative admission "
    "volume over the anchor timeline rather than real calendar "
    "dates."
)

trend_df = admissions.copy()

trend_df["admittime"] = pd.to_datetime(
    trend_df["admittime"]
)

trend_df["admit_month"] = (
    trend_df["admittime"]
    .dt.to_period("M")
    .astype(str)
)

admission_trend = (
    trend_df
    .groupby("admit_month")
    .size()
    .rename("admission_count")
    .reset_index()
    .sort_values("admit_month")
)

st.line_chart(
    admission_trend.set_index("admit_month")
)

with st.expander("View monthly admission counts"):
    st.dataframe(
        admission_trend,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# ADMISSIONS PER PATIENT
# ============================================================

st.divider()

st.subheader("Admissions per Patient")

admission_counts = admissions_per_patient(admissions)

st.caption(
    f"{overview['unique_patients']:,} unique patients across "
    f"{overview['total_admissions']:,} admissions "
    f"(avg {overview['average_admissions_per_patient']:.2f} per patient)."
)

st.dataframe(
    admission_counts.head(15),
    use_container_width=True,
    hide_index=True
)
