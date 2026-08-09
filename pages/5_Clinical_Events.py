import streamlit as st
import pandas as pd

from src.data_loader import load_dataset
from src.clinical_events import (
    load_chartevents,
    load_labevents,
    chartevent_summary,
    lab_event_summary,
    chartevents_by_item,
    lab_events_by_item,
)

st.set_page_config(page_title="Clinical Events", layout="wide")

st.title("📈 Clinical Events")
st.caption("Laboratory and bedside clinical event activity")

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

chartevents = load_chartevents(load_dataset)
labevents = load_labevents(load_dataset)

# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

chart_summary = chartevent_summary(chartevents)
lab_summary = lab_event_summary(labevents)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Chart Events",
    f"{chart_summary['total_events']:,}"
)

col2.metric(
    "Chart Patients",
    chart_summary["unique_patients"]
)

col3.metric(
    "Lab Events",
    f"{lab_summary['total_lab_events']:,}"
)

col4.metric(
    "Lab Patients",
    lab_summary["unique_patients"]
)

st.divider()

# ------------------------------------------------------------
# CHART EVENTS
# ------------------------------------------------------------

st.subheader("Top Chart Event Items")

chart_items = chartevents_by_item(chartevents)

if isinstance(chart_items, pd.Series):
    chart_items = chart_items.reset_index()
    chart_items.columns = ["Item ID", "Events"]

st.dataframe(
    chart_items.head(20),
    use_container_width=True
)

# ------------------------------------------------------------
# LAB EVENTS
# ------------------------------------------------------------

st.subheader("Top Laboratory Items")

lab_items = lab_events_by_item(labevents)

if isinstance(lab_items, pd.Series):
    lab_items = lab_items.reset_index()
    lab_items.columns = ["Item ID", "Events"]

st.dataframe(
    lab_items.head(20),
    use_container_width=True
)

with st.expander("View clinical event summaries"):
    st.json({
        "chart_events": chart_summary,
        "lab_events": lab_summary,
    })
