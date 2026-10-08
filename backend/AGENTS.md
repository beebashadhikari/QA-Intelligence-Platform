# QA Intelligence Platform

You are working inside the QA Intelligence Platform.

## Core Principle

AI assists.

Evidence decides.

Never invent QA evidence.

## QA Skills

The project contains reusable QA skills (paths relative to the
repository root):

- `skills/senior_qa/SKILL.md`
- `skills/test_intelligence/SKILL.md`
- `skills/risk_intelligence/SKILL.md`
- `skills/release_decision/SKILL.md`
- `skills/qa_agent/SKILL.md`

Use the relevant skill instructions when performing QA analysis.

For complete release analysis, use:

`skills/qa_agent/SKILL.md`

The QA Agent skill orchestrates:

- release intelligence
- test intelligence
- risk intelligence
- defect intelligence
- quality health
- release decision

## QA Evidence

The QA platform is the source of truth.

Use available QA MCP tools when evidence is required.

Available QA evidence includes:

- release information
- test recommendations
- risk analysis
- defects
- quality health
- release decision

Never invent:

- test results
- defects
- risk scores
- release status
- execution history

## Reasoning

Separate conclusions into:

- FACT
- INFERENCE
- MISSING EVIDENCE
- RECOMMENDATION

Never present an inference as a fact.

## Release Analysis

When asked whether a release is ready:

1. Verify release context.
2. Retrieve release evidence.
3. Review test intelligence.
4. Review risk intelligence.
5. Review defects.
6. Review quality health.
7. Review release decision.
8. Identify evidence gaps.
9. Provide prioritized QA recommendations.
10. Keep final release approval with the human QA/release owner.

Do not determine readiness from pass rate alone.

## MCP

Use the configured QA MCP server for live QA evidence.

Do not replace live evidence with assumptions.