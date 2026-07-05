from dataclasses import dataclass


@dataclass
class Scenario:
    name: str
    scores: dict
    planner_result: object = None
    monte_carlo_result: dict = None
    notes: str = ""


class ScenarioLab:
    def __init__(self):
        self.scenarios = []

    def add(self, scenario):
        self.scenarios.append(scenario)

    def names(self):
        return [scenario.name for scenario in self.scenarios]

    def get(self, name):
        for scenario in self.scenarios:
            if scenario.name == name:
                return scenario

        return None