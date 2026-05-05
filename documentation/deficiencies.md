# Dissertation Deficiencies

This file tracks places where prospectus-era language was rewritten into dissertation-final language, but the supporting material is not yet present in the manuscript. Each identifier corresponds to a placeholder of the form `<<< deficiency D00X >>>` in the LaTeX sources. When a deficiency is addressed, this file also records what was added so the manuscript and supporting artifacts stay synchronized.

From 2026-04-20 onward, this file also records open manuscript-review findings discovered during full-draft review, even when they are not tied to a placeholder token. Those entries are marked as open review findings and are intended to guide final dissertation cleanup.

## D001 - RQ1 stability and ablation package

- Status: Addressed on 2026-04-19.
- Added notebook: `notebooks/stability_ablation.ipynb`
- Added notebook regeneration helper: `scripts/_generate_stability_ablation_notebook.py`
- Added cached result files:
  - `notebooks/runs_new/stability_ablation/stability_ablation_runs.csv`
  - `notebooks/runs_new/stability_ablation/stability_ablation_summary_numeric.csv`
  - `notebooks/runs_new/stability_ablation/stability_ablation_summary_formatted.csv`
  - `notebooks/runs_new/stability_ablation/stability_ablation_deltas.csv`
  - `notebooks/runs_new/stability_ablation/stability_pairwise_jaccard.csv`
  - `notebooks/runs_new/stability_ablation/stability_pairwise_summary.csv`
  - `notebooks/runs_new/stability_ablation/lag_scaling_runs.csv`
  - `notebooks/runs_new/stability_ablation/selection_frequency_raw.csv`
  - `notebooks/runs_new/stability_ablation/selection_frequency_rectified.csv`
  - `notebooks/runs_new/stability_ablation/selection_frequency_rule.csv`
- Added generated figures to the manuscript `Figures/` directory:
  - `Figures/stability_ablation_summary.png`
  - `Figures/stability_pairwise_jaccard.png`
  - `Figures/stability_selection_frequency.png`
  - `Figures/lag_runtime_scaling.png`
- Updated manuscript discussion in `Chapters/05_rq1.tex`:
  - replaced both `<<< deficiency D001 >>>` placeholders,
  - added a repeated-resample stability and stage-wise ablation subsection,
  - added Table `tab:d001_stability`,
  - added Figures `fig:d001_ablation`, `fig:d001_pairwise_jaccard`, `fig:d001_selection_frequency`, and `fig:d001_runtime_scaling`,
  - added narrative interpreting the ablation deltas, support-stability results, lag-fidelity gains, and runtime-scaling behavior.
- Net effect on the dissertation: D001 is now backed by a concrete synthetic resampling package rather than a placeholder reference.

## D002 - RQ1 expanded baseline and cross-domain comparison package

- Status: Addressed on 2026-04-19.
- Added notebooks:
  - `notebooks/cross_domain.ipynb`
  - `notebooks/goose_bay_robustness.ipynb`
- Added notebook regeneration helpers:
  - `scripts/_generate_cross_domain_notebook.py`
  - `scripts/_generate_goose_bay_robustness_notebook.py`
- Added cached result files:
  - `notebooks/runs_new/cross_domain/synthetic_baseline_summary.csv`
  - `notebooks/runs_new/cross_domain/synthetic_baseline_summary_formatted.csv`
  - `notebooks/runs_new/cross_domain/cross_domain_transfer_summary.csv`
  - `notebooks/runs_new/cross_domain/cross_domain_transfer_summary_formatted.csv`
  - `notebooks/runs_new/cross_domain/ionosphere_protocol_comparison.csv`
  - `notebooks/runs_new/cross_domain/ionosphere_protocol_comparison_formatted.csv`
  - `notebooks/runs_new/cross_domain/cross_domain_takeaways.txt`
  - `notebooks/runs_new/goose_bay_robustness/goose_bay_protocol_summary.csv`
  - `notebooks/runs_new/goose_bay_robustness/goose_bay_protocol_summary_formatted.csv`
  - `notebooks/runs_new/goose_bay_robustness/goose_bay_quantile_sweep_summary.csv`
  - `notebooks/runs_new/goose_bay_robustness/goose_bay_quantile_sweep_summary_formatted.csv`
  - `notebooks/runs_new/goose_bay_robustness/goose_bay_c_sweep_summary.csv`
  - `notebooks/runs_new/goose_bay_robustness/goose_bay_c_sweep_cv_summary.csv`
  - `notebooks/runs_new/goose_bay_robustness/goose_bay_seed2345_decomposition.csv`
  - `notebooks/runs_new/goose_bay_robustness/goose_bay_seed2345_decomposition_formatted.csv`
  - `notebooks/runs_new/goose_bay_robustness/goose_bay_takeaways.txt`
- Moved notebook-generated figures into the manuscript `Figures/` directory:
  - `Figures/cross_domain_transfer_deltas.png`
  - `Figures/cross_domain_ionosphere_protocol_comparison.png`
  - `Figures/goose_bay_delta_j_protocols.png`
  - `Figures/goose_bay_quantile_sweep.png`
  - `Figures/goose_bay_c_sweep_scatter.png`
- Updated manuscript discussion in `Chapters/05_rq1.tex`:
  - replaced both `<<< deficiency D002 >>>` placeholders,
  - added Table `tab:d002_baselines` covering elastic net, adaptive lasso, group lasso, ordered-prefix, and QP-based comparators,
  - added Figures `fig:d002_transfer_deltas`, `fig:d002_ionosphere_protocols`, `fig:d002_goose_bay_protocols`, `fig:d002_goose_bay_quantiles`, and `fig:d002_goose_bay_c_sweep`,
  - added narrative on mixed cross-domain transferability under a standardized protocol,
  - added a protocol audit explaining why the Goose Bay generic probe differs from the published 2022 result,
  - added sensitivity discussion for split choice, rectifier quantiles, and penalty strength `C`, including the implication that the default `C=0.1` and default `25/75` cutlass quantiles understate Goose Bay performance.
- Main dissertation LaTeX edits taken:
  - `main.tex` required no direct change because `Chapters/05_rq1.tex` was already included in the build.
  - `Chapters/05_rq1.tex` now contains the full D002 backfill used by the main dissertation document.
- Net effect on the dissertation: D002 is now backed by a concrete expanded-baseline package, a broader cross-domain transfer panel, and an explicit explanation of why the Goose Bay ionosphere result changes under different protocol settings.

## D003 - RQ2 empirical boundary-condition package

- Status: Corrected on 2026-04-20. The boundary-condition notebook package was integrated into the main dissertation text, and the Chapter 06 D003 placeholders were replaced with a full empirical boundary-condition subsection.
- Added notebook: `notebooks/boundary_conditions.ipynb`
- Added notebook regeneration helper: `scripts/_generate_boundary_conditions_notebook.py`
- Added cached result files:
  - `notebooks/runs_new/boundary_conditions/ic_boundary_runs.csv`
  - `notebooks/runs_new/boundary_conditions/ic_boundary_summary.csv`
  - `notebooks/runs_new/boundary_conditions/ic_stress_runs.csv`
  - `notebooks/runs_new/boundary_conditions/ic_stress_summary.csv`
  - `notebooks/runs_new/boundary_conditions/ic_stress_crossing_summary.csv`
  - `notebooks/runs_new/boundary_conditions/inactive_count_runs.csv`
  - `notebooks/runs_new/boundary_conditions/inactive_count_summary.csv`
  - `notebooks/runs_new/boundary_conditions/threshold_bridge_sweep.csv`
  - `notebooks/runs_new/boundary_conditions/interval_bridge_summary.csv`
  - `notebooks/runs_new/boundary_conditions/negative_complement_summary.csv`
  - `notebooks/runs_new/boundary_conditions/boundary_conditions_summary.csv`
  - `notebooks/runs_new/boundary_conditions/boundary_takeaways.txt`
- Notebook-generated figures currently retained under `notebooks/Figures/`:
  - `notebooks/Figures/boundary_ic_stress_profiles.png`
- Boundary figures moved into the dissertation-wide `Figures/` directory for manuscript inclusion:
  - `Figures/boundary_ic_sweep.png`
  - `Figures/boundary_ic_stress_heatmaps.png`
  - `Figures/boundary_inactive_count_sweep.png`
  - `Figures/boundary_threshold_bridge.png`
- Notebook scope delivered:
  - positive and negative correlation sweeps using an empirical IC proxy,
  - a harder cross-scale stress sweep showing where raw and rectified `\Theta` cross the IC boundary,
  - a fixed-`s=4` inactive-count sweep showing how a larger off-support pool worsens the max-based IC proxy,
  - a threshold bridge from exact zero-threshold sign binarization to shifted one-sided and interval critical ranges,
  - a negative-correlation complement-feature check,
  - a final strong/weak/fail summary table suitable for Chapter 06 backfill.
- Main dissertation LaTeX edits taken:
  - `Chapters/06_rq2.tex` now includes the full D003 backfill: synthetic dataset construction, IC proxy definition, baseline IC sweep interpretation, harder cross-scale boundary maps, fixed-`s=4` inactive-count scaling, threshold-bridge analysis, complement-feature repair, and a manuscript summary table.
  - `Chapters/89_conclusion.tex` now summarizes the strong/weak/fail boundary interpretation in the RQ2 conclusion.
- Net effect on the dissertation: D003 is now backed by a concrete empirical boundary-condition package inside the main document, with figures and a summary table that identify where the theorem is strongest, where it weakens, and where complement features or out-of-scope language are required.

## D004 - RQ3 real-data compression validation package

- Status: Corrected on 2026-04-20. The real-data compression validation package was integrated into the main dissertation text, and the Chapter 07 D004 placeholders were replaced with a full real-data policy, frontier, and non-inferiority summary.
- Added notebook: `notebooks/compression_validation.ipynb`
- Added notebook regeneration helper: `scripts/_generate_compression_validation_notebook.py`
- Added cached result files:
  - `notebooks/runs_new/compression_validation/real_data_frontiers.csv`
  - `notebooks/runs_new/compression_validation/compression_policy_summary.csv`
  - `notebooks/runs_new/compression_validation/strict_policy_noninferiority_summary.csv`
  - `notebooks/runs_new/compression_validation/compression_validation_takeaways.txt`
  - `notebooks/runs_new/compression_validation/compression_validation_metadata.json`
- Compression figure moved into the dissertation-wide `Figures/` directory for manuscript inclusion:
  - `Figures/rq3_real_data_frontiers.png`
- Main dissertation LaTeX edits taken:
  - `Chapters/07_rq3.tex` now includes the prespecified strict deployment policy, Figure `fig:rq3_real_frontiers`, Table `tab:rq3_strict_policy`, a policy-sweep interpretation over `\epsilon \in \{0.01, 0.02, 0.05\}`, and a revised RQ3 answer tied to the held-out validation results.
  - `Chapters/89_conclusion.tex` now summarizes the strict real-data RQ3 outcome in the dissertation conclusion.
