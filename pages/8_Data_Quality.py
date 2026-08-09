import pandas as pd
import streamlit as st

from src.streamlit_data import (
    load_core_data,
    load_dashboard_dataset
)

from src.data_quality import (
    dataset_quality_summary,
    missingness_by_column,
    key_coverage,
    duplicate_summary,
    unmatched_keys,
    invalid_datetime_count
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Data Quality | MIMIC Analytics",
    page_icon="🏥",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

data = load_core_data()

# Extra datasets not included in load_core_data(), pulled in
# so the quality report covers everything the dashboard uses.
data["emar_detail"] = load_dashboard_dataset("emar_detail")
data["ingredientevents"] = load_dashboard_dataset("ingredientevents")
data["inputevents"] = load_dashboard_dataset("inputevents")

quality_datasets = data


# ============================================================
# HEADER
# ============================================================

st.title("🔍 Data Quality")

st.markdown(
    """
    Automated checks across every dataset powering this
    dashboard: completeness, duplicates, referential integrity,
    and timestamp validity.
    """
)

st.divider()


# ============================================================
# OVERALL QUALITY SUMMARY
# ============================================================

st.subheader("Dataset Quality Summary")

summary = dataset_quality_summary(quality_datasets)

summary = summary.sort_values("rows", ascending=False)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Datasets Checked", f"{len(summary):,}")

with col2:
    st.metric(
        "Total Missing Cells",
        f"{summary['missing_cells'].sum():,}"
    )

with col3:
    st.metric(
        "Total Duplicate Rows",
        f"{summary['duplicate_rows'].sum():,}"
    )

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# PER-DATASET DRILL-DOWN
# ============================================================

st.divider()

st.subheader("Per-Dataset Drill-Down")

selected_dataset = st.selectbox(
    "Choose a dataset to inspect",
    options=sorted(quality_datasets.keys())
)

selected_df = quality_datasets[selected_dataset]

col1, col2 = st.columns(2)

with col1:

    st.markdown("**Missingness by Column**")

    missing = missingness_by_column(selected_df)

    missing_with_values = missing[missing["missing_count"] > 0]

    if missing_with_values.empty:
        st.success("No missing values in this dataset.")
    else:
        st.dataframe(
            missing_with_values,
            use_container_width=True
        )

with col2:

    st.markdown("**Duplicate Rows**")

    dup_stats = duplicate_summary(selected_df)

    st.metric(
        "Duplicate Rows",
        f"{dup_stats['duplicate_rows']:,} "
        f"({dup_stats['duplicate_pct']:.2f}%)"
    )

    st.markdown("**Key Coverage**")

    for key_column in ["subject_id", "hadm_id"]:

        if key_column in selected_df.columns:

            coverage = key_coverage(selected_df, key_column)

            st.write(
                f"`{key_column}` — "
                f"{coverage['unique_keys']:,} unique, "
                f"{coverage['missing_keys']:,} missing "
                f"(of {coverage['total_rows']:,} rows)"
            )


# ============================================================
# REFERENTIAL INTEGRITY
# ============================================================

st.divider()

st.subheader("Referential Integrity")

st.caption(
    "Checking that foreign keys in child datasets exist in "
    "their parent dataset. Zero unmatched keys is expected "
    "for a clean relational extract."
)

integrity_checks = [
    ("admissions", "patients", "subject_id"),
    ("icustays", "admissions", "hadm_id"),
    ("diagnoses_icd", "admissions", "hadm_id"),
    ("procedures_icd", "admissions", "hadm_id"),
    ("prescriptions", "admissions", "hadm_id"),
    ("labevents", "admissions", "hadm_id"),
    ("microbiologyevents", "admissions", "hadm_id"),
]

integrity_results = []

for child_name, parent_name, key_column in integrity_checks:

    child_df = quality_datasets.get(child_name)
    parent_df = quality_datasets.get(parent_name)

    if child_df is None or parent_df is None:
        continue

    result = unmatched_keys(child_df, parent_df, key_column)

    integrity_results.append({
        "child_dataset": child_name,
        "parent_dataset": parent_name,
        "key_column": key_column,
        "child_rows": result["child_dataset_rows"],
        "unique_child_keys": result["unique_child_keys"],
        "unmatched_keys": result["unmatched_keys"]
    })

integrity_df = pd.DataFrame(integrity_results)

st.dataframe(
    integrity_df,
    use_container_width=True,
    hide_index=True
)

if (integrity_df["unmatched_keys"] > 0).any():
    st.warning(
        "One or more relationships have unmatched keys — "
        "see the table above."
    )
else:
    st.success("All checked relationships are fully matched.")


# ============================================================
# DATETIME VALIDATION
# ============================================================

st.divider()

st.subheader("Timestamp Validation")

st.caption(
    "Confirming that non-null timestamp columns parse cleanly "
    "as valid datetimes."
)

datetime_checks = [
    ("admissions", "admittime"),
    ("admissions", "dischtime"),
    ("admissions", "edregtime"),
    ("admissions", "edouttime"),
    ("icustays", "intime"),
    ("icustays", "outtime"),
    ("labevents", "charttime"),
    ("microbiologyevents", "charttime"),
    ("chartevents", "charttime"),
    ("prescriptions", "starttime"),
    ("prescriptions", "stoptime"),
]

datetime_results = []

for dataset_name, column in datetime_checks:

    df = quality_datasets.get(dataset_name)

    if df is None:
        continue

    result = invalid_datetime_count(df, column)

    if result is None:
        continue

    datetime_results.append({
        "dataset": dataset_name,
        "column": column,
        "non_null_values": result["non_null_values"],
        "invalid_datetime_values": result["invalid_datetime_values"]
    })

datetime_df = pd.DataFrame(datetime_results)

st.dataframe(
    datetime_df,
    use_container_width=True,
    hide_index=True
)

if (datetime_df["invalid_datetime_values"] > 0).any():
    st.warning(
        "One or more timestamp columns contain unparseable "
        "values — see the table above."
    )
else:
    st.success("All checked timestamp columns parsed cleanly.")
