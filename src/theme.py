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
# BASE CSS
# ============================================================

_CUSTOM_CSS = f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600;700&display=swap');


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
    margin-bottom: 0.6rem;
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
    font-weight: 500;
    color: var(--secondary-text-color) !important;
    max-width: 46rem;
    line-height: 1.6;
    margin: 0;
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
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}}


.mimic-metric-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 26px rgba(0, 0, 0, 0.35);
}}


.mimic-metric-icon {{
    font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    font-size: 1.3rem;
    opacity: 0.9;
    margin-bottom: 0.5rem;
}}


.mimic-metric-value {{
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600;
    font-size: 1.65rem;
    color: {COLORS["text"]} !important;
    line-height: 1.2;
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
    color: var(--text-color) !important;
    margin: 0 0 0.9rem 0;
}}


/* ==========================================================
   DASHBOARD NAVIGATION CARDS
   ========================================================== */

.mimic-nav-icon {{
    font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    font-size: 1.6rem;
}}


.mimic-nav-title {{
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 600;
    font-size: 1.02rem;
    color: var(--text-color) !important;
    margin: 0.4rem 0 0.15rem 0;
}}


.mimic-nav-desc {{
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.85rem;
    color: var(--secondary-text-color) !important;
    line-height: 1.45;
    margin-bottom: 0.6rem;
}}


/* ==========================================================
   SIDEBAR
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
    font-size: 1.3rem;
}}


.mimic-sidebar-brand-text {{
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 700;
    font-size: 1.02rem;
    color: var(--text-color) !important;
    letter-spacing: 0.01em;
}}


.mimic-sidebar-section {{
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--secondary-text-color) !important;
    margin: 1.1rem 0 0.3rem 0.1rem;
}}


.mimic-sidebar-footer {{
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem;
    color: var(--secondary-text-color) !important;
    margin-top: 1.4rem;
    padding-top: 0.9rem;
    border-top: 1px solid var(--secondary-background-color);
}}


/* ==========================================================
   STREAMLIT PAGE LINKS
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


/* Make native Streamlit page links use the dashboard font */
[data-testid="stPageLink-NavLink"],
[data-testid="stPageLink-NavLink"] span {{
    font-family: 'IBM Plex Sans', sans-serif !important;
}}


/* ==========================================================
   NATIVE STREAMLIT CAPTION
   ========================================================== */

[data-testid="stCaptionContainer"] {{
    font-family: 'IBM Plex Sans', sans-serif !important;
}}


/* ==========================================================
   REDUCED MOTION
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
    Inject the shared CSS theme.

    No JavaScript theme detection is used.
    Streamlit's own theme variables control light/dark text.
    """

    st.markdown(
        _CUSTOM_CSS,
        unsafe_allow_html=True
    )


# ============================================================
# ECG WAVEFORM
# ============================================================

def ecg_divider(accent=None, cycles=10, height=34):
    """
    Render the ECG waveform used as the dashboard's
    signature visual divider.
    """

    accent = accent or COLORS["teal"]

    cycle_width = 160
    baseline = height / 2

    segment_template = (
        "L{x0},{b} "
        "L{x1},{b} "
        "L{x2},{small_dip} "
        "L{x3},{big_peak} "
        "L{x4},{deep_trough} "
        "L{x5},{b} "
        "L{x6},{small_bump} "
        "L{x7},{b} "
    )

    path_parts = [f"M0,{baseline}"]

    peak_amplitude = baseline * 0.85
    trough_amplitude = (height - baseline) * 0.7
    small_dip_amplitude = (height - baseline) * 0.35
    small_bump_amplitude = baseline * 0.3

    for cycle in range(cycles):

        x0 = cycle * cycle_width

        path_parts.append(
            segment_template.format(
                x0=x0,
                x1=x0 + 34,
                x2=x0 + 40,
                x3=x0 + 48,
                x4=x0 + 56,
                x5=x0 + 62,
                x6=x0 + 70,
                x7=x0 + 160,
                b=baseline,
                small_dip=baseline + small_dip_amplitude,
                big_peak=baseline - peak_amplitude,
                deep_trough=baseline + trough_amplitude,
                small_bump=baseline - small_bump_amplitude,
            )
        )

    path_d = " ".join(path_parts)
    total_width = cycles * cycle_width

    svg = (
        f'<div style="width:100%; overflow:hidden; '
        f'margin:0.4rem 0 1.4rem 0;">'
        f'<svg viewBox="0 0 {total_width} {height}" '
        f'preserveAspectRatio="none" width="100%" height="{height}">'
        f'<path d="{path_d}" fill="none" stroke="{accent}" '
        f'stroke-width="1.6" stroke-linejoin="round" '
        f'stroke-linecap="round" opacity="0.85"/>'
        f'</svg>'
        f'</div>'
    )

    return svg


# ============================================================
# HERO HEADER
# ============================================================

def render_hero(eyebrow, title, subtitle, accent=None):
    """
    Render the page hero:
    eyebrow + title + subtitle + ECG divider.
    """

    accent = accent or COLORS["teal"]

    # IMPORTANT:
    # Keep the HTML unindented. This prevents Streamlit's
    # Markdown parser from interpreting it as a code block.
    hero_html = (
        f'<div class="mimic-eyebrow">{eyebrow}</div>'
        f'<div class="mimic-hero-title">{title}</div>'
        f'<p class="mimic-hero-subtitle">{subtitle}</p>'
    )

    st.markdown(
        hero_html,
        unsafe_allow_html=True
    )

    st.markdown(
        ecg_divider(accent=accent),
        unsafe_allow_html=True
    )


# ============================================================
# METRIC CARD
# ============================================================

def render_metric_card(icon, value, label, accent=None):
    """
    Render one KPI card.

    Example:
        with col:
            render_metric_card(
                "🏨",
                "275",
                "Admissions",
                accent="#38BDF8"
            )
    """

    accent = accent or COLORS["teal"]

    # IMPORTANT:
    # Keep this HTML as one continuous string.
    # Do not indent the <div> tags inside a multiline string.
    card_html = (
        f'<div class="mimic-metric-card" '
        f'style="--mimic-accent: {accent};">'
        f'<div class="mimic-metric-icon">{icon}</div>'
        f'<div class="mimic-metric-value">{value}</div>'
        f'<div class="mimic-metric-label">{label}</div>'
        f'</div>'
    )

    st.markdown(
        card_html,
        unsafe_allow_html=True
    )


# ============================================================
# METRIC ROW
# ============================================================

def metric_row(columns, cards):
    """
    Render a row of metric cards across pre-created columns.

    Each card must contain:
        icon
        value
        label

    And may optionally contain:
        accent
    """

    for col, card in zip(columns, cards):

        with col:

            render_metric_card(
                icon=card["icon"],
                value=card["value"],
                label=card["label"],
                accent=card.get("accent")
            )
