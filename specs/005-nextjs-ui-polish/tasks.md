# Tasks: Next.js UI Production Polish

**Input**: Design documents from `/specs/005-nextjs-ui-polish/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md

**Tests**: Not requested in spec. Manual visual verification via quickstart.md.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. All changes are frontend-only (no backend files modified).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/src/` for all source changes
- **Styles**: `frontend/src/styles/globals.css`, `frontend/src/components/chat/chat.module.css`
- **Components**: `frontend/src/components/`
- **Pages**: `frontend/src/pages/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Extend the design token foundation that all user stories depend on

- [x] T001 Add `--accent-primary`, `--accent-secondary`, `--accent-light`, `--accent-gradient-from`, `--accent-gradient-to`, `--accent-shadow` tokens to `:root` (indigo/blue values) and `[data-theme='dark']` (gold values) in `frontend/src/styles/globals.css`
- [x] T002 Add corresponding Tailwind theme extensions for accent tokens in `frontend/tailwind.config.js` (map `accent-primary`, `accent-secondary` etc. to CSS variables)
- [x] T003 Add global `@media (prefers-reduced-motion: reduce)` block at end of `frontend/src/styles/globals.css` setting `animation-duration: 0.01ms !important`, `transition-duration: 0.01ms !important`, `animation-iteration-count: 1 !important` on all elements

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core style changes that MUST be complete before ANY user story can proceed

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Redefine `.neon-text` in `frontend/src/styles/globals.css` to use a single subtle text-shadow (`0 0 5px rgba(212, 175, 55, 0.3)`) instead of triple-layered glow
- [x] T005 Redefine `.neon-glow` in `frontend/src/styles/globals.css` to use a single box-shadow layer (`0 0 8px var(--accent-shadow)`) instead of triple-layered glow
- [x] T006 Add global focus-visible utility in `frontend/src/styles/globals.css`: `.focus-ring` class applying `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent-primary)]` pattern
- [x] T007 Add global `.btn-loading` class in `frontend/src/styles/globals.css` with `opacity: 0.7`, `pointer-events: none`, and spinner animation
- [x] T008 [P] Add `@media (prefers-reduced-motion: reduce)` block in `frontend/src/components/chat/chat.module.css` mirroring the globals.css approach for chat-specific animations

**Checkpoint**: Token system and foundational styles ready - user story implementation can begin

---

## Phase 3: User Story 1 - Consistent Visual Design System (Priority: P1) MVP

**Goal**: Unify the dual color palette so light mode uses indigo/blue consistently and dark mode uses gold/black consistently, with no cross-theme color leakage.

**Independent Test**: Navigate all pages in both themes. Verify no hardcoded hex colors remain in JSX. All accent elements match the active theme palette.

### Implementation for User Story 1

- [x] T009 [US1] Replace all hardcoded indigo/purple/blue hex values in `frontend/src/components/Layout/MainLayout.tsx` with CSS variable references (`var(--accent-primary)`, `var(--accent-gradient-from)`, etc.) - affects logo gradient, nav hover colors, Sign In/Join Free buttons
- [x] T010 [US1] Replace all hardcoded blue/cyan/indigo hex values in `frontend/src/pages/index.tsx` with CSS variable references - affects hero badge, h1 gradient, stat card gradients, feature card icon backgrounds, CTA section background
- [x] T011 [P] [US1] Replace hardcoded indigo/blue hex values in `frontend/src/pages/dashboard.tsx` with CSS variable references - affects stat card styling
- [x] T012 [P] [US1] Replace hardcoded color hex values in `frontend/src/pages/chat.tsx` with CSS variable references
- [x] T013 [P] [US1] Replace hardcoded color hex values in `frontend/src/components/Auth/Login.tsx` with CSS variable references - affects icon box gradient, links
- [x] T014 [P] [US1] Replace hardcoded color hex values in `frontend/src/components/Auth/Register.tsx` with CSS variable references - affects icon box gradient, links
- [x] T015 [US1] Update `.btn-primary` and other button classes in `frontend/src/styles/globals.css` to use `var(--accent-gradient-from)` and `var(--accent-gradient-to)` instead of hardcoded gradients
- [x] T016 [US1] Update `.neon-btn` gradient in `frontend/src/styles/globals.css` to use `var(--accent-gradient-from)` and `var(--accent-gradient-to)`
- [x] T017 [US1] Update header logo gradient background in `frontend/src/components/Layout/MainLayout.tsx` from `from-indigo-600 to-purple-600` to use accent CSS variables
- [x] T018 [US1] Update the `style jsx global` block in `frontend/src/components/Layout/MainLayout.tsx` to ensure all utility classes reference CSS variables correctly

**Checkpoint**: All pages use theme-aware accent colors. Visual consistency verified in both light and dark mode.

---

## Phase 4: User Story 2 - Responsive Layout Without Breakage (Priority: P1)

**Goal**: Ensure all pages are fully usable at 320px viewport with mobile navigation, responsive task table, and adaptive chat widget.

**Independent Test**: View all pages at 320px, 375px, 768px widths. Verify no horizontal scrolling, all content accessible, touch targets 44x44px minimum.

### Implementation for User Story 2

- [x] T019 [US2] Add mobile hamburger menu button (visible `md:hidden`) and `useState` toggle in `frontend/src/components/Layout/MainLayout.tsx` - renders a slide-down nav panel with Home, Tasks, AI Chat links
- [x] T020 [US2] Add close-on-click behavior for mobile nav: close menu when a nav link is clicked or when clicking outside the menu area in `frontend/src/components/Layout/MainLayout.tsx`
- [x] T021 [US2] Add mobile card layout for tasks (visible `md:hidden`) in `frontend/src/components/TaskList.tsx` - each task renders as a card with title, status badge, date, checkbox, and delete button
- [x] T022 [US2] Wrap existing task table in `hidden md:block` container in `frontend/src/components/TaskList.tsx` so table only shows on desktop
- [x] T023 [US2] Make ChatBubbleWidget popup responsive in `frontend/src/components/chat/ChatBubbleWidget.tsx` - use `width: min(380px, calc(100vw - 32px))` and `height: min(520px, calc(100vh - 120px))` instead of fixed dimensions
- [x] T024 [US2] Ensure hero section buttons stack properly on mobile in `frontend/src/pages/index.tsx` - verify `flex-col sm:flex-row` layout works at 320px without overflow

**Checkpoint**: All pages usable at 320px. No horizontal scrolling. Mobile nav functional.

---

## Phase 5: User Story 3 - Component Interaction States (Priority: P2)

**Goal**: All interactive elements have visible hover, focus, active, and disabled states with smooth transitions.

**Independent Test**: Tab through every interactive element with keyboard. Hover over every button and link. Verify visible state changes with smooth transitions.

### Implementation for User Story 3

- [x] T025 [US3] Add `focus-visible` ring styles to all buttons and links in `frontend/src/components/Layout/MainLayout.tsx` - nav links, theme toggle, Sign Out, Sign In, Join Free
- [x] T026 [P] [US3] Add `focus-visible` ring styles and loading state to form submit button in `frontend/src/components/TaskForm.tsx` - disable button and show spinner during submission
- [x] T027 [P] [US3] Add `focus-visible` ring styles to all form inputs and buttons in `frontend/src/components/Auth/Login.tsx` - email input, password input, submit button, show/hide toggle
- [x] T028 [P] [US3] Add `focus-visible` ring styles to all form inputs and buttons in `frontend/src/components/Auth/Register.tsx` - name input, email input, password input, submit button
- [x] T029 [P] [US3] Add `focus-visible` ring styles to chat input textarea and send button in `frontend/src/components/chat/ChatInput.tsx`
- [x] T030 [P] [US3] Add `focus-visible` ring styles to voice input button in `frontend/src/components/chat/VoiceInput.tsx`
- [x] T031 [US3] Add consistent `transition-all duration-200 ease-out` to all interactive elements missing transitions in `frontend/src/styles/globals.css` - update `.btn-primary`, `.btn-secondary`, `.btn-danger`, `.input-field` classes
- [x] T032 [US3] Replace all `hover:scale-105` with `hover:scale-[1.02]` across all component files: `frontend/src/pages/index.tsx`, `frontend/src/pages/dashboard.tsx`
- [x] T033 [US3] Add disabled state styling (opacity 0.5, cursor-not-allowed, pointer-events-none) to `.btn-primary`, `.btn-secondary`, `.btn-danger` in `frontend/src/styles/globals.css`

**Checkpoint**: All interactive elements respond to hover, focus-visible, and show disabled/loading states.

---

## Phase 6: User Story 4 - Typography and Readability (Priority: P2)

**Goal**: Clear typographic hierarchy with correct heading levels, consistent type scale, and WCAG AA contrast across all pages.

**Independent Test**: Inspect DOM heading hierarchy on every page. Verify no h1->h3 skips. Check body text line-height is 1.5-1.75. Verify contrast ratios with DevTools.

### Implementation for User Story 4

- [x] T034 [US4] Audit and fix heading hierarchy in `frontend/src/pages/index.tsx` - ensure h1 (hero) > h2 (features section, CTA section) > h3 (feature cards) with no level skips
- [x] T035 [P] [US4] Audit and fix heading hierarchy in `frontend/src/pages/dashboard.tsx` - ensure single h1 for page title, h2 for sections (stats, task list), h3 for subsections
- [x] T036 [P] [US4] Audit and fix heading hierarchy in `frontend/src/pages/chat.tsx` - ensure single h1 for page title, h2 for sections
- [x] T037 [US4] Verify and fix body text line-height across all pages - ensure `leading-relaxed` (1.625) or `leading-7` (1.75) on all paragraph elements; update `frontend/src/styles/globals.css` base body line-height if needed
- [x] T038 [US4] Verify WCAG AA contrast ratios for `--text-secondary` (`#475569` on `#f8fafc` = 5.7:1 OK) and `--text-tertiary` (`#94a3b8` on `#f8fafc` = 3.3:1 FAIL for normal text) in `frontend/src/styles/globals.css` - adjust `--text-tertiary` to meet 4.5:1 ratio
- [x] T039 [US4] Verify dark mode contrast: `--text-secondary` (`#b8b8b8` on `#0a0a0a` = 10.6:1 OK) and `--text-tertiary` (`#6b6b6b` on `#0a0a0a` = 4.0:1 FAIL) in `frontend/src/styles/globals.css` - adjust dark `--text-tertiary` to meet 4.5:1 ratio

