# QA Intelligence Skills Pack

Portable AI-agent skills for the QA Intelligence Platform.

These skills are designed to work with AI agents that can load
instruction files and access the QA Intelligence Platform API.

---

## Core Principle

AI assists. Evidence decides.

The QA Intelligence Platform API is the source of truth for:

- release quality
- test execution intelligence
- risk intelligence
- defects
- release readiness
- recommendations

AI agents must not invent evidence that is unavailable from the platform.

---

## Skills

### senior_qa

General senior QA engineering methodology.

Use this as the foundational QA reasoning skill.

---

### test_intelligence

Determines which tests should be executed first.

Uses:

- test score
- risk level
- test status
- business criticality
- defect evidence
- change evidence
- historical execution evidence

File:

skills/test_intelligence/SKILL.md

---

### risk_intelligence

Analyzes release and module risk.

File:

skills/risk_intelligence/SKILL.md

---

### release_decision

Explains whether a release is:

- READY
- CONDITIONAL
- NOT_READY

File:

skills/release_decision/SKILL.md

---

### qa_agent

Orchestrates the complete QA analysis workflow.

It combines:

- release intelligence
- test intelligence
- risk intelligence
- defect intelligence
- quality health
- release decision

File:

skills/qa_agent/SKILL.md

---

## API

The skills are designed to work with the following API:

### Release

GET /api/releases/{release_version}

### Test Intelligence

GET /api/releases/{release_version}/recommendations

### Risk Intelligence

GET /api/releases/{release_version}/risk

### Quality

GET /api/releases/{release_version}/quality

### Defects

GET /api/releases/{release_version}/defects

### Release Intelligence

GET /api/releases/{release_version}/intelligence

### Dashboard

GET /api/dashboard/release/{release_version}

### Agent

POST /api/agent/analyze

---

## Release Context

The release version is the shared context for all analysis.

Example:

2.4.0

All API calls used during one analysis must refer to the same
release unless the user explicitly requests a comparison.

---

## Evidence Model

Agents should distinguish:

FACT

Directly returned by the platform.

INFERENCE

Reasoning derived from available evidence.

MISSING EVIDENCE

Information required but unavailable.

RECOMMENDATION

An action proposed based on evidence.

---

## Human Decision

The AI agent does not own the final release decision.

The QA or release owner remains responsible for approval.

---

## Vendor Neutrality

This skills pack is intentionally vendor-neutral.

The same skills can be adapted for:

- Gemini
- OpenCode
- Claude Code
- Cursor
- custom AI agents
- internal enterprise agents

The skill instructions should remain stable.

Only the agent-specific loading and tool configuration should change.

---

## Architecture

```text
                 QA Intelligence Platform
                          |
                          | REST API
                          |
              +-----------+-----------+
              |                       |
          Evidence                  Skills
              |                       |
              +-----------+-----------+
                          |
                     AI Agent
                          |
          +---------------+---------------+
          |               |               |
        Gemini         OpenCode        Other AI