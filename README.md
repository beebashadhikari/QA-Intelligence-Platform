# QA Intelligence Platform

**AI-assisted QA engineering platform for evidence-driven release analysis, risk intelligence, test recommendations, defect analysis, quality health, and MCP-powered QA workflows.**

> **Core principle: AI assists. Evidence decides.**

---

## Overview

The **QA Intelligence Platform** is an AI-assisted quality engineering platform designed to help QA engineers, developers, and release teams understand the quality state of a software release using real platform evidence.

Instead of allowing an AI model to freely generate QA conclusions, the platform combines:

* Deterministic QA intelligence
* Structured release and test data
* Risk analysis
* Defect intelligence
* Quality health analysis
* Release decision logic
* Reusable QA reasoning skills
* AI-assisted analysis
* MCP tools for external AI clients

The goal is to make AI useful for QA while keeping evidence, traceability, and human ownership at the center of release decisions.

---

## Core Principle

### AI assists. Evidence decides.

The platform is designed around an important rule:

> AI should reason over available QA evidence, not invent evidence that does not exist.

The system distinguishes between:

* **FACT** — directly supported by platform data
* **INFERENCE** — reasoned conclusion based on available evidence
* **MISSING EVIDENCE** — information required but not currently available
* **RECOMMENDATION** — suggested QA action based on the evidence

The AI must not invent:

* Test results
* Defects
* Risk scores
* Release status
* Historical incidents
* Performance results
* Approval decisions

Final release approval remains the responsibility of the human QA or release owner.

---

# What the Platform Does

The platform provides several QA intelligence capabilities.

### Release Readiness

Provides a consolidated view of release quality using:

* Total test cases
* Passed tests
* Failed tests
* Blocked tests
* Open defects
* Defect severity
* Regression status
* Smoke status
* Quality indicators
* Release decision signals

### Test Execution Intelligence

Analyzes test execution results and identifies:

* Execution health
* Failure patterns
* Blocked areas
* Regression concerns
* Test coverage signals
* Areas requiring additional investigation

### Risk-Based Test Recommendations

Prioritizes QA testing using evidence such as:

* Code changes
* Historical defects
* Failed tests
* Affected functionality
* Business criticality
* Existing risk signals

The objective is to help QA engineers determine **which tests should be executed first**.

### Defect Intelligence

Analyzes defects by:

* Severity
* Status
* Functional area
* Release impact
* Concentration of defects
* Risk implications

### Quality Health

Produces an overall quality-health view based on available QA evidence.

### Release Decision Intelligence

Combines release evidence into a structured release decision signal.

The system can identify states such as:

* Ready
* Conditional
* Not Ready

However, the platform does **not** replace the human release decision.

### AI QA Agent

The AI agent orchestrates the platform's QA intelligence capabilities and produces an evidence-based QA analysis.

### MCP Integration

The platform exposes QA intelligence through an MCP server so external AI clients can use the QA capabilities.

The MCP integration has been tested with:

* MCP Inspector
* OpenCode

---

# Architecture

```text
                         QA Intelligence Platform
                                      |
                 +--------------------+--------------------+
                 |                                         |
             QA REST API                              QA Skills
                 |                                         |
                 |                          +--------------+--------------+
                 |                          |              |              |
                 |                     Senior QA      Risk          Release
                 |                     Intelligence  Intelligence    Decision
                 |                          |              |              |
                 |                          +--------------+--------------+
                 |                                         |
                 +--------------------+--------------------+
                                      |
                               AI / MCP Layer
                                      |
                     +----------------+----------------+
                     |                                 |
                Python AI                         MCP Server
                   Agent                              :8001
                     |                                 |
                     |                         +-------+-------+
                     |                         |               |
                     |                      OpenCode       Inspector
                     |
                     +---------------> QA REST API :8000
```

---

# Technology Stack

### Backend

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* SQLite
* Pydantic
* Pytest

### AI

* Gemini API
* Python AI Agent
* Evidence-driven QA reasoning

### MCP

* MCP server
* MCP Inspector
* OpenCode

### Frontend

* React
* TypeScript

### QA Skills

Reusable QA reasoning skills stored under:

```text
skills/
```

---

# Project Structure

```text
QA-Intelligence-Platform/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── ...
│   │
│   ├── mcp/
│   │   └── server.py
│   │
│   ├── tests/
│   │
│   ├── create_db.py
│   └── seed_data.py
│
├── frontend/
│
├── skills/
│   ├── senior_qa/
│   ├── test_intelligence/
│   ├── risk_intelligence/
│   ├── release_decision/
│   └── qa_agent/
│
├── .env.example
├── .gitignore
├── opencode.json
├── requirements.txt
└── README.md
```

---

# Prerequisites

Before running the project, install:

