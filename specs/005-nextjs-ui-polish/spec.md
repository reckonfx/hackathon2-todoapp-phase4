# Feature Specification: Next.js UI Production Polish

**Feature Branch**: `005-nextjs-ui-polish`
**Created**: 2026-02-07
**Status**: Draft
**Input**: Senior Next.js UI/UX analysis and production-grade improvement plan for the Todo AI Chatbot frontend application.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Consistent Visual Design System (Priority: P1)

As a user, I experience a cohesive, unified visual language across all pages (landing, dashboard, chat, auth) so the application feels professionally crafted and trustworthy.

**Why this priority**: Visual inconsistency is the most visible sign of an unpolished product. The current app mixes indigo/purple gradients (header logo, nav hovers, CTA buttons), blue/cyan gradients (hero section, features, stats), and gold/black theming (dark mode, neon effects, checkboxes). This brand confusion erodes trust and makes the app feel assembled rather than designed.

**Independent Test**: Can be fully tested by navigating all pages and verifying that the color palette, typography weights, border-radius values, and shadow scales are drawn from a single, documented design token set.

**Acceptance Scenarios**:

1. **Given** a user on any page, **When** they view interactive elements (buttons, links, cards), **Then** all elements use colors exclusively from the defined design token palette (no hardcoded hex values outside the token set).
2. **Given** a user navigating from the landing page to the dashboard, **When** they compare visual elements, **Then** the header logo color, button gradients, hover states, and card styles are visually consistent.
3. **Given** a user toggling between light and dark mode, **When** they view any page, **Then** all elements correctly reflect the active theme: indigo/blue accents in light mode, gold/black accents in dark mode, with no cross-theme color leakage.

---

### User Story 2 - Responsive Layout Without Breakage (Priority: P1)

As a mobile user, I can access and use all features (task management, AI chat, navigation) without horizontal scrolling, clipped content, or unreachable interactive elements.

**Why this priority**: Mobile usability directly impacts a large portion of users. The current app hides navigation on mobile (`hidden md:flex`) without providing a mobile menu alternative, and the ChatBubbleWidget popup (380x520px fixed) may overflow on small screens.

**Independent Test**: Can be fully tested by viewing all pages at 320px, 375px, 768px, and 1440px widths and verifying no horizontal overflow, all touch targets are 44x44px minimum, and all content is accessible.

**Acceptance Scenarios**:

1. **Given** a mobile user (320px viewport), **When** they need to navigate between pages, **Then** a mobile navigation mechanism (hamburger menu or bottom nav) is available and functional.
2. **Given** a mobile user on the dashboard, **When** they view the task table, **Then** the table adapts to the viewport without horizontal scrolling (card layout or scrollable container with visual cue).
3. **Given** a mobile user opening the chat widget, **When** the chat popup appears, **Then** it fills the available viewport appropriately without overflowing off-screen.

---

### User Story 3 - Component Interaction States (Priority: P2)

As a user interacting with buttons, forms, and links, I receive clear visual feedback for every state (hover, focus, active, disabled, loading) so I always know what is clickable and what is happening.

**Why this priority**: Missing or inconsistent interaction states make the UI feel unresponsive and reduce user confidence. Several components currently lack focus-visible rings, disabled states, or consistent hover transitions.

**Independent Test**: Can be fully tested by keyboard-tabbing through all interactive elements and hovering/clicking each button, verifying visible state changes.

**Acceptance Scenarios**:

1. **Given** a user tabbing through the interface with a keyboard, **When** they focus on any interactive element, **Then** a visible focus ring appears that meets WCAG 2.1 requirements (3:1 contrast, 2px minimum).
2. **Given** a user hovering over any button, **When** they observe the button, **Then** it shows a smooth transition (150-300ms, ease-out) with a distinguishable hover state.
3. **Given** a form submission is in progress, **When** the user views the submit button, **Then** it shows a loading state (spinner or text change) and is non-interactive until the operation completes.

---

### User Story 4 - Typography and Readability (Priority: P2)

As a user reading content across all pages, I experience a clear typographic hierarchy where headings, body text, and labels are distinctly sized, weighted, and spaced for effortless scanning.

