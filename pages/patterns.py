import streamlit as st

from components.patterns import PATTERN_LIBRARY


def run_pattern_library():
    st.title("Pattern Library")
    st.subheader("Known governability failure archetypes")

    st.markdown("---")

    for name, pattern in PATTERN_LIBRARY.items():
        st.header(name)

        st.write(pattern["description"])

        st.markdown("**Detection Rules**")

        for key, value in pattern.items():
            if key == "description":
                continue

            low, high = value
            st.write(f"- {key}: {low} to {high}")

        st.markdown("---")