- Figure-location note:
  - No additional D004 manuscript figure remained under `notebooks/Figures/`; the notebook already generated the retained RQ3 frontier plot directly into `Figures/`.
- Net effect on the dissertation: D004 is now backed by a concrete real-data anytime-frontier package, an explicit non-inferiority table, and a deployment-policy summary inside the main document rather than a placeholder reference.

## D005 - Front matter and thesis framing overstate results relative to the chapter-level conclusions

- Status: Addressed on 2026-04-20.
- Severity: High.
- Evidence:
  - `main.tex:79`
  - `Chapters/01_introduction.tex:40`-`Chapters/01_introduction.tex:42`
  - `Chapters/05_rq1.tex:335`-`Chapters/05_rq1.tex:342`
  - `Chapters/07_rq3.tex:63`-`Chapters/07_rq3.tex:91`
  - `Chapters/07_rq3.tex:129`-`Chapters/07_rq3.tex:131`
  - `Chapters/89_conclusion.tex:20`-`Chapters/89_conclusion.tex:37`
- Issue:
  - The abstract and thesis statement read as though rectification and compression are broadly successful and operationally usable in general.
  - The body of the dissertation is materially more cautious: RQ1 is answered as "yes, conditionally," and the strict RQ3 deployment policy clears only two of five real-data studies.
  - As written, the manuscript's strongest caveats appear only after the reader has already been given a more universal top-level claim.
- Recommended correction:
  - Rewrite the abstract and thesis statement so they match the final body language: threshold-aligned regimes for RQ1 and policy-scoped, domain-dependent compression for RQ3.
  - Avoid phrases that imply universal superiority over raw sparse fitting unless they are explicitly qualified.
- Changes made:
  - Updated the abstract in `main.tex` to qualify the rectification claim as strongest in threshold-and-lag aligned settings and to describe compression as a policy-controlled path rather than a universal deployment success.
  - Updated the thesis statement in `Chapters/01_introduction.tex` so it now matches the chapter-level conclusions: conditional empirical benefit for rectification and explicit performance-tolerance policies for compression.

## D006 - RQ3 alternates between equivalence, non-inferiority, and "arbitrary policy" language

- Status: Addressed on 2026-04-20.
- Severity: High.
- Evidence:
  - `Chapters/01_introduction.tex:73`
  - `Chapters/07_rq3.tex:63`
  - `Chapters/07_rq3.tex:75`
  - `Chapters/07_rq3.tex:91`
  - `Chapters/07_rq3.tex:106`
  - `Chapters/89_conclusion.tex:37`
- Issue:
  - The introduction and conclusion describe the RQ3 framing as interval-based equivalence logic.
  - The implemented real-data rule is actually a one-sided non-inferiority screen using paired-bootstrap lower bounds on `\Delta AUC` and `\Delta J`.
  - The sentence in Chapter 07 stating that the acceptance rules are "purely arbitrary" directly undercuts the preceding claim that the policy is prespecified and methodologically disciplined.
- Recommended correction:
  - Standardize the terminology. If the implemented held-out rule is non-inferiority rather than equivalence, say so consistently.
  - Replace "purely arbitrary" with language such as "policy-dependent but prespecified" if that is the intended meaning.
- Changes made:
  - Updated `Chapters/07_rq3.tex` to replace the "purely arbitrary" wording with explicit language that the dissertation policy is conservative, prespecified, and application-dependent.
  - Added a sentence clarifying that near-miss cases may reasonably be acceptable under different operating priorities when compression gains are large and held-out shortfall is small.
  - Standardized the dissertation's framing in `Chapters/01_introduction.tex`, `Chapters/04_resquestions.tex`, `Chapters/07_rq3.tex`, and `Chapters/89_conclusion.tex` so the current held-out rule is described as non-inferiority-based rather than equivalence-based.

## D007 - The toy-example uniqueness claim is logically incorrect as written

- Status: Addressed on 2026-04-20.
- Severity: High.
- Evidence:
  - `Chapters/05_rq1.tex:62`-`Chapters/05_rq1.tex:70`
- Issue:
  - The chapter states that "the only possible logical AND combination" producing the shown response vector is the first and fourth columns.
  - That is not true as written. Any superset conjunction that contains columns `A` and `D` and only adds columns that remain `+1` on the event rows would produce the same response vector.
  - The current sentence therefore claims uniqueness without proof and is easy for a careful reader to refute from the displayed matrix itself.
- Recommended correction:
  - Change the claim to something defensible, such as "a minimal explanatory pair is columns 1 and 4," or provide an explicit uniqueness argument if that stronger statement is intended.
- Changes made:
  - Updated `Chapters/05_rq1.tex` so the toy-example claim now states the defensible result: any minimal exact conjunction must contain columns A and D.
  - Added a short justification in the text based on the first two non-event rows, which are excluded only by D and A respectively.

## D008 - Early RQ1 intuition overgeneralizes the correlation-reduction claim

- Status: Addressed on 2026-04-21.
- Severity: Medium.
- Evidence:
  - `Chapters/05_rq1.tex:20`
  - `Chapters/06_rq2.tex:176`-`Chapters/06_rq2.tex:185`
  - `Chapters/06_rq2.tex:262`-`Chapters/06_rq2.tex:279`
  - `Chapters/05_rq1.tex:286`-`Chapters/05_rq1.tex:331`
- Issue:
  - The early RQ1 text says that mapping to `\{\pm1\}` reduces correlation while preserving meaningful relationships.
  - Later chapters explicitly show that the theorem is scoped to the zero-threshold sign regime, that interval rules are weaker and prevalence-sensitive, and that negative-correlation cases may require complement features or out-of-scope language.
  - The toy-example prose therefore sounds more general than the dissertation's own later theory and audit sections allow.
- Recommended correction:
  - Narrow the early intuition language so it is clearly presented as a scoped sign-binarization intuition rather than a general property of all rectification rules.
- Changes made:
  - Updated the early toy-example intuition in `Chapters/05_rq1.tex` so the correlation-reduction statement is now explicitly scoped to the simplest sign-binarized setting.
  - Added a bridge sentence stating that Chapter 6 provides a tractable explanatory mechanism under explicit assumptions, not a universal constraint on every empirical claim in the dissertation.

## D009 - The manuscript scopes the method to threshold-mediated regimes but never gives a practical pre-use diagnostic

- Status: Addressed on 2026-04-21.
- Severity: Medium.
- Evidence:
  - `Chapters/05_rq1.tex:282`-`Chapters/05_rq1.tex:286`
  - `Chapters/05_rq1.tex:331`-`Chapters/05_rq1.tex:342`
  - `Chapters/89_conclusion.tex:58`-`Chapters/89_conclusion.tex:64`
  - Context note: `documentation/prospectus_audit.md:18`-`documentation/prospectus_audit.md:27`
- Issue:
  - The final draft is careful to say the method is strongest when the data are threshold-mediated or threshold-aligned.
  - However, the dissertation still does not tell the reader how to judge that alignment before committing to the pipeline.
  - This leaves the practical guidance incomplete, especially in light of the mixed UNICEF and generic Goose Bay results.
- Recommended correction:
  - Add a short diagnostic subsection or checklist explaining when rectification should be expected to help, when it should be treated as exploratory only, and when it should probably be avoided.
- Changes made:
  - Added a new subsection, `A practical diagnostic for when rectification is worth trying`, to `Chapters/05_rq1.tex` immediately before the RQ1 answer.
  - The new text gives an empirical screening heuristic for when rectification is a strong candidate, when it should be treated cautiously, and how to distinguish meaningful event-related thresholds from arbitrary numerical splits.

## D010 - RQ1 baseline coverage still lacks a direct interpretable-model comparator

- Status: Addressed on 2026-04-21.
- Severity: Medium.
- Evidence:
  - `Chapters/03_relatedwork.tex:47`-`Chapters/03_relatedwork.tex:55`
  - `Chapters/05_rq1.tex:211`-`Chapters/05_rq1.tex:234`
  - Context note: `documentation/prospectus_audit.md:36`
- Issue:
  - The dissertation's interpretability argument is not only "better sparse selection," but also "better operationally usable model forms."
  - The empirical comparator package focuses almost entirely on sparse-penalty variants and a QP selector.
  - Without at least one direct interpretable-model baseline (for example EBM, RuleFit, or a rule-list family), the comparative argument remains incomplete on the interpretability axis it emphasizes.
- Recommended correction:
  - Add a direct interpretable-model comparator, or explicitly justify why that family is out of scope for the dissertation's empirical claims.
- Changes made:
  - Added `scripts/_generate_interpretable_baselines_notebook.py`, which generates `notebooks/interpretable_baselines.ipynb`.
  - The new notebook benchmarks the synthetic Case 1 family across repeated seeds and compares:
    - the CUTLASS sparse rectified baseline,
    - the CUTLASS logic-polished rule candidate,
    - an Explainable Boosting Machine (EBM),
    - RuleFit, and
    - a greedy rule-list baseline.
  - The notebook writes run-level and summary artifacts to `notebooks/runs_new/interpretable_baselines/` and reports held-out fit metrics, execution time, and structural complexity proxies for each method.
  - The notebook also now writes exact-lag selection-frequency heatmaps and per-method lag-frequency CSVs so the direct baseline comparison includes a visual support-recovery view comparable to the stability-ablation notebook.
  - Extended the notebook to record both `selected_features` and `full_support_features`, and added a dual-view heatmap plus full-support CSV exports so the comparison now distinguishes top-`K` benchmark support from full active support.
  - Updated the notebook prose to clarify that top-`K` is a controlled comparison lens rather than a direct utility score, and that CUTLASS logic contributes a native rule size `k` whereas the other baselines do not.
  - Added a runtime-interpretation note to the notebook and manuscript explaining that these timings are end-to-end package timings, that the current CUTLASS prototype is Python/Numpy while EBM uses a compiled native backend, and that a compiled CUTLASS implementation would likely widen CUTLASS's speed advantage over EBM in this benchmark.
  - Integrated the corrected D010 results into the dissertation text in `Chapters/03_relatedwork.tex`, `Chapters/05_rq1.tex`, and `Chapters/89_conclusion.tex`.
  - Added a new RQ1 subsection, `Direct interpretable-model baseline package`, to `Chapters/05_rq1.tex`, including Table `tab:d010_interpretable` and Figures `fig:d010_summary`, `fig:d010_selection_frequency`, and `fig:d010_tradeoff`.
  - Replaced the original D010 lag-recovery figure in the manuscript with the dual-view support heatmap and updated the surrounding Chapter 05 discussion so the left/right pane interpretation is explicit.
  - Increased the dual-view figure label and legend text and adjusted the title spacing so the notebook and manuscript versions remain readable.
  - Copied the D010 benchmark figures into the dissertation `Figures/` directory so they are now part of the main manuscript build.

## D011 - The manuscript still has build-quality issues that affect reference integrity and clean compilation

