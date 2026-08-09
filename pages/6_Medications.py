import pandas as pd
import streamlit as st

from src.streamlit_data import (
    load_core_data,
    load_dashboard_dataset
)

from src.medications import (
    prescription_summary,
    prescriptions_by_drug,
    prescriptions_by_drug_type,
    prescriptions_by_route,
    pharmacy_summary,
    pharmacy_by_medication,
    pharmacy_by_status,
    emar_summary,
    emar_by_medication,
    emar_detail_summary,
    dose_summary,
    inputevent_summary,
    inputevents_by_category,
    ingredientevent_summary,
    medication_coverage_summary
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Medications | MIMIC Analytics",
    page_icon="🏥",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

data = load_core_data()

prescriptions = data["prescriptions"]
pharmacy = data["pharmacy"]
emar = data["emar"]

# Not part of load_core_data(), loaded separately
# (still cached via st.cache_data).
emar_detail = load_dashboard_dataset("emar_detail")
ingredientevents = load_dashboard_dataset("ingredientevents")
inputevents = load_dashboard_dataset("inputevents")


# ============================================================
# HEADER
# ============================================================

st.title("💊 Medications")

st.markdown(
    """
    Ordered, dispensed, and administered medications across
    prescriptions, pharmacy, eMAR, and ICU infusion sources.
    """
)

st.divider()


# ============================================================
# TABS
# ============================================================

prescriptions_tab, pharmacy_tab, emar_tab, icu_tab, coverage_tab = st.tabs(
    [
        "📝 Prescriptions",
        "🏪 Pharmacy",
        "💉 eMAR Administration",
        "🧴 ICU Infusions",
        "🔗 Source Coverage"
    ]
)


# ============================================================
# PRESCRIPTIONS TAB
# ============================================================

with prescriptions_tab:

    rx_summary = prescription_summary(prescriptions)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Prescriptions",
            f"{rx_summary['total_prescriptions']:,}"
        )

    with col2:
        st.metric(
            "Unique Patients",
            f"{rx_summary['unique_patients']:,}"
        )

    with col3:
        st.metric(
            "Unique Admissions",
            f"{rx_summary['unique_admissions']:,}"
        )

    with col4:
        st.metric(
            "Unique Medications",
            f"{rx_summary['unique_medications']:,}"
        )

    st.subheader("Top Prescribed Drugs")

    top_drugs = prescriptions_by_drug(prescriptions).head(20)

    st.bar_chart(
        top_drugs.set_index("drug")["prescription_count"]
    )

    st.dataframe(
        top_drugs,
        use_container_width=True,
        hide_index=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("By Drug Type")

        drug_types = prescriptions_by_drug_type(prescriptions)

        st.bar_chart(
            drug_types.set_index("drug_type")
        )

        st.dataframe(
            drug_types,
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.subheader("By Route")

        routes = prescriptions_by_route(prescriptions).head(15)

        st.bar_chart(
            routes.set_index("route")
        )

        st.dataframe(
            routes,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# PHARMACY TAB
# ============================================================

with pharmacy_tab:

    pharm_summary = pharmacy_summary(pharmacy)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Pharmacy Records",
            f"{pharm_summary['total_pharmacy_records']:,}"
        )

    with col2:
        st.metric(
            "Unique Patients",
            f"{pharm_summary['unique_patients']:,}"
        )

    with col3:
        st.metric(
            "Unique Admissions",
            f"{pharm_summary['unique_admissions']:,}"
        )

    with col4:
        st.metric(
            "Unique Medications",
            f"{pharm_summary['unique_medications']:,}"
        )

    st.subheader("Top Pharmacy Medications")

    top_pharmacy_meds = pharmacy_by_medication(pharmacy).head(20)

    st.bar_chart(
        top_pharmacy_meds.set_index("medication")["pharmacy_events"]
    )

    st.dataframe(
        top_pharmacy_meds,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Pharmacy Order Status")

    status_df = pharmacy_by_status(pharmacy)

    st.bar_chart(
        status_df.set_index("status")
    )

    st.dataframe(
        status_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# eMAR ADMINISTRATION TAB
# ============================================================

with emar_tab:

    emar_stats = emar_summary(emar)
    emar_detail_stats = emar_detail_summary(emar_detail)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total eMAR Events",
            f"{emar_stats['total_emar_events']:,}"
        )

    with col2:
        st.metric(
            "Unique Patients",
            f"{emar_stats['unique_patients']:,}"
        )

    with col3:
        st.metric(
            "Unique Admissions",
            f"{emar_stats['unique_admissions']:,}"
        )

    with col4:
        st.metric(
            "Unique Medications",
            f"{emar_stats['unique_medications']:,}"
        )

    st.caption(
        f"eMAR administration detail: "
        f"{emar_detail_stats['total_emar_detail_records']:,} dose "
        f"records covering "
        f"{emar_detail_stats['unique_emar_events']:,} eMAR events."
    )

    st.subheader("Top Administered Medications")

    top_administered = emar_by_medication(emar).head(20)

    st.bar_chart(
        top_administered.set_index("medication")[
            "administration_events"
        ]
    )

    st.dataframe(
        top_administered,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Administered Dose Summary by Unit")

    doses = dose_summary(emar_detail).sort_values(
        "count",
        ascending=False
    )

    st.dataframe(
        doses.head(20),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# ICU INFUSIONS TAB (INPUT / INGREDIENT EVENTS)
# ============================================================

with icu_tab:

    input_stats = inputevent_summary(inputevents)
    ingredient_stats = ingredientevent_summary(ingredientevents)

    st.markdown("**ICU Input Events**")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Input Events",
            f"{input_stats['total_input_events']:,}"
        )

    with col2:
        st.metric(
            "Unique Patients",
            f"{input_stats['unique_patients']:,}"
        )

    with col3:
        st.metric(
            "Unique Admissions",
            f"{input_stats['unique_admissions']:,}"
        )

    with col4:
        st.metric(
            "Unique Items",
            f"{input_stats['unique_items']:,}"
        )

    st.subheader("Input Events by Order Category")

    categories = inputevents_by_category(inputevents)

    st.bar_chart(
        categories.set_index("ordercategoryname")
    )

    st.dataframe(
        categories,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.markdown("**ICU Ingredient Events**")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Ingredient Events",
            f"{ingredient_stats['total_ingredient_events']:,}"
        )

    with col2:
        st.metric(
            "Unique Patients",
            f"{ingredient_stats['unique_patients']:,}"
        )

    with col3:
        st.metric(
            "Unique Admissions",
            f"{ingredient_stats['unique_admissions']:,}"
        )

    with col4:
        st.metric(
            "Unique Items",
            f"{ingredient_stats['unique_items']:,}"
        )


# ============================================================
# SOURCE COVERAGE TAB
# ============================================================

with coverage_tab:

    st.subheader("Medication Source Coverage")

    st.caption(
        "The same medication activity is recorded across three "
        "independent sources — prescriptions (orders), pharmacy "
        "(dispensing), and eMAR (administration). Coverage differs "
        "because not every order is dispensed or charted the same way."
    )

    coverage = medication_coverage_summary(
        prescriptions,
        pharmacy,
        emar
    )

    st.bar_chart(
        coverage.set_index("source")["rows"]
    )

    st.dataframe(
        coverage,
        use_container_width=True,
        hide_index=True
    )
