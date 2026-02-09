---
id: PHR-005-004
title: tasks-ui-polish-decomposition
stage: tasks
date: 2026-02-07
surface: claude-code
model: claude-opus-4-6
feature: 005-nextjs-ui-polish
branch: 005-nextjs-ui-polish
user: AKE
command: /sp.tasks
labels: [tasks, ui, decomposition, frontend]
links:
  spec: specs/005-nextjs-ui-polish/spec.md
  ticket: ""
  adr: ""
  pr: ""
files:
  - specs/005-nextjs-ui-polish/tasks.md
tests:
  - N/A (task generation phase)
---

## Prompt

/sp.tasks - Generate implementable task list for 005-nextjs-ui-polish feature based on plan.md, spec.md, research.md, data-model.md, and quickstart.md.

## Response snapshot

Generated 59 tasks across 9 phases organized by user story priority:
- Phase 1: Setup (3 tasks) - design token foundation
- Phase 2: Foundational (5 tasks) - blocking style prerequisites
- Phase 3: US1 Design System (10 tasks) - color token migration
- Phase 4: US2 Responsive Layout (6 tasks) - mobile nav, task cards, chat widget
- Phase 5: US3 Interaction States (9 tasks) - focus rings, hover, loading, disabled
- Phase 6: US4 Typography (6 tasks) - heading hierarchy, contrast, line-height
- Phase 7: US5 Polish (7 tasks) - border-radius normalization
- Phase 8: US6 Accessibility (7 tasks) - aria-live, emoji labels, keyboard nav
- Phase 9: Polish (6 tasks) - overflow handling, build validation, safety check

All 15 functional requirements (FR-001 through FR-015) mapped to specific tasks.
All 10 success criteria (SC-001 through SC-010) verifiable via final phase tasks.

## Outcome

- Impact: High - complete executable task list for UI elevation
- Tests: Not requested (manual visual verification)
- Files: tasks.md (59 tasks)
- Next prompts: /sp.implement
- Reflection: Good parallel opportunity identification - 5 user stories can run in parallel after Phase 2

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Format validation PASS (all tasks have checkbox, ID, story label, file paths)
- Prompt variant (if applicable): N/A
- Next experiment: N/A
