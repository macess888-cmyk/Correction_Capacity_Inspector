import pandas as pd
import streamlit as st

from engines.decision_memory_index import (
    search_memory_index,
)


def render_decision_memory_panel():
    st.markdown("---")
    st.header("Decision Memory Index")

    query = st.text_input(
        "Search decision memory",
        key="decision_memory_search",
    )

    results = search_memory_index(query)

    if not results:
        st.info("No matching decision memory found.")
        return []

    st.dataframe(
        pd.DataFrame(results).drop(columns=["search_text"]),
        hide_index=True,
        width="stretch",
    )

    return results