* Python 3.12+
* Git
* Node.js / npm if working with the frontend
* A Gemini API key if AI functionality is required
* OpenCode if you want to use the MCP integration
* MCP Inspector if you want to inspect and test MCP tools

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/beebashadhikari/QA-Intelligence-Platform.git
cd QA-Intelligence-Platform
```

---

## 2. Create a Python virtual environment

On Windows using Git Bash:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/Scripts/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

---

## 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

The platform uses environment variables for local configuration.

This allows the API and MCP server addresses to be changed without modifying source code.

## 1. Create your local `.env`

Copy the example configuration:

```bash
cp .env.example .env
```

On Windows Command Prompt, you can also create the file manually by copying `.env.example` to `.env`.

---

## 2. Configure environment variables

The example configuration looks like:

```env
QA_API_BASE_URL=http://127.0.0.1:8000

MCP_HOST=127.0.0.1
MCP_PORT=8001

GEMINI_API_KEY=your_gemini_api_key_here
```

### QA_API_BASE_URL

Defines the base URL used by the MCP layer to communicate with the QA API.

Example:

```env
QA_API_BASE_URL=http://127.0.0.1:8000
```

This can be changed if the QA API is running on another host or port.

### MCP_HOST

Defines the network interface used by the MCP server.

Example:

```env
MCP_HOST=127.0.0.1
```

### MCP_PORT

Defines the port used by the MCP server.

Example:

```env
MCP_PORT=8001
```

### GEMINI_API_KEY

Your Gemini API key used for AI functionality.

```env
GEMINI_API_KEY=your_actual_key
```

**Never commit your real API key to GitHub.**

The `.env` file is intentionally excluded from version control.

---

# Database Setup

The platform uses SQLite for local development.

Create the database:

```bash
python -m backend.create_db
```

Seed the development/test data:

```bash
python -m backend.seed_data
```

The database is local development data and is intentionally excluded from Git.

---

# Running the QA API

Start the FastAPI backend:

```bash
uvicorn backend.app.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

---

# Running the MCP Server

In a separate terminal, activate the virtual environment and run:

```bash
python -m backend.mcp.server
```

The MCP server will normally run on:

```text
http://127.0.0.1:8001/mcp
```

The MCP server uses the environment variables:

```env
MCP_HOST=127.0.0.1
MCP_PORT=8001
```

This makes the MCP server configurable without changing the Python source code.

---

# MCP Tools

The MCP server exposes QA intelligence tools including:

| Tool                       | Purpose                                           |
| -------------------------- | ------------------------------------------------- |
| `get_release`              | Retrieve release information                      |
| `get_test_recommendations` | Recommend tests based on risk and evidence        |
| `get_risk`                 | Analyze functional risk                           |
| `get_defects`              | Analyze release defects                           |
| `get_quality_health`       | Evaluate overall quality health                   |
| `get_release_decision`     | Generate structured release decision intelligence |

These tools allow external AI clients to interact with the QA Intelligence Platform.

---

# MCP Inspector

MCP Inspector can be used to manually inspect and test the available MCP tools.

Connect Inspector to:

```text
http://127.0.0.1:8001/mcp
```

Once connected, you can test the available tools against a release such as:

```text
2.4.0
```

The MCP tools should return evidence from the QA platform rather than fabricated information.

---

# OpenCode Integration

The project includes an OpenCode MCP configuration.

The MCP server can be configured as:

```json
{
  "mcp": {
    "servers": {
      "qa-intelligence-platform": {
        "type": "remote",
        "url": "http://127.0.0.1:8001/mcp"
      }
    }
  }
}
```

After the MCP server is running, OpenCode can connect to the QA Intelligence Platform and use its MCP tools.

---

# QA Skills

The project includes reusable QA reasoning skills.

```text
skills/
├── senior_qa/
│   └── SKILL.md
│
├── test_intelligence/
│   └── SKILL.md
│
├── risk_intelligence/
│   └── SKILL.md
│
├── release_decision/
│   └── SKILL.md
│
└── qa_agent/
    └── SKILL.md
```

## Senior QA Skill

Provides senior-level QA reasoning principles and evidence-driven analysis.

## Test Intelligence

Focuses on test execution analysis and identifying testing priorities.

## Risk Intelligence

Analyzes risk based on available release and testing evidence.

## Release Decision

Evaluates release readiness using the platform's quality evidence.

## QA Agent

Acts as the master orchestration skill.

The QA Agent combines:

1. Release context
2. Release evidence
3. Test intelligence
4. Risk intelligence
5. Defect analysis
6. Quality health
7. Release decision intelligence
8. QA actions
9. Missing evidence

The final release decision remains with the human QA/release owner.

---

# Evidence Model

The platform uses four important evidence categories.

### FACT

Information directly supported by platform data.

Example:

```text
FACT:
231 of 248 tests passed.
```

### INFERENCE

A reasoned conclusion based on available evidence.

Example:

```text
INFERENCE:
The payment workflow represents an elevated regression concern
because it has significant change and failure signals.
```

### MISSING EVIDENCE

Information required for stronger decision-making but not available.

Example:

