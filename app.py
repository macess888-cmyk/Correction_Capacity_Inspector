import streamlit as st

from pages.inspection import run_single_inspection
from pages.comparison import run_case_comparison
from pages.timeline import run_timeline_engine
from pages.forecast import run_forecast_engine
from pages.simulator import run_simulator
from pages.patterns import run_pattern_library
from pages.recovery import run_recovery_engine

st.set_page_config(
    page_title="Correction Capacity Inspector",
    layout="wide"
)

page = st.sidebar.selectbox(
    "Mode",
    [
        "Single Inspection",
        "Case Comparison",
        "Timeline Engine",
        "Forecast Engine",
        "Scenario Simulator",
        "Pattern Library",
        "Recovery Engine",
    ]
)

if page == "Single Inspection":
    run_single_inspection()

elif page == "Case Comparison":
    run_case_comparison()

elif page == "Timeline Engine":
    run_timeline_engine()

elif page == "Forecast Engine":
    run_forecast_engine()

elif page == "Scenario Simulator":
    run_simulator()

elif page == "Pattern Library":
    run_pattern_library()

elif page == "Recovery Engine":
    run_recovery_engine()