- Status: Addressed on 2026-04-21.
- Severity: Medium.
- Evidence:
  - `Chapters/98_appendices.tex:35`
  - `Chapters/98_appendices.tex:44`
  - `Chapters/98_appendices.tex:55`
  - `Chapters/05_rq1.tex:25`-`Chapters/05_rq1.tex:27`
  - `Chapters/05_rq1.tex:45`-`Chapters/05_rq1.tex:47`
  - `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` on 2026-04-20 reported multiply defined labels and `\scriptsize` warnings.
- Issue:
  - Appendix B previously assigned the same label `fig:curve_generation_1` to three distinct figures, which broke figure-reference uniqueness.
  - The toy matrices in Chapter 05 previously placed `\scriptsize` inside display math, which produced LaTeX font warnings.
- Recommended correction:
  - Keep the appendix figure labels distinct and update any downstream references if needed.
  - Keep size changes outside the display-math environment or use a math-safe layout approach for the matrices.
- Changes made:
  - The Appendix B figure labels in `Chapters/98_appendices.tex` are now unique: `fig:curve_generation_1`, `fig:curve_generation_2`, and `fig:curve_generation_3`.
  - Updated the two Chapter 05 toy-matrix displays in `Chapters/05_rq1.tex` to remove in-math `\scriptsize` usage.
  - The matrices now use a scoped outer font-size block (`\begingroup` / `\footnotesize`) plus a reduced `\arraycolsep`, which is math-safe and local to those two displays.
  - A `pdflatex -interaction=nonstopmode -halt-on-error main.tex` run on 2026-04-21 no longer reports the `Command \scriptsize invalid in math mode` warnings.
  - A clean rebuild cycle with `latexmk -c main.tex` followed by `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` on 2026-04-21 no longer reports the generic `multiply-defined labels` summary in `main.log`.

## D012 - Several visible proofreading issues remain in the front matter, chapter captions, and appendix prose

- Status: Addressed on 2026-04-21.
- Severity: Low.
- Evidence:
  - `main.tex:85` (`guidiance`)
  - `Chapters/05_rq1.tex:83` (`Developement`)
  - `Chapters/05_rq1.tex:97` (`Developement`)
  - `Chapters/98_appendices.tex:532` (`monotinicity`)
  - `Chapters/98_appendices.tex:541` (`monotincity`)
  - `Chapters/07_rq3.tex:100` (`real world` in adjective position)
- Issue:
  - The draft still contains obvious proofreading misses in visible manuscript text.
  - These do not change the science, but they weaken polish in sections readers are likely to notice.
- Recommended correction:
  - Perform one targeted proofreading pass over front matter, figure captions, and appendix theorem prose before final submission.
- Changes made:
  - Corrected `guidiance` to `guidance` in `main.tex`.
  - Corrected both `Developement` caption instances to `Development` in `Chapters/05_rq1.tex`.
  - Corrected both appendix prose misspellings of `monotonicity` in `Chapters/98_appendices.tex`.
  - Corrected `real world` to `real-world` in the Chapter 07 RQ3 figure caption.
  - Ran a quick targeted typo sweep over `main.tex`, `Chapters/*.tex`, and `documentation/*.md`; the logged D012 strings no longer appear in manuscript source files.

## D013 - The synthetic anytime-compression figure caption is misleading about what happens after early stop

- Status: Addressed on 2026-04-21.
- Severity: Medium.
- Evidence:
  - `Chapters/07_rq3.tex:95`-`Chapters/07_rq3.tex:100`
- Issue:
  - The caption states that Youden's `J` falls to zero after `k=7` because the algorithm exits early once it reaches `J=1.0`.
  - If the later prefixes were not actually evaluated, then the post-`k=7` zeros are a plotting or padding artifact, not an observed performance collapse.
  - As written, the caption invites a false interpretation of the curve.
- Recommended correction:
  - Reword the caption so it explicitly says the curve is truncated or zero-padded after early stop, and that values beyond the stopping point should not be interpreted as measured performance.
- Changes made:
  - Updated the caption for `fig:rq3_results` in `Chapters/07_rq3.tex` to state that values beyond the early-stop point are zero-padded for plotting and are not measured post-stop performance.
  - The revised caption now preserves the intended comparison to Figure `fig:hai_Jvsk` without implying that the synthetic frontier was empirically observed to collapse after `k=7`.

## D014 - Contribution framing is inconsistent across chapters and still does not isolate the dissertation-only delta from the prior papers

- Status: Addressed on 2026-04-22.
- Severity: Medium.
- Evidence:
  - `Chapters/01_introduction.tex:44`-`Chapters/01_introduction.tex:52`
  - `Chapters/03_relatedwork.tex:67`-`Chapters/03_relatedwork.tex:75`
  - `Chapters/89_conclusion.tex:39`-`Chapters/89_conclusion.tex:48`
  - Context note: `documentation/report_card.md:45`-`documentation/report_card.md:50`
- Issue:
  - The introduction presents four integrated contributions, while the conclusion presents five primary contributions.
  - Both sections describe the dissertation at a high level, but neither gives a compact reader-facing account of what is new in the dissertation beyond `orender2022`, `JOrender2025Efficient`, and `JOrender2025Anytime`.
  - This weakens the novelty story and makes the manuscript's dissertation-level delta harder to defend quickly.
- Recommended correction:
  - Add one table that maps each prior paper to its scope and then lists the dissertation-only additions (for example, repeated-resample stability/ablation, cross-domain transfer plus Goose Bay audit, empirical boundary-condition package, direct interpretable-model baselines, and held-out policy-based compression validation).
  - Make the contribution count and wording match between the introduction and conclusion.
- Changes made:
  - Updated `Chapters/01_introduction.tex` so the contribution list now contains five items rather than four, aligned in structure and wording with the conclusion chapter.
  - Added Table `tab:dissertation_delta` to `Chapters/01_introduction.tex`, explicitly mapping `orender2022`, `JOrender2025Efficient`, and `JOrender2025Anytime` to their prior-paper scope and the dissertation-level additions beyond each.
  - Updated `Chapters/89_conclusion.tex` so the five-item contribution list now matches the introduction's framing: unified pipeline, scoped theory, anytime deployment compression, dissertation-level empirical validation package, and reproducible implementation pathway.
  - Added a cross-reference sentence in `Chapters/03_relatedwork.tex` directing readers to Table `tab:dissertation_delta` for the manuscript-vs-paper delta.

## D015 - The early RQ1 intuition material still reads like developmental exposition and contains remaining local writing/caption errors

- Status: Addressed on 2026-04-22.
- Severity: Medium.
- Evidence:
  - `Chapters/05_rq1.tex:82`-`Chapters/05_rq1.tex:86`
  - `Chapters/05_rq1.tex:95`-`Chapters/05_rq1.tex:100`
  - `Chapters/05_rq1.tex:318`
  - `Chapters/05_rq1.tex:333`
  - Context note: `documentation/report_card.md:38`-`documentation/report_card.md:43`
- Issue:
  - The prose shifts into first-person and tutorial language ("I show an easy way..."), which is stylistically inconsistent with the rest of the dissertation.
  - Several sentences are imprecise or awkward, such as the critical-range definition in the multi-trigger subsection.
  - The same local section still contains caption-level wording problems (`into to`, `the "anytime" nature of process`) and repetitive "Note that..." scaffolding, which makes Chapter 5 feel less polished than the surrounding chapters.
- Recommended correction:
  - Rewrite the early intuition subsections into concise dissertation voice, tighten the critical-range definition, and remove tutorial-style filler.
  - Do a localized proofreading pass over the Chapter 5 HAI figure captions after the prose rewrite.
- Changes made:
  - Renamed the early Chapter 5 framing from `A Simple Example to Aid Intuition Development` / `Intuition Development` to more concise section labels.
  - Rewrote the early intuition prose in `Chapters/05_rq1.tex` to remove first-person tutorial language and replace it with dissertation-style explanation of the target threshold-mediated regime.
  - Tightened the local definition of the critical range so it now reads as an event-associated interval that helps include event rows while excluding non-event rows.
  - Rewrote the multi-trigger transition so it explains more clearly why LASSO becomes useful once events depend on multiple simultaneous critical ranges.
  - Cleaned the Chapter 5 HAI captions, including the `into to` and `nature of process` wording problems, and made the ROC / `J` captions more direct and professional.

## D016 - The dissertation contains the pieces of an operational workflow, but not a single end-to-end procedure for applying the pipeline to a new dataset

- Status: Addressed on 2026-04-22.
- Severity: Medium.
- Evidence:
  - `Chapters/04_approach.tex:33`-`Chapters/04_approach.tex:51`
  - `Chapters/05_rq1.tex:389`-`Chapters/05_rq1.tex:401`
  - `Chapters/07_rq3.tex:49`-`Chapters/07_rq3.tex:63`
  - `Chapters/89_conclusion.tex:68`-`Chapters/89_conclusion.tex:70`
  - Context note: `documentation/report_card.md:59`-`documentation/report_card.md:64`
- Issue:
  - The approach chapter explains the pipeline, the RQ1 chapter gives a rectification diagnostic, and the RQ3 chapter gives a compression policy.
  - But the reader still has to assemble those pieces manually; there is no single ordered playbook saying when to try raw, rectified, or hybrid features, which defaults to use first, and when the correct outcome is "stop" or "fall back."
  - This leaves utility below what the current material should support.
- Recommended correction:
  - Add a boxed workflow summary or short appendix titled something like `Applying the pipeline to a new dataset`.
  - Include ordered steps, default knobs (`rectifier`, penalty strength, `\epsilon`, non-inferiority margins), and explicit fallback decisions.
- Changes made:
  - Added a new subsection, `Applying the pipeline to a new dataset`, to `Chapters/04_approach.tex`.
  - Added Figure `fig:new_dataset_workflow`, using `Figures/new_dataset_pipeline_workflow.pdf` as the build artifact generated from the editable SVG source.
  - Added explanatory prose immediately below the figure that makes the default starting choices explicit: train-only threshold estimation, semantically aligned one-sided or interval rules as the first rectifier choice, penalty selection by cross-validation or a stable near-plateau region, and the strict compression policy with $\epsilon=0.02$, $\Delta \mathrm{AUC}>-0.02$, and $\Delta J>-0.02$.
  - Added explicit fallback guidance covering when to keep the raw sparse baseline, when to use a hybrid representation, and when to stop at the rectified sparse model rather than compress further.

## D017 - Public reproducibility assets exist, but the manuscript does not surface them clearly enough

- Status: Addressed on 2026-04-22.
- Severity: Low.
- Evidence:
  - `main.tex:79`
  - `Chapters/01_introduction.tex:29`
  - `Chapters/89_conclusion.tex:41`-`Chapters/89_conclusion.tex:47`
  - `Chapters/88_futurework.tex:23`-`Chapters/88_futurework.tex:25`
  - `scripts/_generate_stability_ablation_notebook.py:817`-`scripts/_generate_stability_ablation_notebook.py:827`
  - `scripts/_generate_boundary_conditions_notebook.py:1342`-`scripts/_generate_boundary_conditions_notebook.py:1357`
  - User clarification on 2026-04-22: the `cutlass` Python package is already published on PyPI, and the notebooks in this repository reproduce the dissertation figures and data runs in publicly accessible code.
  - Context note: `documentation/report_card.md:52`-`documentation/report_card.md:57`
