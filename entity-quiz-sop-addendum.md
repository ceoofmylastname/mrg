# Build Spec — Entity Quiz SOP Addendum

> **For Antigravity:** This is an addition to `entity-quiz.html`. Read `entity-quiz-spec.md` first if you haven't. This addendum adds a personalized, state-aware, downloadable filing playbook that appears on the result page beneath the existing tax math section. The whole point: most lead magnets give you a recommendation. This one gives you the recommendation *plus* the exact step-by-step manual to execute on it.

---

## 1. Strategic Context — Why This Matters

The existing quiz tells a user *what* entity to form. This addendum tells them *exactly how to do it themselves* — step by step, link by link, screen by screen. Every SOP is personalized to their name, their state, their ownership structure, and their profit range.

Strategically this transforms the lead magnet from "useful quiz" into a deliverable users would normally pay $97–$297 for. It creates a moment where they go from "this was helpful" to "wait, I just got the entire playbook for free." That moment is when leads convert, get shared, and turn into booked consultations.

The conversion logic is subtle: every SOP ends with a step that says *"this is where most owners hit friction — and where MRG steps in."* That's the BOFU.

---

## 2. Required Changes to `entity-quiz.html`

### 2a. Add a "State" field to the email gate

The current email gate captures first name and email. Add a third required field: **State of formation.**

```html
<div class="field">
  <label>What state will you form the business in?</label>
  <select name="state" required id="state-select">
    <option value="">Select your state…</option>
    <option value="AL">Alabama</option>
    <option value="AK">Alaska</option>
    <!-- ... all 50 states + DC + Puerto Rico ... -->
    <option value="WY">Wyoming</option>
  </select>
</div>
```

Helper text under the field:
> *Most owners file in their home state. If you're planning to form in Delaware or another state for strategic reasons, pick that one.*

The CTA button stays disabled until name, email, AND state are all filled.

### 2b. Add a "Filing Playbook" section to the result page

After the existing tax math table on the result screen, insert a new section that renders the personalized SOP. This section:

- Has its own visual treatment — feels like a premium downloadable resource embedded in the page
- Renders the correct SOP based on the user's recommended entity
- Pulls in user data via interpolation (first name, state, etc.)
- Has a sticky "Download as PDF" button visible while scrolling through the SOP
- Has a "Print" button as a fallback

Section heading: *Your Personalized Filing Playbook*

Sub-heading: *{firstName}, here's exactly how to form your {entityType} in {stateName} — step by step.*

### 2c. Hide the SOP section in the email submission

The SOP only renders after email capture is complete (same trigger as the result reveal). Users don't see any of the playbook content before handing over their email.

---

## 3. Personalization Data Model

These are the variables the SOP renderer pulls from the user's quiz answers:

| Variable | Source | Example values |
|---|---|---|
| `{firstName}` | Email gate input | "Jordan" |
| `{state}` | Email gate input | "CA" |
| `{stateName}` | Lookup from `{state}` code | "California" |
| `{entity}` | Output of `recommendEntity()` | "LLC" |
| `{ownerCount}` | Q1 mapped to integer | 1, 2, 3+, or "solo (planning equity grants)" |
| `{profitRange}` | Q2 raw value | "$80K – $250K" |
| `{growthPlan}` | Q3 mapped to short description | "scaling aggressively" |
| `{wantsProtection}` | Q4 boolean (A or B = true, C = false) | true |
| `{compStrategy}` | Q5 raw value | "Reasonable salary + distributions" |
| `{sosUrl}` | State lookup | "https://bizfileonline.sos.ca.gov" |
| `{filingFee}` | State lookup | "$70" |
| `{processingTime}` | State lookup | "5–10 business days online" |
| `{annualReport}` | State lookup | "Statement of Information due within 90 days, then biennially ($20)" |

All interpolation happens client-side at render time. No backend required.

---

## 4. State Lookup Table

Build this as a JavaScript object inside `entity-quiz.html`. Top 12 most common states get full data. Every other state falls back to a generic template that points the user to their Secretary of State's website.

