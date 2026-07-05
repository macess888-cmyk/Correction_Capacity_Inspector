def classify_quality_score(score):
    if score >= 80:
        return "Strong"
    elif score >= 60:
        return "Developing"
    elif score >= 40:
        return "Weak"
    else:
        return "Critical"


def calculate_decision_quality(history):
    if not history:
        return {
            "quality_score": 0,
            "quality_state": "Unknown",
            "gain_trend": "Unknown",
            "uncertainty_state": "Unknown",
        }

    gains = [
        item.get("Projected Gain", 0)
        for item in history
    ]

    uncertainties = [
        item.get("Uncertainty", "Unknown")
        for item in history
    ]

    average_gain = sum(gains) / len(gains)

    low_uncertainty_count = uncertainties.count("Low")
    medium_uncertainty_count = uncertainties.count("Medium")
    high_uncertainty_count = uncertainties.count("High")

    uncertainty_score = (
        low_uncertainty_count * 100
        + medium_uncertainty_count * 60
        + high_uncertainty_count * 25
    ) / len(uncertainties)

    gain_score = min(100, max(0, average_gain * 10))

    quality_score = round(
        gain_score * 0.55
        + uncertainty_score * 0.45,
        2,
    )

    if len(gains) >= 2 and gains[0] > gains[-1]:
        gain_trend = "Improving"
    elif len(gains) >= 2 and gains[0] < gains[-1]:
        gain_trend = "Declining"
    else:
        gain_trend = "Stable"

    if high_uncertainty_count > low_uncertainty_count:
        uncertainty_state = "High uncertainty dominant"
    elif low_uncertainty_count >= high_uncertainty_count:
        uncertainty_state = "Low uncertainty dominant"
    else:
        uncertainty_state = "Mixed uncertainty"

    return {
        "quality_score": quality_score,
        "quality_state": classify_quality_score(quality_score),
        "gain_trend": gain_trend,
        "uncertainty_state": uncertainty_state,
    }