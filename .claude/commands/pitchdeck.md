---
description: Generate an interactive pitch deck HTML for a partner deal
argument-hint: [PartnerName Country] [--quick]
allowed-tools: [Read, Write, Bash(python3:*), Bash(open:*), Bash(ls:*), Bash(mkdir:*)]
---

You are generating a self-contained, interactive HTML pitch deck for Clear's e-Invoicing partnerships. The deck is a 6-tab single-page app: The Opportunity, Seller Journey, Buyer Experience, What Users See, Your Returns, and Security @ Scale.

Your output is a JSON config file conforming to a strict Pydantic schema. The JSON is then rendered into HTML via a Jinja2 template engine.

## Schema (every field you must generate)

@pitchDeckBot/contentGen/responseSchema.py

## Country Presets

@pitchDeckBot/presets/countries.json

## Sample Config Reference

Before generating JSON, read the sample config for structural reference:
`pitchDeckBot/contentGen/sampleConfig.json`

This is a ~600-line JSON file for the Visa x Clear UAE deal. Use it to understand the exact structure, nesting depth, HTML patterns in phone screens, dashboard row formats, and status-pill CSS classes. Do NOT copy the content -- generate fresh content for the new deal.

---

## Step 1: Parse Arguments

Arguments: `$ARGUMENTS`

Parse the arguments to detect:
- A partner name (e.g., "Visa", "Mastercard") -- first word if present
- A country name (e.g., "UAE", "KSA", "Malaysia") -- second word if present
- `--quick` flag -- minimal questions mode

If a country is detected, look it up in the country presets above and pre-fill: currency, regulatoryBody, invoiceStandard, network, mandateWaves.

---

## Step 2: Ask Questions

Use the AskUserQuestion tool to gather deal information. Ask in phases, 2-4 questions per phase. Do NOT dump all questions at once.

### Phase 1 -- Deal Identity (skip if partner + country parsed from arguments)

Ask:
1. Who is the primary partner? (Name and brand color hex if known)
2. Is there a second partner? (e.g., a local bank for financing -- name and color)
3. Which country? Show the preset list: UAE, KSA, Malaysia, India, EU, Singapore (or custom)

### Phase 2 -- Opportunity Framing (always ask, even in --quick mode)

Ask:
1. What is the core pitch? One sentence describing what this partnership enables.
   Example: "Every e-Invoice carries a Visa payment link, routing B2B payments through Visa rails"
2. What are 3 key stats or dates for the stat cards? (mandate dates, market size, coverage %)
3. What does each partner get from this deal? (one sentence per partner for the returns tab)

### Phase 3 -- Specifics (skip entirely in --quick mode, use sensible defaults)

Ask:
1. Sample company names for the invoice mockup and dashboards? (or generate realistic ones for the country)
2. Any specific security certifications to highlight? (default: OpenPeppol, ISO 27001, SOC 2, AES-256, 3D Secure, encrypted API, PKI, FTA/regulatory signing)
3. Any custom flow steps or variations from the standard seller/buyer journey?

---

## Step 3: Generate the DeckContent JSON

After gathering answers, generate the complete JSON config. Read the sample config first as a structural reference.

### File naming

Use lowercase, underscore-separated names:
- Config: `pitchDeckBot/output/<partner>_<country>_config.json`
- HTML: `pitchDeckBot/output/<partner>_<country>_deck.html`

Example: `visa_uae_config.json`, `mastercard_ksa_deck.html`

### Field-by-field generation guidance

**Top-level fields:**
- `pageTitle`: "<Partner> x Clear <Country> -- e-Invoicing + <product>"
- `footerText`: "<Partner> x Clear <Country> -- Confidential. For internal discussion only."
- `navPartner1Name` / `navPartner1Initial`: Partner name and first letter
- `navPlatformName` / `navPlatformInitial`: Always "Clear" / "C"
- `country`: Country name
- `currency`: From preset or user input

**colors (ColorConfig):**
- `partner1Name`: Lowercase partner name (used as CSS variable name, e.g., "visa")
- `partner1Hex`: Partner brand color (dark shade)
- `partner1Light`: Light tint of partner color
- `partner2Name/Hex/Light`: Second partner or null
- `accentHex`: Gold accent `#F7B600`, `accentLight`: `#FEF3C7`
- `platformHex`: `#16A34A` (Clear green), `platformLight`: `#DCFCE7`