```javascript
const STATE_DATA = {
  CA: {
    name: "California",
    sosUrl: "https://bizfileonline.sos.ca.gov",
    nameSearchUrl: "https://bizfileonline.sos.ca.gov/search/business",
    filingFee: "$70",
    processingTime: "5–10 business days online, longer by mail",
    annualReport: "Statement of Information — due within 90 days of formation, then every 2 years ($20)",
    stateTaxUrl: "https://www.ftb.ca.gov",
    franchiseTax: "$800 minimum annual franchise tax (waived for first year of new LLCs through 2024)",
    notes: "California requires a Statement of Information within 90 days and an $800 annual franchise tax."
  },
  TX: {
    name: "Texas",
    sosUrl: "https://www.sos.state.tx.us/corp/sosda/index.shtml",
    nameSearchUrl: "https://mycpa.cpa.state.tx.us/coa/Index.html",
    filingFee: "$300",
    processingTime: "5–7 business days online",
    annualReport: "Public Information Report — due annually with franchise tax filing (free if under threshold)",
    stateTaxUrl: "https://comptroller.texas.gov",
    franchiseTax: "Franchise tax — no obligation if revenue is under $1.23M (as of 2024)",
    notes: "No state income tax. Franchise tax exempt for most small businesses."
  },
  FL: {
    name: "Florida",
    sosUrl: "https://dos.fl.gov/sunbiz",
    nameSearchUrl: "https://search.sunbiz.org",
    filingFee: "$125",
    processingTime: "2–5 business days online",
    annualReport: "Annual Report due May 1 each year ($138.75)",
    stateTaxUrl: "https://floridarevenue.com",
    franchiseTax: "No franchise tax. No state income tax for individuals.",
    notes: "Affordable filing fees and no state income tax make Florida popular for small businesses."
  },
  NY: {
    name: "New York",
    sosUrl: "https://dos.ny.gov/corporations-state-records-and-uniform-commercial-code",
    nameSearchUrl: "https://apps.dos.ny.gov/publicInquiry",
    filingFee: "$200",
    processingTime: "Approximately 7 business days online",
    annualReport: "Biennial Statement due every 2 years ($9)",
    stateTaxUrl: "https://www.tax.ny.gov",
    franchiseTax: "Annual filing fee based on income — minimum $25",
    notes: "New York requires LLCs to publish formation notice in two newspapers — significant additional cost."
  },
  DE: {
    name: "Delaware",
    sosUrl: "https://corp.delaware.gov",
    nameSearchUrl: "https://icis.corp.delaware.gov/Ecorp/EntitySearch/NameSearch.aspx",
    filingFee: "$110 for LLC, $89 for Corporation",
    processingTime: "1–3 business days online (expedited available)",
    annualReport: "LLC: flat $300 annual tax. Corporation: annual report + franchise tax (minimum $175)",
    stateTaxUrl: "https://revenue.delaware.gov",
    franchiseTax: "Yes — significant for corporations based on share structure",
    notes: "Preferred state for C-Corps raising venture capital. Established case law and business-friendly courts."
  },
  WA: {
    name: "Washington",
    sosUrl: "https://www.sos.wa.gov/corps",
    nameSearchUrl: "https://ccfs.sos.wa.gov/#/BusinessSearch",
    filingFee: "$200 (LLC), $200 (Corporation)",
    processingTime: "2–5 business days online",
    annualReport: "Annual Report due each year ($60 for LLC)",
    stateTaxUrl: "https://dor.wa.gov",
    franchiseTax: "B&O (Business & Occupation) tax based on gross revenue — varies by industry",
    notes: "No state income tax, but B&O tax applies to gross revenue."
  },
  NV: {
    name: "Nevada",
    sosUrl: "https://www.nvsos.gov/sos",
    nameSearchUrl: "https://esos.nv.gov/EntitySearch",
    filingFee: "$75 (LLC), $75 (Corporation) + $150 initial list of managers",
    processingTime: "7–10 business days online",
    annualReport: "Annual List of Managers/Officers + Business License — combined approximately $350/year",
    stateTaxUrl: "https://tax.nv.gov",
    franchiseTax: "No state income tax. No franchise tax. Annual business license required.",
    notes: "Popular for privacy and lack of state income tax. Higher ongoing fees than expected."
  },
  WY: {
    name: "Wyoming",
    sosUrl: "https://wyobiz.wyo.gov",
    nameSearchUrl: "https://wyobiz.wyo.gov/Business/FilingSearch.aspx",
    filingFee: "$100 (LLC)",
    processingTime: "1–2 business days online",
    annualReport: "Annual Report due first day of formation month each year ($60 minimum)",
    stateTaxUrl: "https://revenue.wyo.gov",
    franchiseTax: "No state income tax. No franchise tax.",
    notes: "Often considered the most LLC-friendly state. Strong privacy protections."
  },
  PA: {
    name: "Pennsylvania",
    sosUrl: "https://www.dos.pa.gov/BusinessCharities/Business",
    nameSearchUrl: "https://www.corporations.pa.gov/Search/CorpSearch",
    filingFee: "$125",
    processingTime: "7–10 business days online",
    annualReport: "Decennial Report (every 10 years) — $70",
    stateTaxUrl: "https://www.revenue.pa.gov",
    franchiseTax: "Flat 9.99% corporate net income tax for C-Corps. LLCs pass through.",
    notes: "One of the few states with a decennial (10-year) report instead of annual."
  },
  IL: {
    name: "Illinois",
    sosUrl: "https://www.ilsos.gov/departments/business_services",
    nameSearchUrl: "https://apps.ilsos.gov/businessentitysearch",
    filingFee: "$150",
    processingTime: "10–15 business days online",
    annualReport: "Annual Report due each year ($75 for LLC)",
    stateTaxUrl: "https://www2.illinois.gov/rev",
    franchiseTax: "Personal Property Replacement Tax of 1.5% on LLC income, plus 4.95% individual rate on pass-through",
    notes: "Higher tax burden than many states. Consider Delaware or Nevada for non-resident operators."
  },
  GA: {
    name: "Georgia",
    sosUrl: "https://sos.ga.gov/corporations-division",
    nameSearchUrl: "https://ecorp.sos.ga.gov/BusinessSearch",
    filingFee: "$100",
    processingTime: "5–7 business days online",
    annualReport: "Annual Registration due April 1 each year ($50)",
    stateTaxUrl: "https://dor.georgia.gov",
    franchiseTax: "Net worth tax on corporations — minimal for small entities",
    notes: "Affordable filing fees and straightforward process."
  },
  AZ: {
    name: "Arizona",
    sosUrl: "https://ecorp.azcc.gov",
    nameSearchUrl: "https://ecorp.azcc.gov/EntitySearch/Index",
    filingFee: "$50 (LLC), $60 (Corporation)",
    processingTime: "3–5 business days online",
    annualReport: "Corporations: Annual Report ($45). LLCs: no annual report required.",
    stateTaxUrl: "https://azdor.gov",
    franchiseTax: "No franchise tax for LLCs",
    notes: "Among the lowest fees and least paperwork of any state for LLCs."
  }
};

// Fallback for any state not in the lookup
const STATE_FALLBACK = (stateCode, stateName) => ({
  name: stateName,
  sosUrl: `Search Google for "${stateName} Secretary of State business filings"`,
  nameSearchUrl: `Search Google for "${stateName} business name availability search"`,
  filingFee: "Varies — typically $50–$300",
  processingTime: "Varies by state — typically 5–15 business days online",
  annualReport: `Most states require an annual or biennial report. Check your ${stateName} Secretary of State website.`,
  stateTaxUrl: `Search Google for "${stateName} Department of Revenue business taxes"`,
  franchiseTax: `Varies. Consult your ${stateName} Department of Revenue for state-specific requirements.`,
  notes: `${stateName} requirements vary. Always confirm current fees and processes on official state websites before filing.`
});
```

Use full state names in a lookup helper so `getStateData("CA")` returns the California object, and `getStateData("MT")` returns the Montana fallback with "Montana" interpolated into the messages.

---

## 5. The Four SOPs

Each SOP renders as a self-contained section on the result page. The renderer picks ONE based on `recommendEntity()`'s output. All SOPs share the same visual treatment — header, prerequisites, numbered steps, troubleshooting, next steps.

Style every SOP section like a print-ready document: white background card on the dark page, generous margins, serif heading hierarchy, numbered steps with explicit "what you'll see" notes. It should look like something a user would proudly save to their Documents folder.

---

### 5A. Sole Proprietorship SOP

