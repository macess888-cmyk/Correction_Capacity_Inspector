from dataclasses import dataclass, field
from copy import deepcopy


@dataclass
class PlanningStep:
    step_number: int
    intervention: str
    improvement: float
    cost: float
    before_score: float
    after_score: float
    projected_state: dict
    cascade_trace: list = field(default_factory=list)


@dataclass
class InterventionPlan:
    budget: float
    total_cost: float
    initial_score: float
    final_score: float
    total_gain: float
    steps: list
    final_state: dict


class MultiStepInterventionPlanner:
    def __init__(self, dependency_graph, cascade_engine=None):
        self.dependency_graph = dependency_graph
        self.cascade_engine = cascade_engine

    def network_score(self, state):
        if not state:
            return 0.0
        return round(sum(state.values()), 2)

    def apply_intervention(self, state, target, improvement):
        new_state = deepcopy(state)
        new_state[target] = min(10.0, new_state.get(target, 0) + improvement)
        return new_state

    def apply_simple_cascade(self, state, target, improvement):
        new_state = deepcopy(state)
        trace = []

        if target not in self.dependency_graph:
            return new_state, trace

        for downstream, weight in self.dependency_graph[target].items():
            gain = improvement * weight
            before = new_state.get(downstream, 0)
            after = min(10.0, before + gain)
            new_state[downstream] = after

            trace.append({
                "from": target,
                "to": downstream,
                "weight": weight,
                "gain": round(gain, 2),
                "before": round(before, 2),
                "after": round(after, 2),
            })

        return new_state, trace

    def generate_candidates(self, state, improvement=1.0, cost=1.0):
        candidates = []

        for surface, value in state.items():
            if value < 10:
                candidates.append({
                    "target": surface,
                    "improvement": improvement,
                    "cost": cost,
                })

        return candidates

    def choose_best_step(self, state, remaining_budget):
        current_score = self.network_score(state)
        best = None

        for candidate in self.generate_candidates(state):
            if candidate["cost"] > remaining_budget:
                continue

            target = candidate["target"]
            improvement = candidate["improvement"]

            direct_state = self.apply_intervention(state, target, improvement)
            cascaded_state, trace = self.apply_simple_cascade(
                direct_state,
                target,
                improvement
            )

            after_score = self.network_score(cascaded_state)
            gain = after_score - current_score

            result = {
                "target": target,
                "improvement": improvement,
                "cost": candidate["cost"],
                "before_score": current_score,
                "after_score": after_score,
                "gain": gain,
                "state": cascaded_state,
                "trace": trace,
            }

            if best is None or gain > best["gain"]:
                best = result

        return best

    def generate_plan(self, initial_state, budget=4):
        state = deepcopy(initial_state)
        initial_score = self.network_score(state)
        remaining_budget = budget
        total_cost = 0
        steps = []
        step_number = 1

        while remaining_budget > 0:
            best_step = self.choose_best_step(state, remaining_budget)

            if best_step is None or best_step["gain"] <= 0:
                break

            planning_step = PlanningStep(
                step_number=step_number,
                intervention=best_step["target"],
                improvement=best_step["improvement"],
                cost=best_step["cost"],
                before_score=best_step["before_score"],
                after_score=best_step["after_score"],
                projected_state=best_step["state"],
                cascade_trace=best_step["trace"],
            )

            steps.append(planning_step)

            state = best_step["state"]
            remaining_budget -= best_step["cost"]
            total_cost += best_step["cost"]
            step_number += 1

        final_score = self.network_score(state)

        return InterventionPlan(
            budget=budget,
            total_cost=total_cost,
            initial_score=initial_score,
            final_score=final_score,
            total_gain=round(final_score - initial_score, 2),
            steps=steps,
            final_state=state,
        )