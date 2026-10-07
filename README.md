# QA Intelligence Platform




An AI-assisted QA engineering platform that combines deterministic QA intelligence, reusable QA skills, REST APIs, MCP tools, and AI agents to support evidence-driven release analysis.

> **Core principle: AI assists. Evidence decides.**

---

## What This Platform Does

The QA Intelligence Platform helps QA engineers and release teams analyze release quality using real platform evidence.

It provides:

- Release readiness analysis
- Test execution intelligence
- Risk-based test recommendations
- Defect intelligence
- Quality health analysis
- Release decision intelligence
- AI-assisted QA analysis
- MCP tools for external AI clients
- Reusable QA reasoning skills

The platform does **not** allow the AI to invent QA evidence.

---

## Architecture

```text
                         QA Intelligence Platform
                                  |
              +-------------------+-------------------+
              |                                       |
          QA REST API                            QA Skills
              |                                       |
              |                              +--------+--------+
              |                              |        |        |
              |                         Senior QA  Risk   Release
              |                              |      Intel. Decision
              |                              +--------+--------+
              |                                       |
              +-------------------+-------------------+
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
                 +-------------> QA API :8000
## Configuration

The platform supports environment-based configuration for the QA API and MCP server.

Create a local `.env` file based on `.env.example`:

```bash
cp .env.example .env
