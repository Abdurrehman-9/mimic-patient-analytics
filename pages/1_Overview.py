import altair as alt
import pandas as pd
import streamlit as st

from src.streamlit_data import load_core_data
from src.theme import inject_theme, render_hero, metric_row, COLORS

from src.demographics import gender_distribution, mortality_overview
from src.admissions import hospital_los_summary
from src.icu import icu_overview


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Overview | MIMIC Analytics",
    page_icon="🏥",
    layout="wide"
)

inject_theme()


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
# HERO
# ============================================================

render_hero(
    eyebrow="Executive Overview",
    title="Population & Utilization Summary",
    subtitle=(
        "A high-level read of the patient population, hospital "
        "utilization, ICU activity, and clinical data volume "
        "behind this dashboard."
    ),
    accent=COLORS["teal"]
)


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
# KPI ROWS
# ============================================================

row1 = st.columns(4)

metric_row(
    row1,
    [
        {
            "icon": "👥",
            "value": f"{total_patients:,}",
            "label": "Patients",
            "accent": COLORS["teal"],
        },
        {
            "icon": "🏨",
            "value": f"{total_admissions:,}",
            "label": "Admissions",
            "accent": COLORS["sky"],
        },
        {
            "icon": "🛏️",
            "value": f"{total_icu_stays:,}",
            "label": "ICU Stays",
            "accent": COLORS["violet"],
        },
        {
            "icon": "🧪",
            "value": f"{total_lab_events:,}",
            "label": "Lab Events",
            "accent": COLORS["amber"],
        },
    ]
)

st.write("")

row2 = st.columns(4)

metric_row(
    row2,
    [
        {
            "icon": "📈",
            "value": f"{total_chart_events:,}",
            "label": "Chart Events",
            "accent": COLORS["rose"],
        },
        {
            "icon": "💊",
            "value": f"{total_prescriptions:,}",
            "label": "Prescriptions",
            "accent": COLORS["teal"],
        },
        {
            "icon": "🦠",
            "value": f"{total_micro_events:,}",
            "label": "Microbiology Events",
            "accent": COLORS["sky"],
        },
        {
            "icon": "🎯",
            "value": f"{patients['anchor_age'].mean():.1f}",
            "label": "Average Age",
            "accent": COLORS["violet"],
        },
    ]
)


# ============================================================
# QUICK INSIGHTS STRIP
# ============================================================

st.write("")
st.markdown(
    '<div class="mimic-section-title">Quick Insights</div>',
    unsafe_allow_html=True
)

los_summary = hospital_los_summary(admissions)
icu_stats = icu_overview(icustays)
mortality = mortality_overview(admissions)

icu_utilization_pct = (
    icu_stats["unique_hospital_admissions"] / total_admissions * 100
)

row3 = st.columns(4)

metric_row(
    row3,
    [
        {
            "icon": "📆",
            "value": f"{los_summary['mean_los_days']:.1f} days",
            "label": "Avg Hospital Stay",
            "accent": COLORS["teal"],
        },
        {
            "icon": "🛏️",
            "value": f"{icu_utilization_pct:.1f}%",
            "label": "Admissions Reaching ICU",
            "accent": COLORS["sky"],
        },
        {
            "icon": "⏱️",
            "value": f"{icu_stats['median_icu_los']:.1f} days",
            "label": "Median ICU Stay",
            "accent": COLORS["violet"],
        },
        {
            "icon": "📉",
            "value": f"{mortality['mortality_rate_pct']:.1f}%",
            "label": "In-Hospital Mortality",
            "accent": COLORS["rose"],
        },
    ]
)


# ============================================================
# DATASET COVERAGE + GENDER SPLIT
# ============================================================

st.write("")
st.divider()

chart_col, donut_col = st.columns([2, 1])

with chart_col:

    st.markdown(
        '<div class="mimic-section-title">Dataset Coverage</div>',
        unsafe_allow_html=True
    )

    coverage = {
        "Chart Events": total_chart_events,
        "Laboratory Events": total_lab_events,
        "Prescriptions": total_prescriptions,
        "Microbiology Events": total_micro_events,
        "Admissions": total_admissions,
        "ICU Stays": total_icu_stays,
        "Patients": total_patients,
    }

    coverage_df = pd.DataFrame(
        list(coverage.items()),
        columns=["dataset", "records"]
    ).sort_values("records", ascending=True)

    coverage_chart = (
        alt.Chart(coverage_df)
        .mark_bar(
            cornerRadiusTopRight=4,
            cornerRadiusBottomRight=4
        )
        .encode(
            x=alt.X(
                "records:Q",
                title="Records",
                axis=alt.Axis(format=",.0f")
            ),
            y=alt.Y(
                "dataset:N",
                title=None,
                sort="-x"
            ),
            color=alt.Color(
                "records:Q",
                scale=alt.Scale(
                    range=[COLORS["panel"], COLORS["teal"]]
                ),
                legend=None
            ),
            tooltip=[
                alt.Tooltip("dataset:N", title="Dataset"),
                alt.Tooltip("records:Q", title="Records", format=",.0f"),
            ]
        )
        .properties(height=280)
        .configure_axis(
            labelColor=COLORS["muted"],
            titleColor=COLORS["muted"],
            grid=False,
            domainColor=COLORS["panel_border"]
        )
        .configure_view(strokeWidth=0)
    )

    st.altair_chart(coverage_chart, width='stretch')

with donut_col:

    st.markdown(
        '<div class="mimic-section-title">Gender Split</div>',
        unsafe_allow_html=True
    )

    gender_df = gender_distribution(patients)

    donut_chart = (
        alt.Chart(gender_df)
        .mark_arc(innerRadius=55, outerRadius=95)
        .encode(
            theta=alt.Theta("patient_count:Q", stack=True),
            color=alt.Color(
                "gender:N",
                scale=alt.Scale(
                    domain=["M", "F"],
                    range=[COLORS["sky"], COLORS["rose"]]
                ),
                legend=alt.Legend(
                    title=None,
                    labelColor=COLORS["muted"],
                    orient="bottom"
                )
            ),
            tooltip=[
                alt.Tooltip("gender:N", title="Gender"),
                alt.Tooltip("patient_count:Q", title="Patients"),
            ]
        )
        .properties(height=280)
        .configure_view(strokeWidth=0)
    )

    st.altair_chart(donut_chart, width='stretch')


# ============================================================
# FOOTER
# ============================================================

st.write("")
st.divider()

st.caption(
    "Figures reflect the full dataset loaded into this session. "
    "Use the sidebar to drill into any category."
)
