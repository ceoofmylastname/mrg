# MRG Accounting Service — Website

A modern, static, fully self-contained marketing website for **MRG Accounting Service** (Maya Graves, San Diego, CA).

Pure HTML, CSS, and vanilla JavaScript. No build step, no frameworks, no dependencies. Open `index.html` in a browser and the entire site works.

---

## File Structure

```
mrg-website/
├── index.html                  # Home (TOFU hero, services overview, founder strip, FAQ)
├── founder.html                # Meet the Founder — Maya's full story
├── bookkeeping.html            # Bookkeeping service detail page
├── taxes.html                  # Personal & Business Tax services
├── resources-taxes.html        # IRS forms, deadlines, calculators
├── payroll.html                # QuickBooks Payroll Overview
├── business-consultant.html    # Business Launch Services
├── administrative.html         # 6 administrative solutions
├── contact.html                # Contact + multi-step booking form
├── entity-quiz.html            # Lead magnet — interactive 5-question quiz that recommends Sole Prop / LLC / S-Corp / C-Corp with personalized tax math + confetti + share strip. Promoted via the lead-magnet strip on index.html and business-consultant.html.
├── styles.css                  # Shared design system (used by every page)
├── assets/
│   └── maya-portrait.jpg       # (Drop Maya's headshot here — see below)
└── README.md
```

---

## Design System

- **Aesthetic:** Black & white luxury / editorial magazine
- **Background:** `#0a0a0a` (deep obsidian)
- **Text:** White + grayscale hierarchy
- **Accent:** `#e8d9b4` (subtle warm cream — used sparingly for editorial highlights)
- **Typography:** Inter (sans) + Instrument Serif (italic display) — both via Google Fonts
- **Animations:** Scroll-triggered reveals via IntersectionObserver; hover lifts; ambient glow orbs; marquee strip on home
- **Layout:** Asymmetric editorial grids, glassmorphism cards, generous rounded corners (`var(--radius-lg)`)

All design tokens live as CSS custom properties at the top of `styles.css` (`:root { ... }`). Edit one variable and it cascades across every page.

---

## Navigation

All 9 pages cross-link via the floating glass top nav. On mobile (< 1100px), the nav collapses to a hamburger that opens a full-screen drawer with every link.

**Visible in nav:** Home · Founder · Bookkeeping · Taxes · Payroll · Consultant · Admin · Book a Call (CTA button)

**Full list in mobile drawer:** Home · Meet the Founder · Bookkeeping · Taxes · Resources Taxes · Payroll · Business Consultant · Administrative · Contact Us

---

## Founder Photo

Drop Maya's portrait into `assets/maya-portrait.jpg`. It auto-loads on:
- `index.html` (founder strip section)
- `founder.html` (large portrait at the top)

If the file is missing, both pages gracefully fall back to a styled "MG" initials placeholder. No errors, no broken images.

**Recommended:** Square-ish portrait, at least 800x1000px, high quality. Will be displayed with a slight grayscale filter for design consistency (controlled in `styles.css` — search `.portrait-frame img`).

---

## Brand Details (hardcoded across all pages)

- **Business name:** MRG Accounting Service
- **Tagline:** "Where numbers meet strategy"
- **Founder:** Maya Graves
- **Founded:** 2018
- **Experience:** 22+ years corporate finance
- **HQ:** San Diego, CA
- **Phone:** +1 (619) 454-7001
- **Email:** hello@mrgacct.com (placeholder — replace if needed)
- **Coverage:** Serves clients nationwide

If any of these change, search the codebase and replace globally.

---

## Contact Form

`contact.html` uses a multi-step interactive form (3 steps + success state). Currently the submit handler shows the success screen client-side only — **it does not actually send the form data anywhere yet.**

To wire it up to a real backend, edit the `submit` action inside the inline `<script>` at the bottom of `contact.html`. Easy options:
- [Formspree](https://formspree.io) — drop in form action URL
- [Make / Zapier webhook](https://make.com) — POST the form data
- [Resend](https://resend.com) or SendGrid API — direct email
- GoHighLevel webhook if MRG uses GHL

Look for `// In production: POST to backend` — replace that block with a `fetch()` call to your chosen endpoint.

---

## Entity Quiz (Lead Magnet)

`entity-quiz.html` is a self-contained interactive lead magnet built for social-media traffic. Users answer 5 questions, get a personalized entity recommendation (Sole Prop / LLC / S-Corp / C-Corp), and see the actual tax math behind the answer. The page captures email *before* revealing the result.

**Decision logic** lives inside `recommendEntity()` in the inline `<script>`. It is a deterministic rule cascade — same answers always produce the same result. Do not modify it without updating the spec.

**Email wiring:** the lead form currently does not POST anywhere. Look for the `// TODO: Wire to backend` comment in the inline script. Options:
- **Formspree** — drop a form action URL into a `fetch()` call
- **Resend + Vercel serverless function** — POST to `/api/lead.js`, fan out to Maya + the user's report email
- **GoHighLevel webhook** — POST to an inbound webhook, trigger a GHL workflow

The hidden `entity` field on the form already carries the recommendation, so whatever backend you pick can route reports per-entity.

**Confetti:** loaded from `canvas-confetti` via jsDelivr CDN. Brand-locked palette (white / cream / champagne / ivory — no rainbow).

**Promoted via:** the lead-magnet strip on `index.html` (between marquee and services) and on `business-consultant.html` (before BOFU).

---

## Local Preview

Just double-click `index.html`. No server needed.

If you prefer a local dev server:
```bash
# Python
python3 -m http.server 8080

# Or Node
npx serve .
```
Then open `http://localhost:8080`.

---

## Deployment Options

Since the entire site is static, you can host it free on virtually anything:

- **Netlify** — drag and drop this folder onto netlify.com/drop
- **Vercel** — `vercel --prod` from inside this folder
- **Cloudflare Pages** — connect a Git repo or upload the folder
- **GitHub Pages** — push to a repo, enable Pages
- **GoHighLevel Custom Code block** — paste contents of each HTML file into individual GHL pages (note: you'd need to inline `styles.css` into each page for GHL)
- **Any traditional host (FTP)** — drop the folder in your public directory

---

## Editing Tips for AI Assistants (Antigravity, Cursor, etc.)

When asked to modify the site:

1. **Design tokens live in `styles.css` :root** — change colors, spacing, radius there
2. **Every page has the same nav structure** — update nav once per page (no shared header partial since this is plain HTML)
3. **Every page has the same footer structure** — same caveat
4. **The `reveal` and `reveal-stagger` classes** trigger scroll animations via the IntersectionObserver at the bottom of each page's `<script>` tag
5. **The `.serif` and `.kicker` classes** apply the italic Instrument Serif font for editorial highlights
6. **Each service page follows the pattern:** page-hero → lead-block intro → service grid → process/timeline → stats-strip → bofu → footer

Brand voice for copy edits:
- Direct, confident, no fluff
- Editorial cadence — short sentences, italic punctuation moments
- Frames Maya as a strategic ally, not a vendor
- Use "we" voice (the firm), but reference Maya personally where appropriate
- Avoid em dashes — they read as AI-written. Use periods or parentheses instead.

---

## License & Ownership

Built for MRG Accounting Service. All rights reserved © 2026.