**parties (list of Party):**
Always include at minimum:
- Seller (id: "seller", bg: "bg-seller-light", text: "text-seller")
- Clear (id: "clear", bg: "bg-clear-light", text: "text-clear")
- Partner PayFac or equivalent (id based on role, bg/text matching partner colors)
- Buyer (id: "buyer", bg: "bg-buyer-light", text: "text-buyer")
- Regulatory body (id based on country, bg: "bg-fta-light", text: "text-fta")
- Second partner if applicable

**tab1 (Tab1Opportunity):**
- `headline`: Country-specific mandate + opportunity headline
- `subheadline`: 1-2 sentences setting context
- `statCards`: 3 StatCard objects with value, label, description
- `whatItSolves`: 3 GapItem objects (bold + text) about what e-invoicing handles
- `whatItDoesntSolve`: GapSection about the payment/financing gap
- `quoteBanner`: HTML string with `<strong>` tags highlighting partner name. Use inline HTML.
- `partnerCards`: 1-2 PartnerCard objects (one per partner)

**sellerFlowNodes (dict[str, FlowNode]):**
Follow this standard node ID pattern:
- `sell-erp`: Invoice Created in ERP (layer: compliance, parties: [Seller])
- `sell-transform`: Format Transformation (layer: compliance, parties: [Clear])
- `sell-validate`: Validation Pipeline (layer: compliance, parties: [Clear])
- `sell-proceed`: Proceed / Link already present (layer: payment, parties: [Clear])
- `sell-decision`: Has Pay Link? (layer: payment -- this is the diamond decision node)
- `sell-visa-req`: Request Pay Link (layer: payment, parties: [Clear, <Partner>])
- `sell-ready`: Invoice + Payment Link (layer: payment, parties: [Clear])
- `sell-peppol`: Peppol Delivery (layer: compliance, parties: [Clear, Buyer])
- `sell-email`: Email PDF Invoice (layer: payment, parties: [Clear, Buyer])
- `sell-fta`: Regulatory Reporting (layer: compliance, parties: [Clear, <RegBody>])
- `sell-mashreq`: Financing (layer: payment, parties: [Clear, <2ndPartner>]) -- only if 2nd partner
- `sell-remind`: Payment Reminders (layer: payment, parties: [Clear, Buyer])
- `sell-callback`: Payment Callback (layer: payment, parties: [Clear, Seller])

Each FlowNode: `{ title, subtitle, parties: [string labels], layer: "compliance"|"payment" }`

**sellerValidationSteps:** Validation steps matching the country's invoice standard.
- UAE: XSD, XSLT, BR, Dup, FTA
- KSA: XSD, ZATCA, BR, Dup, Sign
- Other: derive from the invoice standard

**buyerFlowNodes (dict[str, FlowNode]):**
- `buy-receive`: Invoice Received (compliance)
- `buy-validate`: Inbound Validation (compliance)
- `buy-present`: Present to Buyer (compliance)
- `buy-qr`: QR Code Scan (payment)
- `buy-link`: Click-to-Pay (payment)
- `buy-incentives`: Smart Incentives (payment)
- `buy-execute`: Payment Execution (payment)
- `buy-notify`: Settlement + Notify (payment)

**buyerValidationSteps:** Cert, Transport, XSD, Dup (standard for all countries)

**nodeDetails (dict[str, FlowNodeDetail]):**
One entry for EVERY node ID from both seller and buyer flows (typically 21 entries). Each must have:
- `title`: Same as the FlowNode title
- `subtitle`: Same as the FlowNode subtitle
- `parties`: Same parties array
- `detail`: A full paragraph (2-3 sentences) explaining what happens at this step
- `dataFlow`: A technical one-liner describing the data movement (e.g., "ERP -> Clear API: UBL 2.1 XML via REST POST")

