from models import Stage


def get_stage_registry():
    return [
        Stage(
            id="stage_reality",
            name="Reality",
            description="The underlying condition or event before signal formation.",
            status="Candidate",
            outputs=["Signals"],
            inspection_questions=[
                "What is being treated as real?",
                "What remains unobserved?",
                "What assumptions enter before signal formation?",
            ],
        ),
        Stage(
            id="stage_signals",
            name="Signals",
            description="Observable traces, indicators, or disturbances emerging from reality.",
            status="Candidate",
            inputs=["Reality"],
            outputs=["Localization"],
            dependencies=["Reality"],
            inspection_questions=[
                "Are signals visible?",
                "Are signals distorted?",
                "Are signals reproducible?",
            ],
        ),
    ]


def get_all_stages():
    return get_stage_registry()


def get_stage_by_name(name):
    for stage in get_stage_registry():
        if stage.name == name:
            return stage
    return None