---
name: ui-parity-port
description: Use when replicating or porting a UI screen/design into our Next.js + Tailwind frontend from a reference (a shared preview URL or a reference repo such as the Lovable clone).
---

# Porting UI into our frontend (with browser verification)

Use when replicating a screen/design from a reference into our Next.js + Tailwind v4 frontend. The reference is either a cloned repo (e.g. the Lovable `note-nest-language-switch` clone) or a live site. If there is no reference to compare against, ASK the user for the shared URL before starting.

## 1. Read the FULL render chain — not just the page file

Before porting a screen, read every file that shapes how it renders, top to bottom:
- global CSS / theme tokens (`globals.css` / `styles.css`)
- the root layout / shell (reference: `src/routes/__root.tsx`; ours: `app/layout.tsx` + `components/AppShell.tsx`)
- providers (theme, i18n, query)
- the page file
- every component the page imports (grep the page's imports; skip unused library components)
- the i18n strings

Width caps, centering (`mx-auto max-w-*`), and page padding usually live in the ROOT/LAYOUT wrapper, NOT the page file. Missing that wrapper is the #1 cause of "looks off."

## 2. Port classNames verbatim

Both sides use Tailwind v4, so copy the exact className strings. Change only framework-specific bits: `<Link to>` → `<Link href>`, their hooks → ours (e.g. `usePreferences().t` → `useT().t`), icon names. Do NOT re-translate classes from memory — that introduces drift.

Tailwind v4's default border color is `currentColor`, so a bare `border` class renders the FOREGROUND (text) color, not `--border`. The reference almost certainly has a base rule `@layer base { * { border-color: var(--color-border); } }` — when you port its components verbatim (they use bare `border`), you MUST port that base rule into globals too, or every bare border comes out as the text color (pale in dark mode). Writing `border-border` explicitly only fixes classes you author, not verbatim-ported ones, so prefer porting the base rule.

## 3. Verify against the RENDERED DOM in a browser — don't infer from code or screenshots

- Reference ground truth: a repo clone's source IS the spec. A live site: open it in the built-in browser (it may need `request_access`; a Lovable preview may redirect to a login — then rely on the cloned source instead).
- Ours: open `http://localhost:3000` in the built-in browser (their dev server, reachable via the bridge; `request_access` if prompted).
- Diff **computed styles element-by-element across both pages** — never conclude parity from comparing token / CSS-variable VALUES, because identical tokens can still render differently (a bare `border` resolving to `currentColor` instead of `--border` is the classic trap). With `javascript_tool`, read `getComputedStyle` of the SAME key elements (page wrapper, card, button, input, body text, calendar cell) on BOTH pages and compare `backgroundColor`, `color`, `borderColor` AND `borderWidth`, `borderRadius`, `boxShadow`, font, and padding/width. Convert every color to sRGB with a `<canvas>` fill (`ctx.fillStyle = color; ctx.fillRect; getImageData`) before comparing — the browser serializes oklch vs lab inconsistently, so equal colors can look different as raw strings and different token readouts can be equal colors. Report ANY mismatch; do NOT say "they match" until the per-element diff is clean. Zoom into card corners / edges as a visual backup — a 1px border or shadow difference does not show in a full-page screenshot.
- Emulate a wide viewport (~1440) to see centering/gutters — at narrow widths a `max-w-*` column can exactly fill the space and hide the gutters. Screenshot for a final visual check, then reset the viewport to `desktop`.

## 4. After committing, confirm it actually landed

A bridge commit can be silently overwritten (e.g. the file is open in VS Code and the editor saves old content back — tell: same byte count, mtime changed, DOM unchanged). After committing a UI change, re-read the file from disk AND confirm the rendered DOM changed. If it reverted, re-commit and ask the user to close the file or choose "Revert File" in their editor. (The general post-commit re-check rule lives in the project Working Agreement.)

## Work in small chunks

One concern per chunk (tokens → sidebar → page → ...), propose the diff, wait for approval, commit, verify, then move on. Distinguish style differences (CSS/layout) from content differences (copy/i18n) — they are fixed in different places.
