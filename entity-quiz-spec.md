# Build Spec — Entity Decision Engine

> **For Antigravity / Cursor / Claude Code:** This is a complete build brief. Read the entire file before generating code. Every section is load-bearing.

---

## 1. Project Context

You are working inside the `mrg-website/` codebase — a static marketing site for **MRG Accounting Service** (Maya Graves, San Diego, CA). The site is pure HTML + CSS + vanilla JS, no frameworks, no build step. Design system tokens live in `styles.css` (`:root { ... }`).

**Brand voice:** Editorial luxury. Direct, sharp, no fluff. Inter sans + Instrument Serif italic for editorial accents. Pure black `#0a0a0a` background, white text, subtle warm cream `#e8d9b4` accent used sparingly.

Read `README.md` and `styles.css` before writing code. Match the existing aesthetic exactly — do not invent a new design language.

---

## 2. What You Are Building

A single self-contained page: **`entity-quiz.html`** — an interactive 5-question quiz that recommends one of four business entity structures (Sole Proprietorship, LLC, S-Corp, or C-Corp), captures the user's email, and delivers a deeply educational personalized result page with a confetti payoff moment and built-in referral mechanism.

This is MRG's primary lead magnet. Its job is to:
1. Capture qualified leads at the moment they're deciding how to structure a business
2. Educate so thoroughly that users *want* to share it
3. Funnel into MRG's Business Launch and Tax services

The user should finish the quiz and think two things at once: *"That was the most useful thing I've done all week"* and *"I need to send this to three friends."*

---

## 3. Tech Constraints

- **Single self-contained HTML file** named `entity-quiz.html` placed at the root of `mrg-website/`
- Link to the shared `styles.css` (do not duplicate styles unless page-specific)
- All quiz logic, animations, and state in vanilla JS — no React, Vue, jQuery, or build tools
- Use the same Google Fonts already loaded (Inter + Instrument Serif)
- Confetti library may be loaded from CDN (canvas-confetti via jsDelivr is acceptable)
- Print-friendly CSS so the result page can be saved as PDF via browser print
- Mobile responsive (test breakpoints: 480px, 780px, 1100px)
- No localStorage or browser storage APIs — use in-memory state only

---

## 4. Page Structure

The page is a single HTML file with five logical screens, each toggled via JS (one visible at a time):

1. **Landing** — hero, value prop, "Start the Quiz" CTA
2. **Quiz** — one question visible at a time, 5 total, progress bar, smooth transitions
3. **Calculating** — short animated interstitial (2.5 seconds) that feels intentional
4. **Email gate** — soft email capture before result reveal
5. **Result** — personalized entity recommendation with deep education + confetti + share

Use the existing nav bar (copy from `index.html`) and footer (copy from `index.html`). The quiz itself is the page's body content.

---

## 5. Design Direction

**Match the existing site exactly.** Do not invent. Specifically:

- Backgrounds: `var(--black)` with ambient glow orbs (use the `.ambient` and `.glow` system already in styles.css)
- Cards: glassmorphism via the existing `.glass` pattern
- Headlines: Inter 700 for bold modern; italic Instrument Serif for editorial moments (use `<em>` inside headlines, styled via the existing `.serif` class)
- Buttons: white primary (`.btn-primary`), ghost outlined (`.btn-ghost` or `.btn-outline`)
- Spacing: generous, breathable, magazine-like
- Animations: scroll-revealing already exists (`.reveal` class + IntersectionObserver). Re-use it. Add custom animations only for quiz-specific moments below.

**Custom page-specific moments:**

- **Progress bar:** thin horizontal line at top of quiz, fills with `var(--accent)` color as user advances. Smooth `cubic-bezier(.2,.8,.2,1)` transition.
- **Question entry:** each new question fades + slides up from below (300ms)
- **Question exit:** previous question fades + slides up and out (200ms)
- **Option hover:** scale 1.02, border becomes `var(--line-bright)`, subtle warm glow
- **Option selected:** background flips to white, text to black, instant snap (no animation delay — feels responsive)
- **Calculating screen:** centered animated dot loader or rotating editorial "i.", "ii.", "iii." numerals counting up. Copy: *"Analyzing your answers…"* → *"Cross-referencing tax code…"* → *"Building your recommendation."*
- **Result reveal:** the recommendation card scales in from 0.95 → 1.0 with a fade. Confetti fires from bottom-center 200ms after reveal. Use `canvas-confetti`. White + warm-cream colored particles only (no rainbow — stay on brand). Two burst pattern with 400ms delay between bursts.

