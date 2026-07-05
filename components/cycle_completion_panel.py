import pandas as pd
import streamlit as st

from engines.cycle_completion import check_cycle_completion


def render_cycle_completion_panel(cycle):
    st.markdown("---")
    st.header("Cycle Completion")

    result = check_cycle_completion(cycle)

    c1, c2 = st.columns(2)

    c1.metric(
        "Completion",
        f"{result['completion_percent']}%",
    )

    c2.metric(
        "Stages Complete",
        f"{result['completed']} / {result['total']}",
    )

    rows = []

    for stage, info in result["stages"].items():
        rows.append(
            {
                "Stage": stage,
                "Status": info["status"],
            }
        )

    st.dataframe(
        pd.DataFrame(rows),
        hide_index=True,
        width="stretch",
    )

    if result["completion_percent"] == 100:
        st.success("Decision cycle is complete.")
    else:
        st.warning("Decision cycle has missing stages.")

    return result