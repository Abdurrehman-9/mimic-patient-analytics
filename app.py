import streamlit as st

from src.streamlit_data import load_core_data
from src.theme import inject_theme, render_hero, metric_row, COLORS


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MIMIC Patient Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_theme()


# ============================================================
# LOAD DATA (for live top-line numbers, not hardcoded values)
# ============================================================

data = load_core_data()

patients = data["patients"]
admissions = data["admissions"]
icustays = data["icustays"]


# ============================================================
# HERO
# ============================================================

render_hero(
    eyebrow="Clinical Data Analytics Platform",
    title="MIMIC Patient Analytics",
    subtitle=(
        "An interactive analytics platform built on MIMIC-IV "
        "clinical data — spanning admissions, ICU stays, "
        "laboratory testing, medications, and diagnoses for a "
        "100-patient cohort."
    ),
    accent=COLORS["teal"]
)


# ============================================================
# TOP-LINE KPIs
# ============================================================

cols = st.columns(4)

metric_row(
    cols,
    [
        {
            "icon": "👥",
            "value": f"{patients['subject_id'].nunique():,}",
            "label": "Patients",
            "accent": COLORS["teal"],
        },
        {
            "icon": "🏨",
            "value": f"{admissions['hadm_id'].nunique():,}",
            "label": "Admissions",
            "accent": COLORS["sky"],
        },
        {
            "icon": "🛏️",
            "value": f"{icustays['stay_id'].nunique():,}",
            "label": "ICU Stays",
            "accent": COLORS["violet"],
        },
        {
            "icon": "🎯",
            "value": f"{patients['anchor_age'].mean():.1f}",
            "label": "Average Age",
            "accent": COLORS["amber"],
        },
    ]
)

st.write("")


# ============================================================
# NAVIGATION GRID
# ============================================================

st.markdown(
    '<div class="mimic-section-title">Explore the Dashboard</div>',
    unsafe_allow_html=True
)

nav_items = [
    {
        "icon": "🏠",
        "title": "Overview",
        "desc": "Executive KPIs and dataset coverage at a glance.",
        "page": "pages/1_Overview.py",
    },
    {
        "icon": "👥",
        "title": "Demographics",
        "desc": "Patient population by age, gender, and background.",
        "page": "pages/2_Demographics.py",
    },
    {
        "icon": "🏨",
        "title": "Admissions",
        "desc": "Volume, length of stay, and admission trends.",
        "page": "pages/3_Admissions.py",
    },
    {
        "icon": "🛏️",
        "title": "ICU Analysis",
        "desc": "Critical care utilization and length of stay.",
        "page": "pages/4_ICU_Analysis.py",
    },
    {
        "icon": "📈",
        "title": "Clinical Events",
        "desc": "Lab tests, chart events, and microbiology.",
        "page": "pages/5_Clinical_Events.py",
    },
    {
        "icon": "💊",
        "title": "Medications",
        "desc": "Prescriptions, pharmacy, and administration records.",
        "page": "pages/6_Medications.py",
    },
    {
        "icon": "🩻",
        "title": "Diagnoses",
        "desc": "ICD diagnoses, procedures, and DRG severity.",
        "page": "pages/7_Diagnoses.py",
    },
    {
        "icon": "🔍",
        "title": "Data Quality",
        "desc": "Completeness, integrity, and validation checks.",
        "page": "pages/8_Data_Quality.py",
    },
    {
        "icon": "🕒",
        "title": "Patient Timeline",
        "desc": "Single-patient drill-down across every source.",
        "page": "pages/9_Patient_Timeline.py",
    },
]

for row_start in range(0, len(nav_items), 3):

    row_items = nav_items[row_start:row_start + 3]
    row_cols = st.columns(3)

    for col, item in zip(row_cols, row_items):
        with col:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div class="mimic-nav-icon">{item['icon']}</div>
                    <div class="mimic-nav-title">{item['title']}</div>
                    <div class="mimic-nav-desc">{item['desc']}</div>
                    """,
                    unsafe_allow_html=True
                )
                st.page_link(
                    item["page"],
                    label="Open",
                    icon="→"
                )


# ============================================================
# FOOTER
# ============================================================

st.write("")
st.divider()

st.caption(
    "Built on MIMIC-IV clinical data · Data refreshes each session · "
    "Use the sidebar or the cards above to navigate."
)
