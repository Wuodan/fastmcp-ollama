### QA & Documentation Checklist — fastmcp-ollama

Every iteration must pass this checklist before new work starts.

---

#### Code Quality
- [ ] All new and changed files include unit tests.
- [ ] Integration tests cover every new or modified tool.
- [ ] All tests pass with `pytest` (no skipped tests left).
- [ ] Code passes linting (`ruff`) and type checking (`mypy`).

#### Test Coverage
- [ ] Run: pytest --cov=fastmcp_ollama --cov-report=term-missing --cov-branch
- [ ] Generate diff coverage:
      diff-cover coverage.xml --compare-branch=main
- [ ] **Result must show ≥ 90% coverage on changed lines.**
- [ ] Any uncovered lines must be justified in `progress.md`.

#### Documentation
- [ ] `/project-tracking/project_plan.md` updated with new or completed stories.
- [ ] `/project-tracking/tasks.md` synchronized with latest DelegationPlan.
- [ ] `/project-tracking/progress.md` appended with:
      - Date and iteration summary
      - Features and fixes implemented
      - Test results and diff coverage percentage
      - Reviewer(s) and QA confirmation

#### Sign-off
- [ ] QA Tester confirms all checks complete.
- [ ] Senior Developer approves code and test quality.
- [ ] Project Manager records completion in `progress.md` and announces next planning phase.
