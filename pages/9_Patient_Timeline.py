import pandas as pd
import streamlit as st

from src.streamlit_data import load_core_data

from src.patient_timeline import (
    patient_overview,
    admission_timeline,
    patient_event_counts
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Patient Timeline | MIMIC Analytics",
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
diagnoses_icd = data["diagnoses_icd"]
procedures_icd = data["procedures_icd"]
prescriptions = data["prescriptions"]
pharmacy = data["pharmacy"]
emar = data["emar"]
microbiology = data["microbiologyevents"]
labevents = data["labevents"]
chartevents = data["chartevents"]


# ============================================================
# HEADER
# ============================================================

st.title("🕒 Patient Timeline")

st.markdown(
    """
    Drill into a single patient: demographics, hospitalizations,
    ICU stays, and a unified event timeline for a chosen admission.
    """
)

st.divider()


# ============================================================
# PATIENT SELECTOR
# ============================================================

subject_ids = sorted(patients["subject_id"].unique().tolist())

selected_subject_id = st.selectbox(
    "Select a patient (subject_id)",
    options=subject_ids
)


# ============================================================
# PATIENT OVERVIEW
# ============================================================

overview = patient_overview(
    selected_subject_id,
    patients,
    admissions,
    icustays
)

patient_row = overview["patient"]

st.subheader("Patient Overview")

if not patient_row.empty:

    row = patient_row.iloc[0]

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Subject ID", f"{int(row['subject_id'])}")

    with col2:
        st.metric("Gender", str(row.get("gender", "—")))

    with col3:
        st.metric("Anchor Age", f"{row.get('anchor_age', '—')}")

    with col4:
        st.metric(
            "Total Admissions",
            f"{overview['total_admissions']:,}"
        )

    with col5:
        st.metric(
            "Total ICU Stays",
            f"{overview['total_icu_stays']:,}"
        )

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Admission History**")

    st.dataframe(
        overview["admissions"][
            [
                "hadm_id",
                "admittime",
                "dischtime",
                "admission_type",
                "hospital_expire_flag"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.markdown("**ICU Stay History**")

    st.dataframe(
        overview["icu_stays"][
            [
                "stay_id",
                "hadm_id",
                "first_careunit",
                "intime",
                "outtime",
                "los"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# EVENT COUNTS ACROSS ALL SOURCES
# ============================================================

st.divider()

st.subheader("Event Volume Across All Sources")

event_counts = patient_event_counts(
    selected_subject_id,
    admissions,
    icustays,
    diagnoses_icd,
    procedures_icd,
    prescriptions,
    pharmacy,
    emar,
    microbiology,
    labevents,
    chartevents
)

event_counts_df = pd.DataFrame(
    list(event_counts.items()),
    columns=["event_source", "count"]
).sort_values("count", ascending=False)

st.bar_chart(
    event_counts_df.set_index("event_source")
)

st.dataframe(
    event_counts_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# ADMISSION TIMELINE
# ============================================================

st.divider()

st.subheader("Admission Timeline")

patient_admissions = overview["admissions"]

if patient_admissions.empty:

    st.info("This patient has no recorded admissions.")

else:

    hadm_ids = patient_admissions["hadm_id"].tolist()

    selected_hadm_id = st.selectbox(
        "Select an admission (hadm_id)",
        options=hadm_ids
    )

    timeline = admission_timeline(
        subject_id=selected_subject_id,
        hadm_id=selected_hadm_id,
        admissions=admissions,
        icustays=icustays,
        diagnoses=diagnoses_icd,
        procedures=procedures_icd,
        prescriptions=prescriptions,
        pharmacy=pharmacy,
        emar=emar,
        microbiology=microbiology,
        labevents=labevents,
        chartevents=chartevents
    )

    if timeline.empty:

        st.info("No events found for this admission.")

    else:

        st.caption(f"{len(timeline):,} total events for this admission.")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Events by Type**")

            type_counts = (
                timeline["event_type"]
                .value_counts()
                .rename_axis("event_type")
                .reset_index(name="event_count")
            )

            st.bar_chart(
                type_counts.set_index("event_type")
            )

        with col2:
            st.markdown("**Events by Source**")

            source_counts = (
                timeline["source"]
                .value_counts()
                .rename_axis("source")
                .reset_index(name="event_count")
            )

            st.bar_chart(
                source_counts.set_index("source")
            )

        st.markdown("**Full Event Timeline**")

        event_type_filter = st.multiselect(
            "Filter by event type",
            options=sorted(timeline["event_type"].unique().tolist()),
            default=sorted(timeline["event_type"].unique().tolist())
        )

        filtered_timeline = timeline[
            timeline["event_type"].isin(event_type_filter)
        ]

        st.dataframe(
            filtered_timeline,
            use_container_width=True,
            hide_index=True
        )