```markdown
# {firstName}'s Filing Playbook — Sole Proprietorship

**Recommended structure:** Sole Proprietorship
**State of formation:** {stateName}
**Estimated time to complete:** 1–3 hours
**Estimated cost:** $0–$150

---

## Purpose

This playbook walks you through becoming a legitimate sole proprietor in {stateName} — the simplest possible business structure, where you and the business are legally the same entity.

A sole proprietorship requires almost no formal filing to exist. You become one automatically the moment you earn business income under your own name. The steps below cover the things you *should* do to make it official, separate your finances, and stay compliant.

## Before You Start

- [ ] Your legal name and Social Security Number (you'll use SSN for taxes unless you get an EIN)
- [ ] A business name (optional — if you don't have one, you'll operate under your legal name)
- [ ] A general idea of what licenses your industry requires in {stateName}

---

## Step 1: Decide on Your Business Name

**Action:** Choose whether to operate under your legal name or a DBA ("Doing Business As").

If you'll operate as "Jane Smith Consulting" (your legal name), skip to Step 2.

If you want to operate under a different name like "Bright Path Studio," you'll need to file a DBA / Fictitious Business Name with your county clerk's office.

> **What you'll see:** County clerk websites vary widely. Search Google for "{stateName} fictitious business name DBA filing" and look for an official .gov result.

> **Cost:** $25–$100 depending on your county. Sometimes requires publication in a local newspaper.

---

## Step 2: Get an EIN (Optional but Recommended)

**Action:** Apply for a free Employer Identification Number from the IRS.

Go to: https://www.irs.gov/businesses/small-businesses-self-employed/apply-for-an-employer-identification-number-ein-online

- Click **Apply Online Now**
- Fill out the application (takes about 10 minutes)
- You'll receive your EIN immediately

> **Why this matters:** Without an EIN, you'll give your SSN to clients on every W-9. With an EIN, you protect your SSN.

> **Cost:** Free. Anyone charging you for an EIN is scamming you.

---

## Step 3: Open a Separate Business Bank Account

**Action:** Open a business checking account using your EIN (or SSN) and DBA documentation if applicable.

Recommended options for sole proprietors:
- **Bluevine** — no fees, online application, fast approval
- **Novo** — built for solopreneurs
- **Mercury** — premium feel, good for service businesses
- **Local credit union** — relationships matter for future financing

> **Why this is critical:** Mixing personal and business funds is the #1 mistake sole proprietors make. It destroys your audit trail and complicates taxes massively.

---

## Step 4: Check Required Licenses in {stateName}

**Action:** Determine which licenses or permits your industry requires.

Common requirements:
- City or county business license (most cities require one)
- Industry-specific license (contractor, food service, real estate, etc.)
- Professional license (CPA, lawyer, therapist, etc.)
- Sales tax permit if you sell physical goods in {stateName}

Visit: {sosUrl} (start here) and {stateTaxUrl} (for sales tax)

---

## Step 5: Set Up a Bookkeeping System

**Action:** Choose how you'll track income and expenses from day one.

Options:
- **QuickBooks Self-Employed** — designed for sole proprietors, integrates with Schedule C
- **Wave** — free, basic but functional
- **Spreadsheet** — works if you're disciplined, fails when life gets busy

> **Reality check:** Most sole proprietors abandon their bookkeeping by month 4 and then panic in March. Set this up now or hire someone (like MRG) to handle it monthly.

---

## Step 6: Plan for Quarterly Estimated Taxes

**Action:** Calculate and pay quarterly estimated taxes if you'll owe more than $1,000 in tax for the year.

Federal quarterly deadlines:
- **April 15** — Q1
- **June 15** — Q2
- **September 15** — Q3
- **January 15** — Q4 (of the following year)

Use IRS Form 1040-ES. Pay online at: https://www.irs.gov/payments

> **Most-missed step:** Sole proprietors forget that nobody is withholding taxes from their checks. The IRS expects 25–30% of profits forwarded quarterly. Miss it and you'll owe penalties.

---

## Final Step: Verify You're Set Up

You should now have:

- [ ] Business name decided (legal name or DBA filed)
- [ ] EIN from the IRS (optional but recommended)
- [ ] Separate business bank account
- [ ] Required licenses or permits
- [ ] Bookkeeping system in place
- [ ] A calendar reminder for the next quarterly tax payment

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| Bank rejected my application | Missing DBA paperwork or EIN | Get the EIN first, then re-apply |
| Got a notice from {stateName} | Missing local business license | Visit your city/county website and register |
| Confused about what's deductible | Sole proprietors get fewer tools than LLCs | Consider upgrading to an LLC once profit grows |

---

## Where Most Owners Hit Friction (And Where MRG Steps In)

Sole proprietorship is the simplest structure on paper. The problem isn't filing — it's everything that comes after: tracking deductions correctly, paying quarterly estimates on time, separating finances properly, and knowing when to upgrade to an LLC.

**MRG's sole proprietor package handles:**
- Monthly bookkeeping and Schedule C prep
- Quarterly estimated tax calculation and reminders
- Annual tax filing and strategic planning for the next year
- Guidance on when to upgrade to an LLC (typically around $40K–$50K in profit)

Book your free consultation: [contact.html](contact.html)

---

*Generated for {firstName} · {timestamp} · MRG Accounting Service*
```

---

### 5B. LLC SOP

