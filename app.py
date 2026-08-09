import streamlit as st

st.set_page_config(
    page_title="MIMIC Patient Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏥 MIMIC Patient Analytics")

st.markdown(
    """
    ## Clinical Data Analytics Dashboard

    An interactive analytics platform built on MIMIC-IV clinical data.

    Use the **sidebar** to explore:

    - 👥 Patient demographics
    - 🏥 Admissions
    - 🫀 ICU analytics
    - 📈 Clinical events
    - 💊 Medications
    - 🧬 Diagnoses
    - 🧪 Data quality
    - 🕒 Patient timelines
    """
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Patients", "100")

with col2:
    st.metric("Admissions", "275")

with col3:
    st.metric("ICU Stays", "140")

st.divider()

st.info(
    "Select an analysis page from the sidebar to begin exploring the dataset."
)
