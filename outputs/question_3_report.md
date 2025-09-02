# Question 3 Report

## Question
How do my scope 1 & 2 emissions compare with other companies in my industry, and what insights can I derive from this comparison?

## Answer
Full analysis and answer

Executive summary
- Absolute totals (company, reporting period): Scope 1 = 1,253,420.76 tCO2e; Scope 2 = 70,340.12 tCO2e; Combined Scope 1+2 = 1,323,760.88 tCO2e.
- Relative shares: Scope 1 accounts for ~94.7% of the combined scope1+2 footprint; Scope 2 accounts for ~5.3%.
- Key insight: Your footprint is strongly dominated by scope 1 process and stationary combustion emissions (typical for cement/lime/heavy process industries). Purchased electricity (scope 2) is much smaller in absolute terms; the largest near-term reduction opportunities in absolute tCO2e lie in scope 1.

Quantitative comparison and calculations
- Totals used (from validated dataset):
  - Scope 1 total_tCO2e_sum = 1,253,420.76 tCO2e
  - Scope 2 total_tCO2e_sum = 70,340.12 tCO2e
  - Combined = 1,323,760.88 tCO2e
- Shares:
  - Scope1_share = 1,253,420.76 / 1,323,760.88 = 0.9469 → 94.7%
  - Scope2_share = 70,340.12 / 1,323,760.88 = 0.0531 → 5.3%
- Scope1 >> Scope2 ratio: ~17.8 : 1 (scope1 is ~17.8 times scope2 in absolute tCO2e)

Hotspots and facility-level context
- Top scope1 facilities (by total_tCO2e):
  1. F002 East Kiln — 17,400 tCO2e
  2. F045 South Plant — 14,200 tCO2e
  3. F078 Central Mill — 13,050 tCO2e
  4. F120 West Kiln — 12,100 tCO2e
  5. F008 Co-gen Unit — 11,020 tCO2e
- Combined top-5 scope1 = 67,770 tCO2e (~5.41% of total scope1), indicating many facilities contribute moderate amounts rather than a single very large emitter. This pattern suggests both: (a) process emissions (calcination/process) across many plants and (b) distributed stationary combustion sources.
- Top scope2 facilities are smaller in absolute emissions; even the largest scope2 facility contributes only a few thousand tCO2e.

How this compares with industry peers (evidence-based, using available documents)
- The peer benchmarking materials loaded (peer_benchmark_cement_uk.pdf and cement_sector_tool_guide.pdf) stress that meaningful peer comparisons in the cement sector should use production-normalised metrics (tCO2e per tonne of clinker or finished product) rather than raw totals (peer_benchmark_cement_uk.pdf — p.2; cement_sector_tool_guide.pdf — p.3). Quote: "Cement sector emissions intensity benchmarks: tCO2e per tonne of clinker/finished product. Use production-normalised metrics for comparisons and target-setting." (peer_benchmark_cement_uk.pdf — p.2).
- The GHG Protocol guidance similarly requires production & activity data and documentation for fair comparisons and verification (ghg_protocol_corporate_standard.pdf — pp.21–24): "... Energy consumption data (invoices, ... meter readings ...); Production data (tonnes of material produced ...); Emission factors ... Description of how GHG emissions data have been calculated ..." (ghg_protocol, pp.21–24).
- Practical consequence: Using only the available emissions totals (scope1 & scope2) you can qualitatively say: "Your footprint is process-dominated and therefore typical of cement/lime-type industries where calcination and fuel combustion drive most emissions." However, you cannot compute a rigorous intensity (tCO2e/tonne product) comparison to the sector benchmarks without production tonnage (clinker/finished product) and/or peer intensity numeric values. The peer documents loaded recommend normalisation but do not include numeric sector-average intensity figures in the indexed snippets.

Limitations and data-quality considerations that affect comparability
- Missing scope 3 data: scope3.csv is missing — you cannot compare full value-chain intensity nor benchmark total corporate footprint vs peers who report full value-chain footprints.
- Missing production data: needed to compute tCO2e/tonne (clinker/product) for direct peer benchmarking; production data was not present in scope1/scope2 CSVs.
- Data quality issues flagged in the ingestion: missing emission factors on some scope1 rows (e.g., row 912), component-sum mismatches (row 234), negative activity_quantity (row 678), scope2 method/factor inconsistencies (rows 45, 201). These must be resolved or documented before external comparison/verification to avoid misrepresentations.
- Data quality indices: scope1_index 72.4; scope2_index 68.1. Reasonable but require targeted fixes to reach higher verification-readiness.

Actionable insights and recommendations (prioritized)
1) Immediate fixes (high priority — within 1–2 weeks)
   - Correct the flagged integrity issues: scope1 rows 234 (component-sum mismatch), 678 (negative activity quantity), 912 (missing emission factor with positive activity). Scope2 rows 45 and 201 need method/factor reconciling and supplier confirmation. These are blocking or quality-lowering issues for external benchmarking/verification.
   - Collect and attach production tonnages (tonnes clinker / finished product) per facility and reporting period so you can compute tCO2e/tonne (both scope1-only and scope1+2) and directly compare with peer benchmarks.
   - Standardize scope2 accounting method (location vs market) and ensure grid vs market emission factors are populated consistently.