- Issue:
  - The dissertation's reproducibility claim is directionally correct: public code and notebook-based reproduction assets already exist.
  - The remaining problem is manuscript communication, not missing infrastructure. The main text does not clearly point readers to the package, the notebooks, or the regeneration path, while Future Work can still be read as though artifact packaging is mostly prospective.
  - This weakens the professional-relevance and reproducibility story because readers must infer the artifact boundary from the repository rather than from the dissertation itself.
- Recommended correction:
  - Add a short artifact or reproducibility subsection that explicitly points to the published `cutlass` package and the dissertation notebooks/scripts used to regenerate figures and runs.
  - Reword the Future Work packaging paragraph so it is clearly about expanding or polishing the existing public release rather than implying that reproducibility assets do not yet exist.
- Changes made:
  - Added a new subsection, `Public artifacts and regeneration path`, to `Chapters/04_approach.tex`.
  - The new subsection explicitly points readers to the public `cutlass` PyPI package, the public dissertation repository, the study notebooks under `notebooks/`, the paired notebook generators under `scripts/_generate_*.py`, the cached run summaries under `notebooks/runs_new/`, and the manuscript figures under `Figures/`.
  - Updated the reproducibility contribution wording in `Chapters/01_introduction.tex` and `Chapters/89_conclusion.tex` so the contribution is described as a public package plus notebook-backed study regeneration rather than as an abstract workflow claim.
  - Rewrote the `Tooling and Reproducibility` paragraph in `Chapters/88_futurework.tex` so it now treats artifact publication as already accomplished and frames future work as hardening and polishing the existing release.

## D018 - The Chapter 5 runtime claim for the quadratic-programming comparator now contradicts the consolidated benchmark table

- Status: Addressed on 2026-04-22.
- Severity: High.
- Evidence:
  - `Chapters/05_rq1.tex:217`
  - `Chapters/05_rq1.tex:223`-`Chapters/05_rq1.tex:242`
- Issue:
  - The standalone comparator paragraph still says the quadratic-programming method shows runtime differences on the order of `100--200x` relative to rectification plus lasso.
  - The later consolidated benchmark table in the same chapter reports `QP + L1` runtime `2.843` seconds versus `Rectified L1` runtime `2.947` seconds on the synthetic Case 1 study, which does not support a `100--200x` gap.
  - As written, a reader can reasonably conclude that the chapter is mixing two incompatible benchmark configurations or that an older claim was left in place after the expanded baseline package changed.
- Recommended correction:
  - Remove or rewrite the stale `100--200x` statement unless it is explicitly tied to a different earlier experiment.
  - If two distinct benchmark settings are intended, name them directly and explain why the runtime figures differ.
  - Align the local narrative with the actual values shown in the current manuscript tables.
- Changes made:
  - Updated the standalone Katrutsa--Strijov comparator paragraph in `Chapters/05_rq1.tex` so it now states explicitly that the `100--200x` runtime observation came from earlier comparisons using the original R reference implementation.
  - Updated the consolidated benchmark introduction in `Chapters/05_rq1.tex` so it now explains that the later Case 1 table uses a Python reimplementation of the same selector to place the methods on a more level software footing.
  - The chapter now distinguishes implementation-environment effects from the substantive empirical conclusion: the normalized runtime gap is much smaller in the consolidated benchmark, but the lag-localization weakness of the quadratic-programming route remains.

## D019 - The abstract and conclusion still smooth over the strict real-data RQ3 outcome

- Status: Addressed on 2026-04-22.
- Severity: Medium.
- Evidence:
  - `main.tex:79`
  - `Chapters/07_rq3.tex:91`
  - `Chapters/07_rq3.tex:131`
  - `Chapters/89_conclusion.tex:33`-`Chapters/89_conclusion.tex:37`
- Issue:
  - Chapter 7 now states the real-data result clearly: under the strict held-out policy, only two of five studies support deployed compressed rules, while two are near-miss cases and one does not justify simplification at all.
  - The abstract still ends with a broad path from the sparse baseline to `compact operational rules`, and the conclusion still says sparse rectified models can `often` be compressed while preserving practical quality.
  - This does not fully match the dissertation's strongest final claim, which is that the anytime frontier supplies an auditable accept/reject policy for compression rather than broad deployment success across all real-data cases.
- Recommended correction:
  - Rewrite the abstract and RQ3 conclusion summary so they foreground the policy-controlled frontier and the conservative real-data result.
  - State explicitly that, under the strict held-out rule used in the dissertation, only HAI `a1` and `a2` support deployed compressed rules.
  - Emphasize that the main contribution is the auditable decision rule for when to compress and when not to compress.
- Changes made:
  - Updated the abstract in `main.tex` so it now distinguishes the controlled threshold-mediated result from the mixed real-world result: compression works cleanly in explicit threshold-based settings, while the real-data contribution is the policy-controlled frontier for accepting or rejecting simplification.
  - Updated the real-data interpretation and the `Answer to RQ3` section in `Chapters/07_rq3.tex` so the chapter now states the two-part conclusion directly: clean compression in the planted threshold-and-lag regime, and explicit decision criteria for mixed real-world regimes with additive structure and measurement uncertainty.
  - Updated the RQ3 conclusion in `Chapters/89_conclusion.tex` so it now emphasizes that the most important real-data contribution is the acceptance policy rather than a blanket claim of broad compression success.

## D020 - Skimming readers still cannot see the dissertation-only delta from the abstract and conclusion alone

- Status: Addressed on 2026-04-22.
- Severity: Medium.
- Evidence:
  - `main.tex:79`
  - `Chapters/01_introduction.tex:55`-`Chapters/01_introduction.tex:79`
  - `Chapters/89_conclusion.tex:39`-`Chapters/89_conclusion.tex:54`
  - Context note: `documentation/report_card.md:54`-`documentation/report_card.md:59`
- Issue:
  - D014 fixed the chapter-level contribution framing and added the dissertation-delta table in Chapter 1.
  - However, the abstract and conclusion still read mostly as a high-level pipeline summary, so a reader who only scans the front matter and closing chapter still has to infer what is new beyond `orender2022`, `JOrender2025Efficient`, and `JOrender2025Anytime`.
  - This keeps the novelty story weaker than it should be for committee members or other readers who do not study Chapter 1 in detail.
- Recommended correction:
  - Add one sentence to the abstract and one sentence to the conclusion that name the dissertation-only additions directly.
  - At minimum, mention the repeated-resample stability/ablation package, the direct interpretable-model baselines, the cross-domain plus Goose Bay audit, the empirical boundary-condition package, and the strict held-out compression validation.
  - Make the abstract/conclusion novelty language clearly derivative of the Chapter 1 delta table rather than requiring the reader to discover it later.
- Changes made:
  - Updated the abstract in `main.tex` so it now names the dissertation-only additions directly: repeated-resample stability and ablation, direct interpretable baselines, cross-domain plus Goose Bay audit, empirical boundary checks, and strict held-out compression validation.
  - Updated the conclusion in `Chapters/89_conclusion.tex` to add a sentence immediately after the contribution list that surfaces the same dissertation-level delta for skimming readers.
  - Kept the abstract within the dissertation's 350-word limit by replacing a generic contribution sentence with a more specific delta sentence instead of appending a longer paragraph.

## D021 - The workflow guidance is now present, but the defaults and fallback logic are still buried in prose

- Status: Addressed on 2026-04-22.
- Severity: Medium.
- Evidence:
  - `Chapters/04_approach.tex:53`-`Chapters/04_approach.tex:66`
  - `Chapters/05_rq1.tex:389`-`Chapters/05_rq1.tex:401`
  - `Chapters/07_rq3.tex:63`-`Chapters/07_rq3.tex:91`
  - Context note: `documentation/report_card.md:68`-`documentation/report_card.md:73`
- Issue:
  - The manuscript now contains the right workflow ingredients: a playbook figure, a rectification diagnostic, and a strict compression policy.
  - But the reader still has to extract the operational defaults and branch logic from several prose blocks rather than consulting one quick-reference checklist.
  - This is now a utility problem rather than a missing-content problem: the guidance exists, but it is not yet compressed into the form a practitioner would use.
- Recommended correction:
  - Add a one-page checklist or decision table with explicit branches for `stay raw`, `rectify`, `use hybrid features`, and `stop before compression`.
  - Add a compact defaults table for rectifier choice, penalty selection, compression tolerance `\epsilon`, and held-out non-inferiority margins.
  - Add a short troubleshooting note for weak threshold structure, unstable threshold sensitivity, and near-miss compression candidates.
- Changes made:
  - Added an inline quick-reference checklist to `Chapters/04_approach.tex`, giving explicit branches for `stay raw`, `rectify`, `use hybrid features`, `stop before compression`, and `compress` without forcing the reader to reconstruct the decision path from prose.
  - Added Table `tab:workflow_defaults` to `Chapters/04_approach.tex`, listing conservative defaults for rectifier choice, threshold estimation, penalty selection, raw-versus-rectified comparison, compression tolerance, and held-out non-inferiority margins.
  - Added a short troubleshooting list to `Chapters/04_approach.tex` covering weak threshold structure, unstable threshold sensitivity, and near-miss compression candidates.

## D022 - The CS engineering story remains scattered instead of being summarized in one compact view

- Status: Addressed on 2026-04-22.
- Severity: Medium.
- Evidence:
  - `Chapters/01_introduction.tex:94`-`Chapters/01_introduction.tex:100`
  - `Chapters/04_approach.tex:15`
  - `Chapters/04_approach.tex:68`-`Chapters/04_approach.tex:81`
  - `Chapters/05_rq1.tex:202`
  - `Chapters/05_rq1.tex:286`
  - `Chapters/07_rq3.tex:63`-`Chapters/07_rq3.tex:91`
  - `Chapters/89_conclusion.tex:68`-`Chapters/89_conclusion.tex:70`
  - Context note: `documentation/report_card.md:61`-`documentation/report_card.md:66`
- Issue:
  - The manuscript already contains most of the ingredients needed for a strong CS-facing relevance argument: solver reuse, runtime measurements, prototype-versus-compiled discussion, reproducibility artifacts, and deployment logic.
  - Those points are currently dispersed across chapters, so the engineering contribution remains more implicit than explicit.
  - The dissertation also names application domains but still does not identify its intended technical readership in one place (for example, ML engineers working with sensor streams, ICS analysts, or clinical-informatics researchers).
- Recommended correction:
  - Add one compact summary table covering pipeline stage, computational role, solver or artifact reuse, runtime or complexity note, and intended technical user.
  - Use that summary to make the CS contribution legible as representation engineering plus solver reuse plus auditable deployment logic, not only as a domain-method narrative.
  - Name the target CS-facing users explicitly in the summary or conclusion.
