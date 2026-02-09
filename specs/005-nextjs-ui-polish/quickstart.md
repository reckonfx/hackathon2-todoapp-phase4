# Quickstart: Next.js UI Production Polish

**Feature**: 005-nextjs-ui-polish | **Date**: 2026-02-07

## Prerequisites

- Node.js 18+
- Frontend dev server: `cd frontend && npm install && npm run dev`
- Browser with DevTools for visual inspection

## Implementation Sequence

### Step 1: Design Tokens (globals.css)
Add `--accent-*` tokens to `:root` and `[data-theme='dark']` blocks. These are the foundation for all subsequent changes.

### Step 2: Animation Taming (globals.css, chat.module.css)
Reduce `.neon-text` and `.neon-glow` to single-layer effects. Add `@media (prefers-reduced-motion: reduce)` block.

### Step 3: Mobile Navigation (MainLayout.tsx)
Add hamburger toggle and mobile nav panel. Test at 320px viewport.

### Step 4: Interaction States (globals.css, components)
Add `focus-visible` rings, consistent hover transitions, and loading states to all interactive elements.

### Step 5: Typography Hierarchy (all pages)
Audit heading levels. Fix any h1->h3 skips. Verify type scale consistency.

### Step 6: Border-Radius (globals.css, components)
Normalize all border-radius values to the 3-tier scale (8px/12px/16px).

### Step 7: Responsive Task Table (TaskList.tsx)
Add mobile card layout for viewports below 768px.

### Step 8: Responsive Chat Widget (ChatBubbleWidget.tsx)
Make popup fill viewport on screens < 420px.

### Step 9: Accessibility (all components)
Add aria-labels, aria-live regions, verify contrast, test keyboard navigation.

### Step 10: Text Overflow (TaskList.tsx, MainLayout.tsx)
Add truncation with title tooltips for long content.

### Step 11: Final Audit
Run through all SC-001 to SC-010 success criteria. Verify no backend files changed.

## Verification

```bash
# Verify no backend changes
git diff --name-only | grep -v '^frontend/' | grep -v '^specs/'
# Should return empty (no non-frontend/non-spec changes)

# Run frontend build to catch errors
cd frontend && npm run build

# Visual testing
npm run dev
# Test at 320px, 768px, 1440px viewports
# Toggle light/dark mode on each page
# Tab through all interactive elements
# Enable "Reduce motion" in OS settings
```
