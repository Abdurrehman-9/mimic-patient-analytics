# ============================================================
# MIMIC PATIENT ANALYTICS
# SHARED VISUAL THEME
# ============================================================

import streamlit as st


# ============================================================
# COLOR TOKENS
# ============================================================

COLORS = {
    "bg": "#0B1220",
    "panel": "#111C2E",
    "panel_border": "rgba(148, 197, 213, 0.14)",
    "text": "#E7EFF6",
    "muted": "#8CA0B3",
    "teal": "#2DD4BF",
    "sky": "#38BDF8",
    "violet": "#8B7FD6",
    "amber": "#F5A623",
    "rose": "#FB7185",
}


ACCENT_CYCLE = [
    COLORS["teal"],
    COLORS["sky"],
    COLORS["violet"],
    COLORS["amber"],
    COLORS["rose"],
]


# ============================================================
# SHARED CSS
# ============================================================

_CUSTOM_CSS = f"""
<style>

/* ==========================================================
   FONT IMPORT
   ========================================================== */

@import url(
    'https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700'
    '&family=IBM+Plex+Mono:wght@500;600;700&display=swap'
);


/* ==========================================================
   HERO
   ========================================================== */

.mimic-eyebrow {{
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: {COLORS["teal"]} !important;
    margin: 0 0 0.6rem 0;
}}


.mimic-hero-title {{
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 700;
    font-size: 2.6rem;
    line-height: 1.15;
    color: var(--text-color) !important;
    margin: 0 0 0.6rem 0;
}}


.mimic-hero-subtitle {{
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 1.05rem;
    font-weight: 400;
    color: var(--secondary-text-color) !important;
    max-width: 46rem;
    line-height: 1.6;
    margin: 0;
}}


/* ==========================================================
   ECG DIVIDER
   ========================================================== */

.mimic-ecg {{
    width: 100%;
    overflow: hidden;
    margin: 0.4rem 0 1.4rem 0;
}}


/* ==========================================================
   KPI METRIC CARDS
   ========================================================== */

.mimic-metric-card {{
    background: {COLORS["panel"]};
    border: 1px solid {COLORS["panel_border"]};
    border-left: 3px solid var(--mimic-accent, {COLORS["teal"]});
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    height: 100%;
    box-sizing: border-box;
    transition:
        transform 0.15s ease,
        box-shadow 0.15s ease;
}}


.mimic-metric-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 26px rgba(0, 0, 0, 0.35);
}}


.mimic-metric-icon {{
    font-family:
        'Segoe UI Emoji',
        'Apple Color Emoji',
        'Noto Color Emoji',
        sans-serif !important;

    font-size: 1.3rem;
    line-height: 1.2;
    opacity: 0.95;
    margin-bottom: 0.55rem;
}}


.mimic-metric-value {{
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600;
    font-size: 1.65rem;
    line-height: 1.2;
    color: {COLORS["text"]} !important;
    margin: 0;
}}


.mimic-metric-label {{
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: {COLORS["muted"]} !important;
    margin-top: 0.25rem;
}}


/* ==========================================================
   SECTION TITLES
   ========================================================== */

.mimic-section-title {{
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 600;
    font-size: 1.1rem;
    line-height: 1.3;
    color: var(--text-color) !important;
    margin: 0 0 0.9rem 0;
}}


/* ==========================================================
   NAVIGATION / DASHBOARD CARDS
   ========================================================== */

.mimic-nav-icon {{
    font-family:
        'Segoe UI Emoji',
        'Apple Color Emoji',
        'Noto Color Emoji',
        sans-serif !important;

    font-size: 1.6rem;
    line-height: 1.2;
    margin-bottom: 0.25rem;
}}


.mimic-nav-title {{
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 600;
    font-size: 1.02rem;
    line-height: 1.3;
    color: var(--text-color) !important;
    margin: 0.4rem 0 0.15rem 0;
}}


.mimic-nav-desc {{
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.85rem;
    font-weight: 400;
    line-height: 1.45;
    color: var(--secondary-text-color) !important;
    margin: 0 0 0.6rem 0;
}}


/* ==========================================================
   SIDEBAR BRAND
   ========================================================== */

.mimic-sidebar-brand {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.2rem 0 1rem 0;
    margin-bottom: 0.4rem;
    border-bottom: 1px solid var(--secondary-background-color);
}}


.mimic-sidebar-brand-icon {{
    font-family:
        'Segoe UI Emoji',
        'Apple Color Emoji',
        'Noto Color Emoji',
        sans-serif !important;

    font-size: 1.3rem;
    line-height: 1;
}}


.mimic-sidebar-brand-text {{
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 700;
    font-size: 1.02rem;
    line-height: 1.2;
    color: var(--text-color) !important;
    letter-spacing: 0.01em;
}}


/* ==========================================================
   SIDEBAR SECTION LABEL
   ========================================================== */

.mimic-sidebar-section {{
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--secondary-text-color) !important;
    margin: 1.1rem 0 0.3rem 0.1rem;
}}


/* ==========================================================
   SIDEBAR FOOTER
   ========================================================== */

.mimic-sidebar-footer {{
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem;
    color: var(--secondary-text-color) !important;
    margin-top: 1.4rem;
    padding-top: 0.9rem;
    border-top: 1px solid var(--secondary-background-color);
}}


/* ==========================================================
   STREAMLIT SIDEBAR PAGE LINKS
   ========================================================== */

section[data-testid="stSidebar"]
[data-testid="stPageLink-NavLink"] {{
    border-radius: 8px;
    transition: background-color 0.15s ease;
}}


section[data-testid="stSidebar"]
[data-testid="stPageLink-NavLink"]:hover {{
    background-color: rgba(45, 212, 191, 0.08);
}}


section[data-testid="stSidebar"]
[data-testid="stPageLink-NavLink"],
section[data-testid="stSidebar"]
[data-testid="stPageLink-NavLink"] span {{
    font-family: 'IBM Plex Sans', sans-serif !important;
}}


/* ==========================================================
   NATIVE STREAMLIT CAPTIONS
   ========================================================== */

[data-testid="stCaptionContainer"] {{
    font-family: 'IBM Plex Sans', sans-serif !important;
}}


/* ==========================================================
   NATIVE STREAMLIT MARKDOWN
   ========================================================== */

.stMarkdown {{
    font-family: 'IBM Plex Sans', sans-serif;
}}


/* ==========================================================
   ACCESSIBILITY
   ========================================================== */

@media (prefers-reduced-motion: reduce) {{

    .mimic-metric-card {{
        transition: none;
    }}

}}

</style>
"""