---

## 6. The Landing Screen

**Eyebrow:** `Free Tool · 5 Questions · 2 Minutes`

**Headline (H1):**
> Should you be an<br/>*LLC, S-Corp, or C-Corp?*

Use the `<em>` wrapper on the second line to render it in Instrument Serif italic.

**Sub-headline:**
> Choose wrong and you'll overpay taxes for years — or worse, expose your personal assets when the business hits a problem. This 2-minute quiz tells you the entity structure that actually fits your situation, plus the tax math behind why.

**Primary CTA button:** `Start the Quiz →`

**Trust strip below CTA:** four small metrics:
- `5 questions`
- `~2 minutes`
- `Built by 22-yr CPA`
- `Personalized result`

**Visual:** an editorial-style floating frame on the right (similar to the hero card on `index.html`) showing a mockup of the result page. Use a placeholder serif heading like *"Your recommendation: S-Corp"* with sample bullet points.

---

## 7. The 5 Questions

**Each question is asked one at a time.** Layout:

- Question number top-left in Instrument Serif italic: `01.`, `02.`, etc.
- Progress bar at top (5 segments, one fills per question)
- Question text large, editorial, centered or left-aligned
- Optional helper text in `var(--text-2)` explaining context
- Answer options as large clickable cards in a 2×2 or 2×3 grid (depending on count)
- Each option has: a bold title + a one-line description below
- "Back" button bottom-left (disabled on Q1)
- Selecting an option auto-advances after 300ms (gives user time to see selection)

### Question 1

**Title:** How many people will own this business?

**Helper:** Owners with equity, not employees.

**Options:**
- `A. Just me` — *Solo founder, sole control*
- `B. Me + one partner` — *Two co-founders splitting equity*
- `C. Three or more owners` — *Multi-owner group or partnership*
- `D. Just me, but I plan to give employees equity or be acquired` — *Solo now, structured for growth*

### Question 2

**Title:** What's the expected annual profit?

**Helper:** Profit = revenue minus business expenses. Best estimate is fine.

**Options:**
- `A. Under $40,000` — *Side income or early stage*
- `B. $40,000 – $80,000` — *Established small business*
- `C. $80,000 – $250,000` — *Strong profit, real money on the table*
- `D. $250,000+` — *High-profit operator*

### Question 3

**Title:** What are your growth plans over the next 3–5 years?

**Helper:** Be honest. Aspirations matter for picking the right structure today.

**Options:**
- `A. Keep it lean and profitable` — *Solo or small team, no big growth plans*
- `B. Grow steadily, hire a few people` — *Organic growth, reinvest profits modestly*
- `C. Scale aggressively across markets or states` — *Hire fast, expand fast*
- `D. Raise venture capital or outside investors` — *Equity rounds, institutional money*

### Question 4

**Title:** How important is protecting your personal assets?

**Helper:** Your home, savings, personal property — separated from the business legally.

**Options:**
- `A. Critical — I don't want personal exposure` — *Liability shield is non-negotiable*
- `B. Important but not urgent` — *Want protection, willing to phase it in*
- `C. Not a major concern right now` — *Low-risk industry, comfortable with personal exposure*

### Question 5

**Title:** How do you plan to take money out of the business?

**Helper:** This determines how you'll be taxed on what you earn.

**Options:**
- `A. All profits flow to me as personal income` — *Simple pass-through, year-end taxes*
- `B. Reasonable salary + distributions on top` — *Salary on W-2, additional draws as distributions*
- `C. Reinvest most profits back into growth` — *Profits stay inside the business to fund expansion*
- `D. Mix of salary, equity grants, and dividends` — *Complex compensation including stock-based*

---

## 8. Decision Logic — DETERMINISTIC

> **Critical:** Same answers must always produce the same result. Five users answering identically must all see the same entity recommendation. No randomness. No scoring tiebreakers that can swing.

Use a **rule cascade** evaluated top to bottom. The first rule that matches wins. The default case at the end catches everything else.

