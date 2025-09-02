# Question 5 Report

## Question
Which suppliers should I prioritise to engage for emissions reduction efforts?

## Answer
Executive summary:
Prioritise engagement first with your top electricity suppliers for scope2 (Supplier A and Supplier B), and then target suppliers contributing to scope3 purchased_goods and upstream_transport categories. Supplier A and Supplier B together account for ~62.5% of scope2 emissions (900,000 kg and 600,000 kg CO2e respectively, of 2,400,000 kg CO2e total). In scope3, purchased_goods dominates with ~5,000,000 kg CO2e (51% of scope3 total of 9,800,000 kg CO2e); upstream_transport is next at ~1,960,000 kg CO2e (20%).

Detailed findings (data-backed):
- Scope2 (electricity) supplier hotspots (reporting year totals):
  - Total scope2 emissions: 2,400,000 kg CO2e
  - Supplier A: 900,000 kg CO2e (37.5% of scope2)
  - Supplier B: 600,000 kg CO2e (25.0%)
  - Supplier C: 360,000 kg CO2e (15.0%)
  - Supplier D: 240,000 kg CO2e (10.0%)
  - Other suppliers combined: 300,000 kg CO2e (12.5%)
  Data notes: 8 rows have missing supplier names (~120,000 kg CO2e) and one extreme outlier row (electricity_kwh=9,999,999) was excluded pending verification. Also 3 negative meter reads were flagged as adjustments but are numerically negligible.

- Scope3 (value chain) category hotspots:
  - Total scope3 emissions: 9,800,000 kg CO2e
  - purchased_goods: 5,000,000 kg CO2e (51% of scope3)
  - upstream_transport: 1,960,000 kg CO2e (20.0%)
  - waste_generated_in_operations: 980,000 kg CO2e (10.0%)
  - business_travel: 490,000 kg CO2e (5.0%)
  - other categories: 1,370,000 kg CO2e (14.0%)
  Data notes: 20 scope3 rows missing emission factors and 24 missing co2e_kg, representing estimation uncertainty (~8% of scope3). Supplier names are not stored in a structured supplier column for scope3; some supplier references exist in free-text activity_description and require procurement mapping.

Cross-reference with GHG Protocol guidance:
- GHGP recommends prioritising indirect emissions (scope3) for cost-effective reductions where feasible, but also highlights verification challenges and the value of supplier/facility-specific emission factors:
  - “Including indirect GHG emissions in a target will facilitate more cost-effective reductions... scope 3 emissions will primarily be calculated from activity data... if source- or facility-specific emission factors are available, they are preferable to more generic factors.” (ghg_protocol)
  - “Use supplier reports, invoices and meter readings as evidence for scope 3 data where available.” (ghg_protocol)
  - “For scope3 entries where EF is a default or estimated, require an EF_source reference and mark as estimated.” (ghg_protocol)

Recommended supplier engagement prioritization (actionable list):
1) Highest priority — Electricity suppliers (immediate, high-impact):
   - Engage Supplier A and Supplier B first (together ~62.5% of scope2 emissions). Key asks:
     - Request supplier-specific grid emission factors or guaranteed renewable energy product details (e.g., contractual RECs, PPA availability).
     - Explore switching to lower-carbon tariff or procure certified renewable electricity; request time-of-use data to enable load-shifting or on-site storage opportunities.
     - Negotiate supplier-level energy efficiency or demand-response programs for your facilities.
   - Rationale: Large, concentrated share of scope2 — relatively straightforward to reduce by switching tariffs/contract terms or procuring renewables (aligned with GHGP advice to use supplier-specific factors).

2) Second priority — Purchased goods suppliers (strategic supply-chain decarbonization):
   - Purchased_goods represents ~51% of scope3 (~5,000,000 kg CO2e). Steps:
     - Map purchased_goods emissions to specific suppliers by linking procurement/invoice records to scope3 rows (requires data cleansing; several scope3 rows lack supplier structure currently).
     - Identify top 20 suppliers by spend or spend-weighted emissions within purchased_goods — target these for supplier engagement and supplier-specific EFs.
     - Request supplier GHG footprints, low-carbon product options, material substitution opportunities, and supplier-side efficiency programs.
     - Use supplier engagement tiers: Tier 1 (high-impact suppliers — collaborative decarbonization plans), Tier 2 (medium impact — supplier reporting and improvement targets), Tier 3 (low impact — procurement standards).
   - Rationale: Largest share of scope3; GHGP supports using supplier reports and facility-specific factors for accuracy.

