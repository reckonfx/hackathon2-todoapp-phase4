# Implementation Plan: Next.js UI Production Polish

**Branch**: `005-nextjs-ui-polish` | **Date**: 2026-02-07 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/005-nextjs-ui-polish/spec.md`

## Summary

Elevate the Next.js frontend UI from an intermediate-quality prototype to production-grade standards by: (1) unifying the dual color palette into a coherent token system (indigo/blue for light, gold/black for dark), (2) fixing responsive breakage (mobile nav, task table, chat widget), (3) adding complete interaction states across all components, (4) normalizing typography hierarchy, (5) taming animations for professional restraint, and (6) closing accessibility gaps. All changes are strictly visual - zero backend modifications.

## Technical Context

**Language/Version**: TypeScript 5.5, React 19, Next.js 15 (Pages Router)
**Primary Dependencies**: Tailwind CSS 4.1, PostCSS 8.5, Axios 1.7 (no new deps)
**Storage**: N/A (UI-only, no storage changes)
**Testing**: Manual visual inspection, Playwright (existing), browser DevTools audit
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge), viewport 320px-1440px+
**Project Type**: Web application (frontend-only changes)
**Performance Goals**: LCP < 2.5s, CLS < 0.1, no layout shifts from styling changes
**Constraints**: Zero backend file modifications, preserve all API contracts and routes
**Scale/Scope**: ~15 frontend files modified (styles + components + pages), 0 backend files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Spec-First Development
- [x] Is there a corresponding feature specification in `specs/`? (specs/005-nextjs-ui-polish/spec.md)
- [x] Does this plan directly address the requirements in the spec? (FR-001 through FR-015 mapped below)

### II. No Manual Coding
- [x] Is the implementation strategy designed for agent execution? (All changes describable as file edits)
- [x] Are we avoiding any manual code generation? (Claude Code executes all changes)

### III. Reusable Intelligence
- [x] Are new capabilities abstracted into reusable skills? (nextjs-ui-analyzer skill created)
- [x] Is behavior separated from execution tools? (Skill provides analysis framework, not code)

### IV. Deterministic Architecture
- [x] Are the outputs and behaviors predictable and testable? (Visual changes verifiable by inspection)
- [x] Is there any hidden or implicit logic? (No - purely visual CSS/JSX changes)

### V. Progressive Evolution
- [x] Does this implementation build on the previous phase without skipping steps? (Enhances Phase III frontend, no phase skip)
- [x] Is forward compatibility maintained? (UI changes don't affect Phase IV deployment)

### VI. Phase-Specific Constraints
- N/A: This feature is a cross-cutting UI improvement that modifies only frontend visual presentation. It does not violate Phase IV deployment-only scope because it does not modify backend/infrastructure. Phase IV's "Application: Frontend feature changes PROHIBITED" (15.5) is about functional changes; this spec explicitly constrains to visual-only changes (no new features, no logic changes).

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Frontend file modification during Phase IV | UI polish is visual-only, not a feature change. No backend, API, or schema modifications. SC-009 validates safety. | Deferring to Phase V would leave the UI in an inconsistent state for Kubernetes demos. |

## Project Structure

### Documentation (this feature)

```text
specs/005-nextjs-ui-polish/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0: design token research
├── data-model.md        # Phase 1: design token schema
├── quickstart.md        # Phase 1: implementation quickstart
└── checklists/
    └── requirements.md  # Spec quality checklist
```

### Source Code (files to be modified)

```text
frontend/
├── src/
│   ├── styles/
│   │   └── globals.css           # Design tokens, reduced-motion, unified states
│   ├── components/
│   │   ├── Layout/
│   │   │   └── MainLayout.tsx    # Mobile nav, token colors, overflow handling
│   │   ├── chat/
│   │   │   ├── ChatBubbleWidget.tsx  # Responsive popup sizing
│   │   │   ├── ChatContainer.tsx     # Aria-live, emoji labels
│   │   │   ├── ChatBubble.tsx        # Token colors
│   │   │   ├── ChatInput.tsx         # Focus states
│   │   │   ├── ChatMessageList.tsx   # Aria-live region
│   │   │   ├── VoiceInput.tsx        # Focus states
│   │   │   └── chat.module.css       # Token references, reduced-motion
│   │   ├── Auth/
│   │   │   ├── Login.tsx             # Focus rings, token colors
│   │   │   └── Register.tsx          # Focus rings, token colors
│   │   ├── TaskForm.tsx              # Focus rings, loading states
│   │   └── TaskList.tsx              # Mobile card layout, overflow, badges
│   └── pages/
│       ├── index.tsx                 # Heading hierarchy, toned animations, token colors
│       ├── dashboard.tsx             # Stat cards, heading levels, responsive table
│       ├── chat.tsx                  # Heading levels, token colors
│       ├── login.tsx                 # Token colors
│       └── register.tsx              # Token colors
└── tailwind.config.js               # (may need minor token extension)
```

**Structure Decision**: Frontend-only modifications within the existing Pages Router architecture. No new files created except documentation artifacts.

## Design Decisions

### DD-1: Dual-Palette Token Architecture (FR-001)

**Decision**: Extend the existing CSS custom property system to fully cover both palettes.

**Current state**: Partial token coverage. The `:root` and `[data-theme='dark']` blocks define ~20 variables but components still use hardcoded hex values (e.g., `from-indigo-600`, `text-blue-300`, `bg-gradient-to-br from-blue-900/30`).

**Target state**: All color references in component JSX use either:
- Tailwind classes mapped to CSS variables (e.g., `text-brand`, `bg-brand-light`)
- CSS variable references in custom classes (e.g., `var(--brand-primary)`)

**Token additions needed**:
```css
:root {
  /* Light mode: indigo/blue accent palette */
  --accent-primary: #4f46e5;      /* indigo-600 */
  --accent-secondary: #7c3aed;    /* violet-600 */
  --accent-light: #eef2ff;        /* indigo-50 */
  --accent-gradient-from: #4f46e5;
  --accent-gradient-to: #7c3aed;
  --accent-shadow: rgba(79, 70, 229, 0.3);
}

