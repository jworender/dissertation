# The Probable Error of a Mean (Student, 1908)

## Dissertation Alignment Context
The dissertation proposal uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Problem statement:** The paper addresses inference for a population mean when sample size is small and the population variance is unknown.
2. **Why normal approximations fail:** It shows that plugging the sample standard deviation into the usual normal-error formula underestimates uncertainty in small samples.
3. **Sampling framework:** Assuming independent observations from a normal population, it studies the joint behavior of the sample mean and sample variance.
4. **Key pivot construction:** The core statistic is the standardized mean difference \((\bar{x}-\mu)/(s/\sqrt{n})\), where \(s\) is estimated from the same sample.
5. **Distributional result:** The paper derives the exact finite-sample distribution of this statistic (the Student \(t\)-distribution) with \(n-1\) degrees of freedom.
6. **Tail-probability formulation:** It provides integral/tabular forms for computing probabilities and critical values under the small-sample distribution.
7. **Probable error interpretation:** The article translates these results into corrected probable-error/confidence limits for mean estimation.
8. **Contrast with large-sample logic:** It emphasizes heavier tails than the normal law for small \(n\), yielding wider and more honest uncertainty intervals.
9. **Asymptotic connection:** It notes that as sample size grows, the \(t\)-distribution approaches the standard normal, recovering classical approximations.
10. **Practical and historical impact:** The paper establishes a usable small-sample testing/interval framework that became foundational for modern parametric inference.

## Relevance to the Dissertation
The Probable Error of a Mean (Student, 1908) is relevant as theoretical foundation for dependence, conditioning, and inference arguments used in the dissertation.

## Elements from This Paper to Use in the Dissertation
1. Use this source for theoretical statements and notation in the dissertation theory chapters.
2. Apply relevant results to conditioning, dependence, or uncertainty arguments.
3. Link its core concepts to the proposal's correlation-contraction and support-recovery claims.
4. Cite this reference when formalizing proof steps and assumptions.

## Competitive Method Assessment
This is not a competing prediction method. It provides mathematical/inferential foundations that can strengthen or weaken claims depending on assumption fit to the dissertation data. The local PDF has very limited machine-readable text; this comparison uses the canonical publication content.

## Dissertation Citation Traceability

- Chapter: `Anytime Rule Compression (RQ3)`; Section: `Statistical Framing of "No Material Degradation"`; Line: `Chapters/07_rq3.tex:128`; Relevance: Cited to support the statement that Prior work in this line used an equivalence framing (TOST-style logic) with a predeclared margin (for example, $+/- 0.01$ AUC) to justify practical non-loss claims.
- Chapter: `Conclusion`; Section: `Conclusions by Research Question > RQ3 conclusion: Anytime compression makes interpretability operational`; Line: `Chapters/89_conclusion.tex:37`; Relevance: Cited to support the statement that Prespecified non-inferiority framing further supports practical non-loss claims when simplification is the objective and provides a baseline for accepting or rejecting compression in mixed real-world regimes.
