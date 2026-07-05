import streamlit as st

from components.explainability import explain_plan


def render_explainability_panel(
    plan,
    weighted_dependency_graph,
):
    st.markdown("---")
    st.markdown("### Explainability Engine")

    explanation = explain_plan(
        plan,
        weighted_dependency_graph,
    )

    st.info(explanation["summary"])

    e1, e2, e3 = st.columns(3)

    e1.metric("Direct Gain", f"+{explanation['direct_gain']:.2f}")
    e2.metric("Cascade Gain", f"+{explanation['cascade_gain']:.2f}")
    e3.metric("Total Gain", f"+{explanation['total_gain']:.2f}")

    if explanation["primary_surface"]:
        st.write(
            f"**Primary Intervention Surface:** "
            f"{explanation['primary_surface']}"
        )

    st.markdown("#### Affected Surfaces")

    if explanation["affected_surfaces"]:
        for surface in explanation["affected_surfaces"]:
            st.write(f"• {surface}")
    else:
        st.info("No affected downstream surfaces identified.")

    st.markdown("#### Dependency Path")

    if explanation["dependency_path"]:
        for item in explanation["dependency_path"]:
            st.write(
                f"{item['from']} → {item['to']} "
                f"(weight {item['weight']:.2f}) "
                f"+{item['gain']:.2f}"
            )
    else:
        st.info("No dependency path recorded.")

    st.markdown("#### Strongest Dependency")

    strongest = explanation["strongest_dependency"]

    if strongest:
        st.write(
            f"{strongest['from']} → "
            f"{strongest['to']} "
            f"(weight {strongest['weight']:.2f})"
        )
    else:
        st.info("No strongest dependency identified.")

    st.markdown("#### Assumptions")

    for assumption in explanation["assumptions"]:
        st.write(f"• {assumption}")

    st.markdown("#### Remaining Uncertainty")

    st.warning(explanation["uncertainty"])

    for reason in explanation["uncertainty_reasons"]:
        st.write(f"• {reason}")