```text
MISSING EVIDENCE:
No performance testing evidence is currently available.
```

### RECOMMENDATION

An action suggested based on the evidence.

Example:

```text
RECOMMENDATION:
Execute payment regression tests before release approval.
```

This distinction is important because the AI should never present an inference as a fact.

---

# AI QA Agent

The platform includes an AI analysis endpoint.

Example request:

```bash
curl -X POST http://127.0.0.1:8000/api/agent/analyze \
  -H "Content-Type: application/json" \
  -d '{"release_version":"2.4.0","message":"Perform a complete QA analysis. Identify the biggest risks, recommend which tests QA should execute first, and identify missing evidence. Do not invent evidence."}'
```

The agent can analyze:

* Release quality
* Test execution
* Risks
* Defects
* Quality health
* Release decision
* Test priorities
* Missing evidence
* Recommended QA actions

---

# Example QA Analysis

For a release such as `2.4.0`, the platform can combine:

```text
Release
   ↓
Test execution
   ↓
Defects
   ↓
Risk analysis
   ↓
Quality health
   ↓
Release decision
   ↓
QA recommendations
```

The resulting analysis should clearly distinguish evidence from reasoning.

For example:

```text
FACT
248 total tests
231 passed
9 failed
8 blocked

FACT
4 defects identified
2 high-severity defects

INFERENCE
Payment and authentication areas require additional QA attention.

RECOMMENDATION
Prioritize the highest-risk regression scenarios.

MISSING EVIDENCE
Performance testing evidence is unavailable.

HUMAN DECISION
Final release approval remains with the QA/release owner.
```

---

# Testing

Run the automated test suite with:

```bash
pytest
```

The project has been validated against the implemented QA intelligence functionality.

Tests cover areas including:

* Release schemas
* Release metrics
* Defect analysis
* Risk analysis
* Test recommendations
* Release analysis
* Release decision logic
* Quality intelligence

---

# Security

Do not commit sensitive information.

The following should remain local:

```text
.env
*.db
*.sqlite
.venv/
__pycache__/
```

The repository provides:

```text
.env.example
```

instead of exposing real credentials.

Before deploying the platform outside local development:

* Use secure secrets management
* Rotate exposed credentials
* Restrict network access
* Use HTTPS
* Configure authentication
* Review MCP access controls
* Avoid exposing development services directly to the public internet

---

# Development Philosophy

This project is designed around evidence-driven QA rather than unrestricted AI-generated conclusions.

The AI layer should:

* Reason over evidence
* Explain uncertainty
* Identify missing information
* Prioritize testing
* Support QA engineers
* Avoid hallucinating results
* Preserve human decision ownership

The platform should not be treated as an autonomous release approval system.

---

# Current Scope

The current version focuses on:

* QA intelligence
* Release analysis
* Risk-based testing
* Defect analysis
* Quality health
* Release decision support
* AI-assisted QA reasoning
* MCP integration
* Reusable QA skills

It is primarily designed for local development, experimentation, and QA intelligence workflows.

---

# Troubleshooting

## Virtual environment activation fails

If PowerShell activation is blocked, Git Bash can be used:

```bash
source .venv/Scripts/activate
```

---

## API is not reachable

Verify the API is running:

```bash
uvicorn backend.app.main:app --reload
```

Then test:

```bash
curl http://127.0.0.1:8000/health
```

---

## MCP server is not reachable

Verify the MCP server is running:

```bash
python -m backend.mcp.server
```

Then verify the endpoint:

```bash
curl http://127.0.0.1:8001/mcp
```

A response indicating a missing MCP session ID can still indicate that the endpoint itself is alive.

---

## MCP cannot connect to the QA API

Check:

```env
QA_API_BASE_URL=http://127.0.0.1:8000
```

Make sure the QA API is actually running on the configured host and port.

---

## Gemini functionality is not working

Check that `.env` contains a valid:

```env
GEMINI_API_KEY=your_actual_key
```

Do not commit the key.

---

# Release

Current stable release:

**v1.0.0**

Repository:

https://github.com/beebashadhikari/QA-Intelligence-Platform

---

# Future Improvements

Potential future development includes:

* PostgreSQL support
* Authentication and authorization
* CI/CD integration
* GitHub/GitLab integration
* Jira integration
* Automated test result ingestion
* Historical trend analysis
* Production incident intelligence
* Performance testing intelligence
* Advanced dashboard analytics
* Containerized deployment
* Cloud deployment
* Enhanced MCP security
* More AI QA skills

---

# Contributing

Contributions, ideas, improvements, and QA engineering feedback are welcome.

When contributing:

1. Create a feature branch.
2. Make focused changes.
3. Add or update tests where appropriate.
4. Run the test suite.
5. Document important behavior changes.
6. Submit a pull request.

---

# License

Add an appropriate open-source license before distributing the project under a specific open-source license.

---

## Final Principle

> **AI assists. Evidence decides. Humans own the final release decision.**