- Changes made:
  - Added Table `tab:engineering_summary` to `Chapters/04_approach.tex`, summarizing the pipeline as representation engineering plus solver reuse plus auditable deployment logic.
  - The new table explicitly covers pipeline stage, computational role, solver or artifact reuse, runtime or complexity notes, and intended technical users.
  - Updated the practical-implications section in `Chapters/89_conclusion.tex` to name the target CS-facing readership directly: ML engineers working on sensor streams, ICS security analysts, and clinical-informatics researchers.

## D023 - The densest empirical sections still ask the reader to assemble the takeaway manually

- Status: Addressed on 2026-04-22.
- Severity: Medium.
- Evidence:
  - `Chapters/05_rq1.tex:340`-`Chapters/05_rq1.tex:387`
  - `Chapters/07_rq3.tex:61`-`Chapters/07_rq3.tex:93`
  - Context note: `documentation/report_card.md:47`-`documentation/report_card.md:50`
- Issue:
  - The cross-domain Goose Bay audit and the real-data RQ3 frontier discussion are scientifically stronger than earlier drafts, but both are text-heavy and require the reader to synthesize the operative takeaway from several paragraphs of detail.
  - This is now more of a flow problem than a content problem: the evidence is present, but the chapter does not always surface the one-sentence decision output quickly.
  - The resulting density still holds back the clarity score even though the underlying analysis is much improved.
- Recommended correction:
  - Add short boxed summaries or mini-tables at the end of the major result blocks.
  - For RQ1, state the exact practical takeaway from the Goose Bay audit in one place.
  - For RQ3, add a compact accept/reject summary immediately after the frontier discussion so the strict policy outcome can be read at a glance.
- Changes made:
  - Added a short framing sentence and a plain-prose practical-takeaway paragraph to the Goose Bay audit in `Chapters/05_rq1.tex`, so the section now states directly that Goose Bay is a protocol-sensitivity case rather than a contradiction of the earlier positive result.
  - Added a compact decision-summary paragraph to the real-data RQ3 discussion in `Chapters/07_rq3.tex`, stating the strict-policy accept/reject outcome explicitly for `a1`, `a2`, `a3`, `a4`, and the ionosphere probe.
  - Implemented D023 as low-friction scholarly exposition rather than as visual callout boxes, so the manuscript stays dissertation-like while reducing synthesis load on the reader.

## D024 - A few residual copyediting and caption-level inconsistencies remain in Chapters 5 and 6

- Status: Addressed on 2026-04-22.
- Severity: Low.
- Evidence:
  - `Chapters/05_rq1.tex:47`
  - `Chapters/05_rq1.tex:70`
  - `Chapters/05_rq1.tex:318`
  - `Chapters/06_rq2.tex:50`
- Issue:
  - Some local prose is still more informal than the surrounding dissertation voice, for example `Details regarding how to come up with this critical range` and `Here is the boolean response vector`.
  - Chapter 6 still contains the grammatical error `a threshold-based phenomena`, which should be singular.
  - The HAI caption language is also still potentially confusing: it says there is only limited spillover into `P1` and then immediately explains why `P4` also responds, which blurs the intended subsystem interpretation.
- Recommended correction:
  - Do one more localized copyediting pass over the Chapter 5 toy-example prose and nearby captions.
  - Correct the singular/plural grammar in the Chapter 6 assumptions list.
  - Tighten the HAI caption so the residual spillover language matches the explanatory paragraph's subsystem interpretation.
- Changes made:
  - Revised the Chapter 5 toy-example prose in `Chapters/05_rq1.tex` to replace informal phrasing with dissertation-style descriptions of the $\{1,-1\}$ encoding and the corresponding Boolean response vector.
  - Corrected the Chapter 6 assumptions-list grammar in `Chapters/06_rq2.tex` from `threshold-based phenomena` to `threshold-based phenomenon`.
  - Tightened the HAI caption in `Chapters/05_rq1.tex` so it now describes limited spillover outside the attacked subsystem and a smaller coherent `P4` response, matching the accompanying subsystem interpretation.

## D025 - Residual overfull and underfull box warnings indicate that the final typography pass is still outstanding

- Status: Addressed on 2026-04-22.
- Severity: Low.
- Evidence:
  - `main.log:959`
  - `main.log:964`
  - `main.log:969`
  - `main.log:974`
  - `main.log:979`
  - `main.tex:106`
  - `odusci.sty:317`
  - Context note: `documentation/report_card.md:49`-`documentation/report_card.md:52`
- Issue:
  - The dissertation initially built cleanly but still emitted a mix of overfull and underfull box warnings from long headings, dense prose, and wide summary tables.
  - Those warnings were mainly finish-quality issues rather than correctness problems, but they still reduced the perceived polish of the near-final manuscript.
  - After a targeted polish pass, the remaining warnings are five identical underfull boxes at `main.tex:106`, which are generated by the template's preface transition around `\afterpreface` rather than by dissertation chapter text.
- Recommended correction:
  - Run one targeted LaTeX polish pass focused on the specific long-line locations reported in `main.log`.
  - Prefer local rewording, line breaking, or table/caption adjustments over global looseness settings.
  - Rebuild after each pass until the remaining warnings are either removed or justified as unavoidable.
- Changes made:
  - Reflowed the dissertation title in `main.tex` and added `tabularx` support so wide summary material could be tightened without global spacing changes.
  - Shortened dense prose in `Chapters/01_introduction.tex`, `Chapters/02_background.tex`, `Chapters/03_relatedwork.tex`, and `Chapters/05_rq1.tex` to remove the manuscript-generated overfull boxes.
  - Converted the Chapter 4 defaults and engineering-summary tables in `Chapters/04_approach.tex` to `tabularx` layouts with ragged-right columns, which eliminated the table-driven overflow warnings.
  - Rebuilt with `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` after each pass and confirmed that the manuscript-generated overfull warnings are gone.
  - Left the five residual underfull warnings in place because they originate from the ODU template's preface machinery around `\afterpreface`; they are now documented as template-level residuals rather than open dissertation copy/layout defects.

## D026 - The front of the manuscript still buries the CS-facing audience and engineering story behind a broad domain survey

- Status: Addressed on 2026-04-22.
- Severity: Medium.
- Evidence:
  - `Chapters/01_introduction.tex:4`-`Chapters/01_introduction.tex:13`
  - `Chapters/01_introduction.tex:29`
  - `Chapters/04_approach.tex:119`-`Chapters/04_approach.tex:133`
  - `Chapters/89_conclusion.tex:72`
  - Context note: `documentation/report_card_clean.md:79`-`documentation/report_card_clean.md:82`
- Issue:
  - The dissertation's strongest computer-science framing now exists, but it appears late: the explicit engineering pattern and named technical readers show up in Chapter 4 and the conclusion rather than near the front of the manuscript.
  - The introduction instead opens with a broad threshold-and-lag domain list spanning ecosystems, epidemics, control systems, and financial markets.
  - As a result, the front of the dissertation reads more domain-general than the actual manuscript contribution warrants, which weakens immediate CS relevance for skimming readers and committee members.
- Recommended correction:
  - Tighten or replace the broad opening domain list with one paragraph that explicitly names the primary CS-facing users and target settings early.
  - Move the emphasis toward sensor streams, ICS monitoring, clinical longitudinal modeling, representation engineering, solver reuse, and auditable deployment logic.
  - Preserve broader domain examples only as secondary motivation after the technical framing is established.
- Changes made:
  - Replaced the broad opening domain list in `Chapters/01_introduction.tex` with an explicit CS-facing framing paragraph naming the primary technical readers early: ML engineers working with sensor streams, ICS security analysts, and clinical-informatics researchers.
  - Added opening language that foregrounds the dissertation's technical problem as threshold-mediated longitudinal decision support under multicollinearity, emphasizing representation redesign, solver reuse, and auditable deployment logic.
  - Compressed the broader ecosystem / epidemic / control-system / financial examples into one secondary motivation sentence so they remain visible without displacing the front-of-manuscript CS framing.

## D027 - Terminology still drifts between rectification, binarization, and sign-binarization without one canonical bridge sentence

- Status: Addressed on 2026-04-22.
- Severity: Medium.
- Evidence:
  - `main.tex:80`
  - `Chapters/04_approach.tex:35`-`Chapters/04_approach.tex:39`
  - `Chapters/04_approach.tex:142`-`Chapters/04_approach.tex:159`
  - `Chapters/05_rq1.tex:11`
  - `Chapters/05_rq1.tex:20`
  - `Chapters/05_rq1.tex:47`
  - `Chapters/06_rq2.tex:5`
  - `Chapters/06_rq2.tex:37`-`Chapters/06_rq2.tex:42`
  - `Chapters/06_rq2.tex:57`-`Chapters/06_rq2.tex:63`
  - Context note: `documentation/report_card_clean.md:66`-`documentation/report_card_clean.md:68`
- Issue:
  - The manuscript uses `critical-range rectification`, `binarization`, `sign binarization`, and `rectified design` across different chapters, but it still does not give the reader one canonical sentence saying how these terms relate.
  - The intended distinction is recoverable from context: rectification is the general pipeline operation, while zero-threshold sign binarization is the tractable theoretical special case.
  - Even so, the lack of one explicit early bridge forces the reader to reconstruct that relationship repeatedly and makes the theory-to-practice scope boundary harder to track than necessary.
- Recommended correction:
  - Add one explicit terminology note near the start of Chapter 1 or Chapter 4 stating that `rectification` is the dissertation's general pipeline term and that `sign binarization` is the special-case form used for tractable RQ2 analysis.
  - After that note, use `rectification` for the general method family and reserve `sign binarization` for theorem-scoped discussion.
- Changes made:
  - Added an explicit terminology note near the start of `Chapters/01_introduction.tex` stating that `rectification` is the dissertation's general pipeline term and that zero-threshold sign binarization is the theorem-scoped special case used in RQ2.
  - Updated `Chapters/04_approach.tex` so the general pipeline exposition now uses `rectification` in the toy-intuition and Stage 1 wording, while explicitly stating that the tractable analyzed case is the sign-binarized special case.
  - Updated the visible Chapter 5 toy-example wording in `Chapters/05_rq1.tex` so the general empirical method is described as `rectification`, while keeping `sign-binarized` language only where the scoped theoretical intuition is intended.
  - Updated `Chapters/06_rq2.tex` so the theory chapter now identifies sign binarization as the special-case theoretical form of the broader rectification operation and uses `sign-binarized` wording consistently in the theorem setup.

## D028 - Chapter 5 still delays the main empirical case with an overlong toy-example opening

- Status: Addressed on 2026-04-22.
- Severity: Medium.
- Evidence:
  - `Chapters/05_rq1.tex:9`-`Chapters/05_rq1.tex:107`
  - `Chapters/05_rq1.tex:109`
  - Context note: `documentation/report_card_clean.md:66`-`documentation/report_card_clean.md:69`
  - User clarification on 2026-04-22: adviser guidance is that the toy example should remain in the main chapter rather than being moved back to the appendix.