# ============================================================
# THEME INJECTION
# ============================================================

def inject_theme():
    """
    Inject the shared MIMIC Analytics visual theme.

    This function intentionally does not use JavaScript for
    light/dark-mode detection. Streamlit's own theme variables
    are used for text and background-sensitive elements.
    """

    st.markdown(
        _CUSTOM_CSS,
        unsafe_allow_html=True,
    )


# ============================================================
# ECG DIVIDER
# ============================================================

def ecg_divider(accent=None, cycles=10, height=34):
    """
    Generate the SVG ECG waveform used throughout the dashboard.

    Parameters
    ----------
    accent : str, optional
        Stroke color for the ECG line.

    cycles : int
        Number of waveform repetitions.

    height : int
        SVG height in pixels.

    Returns
    -------
    str
        HTML/SVG string.
    """

    accent = accent or COLORS["teal"]

    cycle_width = 160
    baseline = height / 2

    path_parts = [
        f"M0,{baseline}"
    ]

    peak_amplitude = baseline * 0.85
    trough_amplitude = (height - baseline) * 0.70
    small_dip_amplitude = (height - baseline) * 0.35
    small_bump_amplitude = baseline * 0.30

    for cycle in range(cycles):

        x0 = cycle * cycle_width

        path_parts.extend([
            f"L{x0 + 34},{baseline}",
            f"L{x0 + 40},{baseline + small_dip_amplitude}",
            f"L{x0 + 48},{baseline - peak_amplitude}",
            f"L{x0 + 56},{baseline + trough_amplitude}",
            f"L{x0 + 62},{baseline}",
            f"L{x0 + 70},{baseline - small_bump_amplitude}",
            f"L{x0 + 160},{baseline}",
        ])

    path_d = " ".join(path_parts)

    total_width = cycles * cycle_width

    return (
        f'<div class="mimic-ecg">'
        f'<svg '
        f'viewBox="0 0 {total_width} {height}" '
        f'preserveAspectRatio="none" '
        f'width="100%" '
        f'height="{height}">'
        f'<path '
        f'd="{path_d}" '
        f'fill="none" '
        f'stroke="{accent}" '
        f'stroke-width="1.6" '
        f'stroke-linejoin="round" '
        f'stroke-linecap="round" '
        f'opacity="0.85"/>'
        f'</svg>'
        f'</div>'
    )