```javascript
function recommendEntity(answers) {
  // answers = { q1: 'A'|'B'|'C'|'D', q2: ..., q3: ..., q4: ..., q5: ... }

  // RULE 1 — Venture capital plans force C-Corp (VCs require it for stock issuance)
  if (answers.q3 === 'D') return 'C-Corp';

  // RULE 2 — Solo founder structuring for equity grants / acquisition → C-Corp
  if (answers.q1 === 'D') return 'C-Corp';

  // RULE 3 — Mixed compensation including equity grants → C-Corp
  if (answers.q5 === 'D') return 'C-Corp';

  // RULE 4 — Aggressive scaling + high profit + reinvesting → C-Corp
  if (answers.q3 === 'C' && (answers.q2 === 'C' || answers.q2 === 'D') && answers.q5 === 'C') return 'C-Corp';

  // RULE 5 — Sole Proprietorship: solo, low profit, no protection concern, simple pass-through
  if (answers.q1 === 'A' && answers.q2 === 'A' && answers.q4 === 'C' && answers.q5 === 'A') return 'Sole Proprietorship';

  // RULE 6 — S-Corp: profit ≥ $80K AND owner wants salary + distributions structure
  if ((answers.q2 === 'C' || answers.q2 === 'D') && answers.q5 === 'B') return 'S-Corp';

  // RULE 7 — S-Corp: profit $40K-$80K AND wants salary+distributions AND wants protection
  if (answers.q2 === 'B' && answers.q5 === 'B' && (answers.q4 === 'A' || answers.q4 === 'B')) return 'S-Corp';

  // RULE 8 — DEFAULT — LLC is the right answer for most small business owners
  // (covers pass-through taxation + liability protection + flexibility)
  return 'LLC';
}
```

This cascade is the **single source of truth.** Do not modify it. Do not add weighting. Do not introduce randomness. Document each rule's reasoning in code comments so it's auditable.

---

## 9. Email Gate (Between Calculating and Result)

After the calculating animation finishes (2.5 seconds), show a brief email capture screen *before* revealing the result.

**Headline:** Your recommendation is *ready.*

**Sub-headline:** Where should we send your detailed report? You'll also unlock a printable PDF version + Maya's full breakdown of the tax math behind your result.

**Form fields:**
- First name (required)
- Email (required, validated)

**CTA button:** `Reveal My Recommendation →`

**Below button (small text in `var(--text-3)`):**
> We respect your inbox. No spam, no daily emails. You'll get your result, a short follow-up with bonus resources, and that's it unless you opt in for more.

**Validation:** Email regex check on blur. CTA disabled until both fields filled and email is valid format.

**Submit behavior:**
- Capture the values to a JS object (for now — backend wiring is in a separate step)
- Show inline success message OR transition straight to result screen
- The form submit does NOT need to actually POST anywhere yet — leave a clearly-marked TODO comment in the JS pointing to where the Resend/Formspree fetch should be added later
- Add a hidden field capturing the recommended entity so the future backend knows what report to send

```javascript
// TODO: Wire to backend. Suggested:
// fetch('/api/lead', {
//   method: 'POST',
//   headers: { 'Content-Type': 'application/json' },
//   body: JSON.stringify({ firstName, email, entity: recommendation, answers })
// });
```

---

## 10. Result Page — Education Heavy

This is the payoff. The user just gave you their email. You owe them genuine value.

### Layout

1. **Confetti fires** (canvas-confetti, two bursts, white + cream particles only)
2. **Result hero card** — centered, large, with the recommendation
3. **The reasoning** — why this is the right answer for *their* answers (personalized)
4. **The full breakdown** — deep education on the entity (5+ sections)
5. **Tax math** — concrete numbers showing the savings or trade-offs
6. **Next steps** — exactly what to do this week
7. **Maya's note** — personal tone, builds trust
8. **CTA: Book a consultation** — primary
9. **Share strip** — referral mechanism

### Hero card

Top of result page:

> Your recommended structure is
>
> # *S-Corporation*
>
> Based on your answers — {profit range}, {growth plan}, {ownership structure} — an S-Corp is the structure that will save you the most in taxes while protecting your personal assets.

Replace the entity name + reasoning dynamically based on the recommendation. Each entity gets its own reasoning template.

### Reasoning blocks (PERSONALIZED per recommendation)

For each entity, write a 4-sentence reasoning block that pulls in their actual answers. Example for S-Corp:

