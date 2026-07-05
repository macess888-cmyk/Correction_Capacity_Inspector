def check_cycle_completion(cycle):
    stages = {
        "Observation": cycle.observation,
        "Reasoning": cycle.reasoning,
        "Planning": cycle.planning,
        "Execution": cycle.execution,
        "Learning": cycle.learning,
    }

    results = {}

    for stage, data in stages.items():
        complete = bool(data)

        results[stage] = {
            "complete": complete,
            "status": "Complete" if complete else "Missing",
        }

    total = len(results)
    completed = sum(
        1
        for item in results.values()
        if item["complete"]
    )

    completion_percent = round(
        completed / total * 100,
        1,
    )

    return {
        "stages": results,
        "completed": completed,
        "total": total,
        "completion_percent": completion_percent,
    }