# Research: Next.js UI Production Polish

**Feature**: 005-nextjs-ui-polish | **Date**: 2026-02-07

## R-1: CSS Custom Properties + Tailwind 4.x Token Integration

**Decision**: Use CSS custom properties in `:root` / `[data-theme='dark']` and reference them via Tailwind's arbitrary value syntax (`text-[var(--accent-primary)]`) or extended theme config.

**Rationale**: Tailwind CSS 4.x supports CSS variables natively. The project already uses this pattern for `--bg-primary`, `--text-secondary`, etc. Extending it for accent colors maintains consistency with existing architecture.

**Alternatives considered**:
- Tailwind `darkMode: 'class'` with separate utility classes: Rejected because the project already uses `data-theme` attribute, not `dark` class.
- CSS-in-JS theming (styled-components): Rejected because no CSS-in-JS library exists in the project.

## R-2: Mobile Navigation Pattern (Hamburger vs Bottom Nav)

**Decision**: Hamburger menu with slide-down panel.

**Rationale**: The app has only 3 nav items (Home, Tasks, AI Chat). A hamburger is the standard pattern for this count. Bottom nav is better suited for 4-5 items and native mobile apps.

**Alternatives considered**:
- Bottom tab bar: Rejected. Better for mobile apps, adds visual complexity to web, and conflicts with the floating chat bubble widget positioning.
- Sidebar drawer: Rejected. Overkill for 3 nav items, requires overlay and animation complexity.

## R-3: Responsive Table Strategy

**Decision**: Dual rendering - table for desktop (md+), stacked cards for mobile (<md).

**Rationale**: The task table has 7 columns (checkbox, title, details, created, completed, status, actions). At 320px, even with horizontal scrolling, columns would be unusably narrow. Cards provide a mobile-native experience.

**Alternatives considered**:
- Horizontal scrollable table with sticky first column: Still awkward UX on 320px, requires user to discover scroll.
- Collapsible columns (progressive disclosure): Complex to implement, confusing which columns are visible.

## R-4: Animation and prefers-reduced-motion Best Practices

**Decision**: Single `@media (prefers-reduced-motion: reduce)` block at the end of `globals.css` that sets `animation-duration: 0.01ms !important`, `transition-duration: 0.01ms !important`, and `animation-iteration-count: 1 !important`.

**Rationale**: This is the established pattern from MDN and W3C. Using `0.01ms` instead of `0ms` ensures events still fire (some JS depends on animationend/transitionend events).

**Alternatives considered**:
- Per-animation opt-out: Too granular, easy to miss new animations.
- CSS `update` media feature: Not widely supported yet.

## R-5: Focus Ring Strategy

**Decision**: Use `focus-visible` (not `focus`) to show rings only on keyboard navigation. Ring style: 2px solid with offset, using the accent color token.

**Rationale**: `focus-visible` avoids showing focus rings on mouse clicks while maintaining keyboard accessibility. This is the modern standard recommended by WCAG 2.1.

**Alternatives considered**:
- `:focus` on all elements: Shows rings on click, annoying for mouse users.
- Custom `:focus-within` patterns: More complex, same end result.
