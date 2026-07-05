def assess_cycle_risk(
    cycle_completion,
    dashboard,
    quality,
    adaptive,
):
    risks = []

    if cycle_completion["completion_percent"] < 100:
        risks.append(
            {
                "risk": "Incomplete decision cycle",
                "severity": "High",
                "reason": "One or more cycle stages are missing.",
            }
        )

    if dashboard.get("uncertainty") == "High":
        risks.append(
            {
                "risk": "High model uncertainty",
                "severity": "High",
                "reason": "Confidence range is wide.",
            }
        )

    if quality.get("quality_state") in ["Weak", "Critical"]:
        risks.append(
            {
                "risk": "Weak decision quality",
                "severity": "High",
                "reason": "Historical decision quality is weak.",
            }
        )

    if adaptive.get("priority") == "High":
        risks.append(
            {
                "risk": "High-priority adaptive concern",
                "severity": "Medium",
                "reason": adaptive.get("recommendation", ""),
            }
        )

    if not risks:
        risks.append(
            {
                "risk": "No major cycle risks detected",
                "severity": "Low",
                "reason": "Cycle appears structurally stable.",
            }
        )

    return risks