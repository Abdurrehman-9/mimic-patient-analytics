import pandas as pd
import streamlit as st

from src.streamlit_data import (
    load_core_data,
    load_dashboard_dataset
)

from src.clinical_events import (
    chartevent_summary,
    chartevents_by_item,
    build_chart_catalog,
    lab_event_summary,
    lab_events_by_item,
    lab_test_catalog,
    laboratory_test_summary,
    patient_lab_summary,
    reference_range_summary,
    laboratory_flag_summary
)

from src.microbiology import (
    microbiology_summary,
    microbiology_by_specimen,
    microbiology_by_test,
    organism_summary,
    microbiology_interpretations
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Clinical Events | MIMIC Analytics",
    page_icon="🏥",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

data = load_core_data()

chartevents = data["chartevents"]
labevents = data["labevents"]
microbiology = data["microbiologyevents"]
prescriptions = data["prescriptions"]

# Reference/dictionary tables are not part of load_core_data(),
# so they are loaded separately (still cached via st.cache_data).
d_items = load_dashboard_dataset("d_items")
d_labitems = load_dashboard_dataset("d_labitems")


# ============================================================
# HEADER
# ============================================================

st.title("📈 Clinical Events & Laboratory Testing")

st.markdown(
    """
    Bedside chart events and laboratory testing activity,
    including abnormal-result and reference-range coverage.
    """
)

st.divider()


# ============================================================
# TABS
# ============================================================

chart_tab, lab_tab, micro_tab, compare_tab = st.tabs(
    [
        "🩺 Chart Events",
        "🧪 Laboratory Events",
        "🦠 Microbiology",
        "📊 Event Comparison"
    ]
)


# ============================================================
# CHART EVENTS TAB
# ============================================================

with chart_tab:

    chart_summary = chartevent_summary(chartevents)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Chart Events",
            f"{chart_summary['total_events']:,}"
        )

    with col2:
        st.metric(
            "Unique Patients",
            f"{chart_summary['unique_patients']:,}"
        )

    with col3:
        st.metric(
            "Unique Admissions",
            f"{chart_summary['unique_admissions']:,}"
        )

    with col4:
        st.metric(
            "Unique Chart Items",
            f"{chart_summary['unique_items']:,}"
        )

    st.subheader("Most Frequent Chart Items")

    if d_items is not None and not d_items.empty:

        chart_catalog = build_chart_catalog(
            chartevents,
            d_items
        )

        top_chart_items = chart_catalog.head(20)

        st.bar_chart(
            top_chart_items.set_index("label")["event_count"]
        )

        st.dataframe(
            top_chart_items[
                [
                    "itemid",
                    "label",
                    "category",
                    "unitname",
                    "event_count",
                    "unique_patients",
                    "unique_admissions"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        top_chart_items = chartevents_by_item(chartevents).head(20)

        st.bar_chart(
            top_chart_items.set_index("itemid")["event_count"]
        )

        st.dataframe(
            top_chart_items,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# LABORATORY EVENTS TAB
# ============================================================

with lab_tab:

    lab_summary = lab_event_summary(labevents)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Lab Events",
            f"{lab_summary['total_lab_events']:,}"
        )

    with col2:
        st.metric(
            "Unique Patients",
            f"{lab_summary['unique_patients']:,}"
        )

    with col3:
        st.metric(
            "Unique Admissions",
            f"{lab_summary['unique_admissions']:,}"
        )

    with col4:
        st.metric(
            "Unique Lab Tests",
            f"{lab_summary['unique_lab_items']:,}"
        )

    # --------------------------------------------------------
    # Most frequent lab tests
    # --------------------------------------------------------

    st.subheader("Most Frequent Laboratory Tests")

    catalog = lab_test_catalog(labevents, d_labitems)

    top_lab_tests = catalog.head(20)

    st.bar_chart(
        top_lab_tests.set_index("label")["observation_count"]
    )

    st.dataframe(
        top_lab_tests,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # Abnormal rate by test
    # --------------------------------------------------------

    st.divider()

    st.subheader("Abnormal Result Rate by Test")

    test_summary = laboratory_test_summary(labevents, d_labitems)

    most_tested = test_summary.head(20)

    st.dataframe(
        most_tested[
            [
                "itemid",
                "label",
                "fluid",
                "category",
                "total_observations",
                "numeric_observations",
                "abnormal_observations",
                "abnormal_rate_pct"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # Reference range & flag coverage
    # --------------------------------------------------------

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Reference Range Coverage**")

        range_summary = reference_range_summary(labevents)

        st.metric(
            "With Reference Range",
            f"{range_summary['with_reference_range']:,} "
            f"({range_summary['reference_range_pct']:.1f}%)"
        )

        st.metric(
            "Without Reference Range",
            f"{range_summary['without_reference_range']:,}"
        )

    with col2:
        st.markdown("**Abnormal Flag Summary**")

        flag_summary = laboratory_flag_summary(labevents)

        st.dataframe(
            flag_summary,
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------------
    # Patient-level lab activity
    # --------------------------------------------------------

    st.divider()

    st.subheader("Patient-Level Lab Activity")

    patient_summary = patient_lab_summary(labevents)

    st.dataframe(
        patient_summary.sort_values(
            "total_lab_events",
            ascending=False
        ).head(15),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# MICROBIOLOGY TAB
# ============================================================

with micro_tab:

    micro_summary = microbiology_summary(microbiology)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Total Events",
            f"{micro_summary['total_microbiology_events']:,}"
        )

    with col2:
        st.metric(
            "Unique Patients",
            f"{micro_summary['unique_patients']:,}"
        )

    with col3:
        st.metric(
            "Unique Admissions",
            f"{micro_summary['unique_admissions']:,}"
        )

    with col4:
        st.metric(
            "Unique Specimens",
            f"{micro_summary['unique_specimens']:,}"
        )

    with col5:
        st.metric(
            "Unique Tests",
            f"{micro_summary['unique_tests']:,}"
        )

    # --------------------------------------------------------
    # Top tests and specimens
    # --------------------------------------------------------

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Microbiology Tests")

        top_tests = microbiology_by_test(microbiology).head(15)

        st.bar_chart(
            top_tests.set_index("test_name")["test_count"]
        )

        st.dataframe(
            top_tests,
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.subheader("Top Specimen Types")

        top_specimens = microbiology_by_specimen(
            microbiology
        ).head(15)

        st.bar_chart(
            top_specimens.set_index("spec_type_desc")["event_count"]
        )

        st.dataframe(
            top_specimens,
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------------
    # Top organisms
    # --------------------------------------------------------

    st.divider()

    st.subheader("Top Identified Organisms")

    top_organisms = organism_summary(microbiology).head(15)

    st.bar_chart(
        top_organisms.set_index("org_name")["occurrences"]
    )

    st.dataframe(
        top_organisms,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # Susceptibility interpretations
    # --------------------------------------------------------

    st.divider()

    st.subheader("Susceptibility Interpretations")

    st.caption(
        "S = Susceptible, R = Resistant, I = Intermediate, "
        "blank = not applicable (no organism isolated or "
        "susceptibility not tested)."
    )

    interpretations = microbiology_interpretations(microbiology)

    st.dataframe(
        interpretations,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# EVENT COMPARISON TAB
# ============================================================

with compare_tab:

    st.subheader("Clinical Event Volume Across Sources")

    st.caption(
        "Row counts, unique patients, and unique admissions "
        "covered by each clinical data source, side by side."
    )

    comparison_rows = [
        {
            "source": "Chart Events",
            "rows": len(chartevents),
            "unique_patients": chartevents["subject_id"].nunique(),
            "unique_admissions": chartevents["hadm_id"].nunique()
        },
        {
            "source": "Lab Events",
            "rows": len(labevents),
            "unique_patients": labevents["subject_id"].nunique(),
            "unique_admissions": labevents["hadm_id"].nunique()
        },
        {
            "source": "Microbiology Events",
            "rows": len(microbiology),
            "unique_patients": microbiology["subject_id"].nunique(),
            "unique_admissions": microbiology["hadm_id"].nunique()
        },
        {
            "source": "Prescriptions",
            "rows": len(prescriptions),
            "unique_patients": prescriptions["subject_id"].nunique(),
            "unique_admissions": prescriptions["hadm_id"].nunique()
        }
    ]

    comparison_df = pd.DataFrame(comparison_rows)

    st.bar_chart(
        comparison_df.set_index("source")["rows"]
    )

    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )
