def corridor_status(score, max_score=30):
    ratio = score / max_score

    if ratio >= 0.80:
        return "Open", "Healthy recovery corridor"
    elif ratio >= 0.60:
        return "Stable", "Recovery corridor remains usable"
    elif ratio >= 0.40:
        return "Narrowing", "Recovery corridor is under pressure"
    elif ratio >= 0.20:
        return "Closing", "Recovery corridor is near collapse"
    else:
        return "Collapsed", "Recovery corridor has effectively collapsed"


def corridor_bar(score, max_score=30, width=20):
    ratio = max(0, min(score / max_score, 1))
    filled = int(ratio * width)
    empty = width - filled

    return "█" * filled + "░" * empty


def corridor_snapshot(label, score, max_score=30):
    status, explanation = corridor_status(score, max_score)
    bar = corridor_bar(score, max_score)

    return {
        "label": label,
        "score": round(score, 2),
        "max_score": max_score,
        "status": status,
        "bar": bar,
        "explanation": explanation,
    }


def build_corridor_sequence(plan, max_score=30):
    sequence = []

    sequence.append(
        corridor_snapshot(
            "Current",
            plan.initial_score,
            max_score,
        )
    )

    for step in plan.steps:
        sequence.append(
            corridor_snapshot(
                f"After Step {step.step_number}",
                step.after_score,
                max_score,
            )
        )

    sequence.append(
        corridor_snapshot(
            "Final Projection",
            plan.final_score,
            max_score,
        )
    )

    return sequence