- Issue:
  - The chapter now reads more professionally than earlier drafts, but the opening still requires the reader to pass through a coefficient figure, two full matrices, a Boolean response vector, and two intuition figures before reaching the formal evaluation framework.
  - This front-loaded exposition delays the main empirical argument and remains one of the clearest reasons the clarity score is not yet a clean `10/10`.
  - The issue is now structural rather than grammatical: the material is not wrong, but the chapter does not currently orient the reader early enough to why this example is worth the initial space cost.
- Recommended correction:
  - Keep the toy example in the main chapter, but add a short opening preview paragraph before it that tells the reader what the synthetic evidence later shows and why the toy example matters as a local intuition bridge.
  - Add one explicit transition sentence at the end of the toy-example block that points forward to the formal `RQ1 Evaluation Framework` and the repeated-resample synthetic evidence.
  - If needed, tighten the explanatory prose around the toy example so the framing remains useful without forcing the reader to infer its relevance on first pass.
- Changes made:
  - Added a short preview paragraph near the start of `Chapters/05_rq1.tex` explaining that the chapter's main empirical case comes later through repeated-resample synthetic studies, expanded baselines, and real-world audits, and that the toy example is included as a local intuition bridge for those results.
  - Added a forward transition sentence immediately after the toy-example intuition block in `Chapters/05_rq1.tex`, explicitly directing the reader from the illustrative example to the formal `RQ1 Evaluation Framework` and planted-ground-truth synthetic evidence.
  - Preserved the toy example in the main chapter, consistent with adviser guidance, while reducing the risk that readers see it as an unmotivated detour.

## D029 - Chapter 5's synthetic benchmark tables use different reporting protocols without warning, creating avoidable apparent inconsistencies

- Status: Addressed on 2026-04-22.
- Severity: Medium.
- Evidence:
  - `Chapters/05_rq1.tex:155`-`Chapters/05_rq1.tex:164`
  - `Chapters/05_rq1.tex:221`-`Chapters/05_rq1.tex:242`
  - `Chapters/05_rq1.tex:248`-`Chapters/05_rq1.tex:260`
  - `Chapters/05_rq1.tex:286`
- Issue:
  - Chapter 5 presents several synthetic `Case 1` summaries close together, but they are not all aggregated in the same way.
  - The repeated-resample tables report mean $\pm$ standard deviation across three runs, while the expanded correlated-feature table reports one consolidated benchmark row without the same aggregation cue.
  - Because the manuscript does not warn the reader about this protocol shift, nearby values can look contradictory rather than merely differently summarized. For example, rectified support size is `190.0 \pm 117.8` in the repeated-resample view but `344` in the consolidated baseline table, and the reported runtimes change similarly.
- Recommended correction:
  - Add one sentence before Table `tab:d002_baselines` stating explicitly that this table is a different benchmarking protocol and should not be numerically compared row-for-row with the repeated-resample summaries.
  - If possible, add a short parenthetical in the caption clarifying whether the table is a single-run normalized benchmark, a fixed-split benchmark, or another distinct summary protocol.
- Changes made:
  - Added an explicit protocol-transition sentence in `Chapters/05_rq1.tex` immediately before Table `tab:d002_baselines`, stating that the expanded baseline table is a separate normalized single-run benchmark on a fixed `70/30` split with `rseed=1234` and should not be compared row-for-row with the repeated-resample mean `\pm` standard deviation summaries in Table `tab:d001_stability`.
  - Updated the caption of Table `tab:d002_baselines` in `Chapters/05_rq1.tex` to identify it as a normalized single-run benchmark on a fixed `70/30` split (`rseed=1234`), so the reporting protocol is visible even when the table is read in isolation.

## D030 - Chapter 7's formal method description still under-specifies the dissertation's actual two-stage deployment rule

- Status: Addressed on 2026-04-22.
- Severity: High.
- Evidence:
  - `Chapters/07_rq3.tex:25`-`Chapters/07_rq3.tex:31`
  - `Chapters/07_rq3.tex:49`-`Chapters/07_rq3.tex:55`
  - `Chapters/07_rq3.tex:63`-`Chapters/07_rq3.tex:64`
  - `Chapters/07_rq3.tex:72`-`Chapters/07_rq3.tex:95`
  - `Chapters/04_approach.tex:64`
- Issue:
  - The early RQ3 formalism presents a generic anytime objective and a generic $J$-based tolerance rule.
  - The implemented dissertation policy is stronger and more specific: it is a two-stage rule with training-side prefix screening by $J$ followed by held-out paired-bootstrap non-inferiority gates on both AUC and $J$.
  - Because the generic formulation appears first, a careful reader can still momentarily confuse candidate-prefix selection with final deployment adoption, especially in cases like `a3` and `a4`, where a strict `$k$` is reported but deployment is still rejected.
- Recommended correction:
  - Rewrite the `Anytime Compression Objective` / `Adoption Rule` presentation so it explicitly distinguishes the generic anytime framework from the dissertation's implemented strict policy.
  - Add one compact numbered rule list or pseudocode block showing: `(1) choose training-side smallest passing prefix, (2) test held-out paired-bootstrap gates on AUC and J, (3) deploy only if both gates pass; otherwise retain the upstream sparse baseline`.
  - Make the status of `Strict k` explicit as a candidate prefix rather than an automatically deployed artifact.
- Changes made:
  - Rewrote the early RQ3 formalism in `Chapters/07_rq3.tex` so the generic anytime frontier is now described explicitly as a candidate-generation procedure, while the dissertation's actual deployment rule is described separately as the stricter real-data policy.
  - Replaced the generic `Adoption Rule with Relative Tolerance` subsection in `Chapters/07_rq3.tex` with a compact numbered three-step policy list: training-side candidate-prefix nomination, held-out paired-bootstrap non-inferiority screening on AUC and `J`, and final deploy-versus-retain decision.
  - Updated the `Why the Method Is "Anytime"` and `Empirical Results` exposition in `Chapters/07_rq3.tex` so intermediate rules are described as candidate models on the frontier rather than automatically deployable artifacts under the dissertation's strict policy.
  - Revised the real-data frontier caption, result narration, and Table `tab:rq3_strict_policy` in `Chapters/07_rq3.tex` so `Strict k` is now presented as `Candidate k^\star`, making it explicit that cases such as `a3` and `a4` can have nominated compression candidates while still being rejected for deployment.

## D031 - The conclusion still does not compress the dissertation's novelty into one CS-facing sentence

- Status: Addressed on 2026-04-22.
- Severity: Medium.
- Evidence:
  - `Chapters/89_conclusion.tex:39`-`Chapters/89_conclusion.tex:56`
  - `Chapters/89_conclusion.tex:72`-`Chapters/89_conclusion.tex:76`
  - Context note: `documentation/report_card_clean.md:74`-`documentation/report_card_clean.md:76`
- Issue:
  - The conclusion now lists the contributions and the dissertation-only delta clearly, but it still leaves the reader to infer the most compact CS-shaped novelty statement.
  - What the manuscript contributes most distinctly is not just additional evaluation packages; it is the combination of representation engineering, reuse of mature sparse solvers, and auditable compression policy in one pipeline.
  - Without one sentence stating that combination explicitly, the novelty remains slightly more inferential than necessary for skimming readers.
- Recommended correction:
  - Add one compact sentence to the conclusion or final statement that names the dissertation's distinct CS contribution directly: representation-first feature redesign, solver reuse, and policy-controlled interpretable compression.
  - Use that sentence as the bridge between the contribution list and the final claim of defensible scope.
- Changes made:
  - Added one compact synthesis sentence to `Chapters/89_conclusion.tex` immediately after the dissertation-level delta paragraph, explicitly naming the dissertation's distinct CS contribution as the combination of representation-first feature redesign, reuse of mature sparse solvers, and policy-controlled interpretable compression.
  - Positioned that sentence as a bridge from the enumerated contribution list into the manuscript's broader positioning and final defensible-scope claim, so the novelty can be read directly rather than inferred.

## D032 - The front of the manuscript still lacks a one-page executive map for skimming readers

- Status: Addressed on 2026-04-22.
- Severity: Medium.
- Evidence:
  - `Chapters/01_introduction.tex:28`-`Chapters/01_introduction.tex:103`
  - `Chapters/04_approach.tex:163`-`Chapters/04_approach.tex:170`
  - Context note: `documentation/report_card_02.md:56`-`documentation/report_card_02.md:60`
- Issue:
  - The introduction now contains the needed pieces: problem statement, contribution list, dissertation delta, research questions, evaluation priorities, and thesis organization.
  - The approach chapter later adds the pipeline-to-RQ mapping, but that synthesis arrives after the reader has already passed through multiple framing sections.
  - As a result, the front of the dissertation still does not offer one compact, skimmable view of the problem, the pipeline, the target/non-target regime, and the one-sentence answer to each research question.
- Recommended correction:
  - Add a one-page executive map near the end of Chapter 1.
  - The map should contain: the target problem, the three pipeline stages, the target regime, the main boundary cases, and one short answer line for `RQ1`, `RQ2`, and `RQ3`.
  - Use it as the canonical front-of-manuscript summary so later chapters can point back to it rather than re-synthesizing the same overview in prose.
- Changes made:
  - Added a new `Executive Map` section to `Chapters/01_introduction.tex`.
  - Added Table `tab:executive_map`, which now gives a compact front-of-manuscript summary of the target problem, the three-stage pipeline, the target regime, the main boundary cases, and one-sentence answers to `RQ1`, `RQ2`, and `RQ3`.
  - Added a short cross-reference sentence to `Chapters/04_approach.tex` so the pipeline-to-RQ discussion explicitly points back to the Chapter 1 executive map as the skimmable canonical summary.
  - Verified the manuscript still builds with `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` on 2026-04-22.

## D033 - Chapters 2 and 3 still overlap enough to slow the front of the dissertation

- Status: Addressed on 2026-04-22.
- Severity: Medium.
- Evidence:
  - `Chapters/02_background.tex:9`-`Chapters/02_background.tex:43`
  - `Chapters/03_relatedwork.tex:7`-`Chapters/03_relatedwork.tex:57`
  - `Chapters/01_introduction.tex:100`-`Chapters/01_introduction.tex:103`
- Issue:
  - The `Background` and `Related Work` chapters both explain L1 foundations, IC-related dependence issues, structured sparsity, interpretability, and competing families.
  - The distinction between the chapters is defensible in principle, but in practice the early manuscript still repeats method-family exposition before moving the argument forward.
  - This front-loaded duplication weakens flow and makes the dissertation feel longer than it is, especially for committee readers who skim the framing chapters before the core RQ chapters.
- Recommended correction:
  - Sharpen the division of labor between the two chapters.
  - Keep `Background` focused on concepts, assumptions, and theory lenses needed to read the dissertation, and move literature taxonomy / method-family comparison weight into `Related Work`.
  - Remove or compress repeated explanatory paragraphs so the manuscript reaches the dissertation's own approach sooner.