```markdown
# {firstName}'s Filing Playbook — LLC in {stateName}

**Recommended structure:** Limited Liability Company (LLC)
**State of formation:** {stateName}
**Estimated time to complete:** 1–3 weeks
**Estimated cost:** {filingFee} state fee + optional services

---

## Purpose

This playbook walks you through forming a single-member or multi-member LLC in {stateName} from start to finish. By the end, your LLC will be legally formed, properly documented, IRS-registered, and ready to open a business bank account.

You're choosing an LLC because it's the right balance for your situation: liability protection between you and the business, pass-through taxation (no double tax), and flexibility to elect S-Corp tax treatment later if profits grow.

## Before You Start

- [ ] A name for your LLC (must include "LLC" or "Limited Liability Company")
- [ ] Your home address (or registered agent service address)
- [ ] A short description of what your business does
- [ ] {filingFee} for the state filing fee
- [ ] An hour of focused time for the filing itself

---

## Step 1: Choose and Check Your LLC Name

**Action:** Pick a name and verify it's not already taken in {stateName}.

Go to: {nameSearchUrl}

Search for your desired name. If it returns no results, you're clear. If it's taken, brainstorm variations.

Naming rules in {stateName}:
- Must contain "LLC", "L.L.C.", or "Limited Liability Company"
- Cannot include restricted words like "bank," "insurance," or "trust" without special permission
- Must be distinguishable from other registered businesses

> **What you'll see:** A search box and results table. Most state systems show "no records found" if the name is available.

> **Pro tip:** Also check that the matching .com domain and social handles are available before committing.

---

## Step 2: Appoint a Registered Agent

**Action:** Designate someone to receive legal mail on behalf of your LLC.

Three options:

1. **You serve as your own registered agent** — free, but your home address becomes public record
2. **Use a registered agent service** — $100–$300/year, keeps your address private (recommended: Northwest Registered Agent, Harbor Compliance)
3. **Use a friend or family member at a business address** — free, but they must be available during business hours

> **What you'll see:** When filing, you'll provide the agent's name and a physical street address in {stateName} (no P.O. boxes allowed).

---

## Step 3: File Articles of Organization

**Action:** This is the legal formation document. Filing it creates your LLC.

Go to: {sosUrl}

Look for "Form an LLC" or "Start a Business" on the homepage. You'll create an account if you don't have one.

You'll need to provide:
- LLC name (from Step 1)
- Registered agent name and address (from Step 2)
- Principal business address
- Member/manager information (you and any partners)
- Business purpose (a one-sentence description is usually fine)
- Effective date (most people select "upon filing")

Pay the {filingFee} filing fee with a credit card.

> **What you'll see after filing:** A confirmation page with your file number. You'll receive your stamped Articles of Organization via email within {processingTime}.

{#if state === 'NY'}
> **⚠️ New York-specific:** After formation, you have 120 days to publish notice of your LLC formation in two newspapers in your county. This can cost $500–$2,000 depending on county. Plan for this expense.
{/if}

{#if state === 'CA'}
> **⚠️ California-specific:** {franchiseTax} You'll also file a Statement of Information within 90 days.
{/if}

---

## Step 4: Create an Operating Agreement

**Action:** Draft an Operating Agreement, even if you're a single-member LLC.

This internal document outlines:
- Ownership percentages (100% you if single-member, split if multi-member)
- Voting rights and decision-making process
- How profits and losses are distributed
- Procedures for adding or removing members
- Dissolution procedures

Free templates available at:
- https://www.legalzoom.com/articles/operating-agreement-template
- https://www.nolo.com/legal-encyclopedia/free-books/working-with-independent-contractors-book/chapter6-1.html

> **Why this matters even for solo LLCs:** Without an Operating Agreement, your LLC defaults to {stateName}'s generic LLC rules — which may not match your intent. Courts and banks also like to see it.

{#if ownerCount > 1}
> **Multi-member note:** Since you'll have {ownerCount} owners, this agreement is critical. It prevents disputes about money, decisions, and exits. Don't skip it. Don't use a generic template without customization.
{/if}

---

## Step 5: Get an EIN from the IRS

**Action:** Apply for a free Employer Identification Number.

Go to: https://www.irs.gov/businesses/small-businesses-self-employed/apply-for-an-employer-identification-number-ein-online

- Click **Apply Online Now**
- Select **Limited Liability Company**
- Fill in the form (~10 minutes)
- Receive your EIN immediately on screen — save the PDF confirmation

> **Cost:** Free. The IRS does not charge for EINs. Any third-party service charging $50+ is overcharging for what takes 10 minutes.

---

## Step 6: Open a Business Bank Account

**Action:** Open a dedicated business checking account.

Required documents:
- Stamped Articles of Organization
- EIN confirmation letter (CP 575)
- Operating Agreement
- Personal ID
- Initial deposit (usually $25–$100)

Recommended banks for LLCs:
- **Mercury** — free, online, built for startups
- **Bluevine** — free, online, includes high-yield checking
- **Novo** — free, online, integrates well with QuickBooks
- **Local community bank or credit union** — relationships pay off when you need credit later

> **Why this is non-negotiable:** Mixing personal and business funds is called "piercing the corporate veil." If you do it, courts can strip away your liability protection — defeating the entire point of having an LLC.

---

## Step 7: Register for State Taxes in {stateName}

**Action:** Register with your state's revenue department if applicable.

Visit: {stateTaxUrl}

Common registrations:
- **Sales tax permit** — if you'll sell physical goods or taxable services
- **Employer withholding** — if you'll have W-2 employees
- **State income tax** — most states require LLCs to register

> **What you'll see:** A business registration portal. Most states walk you through which taxes apply based on your business type.

---

## Step 8: Get Required Business Licenses

**Action:** Confirm what local and industry-specific licenses you need.

Check three levels:

1. **City business license** — most cities require any business operating within their limits to register and pay an annual fee ($50–$500)
2. **County business license** — fewer counties require this, but worth checking
3. **Industry-specific licenses** — contractors, food service, healthcare, real estate, financial services, and many others require professional licensing

Search Google for "[your city] business license" and "[your industry] license {stateName}".

---

## Step 9: File Your Initial Report

**Action:** File any required initial filing within the post-formation window.

In {stateName}: {annualReport}

Set a calendar reminder for next year so you never miss this.

---

## Step 10: Set Up Bookkeeping From Day One

**Action:** Choose and configure a bookkeeping system before you make your first transaction.

Recommended approach:
- **QuickBooks Online** — industry standard, integrates with everything
- Connect your business bank account for automatic transaction import
- Set up your chart of accounts (or have MRG do it)
- Schedule monthly closes — don't let a year of receipts pile up

> **Why now matters:** The single biggest reason LLC owners get in trouble at tax time is procrastinating on bookkeeping. Day-one setup costs hours. Year-end catch-up costs thousands.

---

## Final Step: Verify You're Live

You should now have:

- [ ] Stamped Articles of Organization from {stateName}
- [ ] Operating Agreement signed and stored
- [ ] EIN from the IRS
- [ ] Business bank account open
- [ ] State tax registrations completed (where required)
- [ ] Required business licenses obtained
- [ ] Initial report filed (where applicable)
- [ ] Bookkeeping system set up and connected to your bank account
- [ ] Calendar reminders set for annual report renewals

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| Articles of Organization rejected | Name not unique or formatting error | Re-check name search, fix and refile (some states refund partial fees) |
| EIN application errors | LLC name doesn't match state filing exactly | Wait 24h after Articles are stamped, then reapply with exact match |
| Bank account denied | Missing Operating Agreement or mismatched EIN | Bring all formation documents, including Operating Agreement |
| {stateName} sent a notice about back taxes/fees | Missed an initial filing requirement | Visit {sosUrl} to check status and resolve before penalties accrue |

---

## When You Should Consider an S-Corp Election

{#if profitRange === '$80K – $250K' OR profitRange === '$250K+'}
**Your profit level ({profitRange}) means you should evaluate an S-Corp election right now.** An S-Corp election can save you {profitRange === '$80K – $250K' ? '$5,000–$12,000' : '$12,000+'} per year in self-employment tax. The election is made via IRS Form 2553, due within 75 days of formation.
{/if}

{#if profitRange === '$40K – $80K'}
**Watch your profit growth carefully.** Once you cross $50K–$60K in annual profit, an S-Corp election typically becomes worth the added complexity. We recommend revisiting this decision when you file your first year of taxes.
{/if}

{#if profitRange === 'Under $40K'}
**Stay LLC-default for now.** S-Corp election adds payroll complexity and only pays off above ~$50K profit. Re-evaluate annually as your business grows.
{/if}

---

## Where Most Owners Hit Friction (And Where MRG Steps In)

Filing the LLC is the easy part. The expensive mistakes happen in the months after:

- Missing your initial state report and accruing penalties
- Setting up bookkeeping incorrectly and discovering it 9 months later
- Not knowing when to elect S-Corp status (and overpaying SE tax for years)
- Not realizing you needed a sales tax permit until the state sends a notice
- Mixing personal and business funds, destroying your liability shield

**MRG's LLC launch package handles:**
- Monthly bookkeeping configured correctly from day one
- Quarterly check-ins to evaluate S-Corp election timing
- Annual report calendar management
- Tax filing aligned with your specific entity structure

Book your free consultation: [contact.html](contact.html)

---

*Generated for {firstName} · {timestamp} · MRG Accounting Service*
```

