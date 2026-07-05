import streamlit as st

from components.dependency_engine import (
    calculate_dependency_effects,
    weakest_surface,
    strongest_surface,
)
from components.leverage import calculate_leverage
from components.cascade import simulate_cascade
from components.optimizer import optimize_intervention
from utils.optimizer_export import save_optimization_plan


def run_reasoning_pipeline(after_scores):
    st.markdown("---")
    st.header("Dependency Engine")

    dependency_map = calculate_dependency_effects(after_scores)

    weakest_name, weakest_value = weakest_surface(after_scores)
    strongest_name, strongest_value = strongest_surface(after_scores)

    st.write(f"**Weakest Surface:** {weakest_name} ({weakest_value} / 5)")
    st.write(f"**Strongest Surface:** {strongest_name} ({strongest_value} / 5)")

    st.markdown("### Dependency Effects")

    for surface, info in dependency_map.items():
        affects = info["affects"]

        if affects:
            st.write(f"**{surface}** influences:")
            for target, weight in affects.items():
                st.write(f"• {target} (weight {weight:.2f})")
        else:
            st.write(f"**{surface}** has no downstream dependency.")

    st.markdown("---")
    st.header("Leverage Point Analyzer")

    leverage_points = calculate_leverage(after_scores)

    for item in leverage_points:
        downstream_text = (
            ", ".join(
                [
                    f"{target} ({weight:.2f})"
                    for target, weight in item["downstream"].items()
                ]
            )
            if item["downstream"]
            else "None"
        )

        st.write(
            f"**{item['surface']}** "
            f"| current score: {item['current_score']} / 5 "
            f"| leverage score: {item['leverage_score']} "
            f"| downstream weight: {item['downstream_weight']:.2f} "
            f"| downstream: {downstream_text}"
        )

    if leverage_points:
        top_leverage = leverage_points[0]
        st.info(
            f"Highest leverage intervention surface: "
            f"{top_leverage['surface']}"
        )

    st.markdown("---")
    st.header("Cascade Simulation Engine")

    cascade_surface = st.selectbox(
        "Intervention Surface",
        list(after_scores.keys()),
    )

    cascade_improvement = st.slider(
        "Improvement Amount",
        0.0,
        3.0,
        1.0,
        0.25,
    )

    cascaded_scores = simulate_cascade(
        after_scores,
        cascade_surface,
        cascade_improvement,
    )

    base_total = sum(after_scores.values())
    cascaded_total = sum(cascaded_scores.values())
    cascade_gain = cascaded_total - base_total

    st.metric("Base Network Score", f"{base_total:.2f} / 30")
    st.metric("Cascaded Network Score", f"{cascaded_total:.2f} / 30")
    st.metric("Cascade Gain", f"{cascade_gain:.2f}")

    st.markdown("### Cascaded Surface Scores")

    for surface, value in cascaded_scores.items():
        original = after_scores[surface]
        delta = value - original

        st.write(
            f"**{surface}:** "
            f"{original:.2f} → {value:.2f} "
            f"({delta:+.2f})"
        )

    st.markdown("---")
    st.header("Intervention Optimizer")

    optimization_budget = st.slider(
        "Optimization Budget",
        1.0,
        5.0,
        3.0,
        0.5,
    )

    optimization = optimize_intervention(
        after_scores,
        optimization_budget,
    )

    if optimization:
        best = optimization[0]

        st.success(f"Best intervention: {best['surface']}")

        st.metric(
            "Projected Network Gain",
            f"{best['gain']:.2f}",
        )

        st.markdown("### Ranked Intervention Options")

        for option in optimization:
            st.write(
                f"**{option['surface']}** "
                f"→ projected gain: {option['gain']:.2f}"
            )

        st.markdown("---")

        if st.button("Save Optimization Plan"):
            filename = save_optimization_plan(
                optimization_budget,
                best,
                optimization,
            )

            st.success(f"Optimization saved to: {filename}")

    else:
        st.info("No optimization options available.")

    return {
        "dependency_map": dependency_map,
        "leverage_points": leverage_points,
        "cascaded_scores": cascaded_scores,
        "optimization": optimization,
    }