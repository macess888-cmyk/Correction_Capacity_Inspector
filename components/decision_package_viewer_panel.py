import streamlit as st

from engines.decision_package_viewer import (
    list_decision_packages,
    load_decision_package,
)
from engines.decision_report import export_markdown_report


def render_decision_package_viewer_panel():
    st.markdown("---")
    st.header("Decision Package Viewer")

    packages = list_decision_packages()

    if not packages:
        st.info("No exported decision packages found.")
        return

    selected = st.selectbox(
        "Select Decision Package",
        packages,
        key="decision_package_selector",
    )

    package = load_decision_package(selected)

    st.markdown("### Dashboard")
    st.json(package.get("dashboard", {}))

    st.markdown("### Rationale")
    st.json(package.get("rationale", {}))

    st.markdown("### Scenario Comparison")
    st.json(package.get("scenarios", []))

    st.markdown("### Export Report")

    if st.button("Export Markdown Report"):
        filename = export_markdown_report(package)

        st.success(
            f"Markdown report exported: {filename}"
        )
