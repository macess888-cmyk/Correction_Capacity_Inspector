PATTERN_LIBRARY = {

    "Authority Vacuum": {
        "authority": (0, 2),
        "decision": (0, 3),
        "description":
            "The system can observe and decide but lacks sufficient authority to act."
    },

    "Evidence Collapse": {
        "evidence": (0, 2),
        "signal": (2, 5),
        "description":
            "Signals exist but evidence quality is too weak for reliable decisions."
    },

    "Time Compression": {
        "time": (0, 2),
        "description":
            "Correction windows are closing faster than the system can respond."
    },

    "Preservation Over Correction": {
        "willingness": (0, 2),
        "authority": (3, 5),
        "description":
            "The system has capacity but repeatedly preserves the current state instead of correcting it."
    },

    "Recovery Corridor Collapse": {
        "time": (0, 1),
        "authority": (0, 2),
        "decision": (0, 2),
        "description":
            "Multiple correction surfaces have weakened, leaving little remaining capacity to alter trajectory."
    },

}

def detect_patterns(
    signal,
    evidence,
    decision,
    authority,
    time,
    willingness,
):

    matches = []

    values = {
        "signal": signal,
        "evidence": evidence,
        "decision": decision,
        "authority": authority,
        "time": time,
        "willingness": willingness,
    }

    for name, pattern in PATTERN_LIBRARY.items():

        matched = True

        for key, rule in pattern.items():

            if key == "description":
                continue

            low, high = rule

            if not (low <= values[key] <= high):
                matched = False

        if matched:
            matches.append(
                {
                    "pattern": name,
                    "description": pattern["description"],
                }
            )

    return matches