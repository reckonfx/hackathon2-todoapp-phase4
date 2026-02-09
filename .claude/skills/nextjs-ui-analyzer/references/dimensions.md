# UI Analysis Dimensions

## 1. Layout & Alignment

Check for:
- **Spacing consistency**: Are padding/margin values from a consistent scale (4px/8px increments or Tailwind spacing)?
- **Visual balance**: Is content weight distributed evenly? Are sections visually balanced?
- **Grid usage**: Is CSS Grid or Flexbox used appropriately? Are containers properly constrained (`max-w-*`)?
- **Alignment precision**: Do elements align across breakpoints? Check left edges, baselines, center alignment.
- **Container widths**: Are max-widths consistent across pages? Do content areas match?

Red flags: Mixed spacing values (13px, 17px), unconstrained widths, misaligned elements across sections.

## 2. Visual Hierarchy & Readability

Check for:
- **Typography scale**: Is there a clear heading hierarchy (h1 > h2 > h3)? Are sizes from a consistent scale?
- **Font weight usage**: Are weights meaningful (bold for emphasis, regular for body)? Max 3 weights per page.
- **Line height**: Body text should be 1.5-1.75 line-height. Headings 1.1-1.3.
- **Color contrast**: Text must meet WCAG AA (4.5:1 for normal text, 3:1 for large text).
- **Scanning flow**: Can users scan the page and understand hierarchy in 3 seconds?
- **Text length**: Line length should be 45-75 characters for readability.

Red flags: Inconsistent heading sizes, low contrast text, walls of text, competing visual weights.

## 3. Component Design Quality

Check for:
- **Button styles**: Do all buttons have consistent padding, border-radius, font-size? Are there clear primary/secondary/tertiary variants?
- **Button states**: Do buttons have hover, focus, active, disabled, and loading states?
- **Form inputs**: Are inputs consistently styled? Do they have focus rings, error states, placeholder text?
- **Validation UI**: Are error messages clear, positioned correctly, and styled consistently?
- **Component reuse**: Are similar UI patterns using the same component or duplicating code?
- **Icon consistency**: Are icons the same size, weight, and style throughout?

Red flags: Inline-styled one-off buttons, missing hover/focus states, inconsistent border-radius values.

## 4. Responsiveness & Adaptability

Check for:
- **Mobile layout**: Does the layout work at 320px width? Are touch targets 44x44px minimum?
- **Tablet layout**: Does the layout gracefully adapt between 768-1024px?
- **Desktop layout**: Is max-width constrained? Does content stretch awkwardly on wide screens?
- **Breakpoint transitions**: Are transitions between breakpoints smooth? Any content jumps?
- **Hidden content**: Is important content hidden on mobile with `hidden md:block`?
- **Text overflow**: Do long strings (emails, URLs, task titles) handle overflow properly?

Red flags: Horizontal scroll on mobile, tiny touch targets, content hidden without alternative.

## 5. Polish & Micro-Details

Check for:
- **Hover states**: Do interactive elements respond to hover? Are transitions smooth (150-300ms)?
- **Focus states**: Are focus rings visible and consistent? Do they use `focus-visible` for keyboard-only?
- **Active states**: Do buttons/links show press feedback?
- **Border radius**: Is `border-radius` consistent across similar components?
- **Shadows**: Are shadow values from a consistent scale? Do they create proper depth hierarchy?
- **Transitions**: Are state changes animated? Duration 150-300ms, ease-out curve.
- **Loading states**: Do async operations show loading feedback? Skeleton screens vs spinners?

Red flags: Instant state changes (no transition), inconsistent border-radius (some 8px, some 12px, some 16px).

## 6. Accessibility & Usability

Check for:
- **Keyboard navigation**: Can all interactive elements be reached via Tab? Is focus order logical?
- **ARIA labels**: Do icon-only buttons have `aria-label`? Do dynamic regions use `aria-live`?
- **Semantic HTML**: Are headings in order? Are lists using `ul/ol`? Are forms using `label`?
- **Color contrast**: Meets WCAG AA minimum (4.5:1 normal text, 3:1 large text, 3:1 UI components)?
- **Color independence**: Is color the only way to convey information (red = error)? Add icons/text too.
- **Screen reader**: Are decorative images marked `aria-hidden`? Is meaningful content accessible?
- **Reduced motion**: Is `prefers-reduced-motion` respected for animations?

Red flags: Missing labels, heading order skips (h1 to h3), color-only status indicators.