---

### 5C. S-Corp SOP

```markdown
# {firstName}'s Filing Playbook — S-Corp in {stateName}

**Recommended structure:** S-Corporation election (filed on top of an LLC)
**State of formation:** {stateName}
**Estimated time to complete:** 2–4 weeks
**Estimated cost:** {filingFee} state LLC fee + payroll software ($40–$80/mo)

---

## Purpose

S-Corp isn't an entity type — it's a **tax election** you make AFTER forming an LLC or Corporation. This playbook walks you through both steps: forming an LLC in {stateName}, then electing S-Corp tax treatment with the IRS.

Why this matters for you: With profit in the {profitRange} range, an S-Corp election can save you significantly on self-employment tax — typically $5,000–$15,000+ per year for someone at your profit level.

## Before You Start

- [ ] A name for your LLC (must include "LLC")
- [ ] {filingFee} for the state LLC filing
- [ ] A plan for what your "reasonable salary" will be (we'll cover this in Step 5)
- [ ] Willingness to run actual payroll (this is non-negotiable for S-Corps)

---

## Step 1: Form Your LLC First

**Action:** Complete the LLC formation steps in {stateName}.

Follow the full LLC playbook (steps 1–10 of the LLC SOP). You need a legally formed LLC before you can elect S-Corp status.

Quick recap:
1. Check name availability at {nameSearchUrl}
2. Appoint a registered agent
3. File Articles of Organization at {sosUrl} ({filingFee})
4. Create an Operating Agreement
5. Get an EIN from the IRS
6. Open a business bank account
7. Register for state taxes
8. Get required licenses
9. File initial state report
10. Set up bookkeeping

**You must complete this before moving to Step 2.**

---

## Step 2: File IRS Form 2553 — The S-Corp Election

**Action:** Elect S-Corp tax treatment by filing Form 2553 with the IRS.

Download Form 2553: https://www.irs.gov/forms-pubs/about-form-2553

Critical deadline: File within **75 days** of LLC formation to have the election apply to your current tax year. Miss the window and the election applies the following year (you'll be taxed as a default LLC for the current year).

The form requires:
- Your LLC's legal name (must match Articles of Organization exactly)
- EIN
- Date of incorporation
- Tax year selection (almost always "calendar year")
- Names, addresses, SSNs of all shareholders/members
- Signed consent from each shareholder/member

**Submit via:**
- Fax (fastest): IRS Service Center fax number based on your state — listed in Form 2553 instructions
- Mail (slower): IRS Service Center address based on your state

Expect IRS confirmation (Form CP261) in 4–8 weeks.

> **Pro tip:** Many CPAs file Form 2553 alongside the LLC formation. If you're doing this yourself, fax it within the first 30 days to give yourself buffer.

---

## Step 3: Determine Your "Reasonable Salary"

**Action:** Establish what salary you'll pay yourself as an S-Corp employee.

The IRS requires S-Corp owner-employees to pay themselves a "reasonable salary" — what someone in your role at your industry would earn. This salary is subject to payroll taxes. Profits above the salary are distributions that escape self-employment tax.

How to determine reasonable:
- Search **Glassdoor** or **PayScale** for your role and industry in {stateName}
- For your profit range ({profitRange}), reasonable salary typically falls between $40,000–$80,000 depending on industry
- Service providers usually need higher salaries (60–70% of profit)
- Capital-intensive businesses can justify lower salaries (30–40% of profit)

> **What the IRS looks for:** A salary that matches market rate for your role, region, and hours worked. Too low and you're a target for audit. Too high and you're overpaying payroll taxes.

> **Document your reasoning:** Save the Glassdoor/PayScale screenshots and a one-page memo on how you determined the salary. If audited, this documentation matters.

---

## Step 4: Set Up Payroll

**Action:** Set up a payroll system to run your salary.

You'll be both employer and employee. Recommended payroll platforms:

- **Gusto** — most popular for S-Corps, $40–$80/mo, handles federal + state filings automatically
- **QuickBooks Payroll** — integrates with QuickBooks Online bookkeeping (this is what MRG uses)
- **OnPay** — affordable alternative, ~$40/mo

Setup checklist:
- [ ] Register as an employer with the IRS (you'll need your EIN)
- [ ] Register with {stateName} for state withholding and unemployment insurance (visit {stateTaxUrl})
- [ ] Set up direct deposit for yourself
- [ ] Configure salary schedule (typically monthly or bi-weekly)
- [ ] Configure tax withholding (federal, state, FICA)

> **What you'll see:** A payroll dashboard showing scheduled pay runs, tax filings, and quarterly forms (941, state equivalents).

> **Reality check:** Running payroll for yourself feels strange the first time. It's just moving money from your business account to your personal account, with payroll taxes withheld and forwarded to the IRS.

---

## Step 5: Take Distributions for Profit Above Your Salary

**Action:** Distribute remaining profits to yourself as owner distributions, not salary.

Mechanics:
- Salary runs through payroll (subject to payroll tax)
- Distributions are simple bank transfers from business to personal (NOT subject to self-employment tax)
- Record each distribution in QuickBooks as an "Owner Distribution" or "Member Draw"

> **The math:** At {profitRange} profit, the SE tax savings on the distribution portion is significant — often $5,000–$15,000+ per year. This is the main reason S-Corp election exists.

---

## Step 6: File Quarterly and Annual Filings

**Action:** Stay current on the additional filings S-Corps require.

| Frequency | Form | Purpose |
|---|---|---|
| Quarterly | Form 941 | Report employer payroll taxes (your payroll provider handles this) |
| Quarterly | State payroll forms | Your payroll provider handles this too |
| Annually | Form 1120-S | S-Corp tax return — due March 15 |
| Annually | Schedule K-1 | Pass-through income statement issued to you personally |
| Annually | W-2 to yourself | Reflects your salary |
| Annually | {stateName} state report | {annualReport} |

> **Critical date:** Form 1120-S is due **March 15** (not April 15 like personal returns). Missing this date costs $200/month per shareholder in penalties.

---

## Step 7: Set Up Bookkeeping That Distinguishes Salary From Distributions

**Action:** Configure your chart of accounts to clearly separate the two.

In QuickBooks (or any accounting system):
- Salary expenses run through Payroll Expenses
- Distributions run through Owner Draw / Member Distribution
- Never mix them — this is what makes S-Corp filing clean at year-end

> **Why this matters:** At tax time, your CPA needs to know exactly what was salary (W-2 reported) versus distribution (K-1 reported). Sloppy bookkeeping turns a clean S-Corp return into a $1,500 cleanup project.

---

## Final Step: Verify Your S-Corp Is Operational

You should now have:

- [ ] LLC formed in {stateName}
- [ ] IRS Form 2553 filed and S-Corp election confirmed (CP261)
- [ ] Reasonable salary determined and documented
- [ ] Payroll system configured and first paycheck run
- [ ] Bank accounts for business and personal kept fully separate
- [ ] Bookkeeping system distinguishing salary from distributions
- [ ] Calendar reminders for quarterly filings and March 15 annual return

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| Form 2553 rejected | Filed past the 75-day window | File Form 2553 with Late Election Relief request — usually granted under Rev Proc 2013-30 |
| IRS questioning my salary | "Reasonable salary" too low | Increase salary going forward and document industry comparisons |
| Confused on what's distribution vs salary | Bookkeeping not separating them | Hire a bookkeeper familiar with S-Corps (MRG specializes in this) |
| Missed March 15 deadline | Calendar oversight | File immediately + extension if needed. Penalty is steep — $200/month/shareholder |

---

## The Tax Math Reminder

At your profit level ({profitRange}):

- LLC default treatment: ALL profit subject to 15.3% self-employment tax
- S-Corp election: ONLY your salary portion subject to payroll tax. Distributions are SE-tax-free.

For someone earning $150,000 profit, this typically means $9,000–$12,000 per year in tax savings. Over 5 years, $50,000+ stays in your pocket instead of going to the IRS.

---

## Where Most Owners Hit Friction (And Where MRG Steps In)

S-Corps work brilliantly when run correctly and become a nightmare when run sloppily. The most common DIY failures:

- Missing the 75-day Form 2553 deadline (most common mistake)
- Paying yourself an unreasonably low salary and triggering audit
- Forgetting Form 1120-S is due March 15 (not April 15)
- Mixing salary and distributions in bookkeeping
- Not registering for state employer taxes in {stateName}

**MRG's S-Corp package handles:**
- Form 2553 election filing
- Reasonable salary determination with audit-proof documentation
- Payroll setup, processing, and all quarterly filings
- Year-end Form 1120-S preparation and K-1 issuance
- Quarterly strategy calls to optimize compensation mix

This is the entity MRG most often recommends and most often runs end-to-end for clients.

Book your free consultation: [contact.html](contact.html)

---

*Generated for {firstName} · {timestamp} · MRG Accounting Service*
```