**Why this priority**: The current typography uses the `neon-text` class extensively on the landing page, applying text-shadow effects that reduce readability. Font sizes jump inconsistently (text-5xl to text-2xl without a clear scale), and heading levels are not always sequential in the DOM.

**Independent Test**: Can be fully tested by inspecting heading hierarchy (h1 > h2 > h3), verifying a consistent type scale (e.g., 1.25 ratio), and checking that body text line lengths stay within 45-75 characters.

**Acceptance Scenarios**:

1. **Given** a user on the landing page, **When** they scan the content, **Then** the heading hierarchy follows a clear descending scale without skipping levels (no h1 followed by h3).
2. **Given** a user reading body text, **When** they view any paragraph, **Then** the line height is 1.5-1.75 and the maximum line length is 75 characters.
3. **Given** a user with low vision, **When** they view any text element, **Then** the color contrast ratio meets WCAG AA (4.5:1 for normal text, 3:1 for large text).

---

### User Story 5 - Polish and Micro-Interactions (Priority: P3)

As a user, I experience smooth, subtle animations and consistent micro-details (border-radius, shadows, transitions) that make the application feel premium without being distracting.

**Why this priority**: The current app uses heavy neon-glow effects and aggressive `hover:scale-105` transforms that feel flashy rather than polished. Inconsistent border-radius values (rounded-xl, rounded-2xl, rounded-lg) across similar components reduce visual cohesion.

**Independent Test**: Can be fully tested by interacting with cards, buttons, and page transitions and verifying that animations are subtle (no jarring scale changes), border-radius is consistent per component type, and shadows create a clear depth hierarchy.

**Acceptance Scenarios**:

1. **Given** a user hovering over feature cards, **When** they observe the hover effect, **Then** the transition is subtle (max scale 1.02, shadow elevation increase) and lasts 200-300ms.
2. **Given** a user viewing cards across different pages, **When** they compare border-radius values, **Then** all cards use the same border-radius value.
3. **Given** a user who prefers reduced motion (OS setting), **When** they view the application, **Then** all animations are disabled or reduced per `prefers-reduced-motion` media query.

---

### User Story 6 - Accessibility Compliance (Priority: P3)

As a user relying on assistive technology, I can fully navigate and use the application with a screen reader or keyboard alone.

**Why this priority**: Several accessibility gaps exist: the mobile navigation has no alternative, some emoji-based icons (robot emoji in chat) lack text alternatives, and color is sometimes the only indicator of state (active vs completed badges).

**Independent Test**: Can be fully tested by navigating the entire app with keyboard only and a screen reader, verifying all interactive elements are reachable and all states are communicated non-visually.

**Acceptance Scenarios**:

1. **Given** a screen reader user on the dashboard, **When** they encounter status badges, **Then** the status is communicated via text or aria-label, not color alone.
2. **Given** a keyboard user, **When** they navigate the full application, **Then** they can reach and activate every interactive element in a logical tab order.
3. **Given** a screen reader user on the chat page, **When** a new message arrives, **Then** it is announced via an aria-live region.

---

### Edge Cases

- What happens when extremely long task titles overflow table cells or card containers?
- How does the UI behave when the browser window is resized rapidly between breakpoints?
- What happens when the theme is toggled mid-animation?
- How does the app appear when the user has a very long name or email in the header user info area?
- What happens when JavaScript is loading (hydration gap) - does the layout shift visibly?

## Clarifications

### Session 2026-02-07

- Q: Should the unified color palette be gold-only, dual palette, or neutral modern? → A: Keep dual palette (gold for dark mode, indigo/blue for light mode)

## Phase Context & Constraints

