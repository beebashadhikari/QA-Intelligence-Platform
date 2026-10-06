from google.genai import types


QA_TOOL_DECLARATIONS = [
    types.FunctionDeclaration(
        name="get_release",
        description=(
            "Get release readiness evidence for a specific release. "
            "Use this when the user asks whether a release is ready, "
            "release status, test execution summary, smoke status, "
            "regression status, or release blockers."
        ),
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "release_version": types.Schema(
                    type="STRING",
                    description="Release version such as 2.4.0",
                ),
            },
            required=["release_version"],
        ),
    ),

    types.FunctionDeclaration(
        name="get_defects",
        description=(
            "Get defect evidence for a specific release. "
            "Use this when the user asks about defects, severity, "
            "open defects, or defect risk."
        ),
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "release_version": types.Schema(
                    type="STRING",
                    description="Release version such as 2.4.0",
                ),
            },
            required=["release_version"],
        ),
    ),

    types.FunctionDeclaration(
        name="get_risk",
        description=(
            "Get risk analysis for modules in a specific release. "
            "Use this when the user asks which modules are risky, "
            "risk levels, risk scores, or areas requiring attention."
        ),
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "release_version": types.Schema(
                    type="STRING",
                    description="Release version such as 2.4.0",
                ),
            },
            required=["release_version"],
        ),
    ),

    types.FunctionDeclaration(
        name="get_recommendations",
        description=(
            "Get risk-based test recommendations for a release. "
            "Use this when the user asks what QA should test, "
            "what tests should be prioritized, or where QA should focus."
        ),
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "release_version": types.Schema(
                    type="STRING",
                    description="Release version such as 2.4.0",
                ),
            },
            required=["release_version"],
        ),
    ),

    types.FunctionDeclaration(
        name="get_quality_health",
        description=(
            "Get product quality health for a release. "
            "Use this when the user asks about overall product quality, "
            "quality score, quality health, or product health."
        ),
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "release_version": types.Schema(
                    type="STRING",
                    description="Release version such as 2.4.0",
                ),
            },
            required=["release_version"],
        ),
    ),

    types.FunctionDeclaration(
        name="get_release_decision",
        description=(
            "Get the deterministic release decision for a specific release. "
            "Use this when the user asks whether a release should proceed, "
            "why a release is READY, CONDITIONAL, NOT_READY, or BLOCKED, "
            "what is blocking the release, what risks remain, or what actions "
            "are required before release approval."
        ),
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "release_version": types.Schema(
                    type="STRING",
                    description="Release version such as 2.4.0",
                ),
            },
            required=["release_version"],
        ),
    ),
]


QA_TOOLS = [
    types.Tool(
        function_declarations=QA_TOOL_DECLARATIONS,
    )
]