2) Short-term strategic steps (1–3 months)
   - Compute product-normalised intensities: tCO2e per tonne of clinker and per tonne finished product for each facility and company-wide (report both scope1-only and scope1+2). Then compare to the peer-benchmark document (peer_benchmark_cement_uk.pdf — p.2) to locate your relative position (above/below sector central tendency).
   - Focus reduction strategy where it matters most: because scope1 ≈95% of scope1+2, prioritize process emissions reduction and fuel switching. Typical levers in cement sector include: clinker substitution (use of SCMs), process efficiency, alternative fuels (biomass/waste-derived fuels where appropriate), electrification where feasible, and assessment for Carbon Capture and Storage (CCS).
   - For scope2, evaluate supplier-specific market-based instruments (PPAs, guarantees of origin) where available to credibly reduce market-based scope2. But note that scope2 reductions will yield much smaller absolute tCO2e reductions than equivalent % improvements in scope1 because of the size disparity.

3) Medium-term (3–12 months)
   - Implement the ingestion and governance rules recommended (schema enforcement, component-sum checks, DQ scoring, automated outlier alerts). These are essential for consistent year-on-year benchmarking and for external verification (see GHG Protocol guidance on verifier expectations — ghg_protocol pp.21–24).
   - Acquire/subscribe to the full peer-benchmark dataset or industry benchmarking service to obtain numeric intensity comparators (percentiles, median, top-quartile values). If peer_benchmark_cement_uk has a data appendix, ingest it.

4) Tactical reduction measures (aligned to hotspots)
   - Process emissions: consider clinker substitution (GS, SCMs), process optimization and waste heat recovery, and evaluate CCS feasibility at major kiln sites.
   - Stationary combustion: fuel switching from high-carbon fuels to lower-carbon options or electrification; implement efficiency projects for boilers/kilns.
   - Cogeneration: re-evaluate allocation methods and ensure correct allocation of emissions vs electricity exported (cement sector tool notes allocation options).
   - Purchased electricity: secure supplier-specific low-carbon electricity (market-based factors) or use PPAs/RECs and document supplier factor for verification.

Suggested metrics and visuals to produce once production data is available
- Primary graph: tCO2e/tonne clinker — company vs sector median and quartiles (bar + boxplot). This is the canonical cement sector comparator (peer_benchmark_cement_uk.pdf — p.2).
- Secondary graph: waterfall chart showing the absolute reduction potential from a set of interventions ranked by tCO2e reduction potential.
- Data-quality dashboard: per-facility DQ score, number of flagged integrity issues, and DQ trend vs previous year.

Citations (from loaded knowledge base)
- GHG Protocol — verification & data requirements: ghg_protocol_corporate_standard.pdf — pp.21–24: guidance on required supporting data (invoices, meters, production data, emission factors, measurement accuracy) and documentation needed for external verification.
- Cement sector guidance: cement_sector_tool_guide.pdf — p.3: WBCSD cement sector tool includes purchased electricity and provides co-generation allocation options; useful for sector-specific allocation rules.
- Peer benchmarking: peer_benchmark_cement_uk.pdf — p.2: recommends normalising emissions to tCO2e per tonne clinker/finished product for peer comparisons and target-setting.

Next steps for you (action plan)
1. Fix integrity issues (rows 234, 678, 912 in scope1; rows 45, 201 in scope2) and re-run the quality checks.
2. Provide production output data (tonnes clinker and/or finished product) per facility + reporting period and re-run intensity calculations (tCO2e/tonne) so you can benchmark numerically against peers.
3. Implement the data governance rules in ETL (component-sum checks, emission-factor presence enforcement, negative-value blocking), and produce a verification package per facility (invoices, meter records, emission factor sources) per GHG Protocol guidance.
4. With corrected data and intensity metrics, obtain the numeric peer benchmark dataset and quantify whether you are above/below median and by how much — then prioritize interventions at facilities with highest absolute and intensity-based opportunity.

Report appendices (available artifacts from this analysis)
- Cleaned previews generated: cleaned_scope1_preview.csv (1243 rows), cleaned_scope2_preview.csv (312 rows).
- Data quality report JSON: ./artifacts/data_quality_report.json — contains row-level DQ scoring and flagged issues referenced above.

Concluding summary
- Your company’s scope1 emissions overwhelmingly dominate the footprint (~95% of scope1+2) — consistent with cement/industrial process sectors where process emissions (calcination) and fuel combustion are the primary drivers.
- To benchmark effectively against peers you must normalise by production (tCO2e/tonne clinker or product) and fix the flagged data quality issues. The peer benchmark docs and the GHG Protocol provide explicit guidance on the necessary production and source documentation.
- Immediate focus should be on correcting data issues and collecting production data; strategic focus should be on process emissions reduction (clinker substitution, efficiency, alternative fuels, CCS) because this will deliver the largest absolute reductions.

Saved report
- The complete report was saved as outputs/question_3_report.md (question_number: 3).

If you want, I can:
- produce the actual cleaned CSV artifacts for download (cleaned_scope1_preview.csv, cleaned_scope2_preview.csv) and the full data_quality_report.json,
- run the intensity calculation (tCO2e/tonne) for you if you provide production tonnage per facility or a company-wide production total,
- or extract additional numeric benchmark percentiles if you can provide or grant access to the full peer benchmarking dataset.

---
*Generated on 2025-09-02 09:49:32*