- Changes made:
  - Updated the `Thesis Organization` paragraph in `Chapters/01_introduction.tex` so the chapter roles are now stated explicitly: `Background` supplies the conceptual ingredients, while `Related Work` handles literature comparison and positioning.
  - Rewrote the opening framing in `Chapters/02_background.tex` so the chapter is now explicitly concept-first rather than a partial duplicate of the literature review.
  - Trimmed comparative method-family exposition from `Chapters/02_background.tex`, especially by replacing the old `Competing approaches` section with a short `Background Summary` that bridges into Chapter 3 instead of re-listing the major baseline families.
  - Updated the opening paragraph of `Chapters/03_relatedwork.tex` so it now explicitly contrasts its role with Chapter 2: literature comparison and positioning rather than conceptual background.
  - Verified the manuscript still builds with `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` on 2026-04-22.

## D034 - Related-work positioning is still prose-only and leaves the novelty comparison too inferential

- Status: Addressed on 2026-04-22.
- Severity: Medium.
- Evidence:
  - `Chapters/03_relatedwork.tex:67`-`Chapters/03_relatedwork.tex:89`
  - `Chapters/89_conclusion.tex:54`-`Chapters/89_conclusion.tex:58`
  - Context note: `documentation/report_card_02.md:63`-`documentation/report_card_02.md:68`
- Issue:
  - The dissertation now states its positioning clearly in prose, especially around integration and intervention point.
  - However, the reader still has to assemble the method-family comparison mentally across narrative paragraphs.
  - Table `tab:dissertation_delta` in Chapter 1 clarifies what is new relative to the prior papers, but it does not show how the dissertation differs from lasso-family penalties, direct interpretable additive models, and direct rule learners on intervention point, output form, and deployment logic.
- Recommended correction:
  - Add one compact comparison table in Chapter 3 or Chapter 9.
  - The columns should distinguish at least: method family, intervention point, representation change or not, output form, deployment-policy support, and the dissertation's intended advantage.
  - Use the table to make the novelty claim legible in one glance rather than only through accumulated prose.
- Changes made:
  - Added Table `tab:method_family_positioning` to `Chapters/03_relatedwork.tex`.
  - The new table compares the dissertation pipeline against the main competing families on method family, intervention point, representation change, typical output form, deployment-policy support, and the dissertation's intended advantage.
  - Added a lead-in sentence in `Chapters/03_relatedwork.tex` explaining that the table is the at-a-glance cross-family positioning view for the chapter.
  - Added a short cross-reference sentence in `Chapters/89_conclusion.tex` so the conclusion now points readers back to the Chapter 3 positioning table instead of leaving the comparison purely prose-based.
  - Verified the manuscript still builds with `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` on 2026-04-22.

## D035 - The workflow chapter is strong in abstract form, but it still lacks one worked end-to-end application example

- Status: Closed in manuscript on 2026-04-23.
- Severity: Medium.
- Evidence:
  - `Chapters/04_approach.tex:53`-`Chapters/04_approach.tex:101`
  - `Chapters/05_rq1.tex:397`-`Chapters/05_rq1.tex:409`
  - `Chapters/07_rq3.tex:94`-`Chapters/07_rq3.tex:98`
  - Context note: `documentation/report_card_02.md:77`-`documentation/report_card_02.md:81`
- Issue:
  - The dissertation now provides an operational workflow, a quick-reference checklist, conservative defaults, and troubleshooting rules.
  - Even so, the reader never sees one concrete walk-through that applies those rules from start to finish on a single dataset.
  - This leaves the practical branch logic slightly more inferential than necessary: the reader understands the generic playbook, but must still mentally compose what `raw baseline -> diagnostic -> rectify or stay raw -> compress or stop` looks like in practice.
- Recommended correction:
  - Add one compact worked example, ideally one to two pages, showing how the workflow would be applied to one existing dataset already discussed in the dissertation.
  - The example should state the raw baseline behavior, the threshold-alignment diagnostic, the chosen branch (`stay raw`, `rectify`, `use hybrid features`, or `compress`), and the final deployment artifact.
  - A worked HAI or Goose Bay walk-through would be sufficient; the goal is not new science, but operational clarity.
- Changes made:
  - Added generator `scripts/_generate_walkthrough_notebook.py`.
  - Generated supporting notebook `notebooks/walkthrough.ipynb`.
  - The notebook works the HAI `attack_p2 (a1)` case from raw sparse baseline through rectified pilot, branch selection, strict-policy anytime compression, and final deployment recommendation.
  - Added subsection `Worked HAI exemplar for the workflow` and Table `tab:workflow_hai_exemplar` to `Chapters/04_approach.tex`.
  - The manuscript now summarizes the HAI `attack_p2 (a1)` path with concrete raw-baseline, rectified-pilot, branch, compression, and final-artifact outcomes drawn from the walkthrough notebook.
  - Added `walkthrough.ipynb` to the Chapter 4 public-artifact list and stated explicitly that the notebook accompanies the manuscript artifacts and uses the custom-built `cutlass` Python package.
  - This closes the manuscript-facing portion of D035 because the workflow chapter now includes an explicit end-to-end exemplar and points readers to the executable notebook.

## D036 - The reproducibility section still lacks a direct study-regeneration map from artifact to manuscript output

- Status: Closed in manuscript on 2026-04-23.
- Severity: Medium.
- Evidence:
  - `Chapters/04_approach.tex:104`-`Chapters/04_approach.tex:117`
  - `Chapters/89_conclusion.tex:46`-`Chapters/89_conclusion.tex:47`
  - Context note: `documentation/report_card_02.md:77`-`documentation/report_card_02.md:82`
- Issue:
  - The dissertation now surfaces the public package, the dissertation repository, the notebook bundles, the generator scripts, and the cached outputs.
  - What is still missing is a direct map from each study package to the manuscript artifacts it supports.
  - A reader can see that the assets exist, but still must infer which notebook or generator corresponds to which figures, tables, or chapters. That weakens the practical auditability of the reproducibility story.
- Recommended correction:
  - Add a compact reproducibility map, either in Chapter 4 or in a short appendix.
  - For each study package, list: notebook, generator script, cached output directory, principal manuscript figures/tables, and the chapter(s) that consume the results.
  - If possible, include one minimal rerun command pattern so technically capable readers can move from manuscript claim to regeneration entry point quickly.
- Changes made:
  - Added appendix chapter `Reproducibility Map` to `Chapters/98_appendices.tex`.
  - Added Table `tab:repro_map_rq1`, mapping the Chapter 4--5 study packages to their notebooks, paired generators, cached run directories, manuscript figures/tables, and consuming chapters.
  - Added Table `tab:repro_map_rq23`, mapping the Chapter 6--7 study packages to the same regeneration details.
  - Added a generic rerun command pattern in the appendix and a preprocessing note for the HAI-backed notebooks via `notebooks/build_hai_cutlass_data.py`.
  - Added a short cross-reference sentence in `Chapters/04_approach.tex` so the public-artifacts subsection now points readers directly to Appendix `\ref{app:reproducibility_map}` for the study-regeneration map.
  - This closes the manuscript-facing portion of D036 because the dissertation now maps each notebook-backed study package to its generator, cached outputs, manuscript artifacts, and consuming chapter.

## D037 - The appendix proof conclusion overstates what the RQ2 theory establishes

- Status: Closed in manuscript on 2026-04-24.
- Severity: High.
- Evidence:
  - `Chapters/98_appendices.tex:590`
  - `Chapters/06_rq2.tex:178`
  - `Chapters/06_rq2.tex:279`-`Chapters/06_rq2.tex:286`
- Issue:
  - The main RQ2 chapter now frames the theorem carefully as a scoped positive-correlation result with boundary checks for weaker regimes.
  - The appendix conclusion still says binarization "enhances positive correlation relationships" and will also deemphasize negative correlation relationships in "the vast majority of the time."
  - That language is stronger and less precise than the main chapter's caveated result, and it risks making the proof sound like a broader monotonic guarantee than the dissertation actually defends.
- Recommended correction:
  - Rewrite the appendix conclusion so it matches the main text: positive-correlation PoC regime only, with negative-correlation behavior treated as a boundary-condition stress case.
  - Replace "enhances positive correlation relationships" with a matrix-norm or IC-oriented statement that directly follows from the derived inequality.
  - Describe complement features as an engineering mitigation explored empirically, not as a theorem-level fix for all negative-correlation cases.
- Expected report-card impact:
  - Improves clarity and novelty rigor by making the theoretical claim harder to misread or overchallenge.
- Changes made:
  - Rewrote the appendix proof conclusion in `Chapters/98_appendices.tex` so the result is stated as the IC-oriented matrix-norm inequality `\|\tilde{G}^{-1}\|_\infty \leq \|G^{-1}\|_\infty` in the positive-correlation PoC regime.
  - Replaced the overbroad "enhances positive correlation relationships" and "vast majority of the time" language with the weak RQ2 probability claim under zero-threshold, jointly normal, positive-correlation assumptions.
  - Reframed negative-correlation behavior as a boundary-condition stress case and complement features as an empirical engineering mitigation, not a theorem-level fix.

## D038 - The synthetic-data appendix still contains old-draft prose and encoding artifacts

- Status: Closed in manuscript on 2026-04-24.
- Severity: Medium.
- Evidence:
  - `Chapters/98_appendices.tex:9`
  - `Chapters/98_appendices.tex:14`
  - `Chapters/98_appendices.tex:24`
  - `Chapters/98_appendices.tex:29`
  - `Chapters/98_appendices.tex:38`
  - `Chapters/98_appendices.tex:58`
- Issue:
  - The synthetic-data appendix reads less polished than the main dissertation, with informal phrases such as "Something like the following curve is generated" and "Note that."
  - It also contains malformed quote encoding around words such as `relevant` and `True`, plus local usage issues such as `discernable`.
  - Because Appendix C now carries an important reproducibility role, this older prose lowers the perceived finish quality of the artifact-backed story.
- Recommended correction:
  - Rewrite the synthetic-data appendix as a concise formal method description with `enumerate` steps and consistent terminology.
  - Remove informal filler, correct encoding artifacts, and standardize wording around data sets, relevant features, labels, and lag flattening.
  - Keep the figures, but make each step state the generated object, why it is generated, and how it supports the threshold-and-lag experiments.
- Expected report-card impact:
  - Improves clarity and professional polish, especially for readers who inspect the appendices to verify reproducibility.
- Changes made:
  - Rewrote the synthetic-data appendix opening in `Chapters/98_appendices.tex` as a concise `enumerate` procedure.
  - Removed informal phrasing such as "Something like..." and "Note that," corrected `discernable`, and replaced malformed quote/label wording with ASCII-safe terminology.
  - Standardized the description around bounded sensor-like channels, relevant features, binary `True`/`False` labels, lag-shifted event generation, lag flattening, row randomization, and the 70/30 train/test split while preserving the existing figure labels and replacing old step-number captions with descriptive captions.

## D039 - The manuscript lacks one compact metric and notation quick reference for the RQ chapters

- Status: Closed in manuscript on 2026-04-24.
- Severity: Medium.
- Evidence:
  - `Chapters/01_introduction.tex:89`-`Chapters/01_introduction.tex:97`
  - `Chapters/05_rq1.tex:122`
  - `Chapters/05_rq1.tex:160`-`Chapters/05_rq1.tex:165`
  - `Chapters/07_rq3.tex:29`
  - `Chapters/07_rq3.tex:53`-`Chapters/07_rq3.tex:55`
