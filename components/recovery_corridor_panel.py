import streamlit as st

from components.recovery_corridor import build_corridor_sequence


def render_recovery_corridor_panel(plan):
    st.markdown("### Recovery Corridor Visualization")

    corridor_sequence = build_corridor_sequence(plan)

    for item in corridor_sequence:
        st.write(
            f"**{item['label']}** "
            f"— {item['status']} "
            f"({item['score']} / {item['max_score']})"
        )

        st.code(item["bar"])
        st.caption(item["explanation"])