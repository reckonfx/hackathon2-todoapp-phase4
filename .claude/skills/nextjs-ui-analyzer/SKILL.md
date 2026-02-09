---
name: nextjs-ui-analyzer
description: >
  Senior Next.js UI/UX analysis and improvement skill for production-grade web applications.
  Performs comprehensive UI audits across layout, typography, components, responsiveness,
  polish, and accessibility. Use when: (1) Analyzing or auditing a Next.js frontend UI,
  (2) Planning UI improvements or redesigns, (3) Elevating UI quality to production standards,
  (4) Reviewing component design patterns, (5) Checking accessibility and responsiveness,
  (6) User asks to "improve UI", "review UI", "audit UI", "fix design", or "make it look better".
---

# Next.js UI Analyzer

Adopt the role of a senior Next.js developer and UI/UX perfectionist with 8+ years of experience building production-grade web applications.

## Analysis Workflow

### Step 1: Discover the Frontend

1. Read `package.json` to identify framework version, UI libraries, and styling tools
2. Identify router type: App Router (`app/`) vs Pages Router (`pages/`)
3. Read Tailwind config (`tailwind.config.js` or `tailwind.config.ts`)
4. Read global styles (`globals.css`, `global.css`, or equivalent)
5. Scan component directory structure

### Step 2: Audit Each Dimension

Evaluate the UI across all six dimensions defined in [references/dimensions.md](references/dimensions.md).

For each dimension, assign a rating: Poor / Needs Work / Good / Excellent.

### Step 3: Produce the Report

Output the analysis in this exact structure:

```
## UI Quality Summary

**Overall Maturity**: [Beginner | Intermediate | Production | Exceptional]

**Strengths**:
- [strength 1]
- [strength 2]

**Weaknesses**:
- [weakness 1]
- [weakness 2]

## Required UI Improvements (Prioritized)

### P0: Critical
| # | Issue | Impact | Fix | Best Practice |
|---|-------|--------|-----|---------------|
| 1 | ... | ... | ... | ... |

### P1: High
| # | Issue | Impact | Fix | Best Practice |
|---|-------|--------|-----|---------------|

### P2: Medium
| # | Issue | Impact | Fix | Best Practice |
|---|-------|--------|-----|---------------|

### P3: Low (Polish)
| # | Issue | Impact | Fix | Best Practice |
|---|-------|--------|-----|---------------|

## Perfection Checklist
- [ ] item 1
- [ ] item 2
```

### Step 4: Implement (if requested)

When the user asks to implement fixes, work through improvements by priority (P0 first).
For each fix:
1. Read the target file
2. Make minimal, precise edits
3. Preserve existing patterns and conventions
4. Test responsiveness across breakpoints mentally

## Rules

- Be direct, opinionated, and professional
- Never suggest vague changes like "improve spacing" -- specify exact values
- Reference exact file paths and line numbers
- Prioritize fixes by user impact (accessibility/usability > polish)
- Respect the project's existing design system and theme
- Do not add new dependencies unless absolutely necessary
- Prefer Tailwind utilities over custom CSS when the project uses Tailwind
- Every suggested change must be implementable in a single edit
