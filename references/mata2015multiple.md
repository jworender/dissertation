# Multiple Transitions of the Susceptible-Infected-Susceptible Epidemic Model on Complex Networks (Mata and Ferreira, 2015)

## Dissertation Alignment Context
The dissertation proposal uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Problem framing and motivation (Section I):** The paper studies SIS epidemic spreading on complex networks, focusing on the long-standing disagreement about epidemic thresholds in scale-free networks with degree exponent gamma > 3.
2. **Competing threshold theories (Section I):** It compares heterogeneous mean-field (HMF), quenched mean-field (QMF), and BCPS-style long-range reinfection arguments, which predict different threshold behaviors.
3. **Core claim (Abstract and Section I):** The authors report that a single network can exhibit multiple epidemic transitions (multiple thresholds), especially when the degree distribution has large gaps and outlier hubs.
4. **Simulation methodology (Section II):** SIS dynamics are simulated with a modified Gillespie scheme and analyzed in the quasistationary (QS) regime to avoid absorbing-state bias in finite systems.
5. **Threshold diagnostics (Section II):** Thresholds are estimated using QS susceptibility peaks and QS-derived lifespan measures, with explicit discussion of why QS captures transitions missed by lifespan-only criteria.
6. **Empirical pattern of multiple peaks (Section III):** Susceptibility curves can present several peaks, interpreted as activations of different subdomains centered around hubs of different connectivity.
7. **Localized versus endemic activity (Section III):** Vanishing-threshold transitions are associated with localized long-term epidemics (small active fractions), while endemic spreading with finite infected density appears at a finite threshold.
8. **Role of network structure (Section III):** Multiple transitions are linked to structural heterogeneity, especially non-directly connected high-degree regions and degree-distribution outliers.
9. **Interpretation against theory (Sections III and IV):** Different observed thresholds align with different theoretical approximations, helping reconcile prior contradictions by separating localized and endemic regimes.
10. **Main conclusion (Section IV):** Epidemic spreading in heterogeneous networks is threshold-multiscale rather than single-threshold in many cases, with practical implications for how onset and persistence are interpreted.

## Relevance to the Dissertation
Multiple Transitions of the Susceptible-Infected-Susceptible Epidemic Model on Complex Networks (Mata and Ferreira, 2015) is relevant as domain evidence that epidemic spreading can be governed by multiple thresholds and delayed regime changes.

## Elements from This Paper to Use in the Dissertation
1. Use this source to justify the epidemic-spreading example in threshold-and-lag motivation text.
2. Reuse terminology around localized versus endemic activation regimes when discussing thresholded event behavior.
3. Borrow the multiple-threshold framing to motivate why single-threshold assumptions may underdescribe longitudinal triggering dynamics.
4. Cite this as a concrete network-science example where distinct parameter ranges activate distinct dynamical subdomains.

## Competitive Method Assessment
This paper does not present the main competing algorithmic pipeline. It is most useful for domain grounding and for supporting the claim that complex longitudinal dynamics can involve multiple distinct thresholds.


## Dissertation Citation Traceability

- Chapter: `Introduction`; Section: `Chapter context (no explicit section)`; Line: `Chapters/01_introduction.tex:10`; Relevance: Cited to support the statement that epidemic spreading can depend on multiple thresholds rather than a single transition point.