**Checkpoint**: All heading hierarchies correct. All text meets WCAG AA contrast. Typography scale consistent.

---

## Phase 7: User Story 5 - Polish and Micro-Interactions (Priority: P3)

**Goal**: Consistent border-radius, subtle animations, and cohesive shadow hierarchy across all components.

**Independent Test**: Compare border-radius values across all card components. Verify hover effects are subtle (max scale 1.02). Toggle reduced-motion OS setting and verify animations stop.

### Implementation for User Story 5

- [x] T040 [US5] Normalize border-radius in `frontend/src/pages/index.tsx` - feature cards: `rounded-2xl`, stat cards: `rounded-2xl`, badges: `rounded-lg`, buttons: `rounded-xl`
- [x] T041 [P] [US5] Normalize border-radius in `frontend/src/pages/dashboard.tsx` - stat cards: `rounded-2xl`, task form: `rounded-2xl`, buttons: `rounded-xl`
- [x] T042 [P] [US5] Normalize border-radius in `frontend/src/components/Auth/Login.tsx` and `frontend/src/components/Auth/Register.tsx` - auth cards: `rounded-2xl`, inputs: `rounded-xl`, buttons: `rounded-xl`
- [x] T043 [P] [US5] Normalize border-radius in `frontend/src/components/TaskList.tsx` - status badges: `rounded-lg`, action buttons: `rounded-xl`, table container: `rounded-2xl`
- [x] T044 [US5] Update `.card` class border-radius to `border-radius: 16px` (rounded-2xl) in `frontend/src/styles/globals.css`
- [x] T045 [US5] Update `.input-field` class border-radius to `border-radius: 12px` (rounded-xl) in `frontend/src/styles/globals.css`
- [x] T046 [US5] Update `.badge-active` and `.badge-completed` border-radius to `border-radius: 8px` (rounded-lg) in `frontend/src/styles/globals.css`

