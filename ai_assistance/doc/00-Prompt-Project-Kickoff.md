### PROJECT KICKOFF PROMPT — fastmcp-ollama
Author: Stefan Kuhn
Context: Cline + FastMCP + Ollama integration
Purpose: Initial orchestration prompt for the virtual development team (MCP servers)
Version: 2025-10-06-R4

---

We are restarting development of the open-source project **fastmcp-ollama**, an MCP server for Ollama built with
the FastMCP framework. The previous attempt moved too quickly into implementation. This time, we enforce clear phase
separation, testing discipline, and continuous documentation updates.

**Primary Objective**
- Deliver a minimal, working, and test-covered MVP for text-based MCP requests under Cline.
- After the MVP, expand functionality gradually using FastMCP and Ollama capabilities.

**QA Discipline**
All testing and documentation must follow `/ai_assistance/doc/QA-Checklist.md`.  
The QA Tester must ensure this checklist is completed and copied into `/project-tracking/progress.md`
at the end of every iteration before any new tasks start.

**Phase 1 — Problem Assessment & Planning (no coding)**
1) Collaborate with the user to agree on target functionality, priorities, and constraints for MVP.
2) Analyze FastMCP features (tools, resources, structured outputs, streaming, attachments).
3) Review Ollama capabilities and identify what is actually possible on both the company and private hosts.
4) Produce a concise feature map and obtain explicit user approval before any coding begins.

**Phase 2 — Design & Delegation**
1) Propose repository layout and high-level architecture.
2) Produce a `DelegationPlan` JSON with small, independent tasks mapped to roles.
3) Include at least:
   - one QA task that defines and executes tests, and
   - one documentation task that updates `/project-tracking` files.
4) Require user confirmation of the plan before implementation.

**Phase 3 — Implementation, Testing, and Coverage Gate**
1) Coding is done by `agentic-coder` and `code-generator`, not by the moderator.
2) QA designs and runs tests using pytest + coverage.py (pytest-cov).
3) Enforce a **quality gate**: **≥90% diff-coverage of changed lines** using a diff-coverage tool (e.g., `diff-cover`)
   against the main branch. Failing the gate blocks merge and triggers additional tests or refactors.
4) `senior-dev` reviews implementation quality and test completeness; only reviewed work proceeds.
5) Project Manager updates:
   - `/project-tracking/project_plan.md` (epics, stories, tasks)
   - `/project-tracking/tasks.md` (active board)
   - `/project-tracking/progress.md` (chronological log)
   - `/ai_assistance/doc/QA-Checklist.md` results copied into `progress.md`
   before new work begins.

**Guiding Principles**
- Working and test-covered > complete and perfect.
- Moderator coordinates, developers and QA execute.
- Keep increments small, reviewable, and documented.
- Use `mcp-ollama` only as a simple behavioral reference, not as a base.
- Expand scope only after passing tests and the diff-coverage gate.

Start **Phase 1: Problem Assessment & Planning.**
Discuss with the user which FastMCP and Ollama capabilities to target in the MVP and produce
a feature map for approval before implementation begins.
