import os
from datetime import datetime


def build_markdown_report(
    package,
):
    dashboard = package.get("dashboard", {})
    rationale = package.get("rationale", {})
    scenarios = package.get("scenarios", [])
    cycle = package.get("cycle", {})
    cycle_completion = package.get("cycle_completion", {})
    cycle_risks = package.get("cycle_risks", [])
    cycle_recommendation = package.get("cycle_recommendation", {})

    lines = []

    lines.append("# Decision Package Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now().isoformat()}")
    lines.append("")

    lines.append("## Dashboard")
    lines.append("")
    for key, value in dashboard.items():
        lines.append(f"- **{key}:** {value}")

    lines.append("")
    lines.append("## Recommendation Rationale")
    lines.append("")
    lines.append(f"Recommended strategy: **{rationale.get('recommendation', 'Unknown')}**")
    lines.append("")

    lines.append("### Reasons")
    for reason in rationale.get("reasons", []):
        lines.append(f"- {reason}")

    lines.append("")
    lines.append("### Assumptions")
    for assumption in rationale.get("assumptions", []):
        lines.append(f"- {assumption}")

    lines.append("")
    lines.append("### Cautions")
    for caution in rationale.get("cautions", []):
        lines.append(f"- {caution}")

    lines.append("")
    lines.append("## Decision Cycle")
    lines.append("")
    if cycle:
        for stage, value in cycle.items():
            lines.append(f"### {stage}")
            lines.append("")
            lines.append(f"```text")
            lines.append(str(value))
            lines.append(f"```")
            lines.append("")
    else:
        lines.append("No decision cycle data available.")

    lines.append("")
    lines.append("## Cycle Completion")
    lines.append("")
    if cycle_completion:
        for key, value in cycle_completion.items():
            lines.append(f"- **{key}:** {value}")
    else:
        lines.append("No cycle completion data available.")

    lines.append("")
    lines.append("## Cycle Risks")
    lines.append("")
    if cycle_risks:
        for risk in cycle_risks:
            lines.append(
                f"- **{risk.get('severity', 'Unknown')}:** "
                f"{risk.get('risk', 'Unknown')} — "
                f"{risk.get('reason', '')}"
            )
    else:
        lines.append("No cycle risks available.")

    lines.append("")
    lines.append("## Cycle Recommendation")
    lines.append("")
    if cycle_recommendation:
        lines.append(
            f"- **Priority:** {cycle_recommendation.get('priority', 'Unknown')}"
        )
        lines.append(
            f"- **Recommendation:** {cycle_recommendation.get('recommendation', 'Unknown')}"
        )
        lines.append(
            f"- **Reason:** {cycle_recommendation.get('reason', '')}"
        )
    else:
        lines.append("No cycle recommendation available.")

    lines.append("")
    lines.append("## Scenario Comparison")
    lines.append("")

    if scenarios:
        headers = list(scenarios[0].keys())
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

        for scenario in scenarios:
            values = [
                str(scenario.get(header, ""))
                for header in headers
            ]
            lines.append("| " + " | ".join(values) + " |")
    else:
        lines.append("No scenarios available.")

    return "\n".join(lines)


def export_markdown_report(
    package,
    output_dir="exports",
):
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report = build_markdown_report(package)

    filename = os.path.join(
        output_dir,
        f"decision_report_{timestamp}.md",
    )

    with open(filename, "w", encoding="utf-8") as file:
        file.write(report)

    return filename