**sellerDashboard, partnerDashboard, buyerDashboard (Dashboard):**
Each needs:
- `iconBgClass`: Full Tailwind class like "bg-primary" (includes the bg- prefix)
- `iconInitial`: Single letter
- `title`: Dashboard title
- `headerStats`: Optional list of HTML strings (partner dashboard only)
- `stats`: 3-4 DashboardStat objects with `value`, `label`, `colorClass` (e.g., "gray-900", "primary", "positive")
- `tableHeaders`: 6-7 column headers
- `rows`: 5 DashboardRow objects, each with `cells` array of raw HTML strings

For table cells that need status pills, use this exact HTML pattern:
```html
<span class="status-pill status-paid">Paid</span>
<span class="status-pill status-pending">Pending</span>
<span class="status-pill status-sent">Sent</span>
<span class="status-pill status-clicked">Clicked</span>
<span class="status-pill status-expired">Expired</span>
<span class="status-pill status-available">Available</span>
```

**invoiceMockup (InvoiceMockup):**
Generate realistic seller/buyer companies for the country. Include:
- sellerName, sellerAddress, sellerTrn (tax registration number)
- buyerName, buyerAddress, buyerTrn
- invoiceNumber (e.g., INV-2027-0847), invoiceDate, dueDate
- lineItems: 3 InvoiceLineItem objects with description, qty, rate, amount
- subtotal, vatRate (e.g., "5%"), vatAmount, total, currency

**phoneScreens (list of 4 PhoneScreen):**
Each screen has `stepLabel` (e.g., "1 / 4 -- Invoice Received") and `contentHtml` (pre-formatted HTML).

CRITICAL: The `contentHtml` must use the exact HTML/CSS patterns from the sample config. Read the sample config's phoneScreens to understand the expected structure:
- Screen 1: Invoice received notification with amount, sender, due date
- Screen 2: Payment options (click-to-pay, QR code, smart incentives)
- Screen 3: Secure payment form with amount, card, invoice ref, security badge
- Screen 4: Payment confirmed with checkmark, amount, status details

Use the partner's brand color in buttons and icons. Use Tailwind classes for styling. Include SVG icons where appropriate.

**tab5 (Tab5Returns):**
- `headline` and `subheadline` about what partners capture
- `returnCards`: One ReturnCard per partner with `partnerName`, `partnerInitial`, `colorClass`, `headline`, and 3-4 `bullets` (ReturnBullet with bold + text)
- `adoptionCard`: AdoptionCard with headline and 4 bullets about SME adoption drivers
- `alignmentCard`: AlignmentCard with headline about Clear's platform alignment and body paragraph

**tab6 (Tab6Security):**
- `headline`: "Security @ Scale"
- `subheadline`: About enterprise security and data sovereignty
- `footprintHeadline` / `footprintSubheadline`: About Clear's global presence
- `footprintCards`: 4-6 FootprintCard objects (India, KSA, Malaysia, EU, target country, optionally "and more...")
  - Each has `country`, `borderColorClass` (e.g., "border-orange-400"), `description`
- `securityCards`: 6-8 SecurityCard objects
  - Each has `name`, `description`, `iconBgClass`, `iconColorClass`, `iconType` ("shield" or "lock")
- `infraHeadline`: "<Country> Infrastructure"
- `infraCards`: 3 InfraCard objects (Data Residency, Low Latency, Data Sovereignty)

---

## Step 4: Validate and Render

After writing the JSON config, run these commands:

```bash
# Ensure output directory exists
mkdir -p pitchDeckBot/output

# Validate against Pydantic schema
python3 -c "
import json, sys
sys.path.insert(0, 'pitchDeckBot/contentGen')
from responseSchema import DeckContent
with open('pitchDeckBot/output/FILENAME_config.json') as f:
    DeckContent(**json.load(f))
print('Schema validation passed')
"
```

If validation fails, read the error, fix the specific field in the JSON, rewrite, and re-validate.

```bash
# Render HTML
python3 pitchDeckBot/templateEngine/renderer.py \
  pitchDeckBot/output/FILENAME_config.json \
  pitchDeckBot/output/FILENAME_deck.html

# Open in browser
open pitchDeckBot/output/FILENAME_deck.html
```

---

## Step 5: Deliver

Show the user:
- Partner and country
- Output file path
- Invite them to review the rendered page in their browser
- Ask if they want any changes

If Slack MCP tools are available (check for `mcp__slack` tools), offer to upload the HTML file to a Slack channel.