---

### 5D. C-Corp SOP

```markdown
# {firstName}'s Filing Playbook — C-Corporation in {stateName}

**Recommended structure:** C-Corporation
**State of formation:** {stateName} (consider Delaware if raising capital — see notes below)
**Estimated time to complete:** 2–6 weeks
**Estimated cost:** $200–$500 in filings, $300–$1,500 if using a service

---

## Purpose

This playbook walks you through forming a C-Corporation — the structure required for raising venture capital, issuing multiple classes of stock, granting employee equity, or planning toward acquisition or IPO.

Your quiz answers ({growthPlan}) put you firmly in C-Corp territory. This is the entity sophisticated investors expect to see and the structure that gives you the most flexibility for scale.

## Important Decision Before Starting

**Should you form in {stateName} or Delaware?**

- **Delaware** is the default for venture-backed startups. Mature case law, business-friendly courts, expected by investors.
- **{stateName}** is appropriate if you're not raising outside capital, want to stay local, and don't need the prestige of a Delaware Inc.

{#if state === 'DE'}
✓ You've already selected Delaware. Smart choice for a C-Corp.
{/if}

{#if state !== 'DE' && (growthPlan includes 'raise venture capital')}
> **Strong recommendation:** If you're raising VC, form in Delaware regardless of where you live. Most institutional investors require it. You can register to do business in {stateName} as a "foreign entity" afterward.
{/if}

For this playbook, we'll assume you're filing in {stateName}. If you choose Delaware, the steps are nearly identical — just use https://corp.delaware.gov as your Secretary of State.

## Before You Start

- [ ] A name for your corporation (must include "Inc.", "Corp.", "Corporation", or similar)
- [ ] A clear plan for stock structure (single class for now, or multiple classes if raising)
- [ ] Names of initial directors and officers
- [ ] $200–$500 in formation fees + ongoing annual fees

---

## Step 1: Choose and Check Your Corporation Name

**Action:** Pick a name and verify availability.

Go to: {nameSearchUrl}

Naming rules in {stateName}:
- Must include a corporate identifier: "Inc.", "Corp.", "Corporation", "Incorporated"
- Must be distinguishable from other registered businesses
- Cannot include restricted terms ("bank", "trust", etc.) without permission

> **Pro tip:** Reserve the name if you're not ready to file immediately — most states offer 30-90 day name reservation for $10–$50.

---

## Step 2: Appoint a Registered Agent

**Action:** Designate someone to receive legal process for the corporation.

Same options as LLC:
1. Yourself (free, but address becomes public)
2. Registered agent service (~$100–$300/year — recommended for C-Corps)
3. Friend, family member, or attorney at a {stateName} address

> **Why this matters more for C-Corps:** Corporations face more legal complexity than LLCs. A professional registered agent service catches subpoenas, lawsuits, and government notices that you'd want handled promptly.

---

## Step 3: File Articles of Incorporation

**Action:** Submit the legal formation document.

Go to: {sosUrl}

Look for "Form a Corporation" or "File Articles of Incorporation."

You'll provide:
- Corporation name
- Registered agent name and {stateName} address
- Principal office address
- Number and type of authorized shares (start with 10,000,000 common stock at $0.0001 par value — this is standard for startups)
- Names and addresses of initial directors (minimum 1, can be you)
- Incorporator's name and signature

Pay the filing fee: {filingFee}

> **What you'll see after filing:** A confirmation page with your file number. Stamped Articles of Incorporation arrive via email within {processingTime}.

> **Authorized shares note:** Authorizing 10M shares now (vs 1,000) costs the same but gives you room to issue shares to investors and employees later without filing amendments. Standard startup practice.

---

## Step 4: Create Corporate Bylaws

**Action:** Draft bylaws — the internal rules governing how your corporation operates.

Bylaws cover:
- Board of directors structure and election process
- Officer roles and responsibilities (CEO, CFO, Secretary, etc.)
- Shareholder meeting procedures
- Voting requirements
- Stock issuance procedures
- Amendment procedures
- Indemnification of directors and officers

Free templates available at:
- https://www.legalzoom.com/articles/corporate-bylaws-template
- https://www.nolo.com (search "corporate bylaws template")

> **Why this matters:** Unlike LLCs, corporations are required to maintain formal corporate governance. Skipping bylaws is one of the fastest ways to lose your liability shield in court.

---

## Step 5: Hold the Organizational Meeting

**Action:** Hold the first meeting of incorporators or directors.

Meeting agenda:
- Adopt the bylaws
- Elect initial directors (if not named in Articles)
- Appoint corporate officers (CEO, CFO, Secretary at minimum)
- Authorize issuance of initial shares
- Authorize opening of corporate bank account
- Set fiscal year
- Adopt corporate seal (optional in most states)

Document everything in meeting minutes. Sign and store with corporate records.

> **What this looks like:** If you're a solo founder, this meeting is you sitting at your desk, going through the agenda, and signing minutes you wrote yourself. Sounds silly. Still required.

---

## Step 6: Issue Stock to Founders

**Action:** Issue stock certificates to yourself and any co-founders.

Steps:
- Determine equity split (100% to you if solo, or split among co-founders)
- Decide on vesting schedule for co-founders (standard: 4 years with 1-year cliff)
- Issue physical or electronic stock certificates
- Record issuance in the corporate stock ledger
- Have each shareholder sign a Stock Purchase Agreement
- **CRITICAL:** File 83(b) election with the IRS within **30 days** of stock issuance if stock is subject to vesting

> **The 83(b) election is the most-missed step in C-Corp formation.** Missing the 30-day window can cost founders hundreds of thousands of dollars in unnecessary taxes as the company grows in value.

> **Strongly recommend hiring an attorney for this step** if you have co-founders or any vesting. Templates exist, but the stakes are high enough to justify legal review.

---

## Step 7: Get an EIN from the IRS

**Action:** Apply for a free Employer Identification Number.

Go to: https://www.irs.gov/businesses/small-businesses-self-employed/apply-for-an-employer-identification-number-ein-online

- Click **Apply Online Now**
- Select **Corporation**, then **C-Corporation**
- Complete the application (~10 minutes)
- Save the EIN confirmation PDF

---

## Step 8: Register for State Taxes

**Action:** Register with {stateName} for required state taxes.

Visit: {stateTaxUrl}

C-Corps in {stateName} typically need to register for:
- State corporate income tax
- Employer withholding (once you hire)
- Sales tax permit (if applicable)
- {franchiseTax}

---

## Step 9: Open a Business Bank Account

**Action:** Open a corporate checking account.

Required documents:
- Stamped Articles of Incorporation
- EIN confirmation
- Corporate bylaws
- Board resolution authorizing account opening
- IDs for all signers

Recommended banks for C-Corps:
- **Mercury** — built for venture-backed startups
- **Brex** — strong choice for funded companies
- **SVB / First Republic** — traditional VC-banking relationships
- **JPMorgan Chase** — when you need traditional banking infrastructure

> **For VC-bound companies:** Mercury and Brex have become standard. Set up early — investors will ask.

---

## Step 10: Set Up Corporate Compliance Calendar

**Action:** Schedule the recurring obligations that keep your corporate status valid.

Critical recurring items:
- **Annual shareholder meeting** (with minutes filed in corporate records)
- **Annual board meeting** (with minutes)
- **Annual report to {stateName}** — {annualReport}
- **Form 1120 (federal corporate tax return)** — due April 15 (or 15th day of 4th month after fiscal year-end)
- **Quarterly estimated tax payments** if profitable
- **State franchise tax filings**

> **Why this matters:** Skipping these formalities is how courts "pierce the corporate veil." Your liability protection depends on maintaining the formalities.

---

## Step 11: Set Up Equity Management Software

**Action:** Use a cap table management tool from day one.

Recommended:
- **Carta** — industry standard for venture-backed companies
- **Pulley** — great for early-stage startups
- **AngelList Stack** — solid free option for early stage

> **Why now matters:** Cap table cleanup at Series A is brutal. Tracking equity in a spreadsheet falls apart fast. Set this up before you issue your second stock grant.

---

## Step 12: Plan for Payroll Setup (Before First Hire)

**Action:** When you're ready to hire, set up payroll.

Same platforms as S-Corp setup:
- Gusto
- QuickBooks Payroll
- Justworks (good for HR + benefits + payroll bundle)

C-Corp founders typically also pay themselves through payroll once the company has revenue. Unlike S-Corps, there's no "reasonable salary" requirement, but salary is the standard mechanism for owner compensation in a C-Corp.

---

## Final Step: Verify You're Operational

You should now have:

- [ ] Stamped Articles of Incorporation
- [ ] Corporate bylaws adopted and signed
- [ ] Organizational meeting minutes recorded
- [ ] Initial shares issued and recorded in stock ledger
- [ ] 83(b) elections filed (if applicable) within 30 days
- [ ] EIN from the IRS
- [ ] Corporate bank account opened
- [ ] State tax registrations completed
- [ ] Annual compliance calendar set up
- [ ] Cap table software in place
- [ ] Quarterly estimated tax reminders scheduled

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| Articles rejected | Name issue or formatting error | Re-check name availability, fix and refile |
| Missed 83(b) election deadline | Didn't know about the 30-day rule | Limited options — sometimes attorneys can file late with IRS forgiveness. Don't miss it. |
| Investors asking why you're not in Delaware | Formed in {stateName} | You can convert to a Delaware C-Corp later — process is called "redomestication" or "conversion" |
| Confused about corporate formalities | C-Corps require more discipline than LLCs | Hire a fractional CFO or law firm to manage compliance |

---

## Where Most Owners Hit Friction (And Where MRG Steps In)

C-Corps are powerful but unforgiving. The expensive mistakes:

- Missing the 83(b) election window (irreversible)
- Failing to maintain corporate formalities (loses liability shield)
- Sloppy cap table management (kills fundraising deals)
- Miscategorizing compensation between salary, bonus, and equity
- Missing Form 1120 deadlines (steep penalties)
- Double-taxation surprises at year-end

**MRG's C-Corp package handles:**
- Form 1120 preparation and filing
- Quarterly estimated tax calculations
- Payroll, including officer compensation strategy
- Compliance calendar management
- Coordination with your law firm on equity and stock issuances
- Pre-investment financial readiness (data rooms, board reporting)

For C-Corps especially, having an experienced CFO-level partner is the difference between a clean fundraise and a deal that falls apart in diligence.

Book your free consultation: [contact.html](contact.html)

---

*Generated for {firstName} · {timestamp} · MRG Accounting Service*
```

