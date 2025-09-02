# Question 6 Report

## Question
Generate a summary report of our total emissions by scope with key insights

## Answer
Summary report: Total emissions by scope (reporting period up to 2024-06-30)

Data sources used (loaded files): scope1.csv (124 rows), scope2.csv (86 rows), scope3.csv (210 rows). Totals below are sums of the emissions fields in those files and include uncorrected flagged records (see Data Quality section).

1) Totals (tonnes)
- Scope 1 (direct):
  - CO2: 12,580.47 t
  - CH4: 0.5132 t
  - N2O: 0.0215 t
  - Total CO2e (as reported in file): 12,612.12 t
  - Rows counted: 124

- Scope 2 (indirect - purchased electricity):
  - CO2: 3,420.90 t
  - CH4: 0.0324 t
  - N2O: 0.0041 t
  - Total CO2e (as reported in file): 3,428.12 t
  - Rows counted: 86

- Scope 3 (value chain):
  - CO2: 18,475.20 t
  - CH4: 1.0210 t
  - N2O: 0.0452 t
  - Total CO2e (as reported in file): 18,486.27 t
  - Rows counted: 210

- Grand total (all scopes, reported CO2e sum): 34,326.51 tCO2e

2) Percentage breakdown of reported CO2e
- Scope 1: 36.75% of total
- Scope 2: 9.99% of total
- Scope 3: 53.26% of total

3) Key insights and interpretation
- Scope 3 dominates the inventory (53%)—purchased goods and upstream categories are the largest contributor. This indicates high value-chain emissions and suggests the greatest reduction opportunity lies with procurement, supplier engagement, and product/material design.
- Scope 1 is material at ~37% driven by on-site combustion/process emissions (12,612 tCO2e). Immediate operational efficiency and fuel-switching opportunities (e.g., replacing diesel/heavy fuel with lower-carbon alternatives or electrification) could reduce this.
- Scope 2 is the smallest reported share (~10%), but ensure all facility meters have correct emission factors. Several scope 2 records have missing or anomalous emission_factors per the data quality assessment; addressing these could adjust scope 2 up or down slightly.

4) Data quality caveats (these affect totals and should be resolved before public reporting/verification)
- Overall data integrity score: 0.87/1.0. Totals include records flagged for review; resolving those may change totals.
- Notable flagged records included: scope1 row with negative activity_quantity (F009), scope1 extreme co2_emissions (F021), scope2 rows with zero or anomalous metered_kwh or emission_factor, and scope3 abnormal large purchase quantity and unit mismatches (tons vs tonnes).
- Emissions arithmetic validation rule is not enforced on all rows: some rows lack emission_factors or supporting calculation method documentation.

5) Compliance / verification references (GHG Protocol)
- Reporting by scope and each GHG: GHG Protocol Corporate Standard requires "Emissions data separately for each scope. Emissions data for all six GHGs separately (CO2, CH4, N2O, HFCs, PFCs, SF6) in metric tonnes and in tonnes of CO2 equivalent." (ghg_protocol_overview.pdf, p.34)
- Verification preparedness and quality control: "Preparing for a GHG verification... Description of quality control procedures applied (internal audits, comparison with last year’s data, recalculation by second person, etc.)." (ghg_protocol_overview.pdf, p.46)

6) Actions recommended (prioritized)
Priority 1 (Immediate, high confidence/impact)
- Correct flagged anomalies before external reporting: verify/correct scope1 negative and extreme values (rows F009, F021), scope2 zero-meter and high emission_factor records, and scope3 unit and outlier issues (tons->tonnes conversions, SupplierX very large quantity).
- Enforce positivity checks (activity_quantity > 0) and emission_factor presence or documented method for all records.
- Recalculate totals after corrections and re-run data quality checks.

Priority 2 (Near term)
- Standardize units (uom canonicalization) across datasets and implement automatic conversions (e.g., tons -> tonnes = *0.907185 where appropriate).
- For scope 2, obtain supplier-specific or grid-region emission factors where missing and standardize kWh unit formatting.
- Implement the emissions arithmetic validation rule: verify co2_emissions ≈ activity_quantity * emission_factor (±2%). Flag exceptions.

Priority 3 (Governance)
- Publish canonical data dictionary and require source_document_id for manual entries and procurement invoices.
- Implement outlier detection workflows and two-person verification for material records.
- Prepare verification pack: calculation worksheets, emission factor sources, and evidence for flagged records.

7) Simple visualization (text-based) — reported CO2e by scope
- Scope3: ##################### 53.3% (18,486 tCO2e)
- Scope1: ############# 36.8% (12,612 tCO2e)
- Scope2: ###### 10.0% (3,428 tCO2e)

8) Next steps to finalize accurate reporting
- Run corrective actions on flagged rows and re-run analyze_emissions to produce finalized totals.
- Conduct documentation sweep to attach source documents for manual entries and large purchases.
- Use GHG Protocol guidance (see citations above) to assemble reporting disclosures: organizational and operational boundaries, base year policy, methodological choices, and quality/uncertainty discussion.

Appendix: Calculations used
- Scope totals are sums of the file columns: total_co2e (per-row). Grand total = sum(scope1.total_co2e + scope2.total_co2e + scope3.total_co2e) = 12,612.12 + 3,428.12 + 18,486.27 = 34,326.51 tCO2e (as aggregated by the analysis tool). Note: small differences may exist due to row-level rounding.

Citations
- GHG Protocol Corporate Standard guidance: ghg_protocol_overview.pdf, p.34 and p.46.
- Sector calculation & quality checklist reference: sector_cement_tool.pdf (sector-specific emission factor and QC guidance).

Saved report
- The full report has been saved to outputs/question_6_report.md (includes the complete analysis above).

If you want, I can:
- Produce a CSV extract of the flagged rows for distribution to data owners (recommended immediate step).
- Re-run the summary after applying automated unit normalization and removing/flagging duplicates.

---
*Generated on 2025-09-02 10:00:56*
