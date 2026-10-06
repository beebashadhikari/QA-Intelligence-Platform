from pathlib import Path
import json


SKILL_PATH = (
    Path(__file__).resolve().parents[3]
    / "skills"
    / "senior_qa"
    / "SKILL.md"
)


def load_senior_qa_skill() -> str:
    if not SKILL_PATH.exists():
        raise FileNotFoundError(
            f"Senior QA skill was not found at: {SKILL_PATH}"
        )

    return SKILL_PATH.read_text(
        encoding="utf-8",
    )


def build_qa_prompt(
    user_request: str,
    release_version: str,
    evidence: dict,
) -> str:

    skill = load_senior_qa_skill()

    evidence_json = json.dumps(
        evidence,
        indent=2,
        default=str,
    )

    prompt = (
        f"{skill}\n\n"

        "## Current User Request\n\n"
        f"{user_request}\n\n"

        "## Release Under Analysis\n\n"
        f"{release_version}\n\n"

        "## Initial QA Context\n\n"
        "The following information is available "
        "without using a tool.\n\n"
        f"{evidence_json}\n\n"

        "## Tool Usage Rules\n\n"

        "You have access to controlled QA tools.\n\n"

        "Use tools when additional QA evidence is "
        "required to answer the user's request.\n\n"

        "Choose tools based on the user's actual question. "
        "Do not call every tool automatically.\n\n"

        "Available tools provide:\n"
        "- release readiness evidence\n"
        "- defect evidence\n"
        "- module risk analysis\n"
        "- risk-based test recommendations\n"
        "- product quality health\n\n"

        "Use only the available QA tools.\n"
        "Do not invent tool results.\n"
        "Do not assume evidence that has not been provided.\n"
        "You may call multiple tools when necessary.\n"
        "Do not call tools unnecessarily.\n\n"

        "## Evidence Rules\n\n"

        "Treat tool results as authoritative QA evidence.\n\n"

        "Separate your reasoning into four categories:\n"
        "1. FACT - directly supported by tool results or "
        "explicit user input.\n"
        "2. INFERENCE - a conclusion reasonably derived "
        "from available evidence.\n"
        "3. MISSING EVIDENCE - information required for a "
        "stronger conclusion but not available.\n"
        "4. RECOMMENDATION - an action based on the evidence.\n\n"

        "Never convert an inference into a fact.\n"
        "Never invent missing evidence.\n"
        "Never invent risk scores.\n"
        "Never assume a failed test is automatically a "
        "product defect.\n\n"

        "## Confidence Rules\n\n"

        "Confidence must reflect evidence completeness.\n\n"

        "HIGH confidence:\n"
        "Use only when the available evidence is strong, "
        "consistent, and sufficient for the specific question.\n\n"

        "MEDIUM confidence:\n"
        "Use when the available evidence supports the "
        "conclusion but important evidence is missing.\n\n"

        "LOW confidence:\n"
        "Use when important evidence is unavailable, "
        "contradictory, stale, or insufficient.\n\n"

        "If important quality dimensions such as performance "
        "testing, production incident history, or relevant "
        "environment evidence are unavailable, do not claim "
        "HIGH confidence for a broad release-quality assessment "
        "unless the available evidence is demonstrably sufficient "
        "for the specific question.\n\n"

        "## Recommendation Rules\n\n"

        "Recommendations must be actionable and evidence-based.\n\n"

        "When a test is blocked because of an unavailable "
        "environment, dependency, configuration, or test data, "
        "do not simply recommend executing the same test again. "
        "Recommend resolving the blocking condition and then "
        "rerunning the affected test.\n\n"

        "When a test has failed, consider possible causes "
        "including product defects, automation problems, test "
        "data, environment problems, configuration, "
        "infrastructure, dependencies, or flakiness.\n\n"

        "Recommendations should prioritize areas where multiple "
        "risk signals overlap, such as business criticality, "
        "recent changes, high-severity defects, failed tests, "
        "blocked tests, or instability.\n\n"

        "## Release Decision Rules\n\n"

        "Do not determine release readiness from pass rate alone.\n\n"

        "Consider available evidence including:\n"
        "- critical defects\n"
        "- high-severity defects\n"
        "- smoke status\n"
        "- regression status\n"
        "- failed tests\n"
        "- blocked tests\n"
        "- test stability\n"
        "- recent changes\n"
        "- business criticality\n"
        "- module risk\n"
        "- quality health\n"
        "- missing evidence\n\n"

        "A conditional release must clearly explain what "
        "conditions or risks remain.\n\n"

        "Final release approval always remains a human decision.\n\n"

        "## Final Output\n\n"

        "After gathering the evidence you need, "
        "return ONLY valid JSON.\n\n"

        "Do not use Markdown.\n"
        "Do not wrap the JSON in code fences.\n"
        "Do not add explanations before or after the JSON.\n\n"

        "The JSON must contain exactly these fields:\n\n"

        "{\n"
        '  "assessment": "short overall conclusion",\n'
        '  "status": "READY | CONDITIONAL | NOT_READY | BLOCKED",\n'
        '  "facts": ["fact 1", "fact 2"],\n'
        '  "risks": [\n'
        "    {\n"
        '      "module": "module name",\n'
        '      "level": "LOW | MEDIUM | HIGH",\n'
        '      "score": 0.0,\n'
        '      "reason": "why this module is risky"\n'
        "    }\n"
        "  ],\n"
        '  "recommendations": [\n'
        "    {\n"
        '      "action": "recommended action",\n'
        '      "reason": "why it is recommended",\n'
        '      "priority": "LOW | MEDIUM | HIGH"\n'
        "    }\n"
        "  ],\n"
        '  "missing_evidence": ["missing evidence 1"],\n'
        '  "confidence": "HIGH | MEDIUM | LOW",\n'
        '  "human_decision": "what requires human judgment"\n'
        "}\n\n"

        "## Final Validation Rules\n\n"

        "Before returning the JSON, verify:\n"
        "- Every fact is supported by evidence.\n"
        "- Every risk is supported by evidence.\n"
        "- Every score comes from a tool result or "
        "explicit evidence.\n"
        "- Every recommendation follows from evidence.\n"
        "- Blocked tests are handled according to their "
        "blocking condition.\n"
        "- Missing evidence is explicitly listed.\n"
        "- Confidence matches evidence completeness.\n"
        "- Human release approval is not replaced by AI.\n"
    )

    return prompt