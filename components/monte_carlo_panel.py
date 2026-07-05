import streamlit as st
import pandas as pd

from engines.monte_carlo import run_monte_carlo


def render_monte_carlo_panel(
    scores,
    dependency_graph,
):
    st.markdown("---")
    st.header("Monte Carlo Cascade Engine")

    intervention_surface = st.selectbox(
        "Monte Carlo Intervention Surface",
        list(scores.keys()),
        key="monte_carlo_surface",
    )

    iterations = st.slider(
        "Simulation Iterations",
        100,
        10000,
        1000,
        100,
        key="monte_carlo_iterations",
    )

    variation = st.slider(
        "Dependency Weight Variation",
        0.0,
        0.50,
        0.10,
        0.01,
        key="monte_carlo_variation",
    )

    improvement = st.slider(
        "Intervention Improvement",
        0.25,
        3.0,
        1.0,
        0.25,
        key="monte_carlo_improvement",
    )

    result = run_monte_carlo(
        scores=scores,
        dependency_graph=dependency_graph,
        intervention_surface=intervention_surface,
        iterations=iterations,
        variation=variation,
        improvement=improvement,
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Average Gain",
        f"+{result['average_gain']:.3f}",
    )

    c2.metric(
        "Best Case",
        f"+{result['best_gain']:.3f}",
    )

    c3.metric(
        "Worst Case",
        f"+{result['worst_gain']:.3f}",
    )

    c4.metric(
        "Iterations",
        result["iterations"],
    )

    st.markdown("### 95% Confidence Range")

    st.write(
        f"{result['confidence_low']:.3f} "
        f"→ "
        f"{result['confidence_high']:.3f}"
    )

    st.markdown("### Sensitivity Ranking")

    sensitivity_rows = [
        {
            "Surface": surface,
            "Average Perturbed Weight": weight,
        }
        for surface, weight in result["sensitivity"].items()
    ]

    if sensitivity_rows:
        sensitivity_rows.sort(
            key=lambda x: x["Average Perturbed Weight"],
            reverse=True,
        )

        st.dataframe(
            pd.DataFrame(sensitivity_rows),
            hide_index=True,
            width="stretch",
        )

    else:
        st.info(
            "No downstream sensitivity detected for selected surface."
        )

    with st.expander("Raw Monte Carlo Result"):
        st.json(result)

    return result