> You're earning between $80K and $250K in profit, which is the sweet spot where S-Corp tax savings start to dramatically outweigh the additional paperwork. You also indicated you'd prefer to take a reasonable salary plus distributions, which is exactly how S-Corps unlock self-employment tax savings on profits above your salary. With your interest in steady growth and personal asset protection, an S-Corp gives you the liability shield of a corporation with the pass-through taxation of a partnership.

Each entity needs its own reasoning template that interpolates the user's specific answers. Show *why* by referencing what they told you.

### The full breakdown — for each entity

Provide a deep education section with these subsections (use clean editorial section headings):

**Sole Proprietorship**
- *What it is* — simplest possible business structure, no separation between you and the business
- *Tax treatment* — all profits flow to your personal 1040 via Schedule C, subject to self-employment tax
- *Liability* — none. Personal assets fully exposed.
- *Best for* — side income, very low risk industries, testing a business idea
- *Watch outs* — no protection if sued, harder to build business credit, looks less professional
- *Setup time* — instant (you're already one if you've earned business income)
- *Estimated annual cost to maintain* — $0–$200

**LLC (Limited Liability Company)**
- *What it is* — flexible legal entity that separates business from personal
- *Tax treatment* — by default, single-member LLCs are taxed like sole props; multi-member like partnerships. Can elect S-Corp taxation later.
- *Liability* — strong protection if maintained properly (separate bank account, proper documentation)
- *Best for* — most small businesses. The default answer when there's no compelling reason to choose otherwise.
- *Watch outs* — must respect the corporate veil (don't mix personal and business funds), annual state filing fees in most states
- *Setup time* — 1–4 weeks
- *Estimated annual cost to maintain* — $50–$800 depending on state

**S-Corporation (S-Corp election)**
- *What it is* — a tax election (made by an LLC or corporation) that changes how the IRS taxes your business
- *Tax treatment* — you pay yourself a "reasonable salary" subject to payroll tax; remaining profits are distributions NOT subject to self-employment tax
- *Liability* — same as your underlying entity (LLC or corp)
- *Best for* — profitable businesses earning $50K+ in net income where the owner is actively working in the business
- *Watch outs* — must run actual payroll, file Form 1120-S, "reasonable salary" must be defensible, more administrative complexity
- *Setup time* — election filed via Form 2553, effective for that tax year if filed within 75 days
- *Estimated annual cost to maintain* — $1,500–$3,500 (payroll, additional filings, accountant fees)
- *Why this matters* — the SE tax savings on $100K profit can easily be $5K–$8K per year, more than paying for the added complexity

**C-Corporation**
- *What it is* — a fully separate legal entity that pays its own taxes
- *Tax treatment* — corporate income tax at 21%, then dividends taxed again at the personal level (double taxation)
- *Liability* — strongest protection of any entity type
- *Best for* — businesses raising venture capital, planning to issue multiple classes of stock, granting equity to employees, or reinvesting profits heavily
- *Watch outs* — double taxation on distributed profits, more complex compliance, board governance requirements
- *Setup time* — 2–6 weeks
- *Estimated annual cost to maintain* — $2,000–$10,000+
- *Why this matters* — VCs and institutional investors require C-Corp structure (typically Delaware C-Corp). Equity compensation plans require it. If you're building to raise or sell, this is the only viable answer.

### Tax math section

Show a concrete example with actual numbers based on their profit range. Example for S-Corp recommendation at $150K profit:

> **The math for you:**
>
> | | LLC (default) | S-Corp election |
> |---|---|---|
> | Net profit | $150,000 | $150,000 |
> | Reasonable salary | — | $60,000 |
> | Distributions | — | $90,000 |
> | Self-employment tax (15.3%) | $21,182 | $9,180 |
> | **Annual SE tax savings** | — | **$12,002** |
>
> Over five years, that's **$60,000+** kept in your pocket instead of sent to the IRS — and that's before factoring in the tax planning we'd add on top.

Build a similar table for whichever entity is recommended. Use realistic numbers based on the user's profit answer.

### Next steps

Three concrete actions, numbered:

1. *Schedule a free consultation with Maya* — 30 minutes, no pressure, walk through your specific situation
2. *Bookmark the Resources page* — IRS forms, deadlines, calculators you'll need
3. *Forward this quiz to two business owners you know* — they'll thank you

### Maya's note

A short signed message that feels personal, not templated:

> A note from Maya —
>
> *Entity selection is one of the most important early decisions you'll make as a founder. The right structure compounds in your favor for years. The wrong one quietly costs you tens of thousands.*
>
> *If you want to talk through your specific situation — including the parts a quiz can't capture — I'm one click away.*
>
> — Maya Graves, Founder & Lead Strategist, MRG Accounting Service

### Primary CTA

`Book My Free Consultation →` — links to `contact.html#consult`

### Share strip

A horizontal strip at the bottom with:

> **Know someone starting a business?**
>
> Forward this quiz. They'll thank you — and you'll save them from picking the wrong structure.

Three share buttons:
- Copy link (copies the page URL to clipboard, shows brief "Copied!" confirmation)
- Email (mailto with subject line + body filled in)
- Text/SMS (sms: link for mobile)

**Pre-filled share copy:**
> Subject: This entity quiz is worth 2 minutes
> Body: I just took this LLC vs S-Corp vs C-Corp quiz from a CPA in San Diego — it's the clearest breakdown I've seen. Worth the 2 minutes if you're starting or restructuring a business. [URL]

---

## 11. Animations & Micro-interactions Reference

| Moment | Animation |
|---|---|
| Page load | Hero fades up via existing `.reveal` class |
| Progress bar | Width transition, 400ms cubic-bezier |
| Question enter | Fade + translateY(20px → 0), 300ms |
| Question exit | Fade + translateY(0 → -20px), 200ms |
| Option hover | Scale 1.02, border lightens |
| Option selected | Snap to selected state, no delay |
| Calculating | Rotating numerals i. ii. iii., 2.5s total |
| Email gate enter | Fade + slide up, 400ms |
| Result hero | Scale 0.95 → 1.0 + fade, 500ms |
| Confetti | canvas-confetti, two bursts, 400ms apart, white + cream particles |
| Share button click | Brief scale pulse + "Copied!" tooltip |

---

## 12. Acceptance Criteria

Before marking this complete, verify:

- [ ] All 5 questions render, advance forward and backward, preserve selections
- [ ] Progress bar fills smoothly and matches the current question
- [ ] Decision logic is implemented exactly as written in section 8 — no scoring, no randomness
- [ ] Tested all four entity outcomes by answering different combinations
- [ ] Same answer combination always produces same recommendation (test: refresh and re-answer identically — must match)
- [ ] Email capture validates email format and requires both fields
- [ ] Calculating screen runs for ~2.5 seconds and feels intentional (not bug-like)
- [ ] Confetti fires once on result reveal, white + cream particles only
- [ ] Result page is personalized — reasoning block references the user's actual answers
- [ ] Tax math table uses numbers appropriate to the user's profit range answer
- [ ] Maya's note appears with proper styling
- [ ] Share buttons work — copy-link, mailto, sms
- [ ] Mobile responsive — quiz is usable on a 380px-wide screen
- [ ] Print-to-PDF produces a clean printable version of the result page (no nav, no quiz, just the result)
- [ ] Matches existing site visual aesthetic (run the site in a browser and compare)
- [ ] No console errors
- [ ] Loads in under 2 seconds on a normal connection

---

## 13. After Build — Wiring the Email

The submit handler should be wired to a real backend in a follow-up task. Suggested approaches:

**Option A — Formspree (zero backend)**
Replace the TODO with a fetch POST to a Formspree form endpoint. Formspree forwards the lead data to any email and integrates with Mailchimp, ConvertKit, etc.

**Option B — Resend + Vercel serverless function**
Add a `/api/lead.js` serverless function that receives the POST, calls the Resend API to send Maya the lead notification AND emails the user their personalized report (use HTML email template generated server-side from the same content shown on the result page).

**Option C — GoHighLevel webhook**
If MRG is on GHL, POST to a GHL inbound webhook that adds the contact to a "Entity Quiz Lead" pipeline and triggers a workflow that emails the report.

Document the chosen approach in `README.md` once decided.

---

## 14. File Output

Save the finished page as:

```
mrg-website/entity-quiz.html
```

Update the home page (`index.html`) and the Business Consultant page (`business-consultant.html`) to add a CTA banner promoting the new quiz. Suggested placement: a horizontal strip above the footer or just below the hero.

Update `README.md` to add `entity-quiz.html` to the file structure section.

---

**End of spec.** Ship it.