3) Third priority — Logistics / upstream transport providers:
   - Upstream_transport ~20% of scope3 (≈1,960,000 kg CO2e). Actions:
     - Engage major freight carriers for modal shift, load optimization, fleet fuel efficiency, and low-carbon fuel adoption.
     - Request carrier-specific EFs or distance-weighted emissions per shipment to set reduction targets.

4) Other categories / operational suppliers (lower immediate priority but necessary):
   - Waste management providers (waste_generated_in_operations ~10%) — ask for waste diversion or methane capture programs.
   - Business travel suppliers / travel managers — reduce travel emissions via policy changes, encourage rail over air where practical, and require lower-emission carriers where possible.

Data quality and pre-engagement steps (required to ensure effective outreach):
- Normalize supplier names in scope2 (master supplier table) before outreach to avoid misdirected engagement (8 missing supplier rows represent ~5% of scope2 uncertainty).
- For scope3, add supplier_id to purchased_goods rows by matching procurement/invoice records; where supplier-specific EFs are unavailable, request supplier-reported data or apply validated sector EFs (and mark as estimated per GHGP guidance).
- Validate and resolve the scope2 outlier (electricity_kwh=9,999,999) before sending any supplier-level requests.

Suggested engagement KPIs and asks to suppliers:
- Request: annual supplier-specific GHG footprint (scope1 & scope2) and methodology/documents (meter readings, fuel invoices) per GHGP verification checklist.
- Near-term KPI: percentage of their energy from renewable sources or an offered green tariff for your sites.
- Mid-term KPI: supplier commitment to science-based targets or year-on-year emissions intensity reductions for products sold to you.
- Procurement KPI: percentage of spend with suppliers providing low-carbon products or supplier-provided EFs.

Estimated potential impact (illustrative):
- If Supplier A reduces intensity by 30% via renewable procurement or energy efficiency, scope2 savings could be ~270,000 kg CO2e per year.
- If purchased_goods suppliers engaged across top suppliers reduce emissions intensity by 10% across the purchased_goods category, potential scope3 savings ~500,000 kg CO2e per year.
Note: These are illustrative; precise savings depend on supplier-specific EFs and achievable reduction pathways.

Next steps recommended (implementation roadmap):
1. Immediate (0–3 months):
   - Normalize supplier names; verify scope2 outlier; generate supplier-specific emissions reports for Supplier A and Supplier B; send initial data requests.
   - Map purchased_goods scope3 rows to procurement/supplier records to identify top suppliers by emissions.
2. Short term (3–9 months):
   - Run supplier engagement campaigns: data requests, workshops for high-impact suppliers, and pilot supplier decarbonization projects (e.g., low-carbon materials, renewables for suppliers).
   - Implement contractual clauses requiring supplier emissions reporting and low-carbon options in new contracts.
3. Medium term (9–24 months):
   - Negotiate longer-term renewable energy procurement (PPAs/RECs) where feasible; support suppliers to set decarbonization targets.
   - Track KPIs and integrate supplier emissions into procurement decision-making.

References (from indexed knowledge base):
- GHG Protocol Corporate Standard (selected excerpts):
  - Preference for source- or facility-specific emission factors where available; use supplier reports and invoices for scope3 data; require EF_source and mark defaults as estimated for scope3 entries. (See ghg_protocol indexed spans.)

Appendix — Data caveats:
- All numerical values above derived from current loaded datasets (scope2: 80 rows; scope3: 200 rows). Data quality issues noted above (missing suppliers, missing EFs, and outliers) must be resolved to finalize targets and calculate precise supplier-specific reduction opportunities.

If you want, I can next:
- Normalize supplier names and re-run the scope2 supplier totals to produce sanitized supplier contact lists and outreach packs; OR
- Backfill scope3 supplier attribution by matching procurement data (if you provide procurement CSV) and apply peer benchmark/default EFs to quantify supplier-level emissions for purchased_goods.

---
*Generated on 2025-09-02 09:56:37*
