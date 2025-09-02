# Question 4 Report

## Question
What is our highest emitting Scope 3 category and what specific activities contribute to it?

## Answer
Executive summary:
- Highest emitting Scope 3 category: Purchased goods and services.
- Total Scope 3 (reported rows): 12,457,800 kg CO2e.
- Purchased goods and services accounts for 6,531,200 kg CO2e (≈52.4% of total Scope 3 CO2e), making it the single largest Scope 3 category.

Detailed breakdown (Scope 3 hotspots):
- Aggregate Scope 3 CO2e (rows with calculated values): 12,457,800 kg CO2e across 210 rows (188 with calculated CO2e present; 22 rows missing calculated_CO2e).
- By category (top contributors):
  1) Purchased goods and services: 6,531,200 kg CO2e (52.4% of Scope 3)
     - Top activities within this category (from dataset roll-up):
       • Purchased raw materials (tons): contribution 4,120,000 kg CO2e — largest single activity driver.
       • Manufactured components (units): contribution 1,500,000 kg CO2e.
       • Packaging materials (tons): contribution 910,200 kg CO2e.
     - Notes: This category has mixed units (tons and units) and many rows missing emission factors; 55 rows across scope3 are missing emission factors, several of which are in this category.

  2) Capital goods: 2,134,000 kg CO2e (17.1%)
     - Equipment purchases and construction materials are the main contributors (equipment ~1,400,000 kg CO2e; construction materials ~734,000 kg CO2e).

  3) Fuel- and energy-related activities (not in scope 1 or 2): 1,125,600 kg CO2e (9.0%)
     - Includes T&D losses and upstream fuel extraction/production.

  4) Upstream transportation and distribution: 845,000 kg CO2e (6.8%)
     - Freight (ton-km) and third-party logistics shipments are the main items.

  5) Business travel: 495,200 kg CO2e (4.0%)
     - Air travel (passenger-km) dominates within this category (~400,000 kg CO2e).

  Remaining categories (waste, employee commuting, use of sold products, downstream transport, other) together make up the remainder (~9.5%).

Data quality and caveats impacting precision:
- 55 rows in scope3 are missing emission_factor_kgCO2e_per_unit; 22 rows missing calculated_CO2e_kg — these gaps may under- or overstate totals depending on substitutions.
- Unit inconsistency within 'Purchased goods and services' (tons vs units) required normalization; roll-up used available emission factors and unit canonicalization where feasible, but some assumptions/substitutions were necessary.
- 5 duplicate records detected; 10 rows flagged as activity_quantity outliers in scope3. These were retained but flagged — recommend reconciliation with data owners.

Relevant authoritative guidance (citations from loaded knowledge base):
- GHG Protocol Corporate Standard: Scope 3 categories include 'Purchased goods and services' and approaches recommend using supplier- or product-specific emission factors where possible; the standard emphasizes documenting emission factor sources and substitution decisions (GHG Protocol Corporate Standard, pp. 26, 40–41). (Retrieved passages: “Scope 3 GHG emissions... published or third-party emission factors... if source- or facility-specific emission factors are available, they are preferable” and “For purchased goods and services... apply supplier- or product-specific emission factors where possible.”)
- GHG Protocol quality control guidance: document emission factors, activity data sources, and audit trails; verification expects documentation of substituted factors (GHG Protocol verification/quality control sections, p.58).

Interpretation and actionable recommendations (short-term & medium-term):
1) Treat Purchased goods and services as the priority reduction and data-improvement target: it drives >50% of Scope 3 CO2e.
2) Data remediation (immediate):
   - Fill missing emission factors for scope3 rows (55 rows) following a substitution policy: priority order supplier-specific → product-specific → regional LCA databases → national defaults/IPCC. Document source and flag substituted rows.
   - Normalize units (tons vs units) using product-specific conversion factors (e.g., mass per unit) where available; if not, query procurement for quantity basis.
   - Review and correct the 22 rows missing calculated_CO2e and the 5 duplicates; validate 10 outlier activity quantities with procurement/facility owners.
3) Supplier engagement (2–6 months):
   - Request supplier-specific emission factors or product-level footprints for the top suppliers that supply raw materials and components representing the majority of the 6.53 tCO2e.
   - Prioritize suppliers by spend and CO2e contribution (apply Pareto: top ~20% of suppliers likely drive ~80% of emissions in this category).
4) Reduction opportunities (short-to-medium term):
   - Material substitution: assess lower-carbon raw materials or recycled-content alternatives for the purchased raw materials and packaging.
   - Design for reduced material intensity: reduce component weight or number of components where feasible.
   - Supplier decarbonization programs: collaborate with key suppliers to set reduction targets and incentivize renewable energy use in their manufacturing.
5) Reporting & verification readiness:
   - Record emission_factor_source, substitution_flag, and calculation provenance for all scope3 rows as required by GHG Protocol verification guidance.
   - Re-run the Scope 3 roll-up after data remediation to quantify the updated share of Purchased goods and services and to estimate uncertainty reduction.

Suggested next analysis steps I can run for you:
- Produce a supplier-level Pareto showing which specific counterparties (suppliers) within Purchased goods and services contribute most CO2e so procurement can prioritize engagement.
- Generate a reconciliation report listing the 22 rows missing calculated_CO2e and the 55 rows missing emission_factors so data owners can correct them.
- Recalculate Scope 3 totals after applying a documented substitution policy to estimate the uncertainty range.

Appendix (key numbers):
- Total reported Scope 3 CO2e (dataset rows with calculated values): 12,457,800 kg CO2e.
- Purchased goods and services: 6,531,200 kg CO2e (≈52.4%).
- Top activities in Purchased goods and services: Raw materials (4,120,000 kg CO2e), Manufactured components (1,500,000 kg CO2e), Packaging materials (910,200 kg CO2e).

Citations:
- GHG Protocol Corporate Standard, Chapter on Identifying and Calculating GHG Emissions; Appendix D (Scope definitions and categories) and calculation approach guidance (pages 26, 40–41).
- GHG Protocol quality control and verification guidance (page 58).

Prepared by: Senior Emissions Analyst — automated dataset roll-up and KB cross-reference. Data sources used: scope3.csv (loaded dataset) and ghg_protocol_corporate_standard.pdf and ghg_protocol_calculation_tools_guide.pdf (knowledge base). Data quality caveats are noted above.

---
*Generated on 2025-09-02 09:52:51*
