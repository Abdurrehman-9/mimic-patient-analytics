import pandas as pd
import streamlit as st

from src.streamlit_data import load_core_data

from src.icu import (
    icu_overview,
    care_unit_distribution,
    icu_los_summary,
    icu_stays_per_patient,
    icu_stays_per_admission,
    validate_icu_los
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ICU Analysis | MIMIC Analytics",
    page_icon="🏥",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

data = load_core_data()

icustays = data["icustays"]


# ============================================================
# HEADER
# ============================================================

st.title("🛏️ ICU Analysis")

st.markdown(
    """
    Intensive care utilization: stay volume, care unit
    distribution, and length of stay.
    """
)

st.divider()


# ============================================================
# KPI ROW
# ============================================================

overview = icu_overview(icustays)
los_summary = icu_los_summary(icustays)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total ICU Stays", f"{overview['total_icu_stays']:,}")

with col2:
    st.metric(
        "Unique ICU Patients",
        f"{overview['unique_icu_patients']:,}"
    )

with col3:
    st.metric(
        "Unique Admissions",
        f"{overview['unique_hospital_admissions']:,}"
    )

with col4:
    st.metric(
        "Avg ICU LOS (days)",
        f"{overview['average_icu_los']:.2f}"
    )

with col5:
    st.metric(
        "Median ICU LOS (days)",
        f"{overview['median_icu_los']:.2f}"
    )


# ============================================================
# CARE UNIT DISTRIBUTION
# ============================================================

st.divider()

st.subheader("Care Unit Distribution")

care_units = care_unit_distribution(icustays)

st.bar_chart(
    care_units.set_index("care_unit")
)

st.dataframe(
    care_units,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# ICU LENGTH OF STAY
# ============================================================

st.divider()

st.subheader("ICU Length of Stay")

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

los_bins = [0, 0.5, 1, 2, 3, 5, 7, 10, 14, float("inf")]
los_labels = [
    "0–0.5", "0.5–1", "1–2", "2–3", "3–5",
    "5–7", "7–10", "10–14", "14+"
]

los_hist_df = icustays.copy()

los_hist_df["los_bucket"] = pd.cut(
    los_hist_df["los"],
    bins=los_bins,
    labels=los_labels,
    right=False
)

los_histogram = (
    los_hist_df["los_bucket"]
    .value_counts()
    .sort_index()
    .rename_axis("los_bucket")
    .reset_index(name="stay_count")
)

st.bar_chart(
    los_histogram.set_index("los_bucket")
)


# ============================================================
# ICU STAYS PER PATIENT / ADMISSION
# ============================================================

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("ICU Stays per Patient")

    per_patient = icu_stays_per_patient(icustays)

    st.dataframe(
        per_patient.head(15),
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.subheader("ICU Stays per Admission")

    per_admission = icu_stays_per_admission(icustays)

    st.dataframe(
        per_admission.head(15),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# ICU LOS VALIDATION (DATA QUALITY CHECK)
# ============================================================

st.divider()

st.subheader("ICU LOS Validation")

st.caption(
    "Comparing the recorded `los` field against a length of stay "
    "independently calculated from `intime` and `outtime`."
)

validated = validate_icu_los(icustays)

max_abs_difference = validated["los_difference"].abs().max()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Max Absolute Difference (days)",
        f"{max_abs_difference:.6f}"
    )

with col2:
    st.metric(
        "Stays Checked",
        f"{len(validated):,}"
    )

with st.expander("View ICU LOS validation detail"):
    st.dataframe(
        validated[
            [
                "stay_id",
                "subject_id",
                "hadm_id",
                "intime",
                "outtime",
                "los",
                "calculated_los",
                "los_difference"
            ]
        ].head(30),
        use_container_width=True,
        hide_index=True
    )
