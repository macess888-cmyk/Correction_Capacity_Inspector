def recommendation(surface):

    recommendations = {

        "Signal Visibility":
            (
                "Improve monitoring and increase observability. "
                "The system cannot correct what it cannot reliably see."
            ),

        "Evidence Integrity":
            (
                "Strengthen evidence collection and validation. "
                "Poor evidence reduces confidence in every downstream decision."
            ),

        "Decision Capacity":
            (
                "Clarify decision ownership and reduce decision bottlenecks."
            ),

        "Authority To Act":
            (
                "Ensure responsible actors have explicit authority to intervene."
            ),

        "Remaining Time":
            (
                "Reduce delay and intervene earlier before the recovery corridor closes."
            ),

        "Correction Willingness":
            (
                "Address incentives, culture, or governance barriers preventing action."
            ),

    }

    return recommendations.get(
        surface,
        "No recommendation available."
    )