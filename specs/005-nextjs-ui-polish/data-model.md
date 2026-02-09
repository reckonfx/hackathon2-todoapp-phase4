# Data Model: Design Token Schema

**Feature**: 005-nextjs-ui-polish | **Date**: 2026-02-07

This feature has no database entities. The "data model" is the design token schema — the CSS custom property system that governs all visual values.

## Design Token Schema

### Color Tokens

| Token | Light Mode Value | Dark Mode Value | Usage |
|-------|-----------------|-----------------|-------|
| `--bg-primary` | `#f8fafc` | `#0a0a0a` | Page backgrounds |
| `--bg-secondary` | `#ffffff` | `#141414` | Card/section backgrounds |
| `--bg-tertiary` | `#f1f5f9` | `#1f1f1f` | Subtle backgrounds, hover states |
| `--text-primary` | `#0f172a` | `#ffffff` | Headings, primary text |
| `--text-secondary` | `#475569` | `#b8b8b8` | Body text, descriptions |
| `--text-tertiary` | `#94a3b8` | `#6b6b6b` | Placeholders, hints |
| `--brand-primary` | `#d4af37` | `#d4af37` | Brand gold (shared) |
| `--brand-secondary` | `#b8962e` | `#f4c430` | Brand gold variant |
| `--brand-light` | `#fef3c7` | `rgba(212, 175, 55, 0.2)` | Brand tint background |
| `--accent-primary` | `#4f46e5` | `#d4af37` | **NEW** Primary interactive accent |
| `--accent-secondary` | `#7c3aed` | `#f4c430` | **NEW** Secondary accent/gradient |
| `--accent-light` | `#eef2ff` | `rgba(212, 175, 55, 0.2)` | **NEW** Accent tint background |
| `--accent-gradient-from` | `#4f46e5` | `#d4af37` | **NEW** Gradient start |
| `--accent-gradient-to` | `#7c3aed` | `#f4c430` | **NEW** Gradient end |
| `--accent-shadow` | `rgba(79, 70, 229, 0.3)` | `rgba(212, 175, 55, 0.3)` | **NEW** Accent glow/shadow |
| `--success` | `#10b981` | `#10b981` | Success states |
| `--danger` | `#ef4444` | `#ef4444` | Error/delete states |
| `--warning` | `#f59e0b` | `#f59e0b` | Warning states |
| `--border-color` | `#e2e8f0` | `#2a2a2a` | Borders |

### Shadow Tokens

| Token | Light Mode | Dark Mode |
|-------|-----------|-----------|
| `--shadow-sm` | Standard subtle | Dark subtle |
| `--shadow-md` | Standard medium | Gold-tinted medium |
| `--shadow-lg` | Standard large | Gold-tinted large |
| `--shadow-xl` | Standard extra-large | Gold-tinted extra-large |

### Border-Radius Scale

| Size | Value | Tailwind Class | Usage |
|------|-------|---------------|-------|
| Small | 8px | `rounded-lg` | Badges, chips, pills |
| Medium | 12px | `rounded-xl` | Buttons, inputs, small cards |
| Large | 16px | `rounded-2xl` | Large cards, modals, sections |

### Transition Tokens

| Property | Value | Usage |
|----------|-------|-------|
| Duration (fast) | 150ms | Hover states, color changes |
| Duration (normal) | 200ms | Most transitions |
| Duration (slow) | 300ms | Layout changes, complex animations |
| Easing | ease-out | All transitions |

## State Model

No database state changes. No entity lifecycle transitions.

## Relationships

Tokens are consumed by components. No entity relationships.
