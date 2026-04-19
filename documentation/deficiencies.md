# Dissertation Deficiencies

This file tracks places where prospectus-era language was rewritten into dissertation-final language, but the supporting material is not yet present in the manuscript. Each identifier corresponds to a placeholder of the form `<<< deficiency D00X >>>` in the LaTeX sources.

## D001 - RQ1 stability and ablation package

- Needed: repeated-fold or bootstrap stability summaries, lag-fidelity metrics, stage-wise ablation results, and runtime scaling summaries for the rectification pipeline.
- Affected files: `main.tex`, `Chapters/05_rq1.tex`
- Suggested backfill: one stability table, one ablation figure/table, and a short narrative paragraph tying those results to the RQ1 claim.

## D002 - RQ1 expanded baseline and cross-domain comparison package

- Needed: consolidated comparisons against additional correlated-feature baselines and at least one broader cross-domain validation summary beyond the currently shown core case studies.
- Affected files: `main.tex`, `Chapters/05_rq1.tex`
- Suggested backfill: one benchmark table covering elastic net/adaptive/group/ordered/QP comparators plus a concise transferability discussion.

## D003 - RQ2 empirical boundary-condition package

- Needed: empirical stress tests or summarized results for correlation sweeps, threshold perturbations, negative-correlation cases, and/or a bridge from the zero-threshold theorem to practical critical-range settings.
- Affected files: `Chapters/06_rq2.tex`
- Suggested backfill: one subsection with a figure or table showing where the theorem's mechanism holds strongly, weakly, or fails.

## D004 - RQ3 real-data compression validation package

- Needed: full real-data `J`-versus-`k` curves, equivalence or non-inferiority comparisons, and a prespecified adoption-policy summary for compressed rule models.
- Affected files: `Chapters/07_rq3.tex`
- Suggested backfill: one real-data anytime frontier figure, one equivalence table, and a short paragraph defining the deployment policy used to accept a compressed rule.
