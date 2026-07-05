import streamlit as st

from engines.correction_topology import (
    get_topology,
    get_break_surfaces,
    previous_stage,
    next_stage,
    break_surfaces_for_stage,
)

from engines.correction_stage_metadata import (
    get_stage_metadata,
)


def render_correction_topology_panel():

    st.header("Correction Topology Explorer")

    st.caption(
        "Implementation-independent correction geometry."
    )

    st.markdown("---")
    st.subheader("Forward Topology")

    topology = get_topology()

    selected_stage = st.selectbox(
        "Inspect Stage",
        topology,
    )

    for stage in topology:
        st.write(stage)

        if stage != topology[-1]:
            st.markdown("⬇")

    st.markdown("---")
    st.subheader("Topology Navigation")

    previous = previous_stage(selected_stage)
    next_item = next_stage(selected_stage)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("Previous")
        st.success(previous) if previous else st.info("START")

    with col2:
        st.write("Current")
        st.warning(selected_stage)

    with col3:
        st.write("Next")
        st.success(next_item) if next_item else st.info("END")

    st.markdown("---")
    st.subheader("Break Surface Explorer")

    surfaces = get_break_surfaces()

    surface_names = [
        surface["name"]
        for surface in surfaces
    ]

    selected_surface_name = st.selectbox(
        "Inspect Break Surface",
        surface_names,
    )

    selected_surface = next(
        surface
        for surface in surfaces
        if surface["name"] == selected_surface_name
    )

    st.markdown(
        f"""
**{selected_surface['name']}**

Between:
{selected_surface['between'][0]}

↓

{selected_surface['between'][1]}

{selected_surface['description']}
"""
    )

    st.markdown("---")
    st.subheader("Stage Metadata")

    metadata = get_stage_metadata(selected_stage)

    st.write(f"**Purpose:** {metadata.get('purpose','')}")

    st.write("**Inputs**")
    st.write(metadata.get("inputs", []))

    st.write("**Outputs**")
    st.write(metadata.get("outputs", []))

    st.write("**Inspection Questions**")

    for question in metadata.get("questions", []):
        st.write(f"• {question}")

    st.markdown("### Connected Break Surfaces")

    connected_surfaces = break_surfaces_for_stage(selected_stage)

    if connected_surfaces:
        for surface in connected_surfaces:
            st.warning(
                f"{surface['name']}: "
                f"{surface['between'][0]} → {surface['between'][1]}"
            )
    else:
        st.info("No break surfaces directly connected to this stage.")

    st.info(
        """
Status

OBSERVED

NOT ESTABLISHED

UNKNOWN → HOLD
"""
    )