- **Scope**: UI/Styling changes ONLY - no backend logic, API contracts, or data flow modifications
- **Interface**: Next.js Pages Router with React 19, Tailwind CSS 4.1, custom CSS variables
- **Theme System**: CSS variables with `data-theme` attribute (light/dark), must preserve toggle functionality
- **Existing Patterns**: Mix of Tailwind utilities, CSS Modules (chat), and global CSS classes
- **Safety**: All changes must be visual-only; props, routes, environment variables, and API calls remain untouched

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: UI MUST use a dual-palette color token system (indigo/blue for light mode, gold/black for dark mode) where all colors reference CSS custom properties (no hardcoded hex values in component JSX except within the token definition layer). Each theme must be internally consistent with no cross-theme color leakage
- **FR-002**: UI MUST provide a mobile navigation mechanism (hamburger menu or equivalent) accessible at viewports below 768px
- **FR-003**: All interactive elements MUST have visible hover, focus, active, and disabled states with transitions between 150-300ms
- **FR-004**: UI MUST use a consistent border-radius scale: 8px for small elements (badges, chips), 12px for medium elements (buttons, inputs), 16px for large elements (cards, modals)
- **FR-005**: All buttons MUST display a loading state (spinner or text change) during async operations, and be non-interactive while loading
- **FR-006**: Typography MUST follow a consistent scale with no heading level skips in the DOM (h1 > h2 > h3, never h1 > h3)
- **FR-007**: The task table on the dashboard MUST be usable on mobile viewports (320px) without horizontal scrolling
- **FR-008**: The ChatBubbleWidget popup MUST be responsive, filling available viewport width on screens narrower than 420px
- **FR-009**: All text MUST meet WCAG AA contrast ratios (4.5:1 for normal text, 3:1 for large text and UI components)
- **FR-010**: UI MUST respect `prefers-reduced-motion` by disabling or reducing all CSS animations and transitions
- **FR-011**: Status indicators (active/completed badges) MUST communicate state via text or icon in addition to color
- **FR-012**: All emoji-based indicators (robot emoji in chat header, etc.) MUST have `aria-label` attributes for screen readers
- **FR-013**: Long text content (task titles, user names, emails) MUST handle overflow gracefully with truncation and tooltips
- **FR-014**: The `neon-text` and `neon-glow` effects MUST be toned down or removed to improve readability and reduce visual noise
- **FR-015**: Hover scale transforms on cards MUST be reduced from `scale-105` to a maximum of `scale-[1.02]` for professional restraint

### Key Entities

- **Design Token**: CSS custom property defining a color, spacing, shadow, or border-radius value used consistently across the UI
- **Component State**: A visual representation of an interactive element's current condition (default, hover, focus, active, disabled, loading)
- **Breakpoint**: A viewport width threshold (320px, 768px, 1024px, 1440px) where the layout adapts

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All pages pass visual consistency audit: zero hardcoded color values outside the design token layer; light mode uses indigo/blue accents consistently, dark mode uses gold/black accents consistently
- **SC-002**: Application is fully usable at 320px viewport width with no horizontal scrolling on any page
- **SC-003**: All interactive elements have 4 visible states (default, hover, focus, disabled) verified by manual inspection
- **SC-004**: WCAG AA color contrast compliance across all text elements (verifiable via automated contrast checker)
- **SC-005**: Zero heading level skips across all pages (verifiable via DOM inspection)
- **SC-006**: Border-radius consistency: all similar component types use the same radius value (verifiable by auditing computed styles)
- **SC-007**: All CSS animations respect `prefers-reduced-motion` (verifiable by toggling OS setting)
- **SC-008**: Task table is fully functional on mobile without horizontal scrolling (verifiable at 320px viewport)
- **SC-009**: Backend logic, API calls, routes, and environment variables remain completely unchanged (verifiable by git diff excluding .css, .tsx styling changes)
- **SC-010**: 100% of interactive elements reachable via keyboard Tab navigation in logical order

### Assumptions

- The application uses a dual color palette: indigo/blue accents for light mode, gold/black accents for dark mode. Both palettes are intentional and must be internally consistent within their respective themes (no cross-theme color leakage)
- The Pages Router architecture will be preserved (no migration to App Router)
- No new npm dependencies will be added for UI changes (all improvements use existing Tailwind CSS and custom CSS)
- The chat module's CSS Modules approach (`chat.module.css`) will be preserved
- Performance budgets are standard web expectations (LCP < 2.5s, CLS < 0.1)