[data-theme='dark'] {
  /* Dark mode: gold accent palette */
  --accent-primary: #d4af37;
  --accent-secondary: #f4c430;
  --accent-light: rgba(212, 175, 55, 0.2);
  --accent-gradient-from: #d4af37;
  --accent-gradient-to: #f4c430;
  --accent-shadow: rgba(212, 175, 55, 0.3);
}
```

**Impact**: FR-001, SC-001. Enables per-theme consistency without cross-theme leakage.

### DD-2: Mobile Navigation Strategy (FR-002)

**Decision**: Add a hamburger menu toggle that reveals a slide-down mobile nav panel on viewports below 768px.

**Rationale**: Simpler than a sidebar drawer. Uses existing nav links, just changes their visibility and layout. No new routes or functionality.

**Implementation**:
- Add a `useState` toggle in `MainLayout.tsx` for mobile menu open/close
- Hamburger icon button visible only on `md:hidden`
- Existing nav links rendered in a vertical list below the header when open
- Close on link click or outside click

**Impact**: FR-002, SC-002.

### DD-3: Task Table Mobile Adaptation (FR-007)

**Decision**: On viewports below 768px, render tasks as stacked cards instead of a table.

**Rationale**: Tables with 7 columns cannot fit at 320px. A responsive card layout preserves all information in a scannable format.

**Implementation**:
- Wrap table in a `hidden md:block` container
- Add a card-based layout in a `md:hidden` container
- Cards show: title, status badge, date, and action buttons
- Details available via expand/collapse

**Impact**: FR-007, SC-002, SC-008.

### DD-4: Animation Restraint (FR-014, FR-015)

**Decision**: Replace `neon-text`, `neon-glow` with subtle shadows. Reduce `hover:scale-105` to `hover:scale-[1.02]`. Add `prefers-reduced-motion` media query.

**Implementation**:
- In `globals.css`: redefine `.neon-text` to use a single subtle text-shadow (not triple-layered)
- In `globals.css`: redefine `.neon-glow` to use a single box-shadow layer
- In all component JSX: replace `scale-105` with `scale-[1.02]`
- Add `@media (prefers-reduced-motion: reduce)` block disabling all animations

**Impact**: FR-014, FR-015, SC-007.

### DD-5: Accessibility Patterns (FR-009 through FR-012)

**Decision**: Systematic accessibility pass across all components.

**Patterns**:
- Focus rings: `focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[var(--accent-primary)]`
- Status badges: Already have text ("Active"/"Completed"), verify sufficient contrast
- Emoji labels: Wrap in `<span role="img" aria-label="...">` or replace with SVG icons
- Chat messages: Add `aria-live="polite"` to message list container
- Heading hierarchy: Audit all pages, fix any h1->h3 skips

**Impact**: FR-009 through FR-012, SC-003, SC-004, SC-010.

### DD-6: Border-Radius Scale (FR-004)

**Decision**: Standardize on 3-tier scale: `rounded-lg` (8px) for small, `rounded-xl` (12px) for medium, `rounded-2xl` (16px) for large.

**Current state**: Mixed usage of `rounded-lg`, `rounded-xl`, `rounded-2xl` across similar components.

**Mapping**:
- Badges, chips, small pills: `rounded-lg`
- Buttons, inputs, small cards: `rounded-xl`
- Large cards, modals, sections: `rounded-2xl`

**Impact**: FR-004, SC-006.

### DD-7: Text Overflow Handling (FR-013)

**Decision**: Apply `truncate` (Tailwind's `overflow-hidden text-ellipsis whitespace-nowrap`) to constrained-width containers. Add `title` attribute for tooltip on hover.

**Targets**:
- Task titles in table/card: `max-w-[200px] truncate` with `title={task.title}`
- User name/email in header: `max-w-[150px] truncate`
- Chat message content: No truncation (messages should wrap naturally)

**Impact**: FR-013.

## Implementation Order

| Phase | Scope | Files | Requirements |
|-------|-------|-------|--------------|
| 1 | Design token system | globals.css, tailwind.config.js | FR-001 |
| 2 | Reduced-motion + animation taming | globals.css, chat.module.css | FR-010, FR-014, FR-015 |
| 3 | Mobile navigation | MainLayout.tsx | FR-002 |
| 4 | Component interaction states | globals.css, all components | FR-003, FR-005 |
| 5 | Typography + heading hierarchy | All pages | FR-006 |
| 6 | Border-radius normalization | globals.css, all components | FR-004 |
| 7 | Responsive task table | TaskList.tsx, dashboard.tsx | FR-007 |
| 8 | Responsive chat widget | ChatBubbleWidget.tsx | FR-008 |
| 9 | Accessibility pass | All components | FR-009, FR-011, FR-012 |
| 10 | Text overflow handling | TaskList.tsx, MainLayout.tsx | FR-013 |
| 11 | Final audit + safety validation | All modified files | SC-001 through SC-010 |
