import pandas as pd
import streamlit as st

from src.streamlit_data import (
    load_core_data,
    load_dashboard_dataset
)

from src.diagnoses import (
    diagnosis_summary,
    diagnoses_by_code,
    primary_diagnosis_summary,
    procedure_summary,
    procedures_by_code,
    primary_procedures
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Diagnoses | MIMIC Analytics",
    page_icon="🏥",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

data = load_core_data()

diagnoses_icd = data["diagnoses_icd"]
procedures_icd = data["procedures_icd"]
drgcodes = data["drgcodes"]

# Not part of load_core_data(), loaded separately
# (still cached via st.cache_data).
d_icd_diagnoses = load_dashboard_dataset("d_icd_diagnoses")
d_icd_procedures = load_dashboard_dataset("d_icd_procedures")


# ============================================================
# HEADER
# ============================================================

st.title("🩻 Diagnoses & Procedures")

st.markdown(
    """
    ICD-coded diagnoses and procedures, primary-diagnosis
    breakdowns, and DRG severity/mortality classification.
    """
)

st.divider()


# ============================================================
# TABS
# ============================================================

diagnoses_tab, procedures_tab, drg_tab = st.tabs(
    ["🩺 Diagnoses", "🔧 Procedures", "🏷️ DRG Codes"]
)


# ============================================================
# DIAGNOSES TAB
# ============================================================

with diagnoses_tab:

    diag_summary = diagnosis_summary(diagnoses_icd)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Diagnosis Records",
            f"{diag_summary['total_diagnosis_records']:,}"
        )

    with col2:
        st.metric(
            "Unique Patients",
            f"{diag_summary['unique_patients']:,}"
        )

    with col3:
        st.metric(
            "Unique Admissions",
            f"{diag_summary['unique_admissions']:,}"
        )

    with col4:
        st.metric(
            "Unique Diagnosis Codes",
            f"{diag_summary['unique_diagnosis_codes']:,}"
        )

    st.subheader("Most Frequent Diagnoses (All Positions)")

    top_diagnoses = diagnoses_by_code(
        diagnoses_icd,
        d_icd_diagnoses
    ).head(20)

    st.bar_chart(
        top_diagnoses.set_index("long_title")["diagnosis_count"]
    )

    st.dataframe(
        top_diagnoses,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Most Frequent Primary Diagnoses")

    st.caption(
        "Primary diagnosis is defined as `seq_num == 1` for "
        "the admission."
    )

    top_primary = primary_diagnosis_summary(
        diagnoses_icd,
        d_icd_diagnoses
    ).head(20)

    st.bar_chart(
        top_primary.set_index("long_title")["admissions"]
    )

    st.dataframe(
        top_primary,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PROCEDURES TAB
# ============================================================

with procedures_tab:

    proc_summary = procedure_summary(procedures_icd)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Procedure Records",
            f"{proc_summary['total_procedure_records']:,}"
        )

    with col2:
        st.metric(
            "Unique Patients",
            f"{proc_summary['unique_patients']:,}"
        )

    with col3:
        st.metric(
            "Unique Admissions",
            f"{proc_summary['unique_admissions']:,}"
        )

    with col4:
        st.metric(
            "Unique Procedure Codes",
            f"{proc_summary['unique_procedure_codes']:,}"
        )

    st.subheader("Most Frequent Procedures")

    top_procedures = procedures_by_code(
        procedures_icd,
        d_icd_procedures
    ).head(20)

    st.bar_chart(
        top_procedures.set_index("long_title")["procedure_count"]
    )

    st.dataframe(
        top_procedures,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Primary Procedures")

    st.caption(
        "Primary procedure is defined as `seq_num == 1` for "
        "the admission."
    )

    primary_proc = primary_procedures(
        procedures_icd,
        d_icd_procedures
    )

    primary_proc_summary = (
        primary_proc
        .groupby("long_title", dropna=False)
        .size()
        .rename("admission_count")
        .reset_index()
        .sort_values("admission_count", ascending=False)
        .head(20)
    )

    st.dataframe(
        primary_proc_summary,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# DRG CODES TAB
# ============================================================

with drg_tab:

    st.subheader("DRG Severity & Mortality")

    st.caption(
        "Diagnosis-Related Group (DRG) codes classify admissions "
        "by clinical complexity. Severity and mortality scores "
        "range from 0 (minor) to higher values (major/extreme)."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total DRG Records", f"{len(drgcodes):,}")

    with col2:
        st.metric(
            "Unique Admissions",
            f"{drgcodes['hadm_id'].nunique():,}"
        )

    with col3:
        st.metric(
            "Unique DRG Codes",
            f"{drgcodes['drg_code'].nunique():,}"
        )

    st.subheader("Most Frequent DRG Descriptions")

    top_drg = (
        drgcodes
        .groupby("description", dropna=False)
        .size()
        .rename("admission_count")
        .reset_index()
        .sort_values("admission_count", ascending=False)
        .head(20)
    )

    st.bar_chart(
        top_drg.set_index("description")
    )

    st.dataframe(
        top_drg,
        use_container_width=True,
        hide_index=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Severity Distribution")

        severity_df = (
            drgcodes["drg_severity"]
            .dropna()
            .value_counts()
            .sort_index()
            .rename_axis("drg_severity")
            .reset_index(name="admission_count")
        )

        st.bar_chart(
            severity_df.set_index("drg_severity")
        )

    with col2:
        st.subheader("Mortality Score Distribution")

        mortality_df = (
            drgcodes["drg_mortality"]
            .dropna()
            .value_counts()
            .sort_index()
            .rename_axis("drg_mortality")
            .reset_index(name="admission_count")
        )

        st.bar_chart(
            mortality_df.set_index("drg_mortality")
        )