**Checkpoint**: Border-radius consistent across all similar component types. Animations subtle and reduced-motion compliant.

---

## Phase 8: User Story 6 - Accessibility Compliance (Priority: P3)

**Goal**: Full keyboard navigation, screen reader support, and non-color status indicators across the entire application.

**Independent Test**: Navigate full app with keyboard only. Use screen reader to verify all elements are announced. Check that status is communicated via text, not color alone.

### Implementation for User Story 6

- [x] T047 [US6] Add `aria-live="polite"` attribute to the message list container in `frontend/src/components/chat/ChatMessageList.tsx`
- [x] T048 [P] [US6] Wrap emoji indicators in `<span role="img" aria-label="...">` in `frontend/src/components/chat/ChatContainer.tsx` - robot emoji in header needs `aria-label="AI Assistant"`
- [x] T049 [P] [US6] Wrap emoji indicators in `<span role="img" aria-label="...">` in `frontend/src/components/chat/ChatBubbleWidget.tsx` - chat bubble emoji needs aria-label (bubble uses SVG, not emoji - already has aria-label)
- [x] T050 [P] [US6] Verify status badges in `frontend/src/components/TaskList.tsx` communicate state via text content (already show "Active"/"Completed" text) - add `aria-label` attribute to badge spans for screen readers
- [x] T051 [P] [US6] Add `aria-label` to voice input button states in `frontend/src/components/chat/VoiceInput.tsx` - differentiate "Start recording" vs "Stop recording" states (already implemented)
- [x] T052 [US6] Verify logical tab order across `frontend/src/components/Layout/MainLayout.tsx` - ensure mobile nav items are tabbable when open, not tabbable when closed (use `tabIndex={-1}` or `aria-hidden` on closed menu)
- [x] T053 [US6] Add `aria-label="Navigation menu"` to the mobile hamburger button in `frontend/src/components/Layout/MainLayout.tsx`

