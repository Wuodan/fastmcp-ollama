### PROJECT KICKOFF PROMPT — fastmcp-ollama
Author: Stefan Kuhn
Context: Cline + FastMCP + Ollama integration
Purpose: Initial orchestration prompt for the virtual development team (MCP servers)
Version: 2025-10-05

---

We are starting development of the open-source project **fastmcp-ollama** — an advanced, extensible MCP server for
Ollama, implemented with the FastMCP framework.

The project’s purpose is to build a reliable, understandable, and practical reference implementation of an MCP
server for Ollama — not a theoretical showcase. The first goal is to get a minimal viable version working quickly,
then expand functionality step by step as experience and confidence grow.

**Overall Objective**
fastmcp-ollama should become a clean and modular implementation that:
- Implements useful FastMCP functionality early, not necessarily all at once.
- Exposes Ollama’s capabilities (models, streaming, tools, image and multimodal processing) through the MCP interface.
- Works end-to-end with text-based interactions first, adding image and multimodal features later.
- Demonstrates what **Cline, FastMCP, and Ollama** can accomplish together once core functionality is proven.

**Your Mission**
1. **Analyze** what FastMCP currently supports (tools, resources, structured outputs, streaming, attachments, etc.)
   and what Ollama provides as a backend (models, vision, embeddings, function calling).
2. **Identify** which of these features are essential for a minimal viable implementation that works reliably under Cline.
3. **Plan** short, achievable iterations — always aiming for a working, testable end-to-end result.
4. **Output** a `DelegationPlan` JSON assigning tasks to specific team members defined in the systemPrompt.
5. **Design** a simple, logical repository structure for source, tests, Dockerfile, and example configs.
6. **Document** findings and plans to `/project-tracking/project_plan.md` and progress to `/project-tracking/progress.md`.

**Guiding Principles**
- Working and useful always comes before complete and perfect.
- Cline is the coordination layer; FastMCP is the framework; Ollama is the backend.
- Keep iterations small, tested, and reviewable.
- Use `mcp-ollama` as a simple working reference, not as a base.
- Maintain clean, modular, and well-tested code.
- Expand scope only when the existing version is stable and valuable.

Start **Phase 1: Exploration and Planning.**
Inspect FastMCP documentation, identify core features to include in the first MVP of fastmcp-ollama, and produce
your first DelegationPlan for initial implementation.