# ============================================================
# HERO
# ============================================================

def render_hero(
    eyebrow,
    title,
    subtitle,
    accent=None,
):
    """
    Render the standard dashboard hero section.

    Includes:
        - eyebrow
        - title
        - subtitle
        - ECG divider
    """

    accent = accent or COLORS["teal"]

    # IMPORTANT:
    # Keep these HTML elements as one continuous string.
    # Do not indent the HTML inside a multiline Markdown
    # string, otherwise Streamlit can interpret it as code.

    hero_html = (
        f'<div class="mimic-eyebrow">'
        f'{eyebrow}'
        f'</div>'

        f'<div class="mimic-hero-title">'
        f'{title}'
        f'</div>'

        f'<p class="mimic-hero-subtitle">'
        f'{subtitle}'
        f'</p>'
    )

    st.markdown(
        hero_html,
        unsafe_allow_html=True,
    )

    st.markdown(
        ecg_divider(accent=accent),
        unsafe_allow_html=True,
    )


# ============================================================
# SINGLE METRIC CARD
# ============================================================

def render_metric_card(
    icon,
    value,
    label,
    accent=None,
):
    """
    Render a single KPI metric card.

    Parameters
    ----------
    icon : str
        Emoji/icon displayed at the top.

    value : str
        Main KPI value.

    label : str
        KPI label.

    accent : str, optional
        Left-border accent color.
    """

    accent = accent or COLORS["teal"]

    # IMPORTANT:
    # This is intentionally built as one continuous HTML
    # string. Do NOT indent the HTML inside a multiline
    # f-string. That was the source of the visible
    # <div class="..."> problem.

    card_html = (
        f'<div '
        f'class="mimic-metric-card" '
        f'style="--mimic-accent: {accent};">'
        
        f'<div class="mimic-metric-icon">'
        f'{icon}'
        f'</div>'

        f'<div class="mimic-metric-value">'
        f'{value}'
        f'</div>'

        f'<div class="mimic-metric-label">'
        f'{label}'
        f'</div>'

        f'</div>'
    )

    st.markdown(
        card_html,
        unsafe_allow_html=True,
    )


# ============================================================
# METRIC ROW
# ============================================================

def metric_row(
    columns,
    cards,
):
    """
    Render multiple metric cards across Streamlit columns.

    Expected card structure:

        {
            "icon": "👥",
            "value": "100",
            "label": "Patients",
            "accent": "#2DD4BF"
        }

    The accent key is optional.
    """

    for col, card in zip(columns, cards):

        with col:

            render_metric_card(
                icon=card["icon"],
                value=card["value"],
                label=card["label"],
                accent=card.get("accent"),
            )