---

## 6. Download Mechanism

The user can save the SOP as a PDF via two methods. Implement both.

### 6a. Primary — Custom PDF via html2pdf.js

Load html2pdf.js from CDN:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
```

Sticky "Download PDF" button on the result page:

```javascript
document.getElementById('download-sop').addEventListener('click', () => {
  const element = document.getElementById('sop-content');
  const opt = {
    margin:       [15, 15, 15, 15],
    filename:     `${firstName}-${entity}-Playbook.pdf`,
    image:        { type: 'jpeg', quality: 0.98 },
    html2canvas:  { scale: 2, useCORS: true, backgroundColor: '#ffffff' },
    jsPDF:        { unit: 'mm', format: 'letter', orientation: 'portrait' },
    pagebreak:    { mode: ['avoid-all', 'css', 'legacy'] }
  };
  html2pdf().set(opt).from(element).save();
});
```

The element with id `sop-content` should wrap only the SOP section, NOT the rest of the result page. Use a print stylesheet to format the PDF cleanly:

```css
@media print, .pdf-mode {
  #sop-content {
    background: #ffffff;
    color: #0a0a0a;
    padding: 40px;
    font-family: 'Inter', sans-serif;
  }
  #sop-content h1 { font-size: 28px; }
  #sop-content h2 { font-size: 22px; margin-top: 24px; }
  #sop-content h3 { font-size: 18px; margin-top: 16px; }
  #sop-content table { width: 100%; border-collapse: collapse; }
  #sop-content table td, #sop-content table th {
    border: 1px solid #ddd; padding: 8px;
  }
  /* Hide UI chrome — nav, buttons, etc. */
  nav, footer, .download-bar, .share-strip { display: none !important; }
}
```

### 6b. Fallback — Browser Print

Provide a secondary "Print" button that triggers `window.print()`. The print stylesheet above handles formatting.

```html
<button onclick="window.print()" class="btn btn-outline">Or Print This Page</button>
```

---

## 7. Acceptance Criteria

Before marking this addendum complete, verify:

- [ ] State dropdown added to email gate with all 50 states + DC
- [ ] Form submit blocked until name, email, AND state are all filled
- [ ] SOP section renders on result page after email capture only
- [ ] Correct SOP renders based on `recommendEntity()` output
- [ ] All `{firstName}` references in the SOP show the user's actual name
- [ ] All `{stateName}` references show full state name (not code)
- [ ] All `{sosUrl}`, `{filingFee}`, etc. interpolate correctly from STATE_DATA
- [ ] Fallback works for states not in STATE_DATA (e.g., Montana)
- [ ] Conditional sections (`{#if ...}`) render correctly based on quiz answers
- [ ] "Download PDF" button generates a clean white PDF
- [ ] PDF filename follows pattern: `Jordan-LLC-Playbook.pdf`
- [ ] Print button works as fallback
- [ ] PDF includes the SOP only, not nav/footer/buttons
- [ ] PDF table formatting is clean (borders, padding, no overlap)
- [ ] Same quiz answers + same state + same name produce identical SOP (deterministic)
- [ ] Mobile responsive — SOP is readable on a 380px screen
- [ ] Print preview looks good before saving

---

## 8. Update README.md

After implementation, add this section to README.md, under the Entity Quiz section:

```markdown
### SOP Playbook

The quiz result page includes a personalized filing playbook (the "SOP") based on the user's recommended entity and state. Logic lives alongside `recommendEntity()` in the inline script — see `entity-quiz-sop-addendum.md` for the full spec, state lookup table, and SOP templates.

Users can download the SOP as a branded PDF via html2pdf.js (loaded from CDN). The PDF filename includes the user's first name, entity, and "Playbook" — e.g., `Jordan-LLC-Playbook.pdf`.

State lookup data lives in the `STATE_DATA` object. Top 12 states have full data; all others use `STATE_FALLBACK` with generic instructions pointing users to their state's Secretary of State website.
```

---

**End of addendum.** Ship it.