- Issue:
  - The dissertation defines its evaluation terms locally, but the definitions are scattered across the introduction, RQ1, and RQ3.
  - Dense empirical sections use AUC, Youden's J, exact-lag F1, pairwise Jaccard, nonzero support size, `k^\star`, `m`, and held-out deployment gates without one nearby reference table.
  - Readers can reconstruct the terms, but the extra lookup burden is exactly the kind of density that kept the reconciled clarity score below a perfect score.
- Recommended correction:
  - Add a compact "Metric and notation guide" near the end of Chapter 1 or at the start of Chapter 5.
  - Include AUC, Youden's J, exact-lag F1, pairwise Jaccard, total nonzero, active support, `k^\star`, `m`, compression ratio, `Deploy?`, and the paired-bootstrap non-inferiority lower-bound checks.
  - Keep it brief and point readers back to the detailed chapter-specific definitions where needed.
- Expected report-card impact:
  - Improves clarity by reducing reader load across the empirical and deployment chapters.
- Changes made:
  - Added a near-end Chapter 5 section, `Metric and Notation Guide`, with Table `tab:metric_notation_guide`.
  - Included compact definitions and dissertation roles for AUC, Youden's `J`, exact-lag F1, pairwise Jaccard, total nonzero, active support, `k^\star`, `m`, compression ratio, `Deploy?`, and paired-bootstrap non-inferiority lower-bound checks.
  - Positioned the guide immediately before `Answer to RQ1` so readers encounter the shared empirical vocabulary before moving into the RQ2 and RQ3 chapters.

## D040 - The repository README still presents the project as a template before it presents the dissertation artifact

- Status: Closed in repository documentation on 2026-04-24.
- Severity: Medium.
- Evidence:
  - `README.md:1`
  - `README.md:6`-`README.md:12`
  - `README.md:115`-`README.md:138`
  - `README.md:154`
- Issue:
  - The new reproduction quickstart is useful, but the README title remains `ODU College of Sciences LaTeX ETD Template`.
  - A reader landing on the repository can still mistake the project for a generic LaTeX template rather than the dissertation manuscript, notebooks, cached outputs, and reproduction instructions.
  - The retained template instructions also include template-specific links and one visible encoding artifact in the document-class line.
- Recommended correction:
  - Retitle the README around the dissertation and reproduction artifact.
  - Move retained ODU template material under a clearly marked "ODU Template Notes" or "LaTeX Template Reference" section.
  - Fix the remaining README encoding artifact and remove or qualify template-only guidance that is no longer accurate for this repository.
- Expected report-card impact:
  - Improves external clarity and utility by making the repository's purpose immediately legible.
- Changes made:
  - Completely rewrote `README.md` around the dissertation repository rather than the inherited LaTeX starter material.
  - Added dissertation-specific sections for repository structure, environment setup, data inputs, PDF building, representative workflow execution, study-package regeneration, runtime expectations, and manuscript-to-artifact audit flow.
  - Removed the generic ODU template instructions, Overleaf links, front-matter instructions, and template-specific examples from the body of the README.
  - Confined credit for the `ODU College of Sciences LaTeX ETD Template` to the final paragraph, as requested.

## D041 - The data manifest still leaves HAI acquisition under-specified for external readers

- Status: Closed in repository documentation on 2026-04-24.
- Severity: Medium.
- Evidence:
  - `README.md:65`-`README.md:89`
  - `references/shin2020.md:21`-`references/shin2020.md:33`
- Issue:
  - The README now names the HAI 1.0 dataset and the required local filenames, but it does not provide a direct source URL, version note, expected archive or CSV names, or integrity checks.
  - The Ionosphere row is more actionable because it includes the UCI download URL, while the HAI row still requires the reader to locate the public source independently.
  - That gap is small for an insider but material for an external CS reader trying to reproduce the real-data notebooks with minimal friction.
- Recommended correction:
  - Add the verified HAI 1.0 source page or download URL, the expected raw files, and any version/date information available from the Shin et al. dataset release.
  - Add optional file sizes or checksums for `train1.csv`, `train2.csv`, `test1.csv`, and `test2.csv` after verifying the public artifacts.
  - State whether processed parquet outputs are generated deterministically from those raw CSVs and where they will be written.
- Expected report-card impact:
  - Improves utility by closing the largest remaining real-data setup gap in the README.
- Changes made:
  - Added the HAI upstream repository, `https://github.com/icsdataset/hai`, to the README data manifest and to `references/shin2020.md`.
  - Added the HAI 20.07 / HAI1.0 version note from the upstream repository, including the relationship to the original February 2020 HAI v1.0 release.
  - Listed the expected raw local files (`train1.csv`, `train2.csv`, `test1.csv`, and `test2.csv`) and recorded local byte sizes plus SHA-256 checksums in `references/shin2020.md`.
  - Stated that `notebooks/build_hai_cutlass_data.py` writes deterministic derived outputs under `notebooks/processed_data/`, including `hai_manifest.json` and balanced parquet files consumed by the HAI-backed notebooks.

## D042 - Environment capture and smoke verification are not yet turnkey enough for a fresh external setup

- Status: Closed in repository documentation on 2026-04-24.
- Severity: Medium.
- Evidence:
  - `README.md:42`-`README.md:63`
  - `requirements.txt:1`
  - `scripts/_generate_walkthrough_notebook.py:52`
  - No `environment.yml`, `environment.yaml`, or smoke-test script was found by `rg --files`.
- Issue:
  - The `requirements.txt` file is useful, but the authoritative working setup is a conda environment named `cutlass`.
  - A pip-only requirements file may not recreate the notebook kernel consistently across machines, especially for packages with compiled dependencies.
  - There is also no fast smoke command that checks the environment, raw data paths, kernel registration, and a minimal study artifact before a reader launches long-running notebooks.
- Recommended correction:
  - Add a conda-native `environment.yml` generated from the working `cutlass` environment or a carefully curated equivalent.
  - Add a short smoke script such as `scripts/smoke_reproduction.py` that verifies core imports, package versions, `cutlass` kernel availability, required raw data files when real-data notebooks are requested, and presence/readability of cached outputs under `notebooks/runs_new/`.
  - Document a one-command or two-command readiness check in the README before the full notebook regeneration commands.
- Expected report-card impact:
  - Improves utility and professional relevance by making the artifact path more robust for outside CS readers.
- Changes made:
  - Added `environment.yml` as the preferred conda setup path for the `cutlass` notebook environment, using conda for the compiled scientific stack and pip for dissertation-specific packages.
  - Added `scripts/smoke_reproduction.py`, which checks core imports, package versions against `requirements.txt`, the registered `cutlass` Jupyter kernel, representative cached outputs under `notebooks/runs_new/`, and optional real-data plus processed HAI artifacts.
  - Updated `README.md` to document `conda env create -f environment.yml`, kernel registration, the default cached-artifact smoke command, and the `--with-real-data` readiness check for full real-data regeneration.

## D043 - The current LaTeX log shows a manuscript overfull-box regression after the prior typography item was closed

- Status: Closed in manuscript on 2026-04-24.
- Severity: Low.
- Evidence:
  - `main.log:959`
  - `main.log:964`
  - `main.log:969`
  - `main.log:974`
  - `main.log:979`
  - `main.log:1189`
  - `Chapters/05_rq1.tex:290`-`Chapters/05_rq1.tex:291`
- Issue:
  - D025 documented that the remaining warnings were template-level underfull boxes only.
  - The current log again reports an overfull box in manuscript chapter text, apparently in the dense direct-interpretable-baseline discussion around Chapter 5 lines 290--291.
  - This is not a substantive correctness problem, but it is a final-polish regression that contradicts the earlier closure note.
- Recommended correction:
  - Reflow or locally shorten the Chapter 5 paragraph around the reported line pair, then rebuild.
  - Confirm that the only remaining warnings are the documented template-level underfull boxes, or update D025/D043 with the exact remaining source.
- Expected report-card impact:
  - Improves professional polish and prevents a reviewer from interpreting the build log as unfinished cleanup.
- Changes made:
  - Shortened and split the dense direct-interpretable-baseline paragraph in `Chapters/05_rq1.tex`, replacing the long opening reference chain with a shorter sentence and moving the runtime/backend caveat into its own paragraph.
  - Rebuilt with `pdflatex -synctex=1 -interaction=nonstopmode -halt-on-error main.tex`.
  - Confirmed that the Chapter 5 overfull-box warning is gone. The remaining box warnings are the five already documented template-level underfull boxes at `main.tex:106`; the log also retains the existing biblatex fallback warning and PDF-version inclusion warnings for `Figures/first_irrelevant.pdf` and `Figures/both_relevant.pdf`, which are not overfull-box regressions.

## D044 - The project lacks a rule-card template for deployed compressed rules

- Status: Closed in manuscript and repository documentation on 2026-04-24.
- Severity: Medium.
- Evidence:
  - `documentation/report_card_03.md:78`
  - `Chapters/04_approach.tex:108`-`Chapters/04_approach.tex:124`
  - `Chapters/07_rq3.tex:53`-`Chapters/07_rq3.tex:55`
  - `notebooks/runs_new/walkthrough/hai_a1_walkthrough_selected_rule.csv`
  - `notebooks/runs_new/walkthrough/hai_a1_walkthrough_deployment_summary.csv`
- Issue:
  - The manuscript now explains when a compressed rule is deployment-eligible, and the walkthrough writes selected-rule and deployment-summary artifacts.
  - What is still missing is a standardized rule-card template that tells a practitioner exactly what to record when a compressed rule is accepted.
  - Without that schema, the utility story remains research-facing: the rule exists, but the handoff artifact for audit, monitoring, and operational review is not yet defined.
- Recommended correction:
  - Add a rule-card template to the README, appendix, or documentation folder.
  - Include selected feature-lag conditions, threshold ranges, vote threshold `m`, retained prefix `k`, baseline metrics, validation deltas, non-inferiority margins, intended use, known failure modes, retraining trigger, and monitoring trigger.
  - Optionally make the walkthrough notebook emit a filled example rule card for HAI `attack_p2 (a1)` alongside the existing CSV outputs.
- Expected report-card impact:
  - Improves utility by turning the accepted compressed rule from an experimental output into a reviewable deployment artifact.
- Changes made:
  - Added a repository-facing `Rule-Card Template For Accepted Compressed Rules` section to `README.md`.
  - Added Appendix `Rule-Card Template for Accepted Compressed Rules` to `Chapters/98_appendices.tex`, including fields for selected feature-lag conditions, critical-range bounds, vote threshold `m`, retained prefix `k`, baseline and rule metrics, validation deltas, non-inferiority margins, intended use, known failure modes, monitoring triggers, retraining triggers, and artifact links.
  - Added manuscript cross-references from the Chapter 4 worked HAI exemplar and the Chapter 7 strict deployment policy to Appendix `\ref{app:rule_card_template}` so readers know where to find the handoff template.