**Checkpoint**: All interactive elements keyboard-accessible. Screen reader announces all status and state changes. No color-only indicators.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Text overflow handling and final safety validation across all modified files

- [x] T054 Add text truncation with `title` tooltip to task titles in table view in `frontend/src/components/TaskList.tsx` - apply `max-w-[200px] truncate` with `title={task.title}`
- [x] T055 [P] Add text truncation to user name and email in header in `frontend/src/components/Layout/MainLayout.tsx` - apply `max-w-[150px] truncate` with `title` attributes
- [x] T056 [P] Add text truncation to task titles in mobile card layout in `frontend/src/components/TaskList.tsx` - apply `truncate` class with `title={task.title}`
- [x] T057 Run `npm run build` in `frontend/` to verify no build errors from styling changes
- [ ] T058 Verify safety constraint SC-009: run `git diff --name-only` and confirm zero files outside `frontend/` and `specs/` directories were modified
- [ ] T059 Run quickstart.md verification steps: test at 320px, 768px, 1440px viewports; toggle light/dark mode on each page; tab through all interactive elements; enable reduce-motion OS setting

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Phase 2 - token system must exist before replacing hardcoded colors
- **User Story 2 (Phase 4)**: Depends on Phase 2 - can run in parallel with US1
- **User Story 3 (Phase 5)**: Depends on Phase 2 - can run in parallel with US1/US2 (different files mostly)
- **User Story 4 (Phase 6)**: Depends on Phase 2 - can run in parallel with US1/US2/US3
- **User Story 5 (Phase 7)**: Depends on Phase 2 - can run in parallel with others
- **User Story 6 (Phase 8)**: Depends on Phase 4 (needs mobile nav to exist for T052/T053)
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Phase 2 - No dependencies on other stories
- **US2 (P1)**: Can start after Phase 2 - No dependencies on other stories
- **US3 (P2)**: Can start after Phase 2 - No dependencies on other stories (focus rings on independent files)
- **US4 (P2)**: Can start after Phase 2 - No dependencies on other stories
- **US5 (P3)**: Can start after Phase 2 - No dependencies on other stories
- **US6 (P3)**: Depends on US2 completion (mobile nav must exist for accessibility tasks T052/T053)

