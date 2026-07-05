import streamlit as st

from orchestrators.observation_pipeline import run_observation_pipeline
from orchestrators.reasoning_pipeline import run_reasoning_pipeline
from orchestrators.cycle_pipeline import run_cycle_pipeline
from orchestrators.reporting_pipeline import run_reporting_pipeline
from orchestrators.memory_pipeline import (
    run_memory_pipeline,
)
from orchestrators.decision_intelligence_pipeline import (
    run_decision_intelligence_pipeline,
)
from orchestrators.planning_pipeline import (
    run_planning_pipeline,
)
from orchestrators.visualization_pipeline import (
    run_visualization_pipeline,
)
from orchestrators.analysis_pipeline import (
    run_analysis_pipeline,
)

from config.dependency_graph import WEIGHTED_DEPENDENCY_GRAPH


def run_simulator():

    observation = run_observation_pipeline()

    before_scores = observation["before_scores"]
    after_scores = observation["after_scores"]

    before_values = observation["before_values"]
    after_values = observation["after_values"]

    weighted_dependency_graph = WEIGHTED_DEPENDENCY_GRAPH

    analysis = run_analysis_pipeline(
        before_scores,
        after_scores,
    )

    run_visualization_pipeline(
        before_values,
        after_values,
        after_scores,
        weighted_dependency_graph,
    )

    reasoning = run_reasoning_pipeline(after_scores)

    planning = run_planning_pipeline(
        before_scores,
        after_scores,
        weighted_dependency_graph,
    )

    plan = planning["plan"]
    monte_result = planning["monte_result"]
    sensitivity_rows = planning["sensitivity_rows"]
    active_scenarios = planning["active_scenarios"]

    decision = run_decision_intelligence_pipeline(
        plan,
        monte_result,
        sensitivity_rows,
        active_scenarios,
    )

    dashboard = decision["dashboard"]
    rationale = decision["rationale"]

    memory = run_memory_pipeline()

    history = memory["history"]
    trends = memory["trends"]
    quality = memory["quality"]
    learning = memory["learning"]
    adaptive = memory["adaptive"]
    memory_recommendation = memory["memory_recommendation"]

    cycle = run_cycle_pipeline(
        dashboard,
        rationale,
        trends,
        quality,
        learning,
        adaptive,
        memory_recommendation,
    )

    decision_cycle = cycle["decision_cycle"]
    cycle_completion = cycle["cycle_completion"]
    cycle_risks = cycle["cycle_risks"]
    cycle_recommendation = cycle["cycle_recommendation"]

    run_reporting_pipeline(
        dashboard,
        rationale,
        active_scenarios,
        decision_cycle,
        cycle_completion,
        cycle_risks,
        cycle_recommendation,
    )