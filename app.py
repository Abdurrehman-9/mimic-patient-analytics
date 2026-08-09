import streamlit as st

from src.streamlit_data import load_core_data
from src.theme import inject_theme, render_hero, metric_row, COLORS


# ============================================================
# PAGE CONFIG
# Must be the first Streamlit command in the entry-point script.
# ============================================================

st.set_page_config(
    page_title="MIMIC Patient Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_theme()


# ============================================================
# PAGE DEFINITIONS
#
# Titles/icons are tracked in PAGE_REGISTRY below (not read back
# off the Page objects, since Page.title/.icon aren't reliably
# populated until after st.navigation() processes them).
# ============================================================

PAGE_REGISTRY = [
    {
        "key": "overview",
        "path": "pages/1_Overview.py",
        "title": "Overview",
        "icon": "📊",
        "desc": "Executive KPIs and dataset coverage at a glance.",
    },
    {
        "key": "demographics",
        "path": "pages/2_Demographics.py",
        "title": "Demographics",
        "icon": "👥",
        "desc": "Patient population by age, gender, and background.",
    },
    {
        "key": "admissions",
        "path": "pages/3_Admissions.py",
        "title": "Admissions",
        "icon": "🏨",
        "desc": "Volume, length of stay, and admission trends.",
    },
    {
        "key": "icu",
        "path": "pages/4_ICU_Analysis.py",
        "title": "ICU Analysis",
        "icon": "🛏️",
        "desc": "Critical care utilization and length of stay.",
    },
    {
        "key": "clinical",
        "path": "pages/5_Clinical_Events.py",
        "title": "Clinical Events",
        "icon": "📈",
        "desc": "Lab tests, chart events, and microbiology.",
    },
    {
        "key": "medications",
        "path": "pages/6_Medications.py",
        "title": "Medications",
        "icon": "💊",
        "desc": "Prescriptions, pharmacy, and administration records.",
    },
    {
        "key": "diagnoses",
        "path": "pages/7_Diagnoses.py",
        "title": "Diagnoses",
        "icon": "🩻",
        "desc": "ICD diagnoses, procedures, and DRG severity.",
    },
    {
        "key": "quality",
        "path": "pages/8_Data_Quality.py",
        "title": "Data Quality",
        "icon": "🔍",
        "desc": "Completeness, integrity, and validation checks.",
    },
    {
        "key": "timeline",
        "path": "pages/9_Patient_Timeline.py",
        "title": "Patient Timeline",
        "icon": "🕒",
        "desc": "Single-patient drill-down across every source.",
    },
]

for entry in PAGE_REGISTRY:
    entry["page"] = st.Page(
        entry["path"],
        title=entry["title"],
        icon=entry["icon"],
        url_path=entry["key"]
    )


# ============================================================
# HOME PAGE CONTENT
# ============================================================

def render_home():

    data = load_core_data()

    patients = data["patients"]
    admissions = data["admissions"]
    icustays = data["icustays"]

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

    st.markdown(
        '<div class="mimic-section-title">Explore the Dashboard</div>',
        unsafe_allow_html=True
    )

    for row_start in range(0, len(PAGE_REGISTRY), 3):

        row_items = PAGE_REGISTRY[row_start:row_start + 3]
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
                        icon=":material/arrow_forward:"
                    )

    st.write("")
    st.divider()

    st.caption(
        "Built on MIMIC-IV clinical data · Data refreshes each session · "
        "Use the sidebar or the cards above to navigate."
    )


home_page = st.Page(
    render_home,
    title="Home",
    icon="🏠",
    default=True,
    url_path="home"
)


# ============================================================
# CUSTOM SIDEBAR
#
# Streamlit's built-in page list (position="sidebar") renders as
# a plain, unstyled text list with no icons. We hide it and build
# our own instead, using the same public st.page_link API, so it
# picks up the dashboard's theme and icon set.
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="mimic-sidebar-brand">
            <span class="mimic-sidebar-brand-icon">🏥</span>
            <span class="mimic-sidebar-brand-text">MIMIC Analytics</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.page_link(home_page, label="Home", icon="🏠")

    st.markdown(
        '<div class="mimic-sidebar-section">Explore</div>',
        unsafe_allow_html=True
    )

    for item in PAGE_REGISTRY:
        st.page_link(
            item["page"],
            label=item["title"],
            icon=item["icon"]
        )

    st.markdown(
        '<div class="mimic-sidebar-footer">MIMIC-IV · 100 patients</div>',
        unsafe_allow_html=True
    )


# ============================================================
# NAVIGATION
# Built-in nav UI is hidden ("position=hidden") since the sidebar
# above replaces it; st.navigation still owns routing.
# ============================================================

nav = st.navigation(
    {"": [home_page], "Explore": [item["page"] for item in PAGE_REGISTRY]},
    position="hidden"
)

nav.run()