### Within Each User Story

- Global style changes before component-level changes
- Page-level changes can run in parallel when marked [P]
- Integration/verification tasks last

### Parallel Opportunities

- T011, T012, T013, T014 can run in parallel (different page/component files)
- T026, T027, T028, T029, T030 can run in parallel (different component files)
- T035, T036 can run in parallel (different page files)
- T040, T041, T042, T043 can run in parallel (different files)
- T047, T048, T049, T050, T051 can run in parallel (different component files)
- T054, T055, T056 can run in parallel (different targets within files)
- US1, US2, US3, US4, US5 can all run in parallel after Phase 2

---

## Parallel Example: User Story 1

```bash
# After T015-T018 (global style updates), launch all page/component updates in parallel:
Task: "T011 [P] [US1] Replace hardcoded colors in frontend/src/pages/dashboard.tsx"
Task: "T012 [P] [US1] Replace hardcoded colors in frontend/src/pages/chat.tsx"
Task: "T013 [P] [US1] Replace hardcoded colors in frontend/src/components/Auth/Login.tsx"
Task: "T014 [P] [US1] Replace hardcoded colors in frontend/src/components/Auth/Register.tsx"
```

## Parallel Example: User Story 3

```bash
# All focus-ring tasks on different component files, can run in parallel:
Task: "T026 [P] [US3] Add focus-visible rings in frontend/src/components/TaskForm.tsx"
Task: "T027 [P] [US3] Add focus-visible rings in frontend/src/components/Auth/Login.tsx"
Task: "T028 [P] [US3] Add focus-visible rings in frontend/src/components/Auth/Register.tsx"
Task: "T029 [P] [US3] Add focus-visible rings in frontend/src/components/chat/ChatInput.tsx"
Task: "T030 [P] [US3] Add focus-visible rings in frontend/src/components/chat/VoiceInput.tsx"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T008)
3. Complete Phase 3: User Story 1 - Design System (T009-T018)
4. Complete Phase 4: User Story 2 - Responsive Layout (T019-T024)
5. **STOP and VALIDATE**: Test at 320px and 1440px in both themes
6. Demo-ready with consistent colors and responsive layout

### Incremental Delivery

1. Setup + Foundational -> Token system ready
2. Add US1 -> Consistent colors in both themes -> Validate
3. Add US2 -> Mobile-responsive layout -> Validate
4. Add US3 -> Complete interaction states -> Validate
5. Add US4 -> Typography hierarchy fixed -> Validate
6. Add US5 -> Visual polish normalized -> Validate
7. Add US6 -> Full accessibility -> Validate
8. Polish -> Overflow handling + final audit -> Ship

### Sequential Single-Developer Strategy

1. Phase 1 + 2 (8 tasks, ~30 min)
2. Phase 3: US1 (10 tasks, ~45 min)
3. Phase 4: US2 (6 tasks, ~30 min)
4. Phase 5: US3 (9 tasks, ~30 min)
5. Phase 6: US4 (6 tasks, ~20 min)
6. Phase 7: US5 (7 tasks, ~20 min)
7. Phase 8: US6 (7 tasks, ~20 min)
8. Phase 9: Polish (6 tasks, ~15 min)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each phase completion
- Stop at any checkpoint to validate story independently
- **Safety**: Zero backend files modified. SC-009 validated in T058.
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
