---
id: PHR-005-001
title: spec-nextjs-ui-polish
stage: spec
date: 2026-02-07
surface: claude-code
model: claude-opus-4-6
feature: 005-nextjs-ui-polish
branch: 005-nextjs-ui-polish
user: AKE
command: /sp.specify
labels: [spec, ui, nextjs, polish, accessibility]
links:
  spec: specs/005-nextjs-ui-polish/spec.md
  ticket: ""
  adr: ""
  pr: ""
files:
  - specs/005-nextjs-ui-polish/spec.md
  - specs/005-nextjs-ui-polish/checklists/requirements.md
tests:
  - N/A (specification phase)
---

## Prompt

/sp.specify - Next.js UI analyzer skill: Evaluate the current UI of the Next.js application and produce a safe, high-confidence UI improvement plan that fixes UI bugs and inconsistencies, improves visual quality and polish, elevates UI to production-grade standards, without altering core functionality or backend behavior. Evaluation scope covers UI bugs, layout/alignment, design system quality, interaction/polish, accessibility, and maintainability.

## Response snapshot

Generated comprehensive specification for Next.js UI Production Polish (005-nextjs-ui-polish) with:
- 6 prioritized user stories (P1: design system consistency + responsive layouts; P2: interaction states + typography; P3: polish/micro-interactions + accessibility)
- 15 functional requirements covering color tokens, mobile nav, interaction states, border-radius scale, loading states, typography hierarchy, responsive tables, chat widget, WCAG contrast, reduced-motion, status indicators, aria-labels, text overflow, neon effect reduction, and hover transform restraint
- 10 measurable success criteria with verification methods
- 5 documented assumptions
- Strict safety constraints: UI-only changes, no backend modifications
- Quality checklist passed all validation items

## Outcome

- Impact: High - provides actionable roadmap for UI elevation
- Tests: N/A (specification phase)
- Files: spec.md, checklists/requirements.md
- Next prompts: /sp.clarify or /sp.plan
- Reflection: Feature description was comprehensive; no clarification markers needed due to clear scope constraints

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Checklist validation PASS (all items checked)
- Prompt variant (if applicable): N/A
- Next experiment: N/A
