# ============================================================
# MIMIC PATIENT ANALYTICS
# SHARED VISUAL THEME
# ============================================================
#
# A small, self-contained design system used by app.py and the
# dashboard pages. Centralizing it here means every page can
# opt into the same look with two lines of code, and the theme
# only has to be tuned in one place.
#
# Design direction:
#   - Deep clinical navy, not pure black — closer to a hospital
#     monitor bay than a generic "dark mode" default.
#   - Teal ("vitals") as the primary accent, with violet, amber,
#     rose, and sky as supporting accents for variety across KPI
#     cards.
#   - IBM Plex Sans for headings, IBM Plex Mono for big numbers —
#     a clinical-instrument, data-readout feel.
#   - A hand-drawn ECG waveform is the one signature visual
#     element, used deliberately and sparingly, because vital-sign
#     waveforms are literally the chartevents data this dashboard
#     analyzes.

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

# Cycled across KPI cards so a row of metrics reads as a set,
# not eight identical boxes.
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
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@500;600;700&family=IBM+Plex+Mono:wght@500;600;700&display=swap');

.mimic-eyebrow {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: {COLORS["teal"]};
    margin-bottom: 0.6rem;
}}

.mimic-hero-title {{
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 700;
    font-size: 2.6rem;
    line-height: 1.15;
    color: {COLORS["text"]};
    margin: 0 0 0.6rem 0;
}}

.mimic-hero-subtitle {{
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 1.05rem;
    font-weight: 500;
    color: {COLORS["muted"]};
    max-width: 46rem;
    line-height: 1.6;
    margin: 0;
}}

.mimic-metric-card {{
    background: {COLORS["panel"]};
    border: 1px solid {COLORS["panel_border"]};
    border-left: 3px solid var(--mimic-accent, {COLORS["teal"]});
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    height: 100%;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}}

.mimic-metric-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 26px rgba(0, 0, 0, 0.35);
}}

.mimic-metric-icon {{
    font-size: 1.3rem;
    opacity: 0.9;
    margin-bottom: 0.5rem;
}}

.mimic-metric-value {{
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    font-size: 1.65rem;
    color: {COLORS["text"]};
    line-height: 1.2;
}}

.mimic-metric-label {{
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: {COLORS["muted"]};
    margin-top: 0.25rem;
}}

.mimic-section-title {{
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 600;
    font-size: 1.1rem;
    color: {COLORS["text"]};
    margin: 0 0 0.9rem 0;
}}

.mimic-nav-icon {{
    font-size: 1.6rem;
}}

.mimic-nav-title {{
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 600;
    font-size: 1.02rem;
    color: {COLORS["text"]};
    margin: 0.4rem 0 0.15rem 0;
}}

.mimic-nav-desc {{
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.85rem;
    color: {COLORS["muted"]};
    line-height: 1.45;
    margin-bottom: 0.6rem;
}}

@media (prefers-reduced-motion: reduce) {{
    .mimic-metric-card {{
        transition: none;
    }}
}}
</style>
"""


def inject_theme():
    """
    Inject the shared CSS once at the top of a page.
    Safe to call on every page — Streamlit re-renders the
    <style> block per page load, and class names are
    namespaced with a `mimic-` prefix to avoid colliding
    with Streamlit's own DOM.
    """

    st.markdown(_CUSTOM_CSS, unsafe_allow_html=True)


# ============================================================
# ECG WAVEFORM — SIGNATURE ELEMENT
# ============================================================

def ecg_divider(accent=None, cycles=10, height=34):
    """
    Render a hand-built ECG waveform as an inline SVG divider.

    This is the dashboard's one signature visual: a vital-sign
    waveform, because that is literally what the underlying
    chartevents data represents.
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
                x0=x0 + 0,
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

    svg = f"""
    <div style="width:100%; overflow:hidden; margin: 0.4rem 0 1.4rem 0;">
        <svg
            viewBox="0 0 {total_width} {height}"
            preserveAspectRatio="none"
            width="100%"
            height="{height}"
        >
            <path
                d="{path_d}"
                fill="none"
                stroke="{accent}"
                stroke-width="1.6"
                stroke-linejoin="round"
                stroke-linecap="round"
                opacity="0.85"
            />
        </svg>
    </div>
    """

    return svg


# ============================================================
# HERO HEADER
# ============================================================

def render_hero(eyebrow, title, subtitle, accent=None):
    """
    Render the page hero: eyebrow label, title, subtitle,
    followed by the ECG signature divider.
    """

    accent = accent or COLORS["teal"]

    st.markdown(
        f"""
        <div class="mimic-eyebrow">{eyebrow}</div>
        <div class="mimic-hero-title">{title}</div>
        <p class="mimic-hero-subtitle">{subtitle}</p>
        """,
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
    Render one KPI card as styled HTML. Place inside an
    st.columns() cell:

        with col:
            render_metric_card("🏨", "275", "Admissions", accent="#38BDF8")
    """

    accent = accent or COLORS["teal"]

    st.markdown(
        f"""
        <div class="mimic-metric-card" style="--mimic-accent: {accent}">
            <div class="mimic-metric-icon">{icon}</div>
            <div class="mimic-metric-value">{value}</div>
            <div class="mimic-metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def metric_row(columns, cards):
    """
    Render a row of metric cards across pre-created columns.

    Parameters
    ----------
    columns : list of st.columns() cells
    cards : list of dicts, each with keys:
        icon, value, label, and optionally accent
    """

    for col, card in zip(columns, cards):
        with col:
            render_metric_card(
                icon=card["icon"],
                value=card["value"],
                label=card["label"],
                accent=card.get("accent")
            )
