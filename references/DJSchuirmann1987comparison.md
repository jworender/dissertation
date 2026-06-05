# A Comparison of the Two One-Sided Tests Procedure and the Power Approach for Assessing Equivalence of Average Bioavailability (Schuirmann, 1987)

## Dissertation Alignment Context
The dissertation proposal uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Motivation and contribution (Introduction):** The paper addresses how to statistically establish equivalence (not just no-difference) in bioavailability studies and compares the commonly used power approach with the Two One-Sided Tests (TOST) procedure.
2. **Formal problem setup (Statement of the Problem):** It defines interval hypotheses for equivalence, where the true mean difference must lie within prespecified bounds \([\\theta_1, \\theta_2]\\), and clarifies that these bounds are domain/clinical choices.
3. **Data and modeling assumptions:** The analysis is developed for normal-theory crossover designs (balanced case first), using the estimated mean difference, its standard error, and associated degrees of freedom.
4. **TOST method section:** The paper formulates two one-sided t-tests for lower and upper equivalence bounds and shows this is operationally equivalent to checking whether a \(1-2\\alpha\) confidence interval lies entirely within the equivalence interval.
5. **Power approach section:** It describes the ad hoc practice of combining a non-significant no-difference test with an estimated power requirement (often 0.80), then critiques its logic for equivalence decisions.
6. **Rejection-region comparison:** Through geometric rejection-region analysis, the paper shows TOST has a more coherent decision structure, while the power approach yields counterintuitive behavior for some precision regimes.
7. **Probability-characteristic comparison:** It compares true error behavior across study sensitivity levels and shows TOST offers controlled, interpretable Type I behavior via chosen nominal one-sided alpha, whereas the power approach can have undesirable operating characteristics.
8. **Comparison with Hauck-Anderson procedure:** The paper examines an alternative equivalence method, highlighting that it can be more liberal and may produce problematic conclusions under some p-value configurations.
9. **Practical extensions and appendices:** It discusses log-scale equivalence (e.g., ratio criteria), unbalanced-design formulas, and computational details used to generate figures and operating-characteristic curves.
10. **Overall conclusion:** The paper argues that TOST provides a principled and generally superior framework for equivalence testing relative to the standard power approach in average bioavailability assessment.

## Relevance to the Dissertation
A Comparison of the Two One-Sided Tests Procedure and the Power Approach for Assessing Equivalence of Average Bioavailability (Schuirmann, 1987) is relevant for experimental methodology because it provides a principled way to compare simplified vs. baseline models.

## Elements from This Paper to Use in the Dissertation
1. Use this paper's evaluation procedure as a formal comparison tool in ablations.
2. Define practical margins before testing whether compressed rules are non-inferior.
3. Reuse concepts around journal, pharmacokinetics, biopharmaceutics to improve statistical rigor in model comparisons.
4. Report interval-based conclusions in addition to mean metric differences.

## Competitive Method Assessment
This is not a competing classifier; it is a competing evaluation procedure. It is strongest when the goal is practical non-inferiority/equivalence and weaker when only point-estimate ranking is needed.

## Dissertation Citation Traceability

- Chapter: `Introduction`; Section: `Evaluation Priorities`; Line: `Chapters/01_introduction.tex:139`; Relevance: Cited to support the statement that Practical non-inferiority where needed: when compressed rules are compared against upstream sparse baselines, the evaluation uses prespecified non-inferiority margins to determine whether performance loss is practically small.
- Chapter: `Anytime Rule Compression (RQ3)`; Section: `Statistical Framing of "No Material Degradation"`; Line: `Chapters/07_rq3.tex:128`; Relevance: Cited to support the statement that Prior work in this line used an equivalence framing (TOST-style logic) with a predeclared margin (for example, $+/- 0.01$ AUC) to justify practical non-loss claims.
- Chapter: `Conclusion`; Section: `Conclusions by Research Question > RQ3 conclusion: Anytime compression makes interpretability operational`; Line: `Chapters/89_conclusion.tex:37`; Relevance: Cited to support the statement that Prespecified non-inferiority framing further supports practical non-loss claims when simplification is the objective and provides a baseline for accepting or rejecting compression in mixed real-world regimes.
