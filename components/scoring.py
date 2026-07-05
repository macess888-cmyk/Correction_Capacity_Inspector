def interpret_score(score, max_score=30):
    if score >= 26:
        return (
            "RECOVERABLE",
            "Correction capacity appears strong. The system likely has enough visibility, evidence, authority, willingness, and time to alter trajectory."
        )
    elif score >= 19:
        return (
            "RECOVERY WINDOW OPEN",
            "Correction capacity exists, but some surfaces are weakening. Intervention should happen before the loop compounds."
        )
    elif score >= 12:
        return (
            "RECOVERY WINDOW CLOSING",
            "Correction capacity is degraded. The system may still see the problem but may struggle to act quickly enough."
        )
    else:
        return (
            "COMPOUNDING FAILURE RISK",
            "Correction capacity is weak. The system may be losing the ability to perceive, decide, or intervene before consequence hardens."
        )


def risk_state_from_score(score, max_score=30):
    failure_risk = max_score - score

    if failure_risk <= 5:
        risk_state = "LOW"
    elif failure_risk <= 12:
        risk_state = "MODERATE"
    elif failure_risk <= 18:
        risk_state = "HIGH"
    else:
        risk_state = "CRITICAL"

    return failure_risk, risk_state


def trajectory_quadrant(capacity_score, willingness_score):
    if capacity_score >= 20 and willingness_score >= 4:
        return (
            "HIGH CAPACITY / HIGH WILLINGNESS",
            "Recoverable. The system can likely see, decide, act, and absorb correction costs."
        )
    elif capacity_score >= 20 and willingness_score < 4:
        return (
            "HIGH CAPACITY / LOW WILLINGNESS",
            "Preservation over correction risk. The system may see the problem but avoid absorbing correction costs."
        )
    elif capacity_score < 20 and willingness_score >= 4:
        return (
            "LOW CAPACITY / HIGH WILLINGNESS",
            "Support needed. Willingness exists, but the system lacks enough evidence, authority, visibility, or time."
        )
    else:
        return (
            "LOW CAPACITY / LOW WILLINGNESS",
            "Compounding failure risk. The system may lack both ability and willingness to correct."
        )


def preservation_risk_from_choice(choice):
    if choice == "YES":
        return "HIGH"
    elif choice == "PARTIALLY":
        return "MODERATE"
    elif choice == "NO":
        return "LOW"
    return "UNKNOWN"