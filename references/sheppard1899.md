# On the Application of the Theory of Error to Cases of Normal Distribution and Normal Correlation (Sheppard, 1899)

## Dissertation Alignment Context
The dissertation uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into binary indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Purpose and scope:** Sheppard develops formulas for testing normal distribution and normal correlation in finite samples, focusing on one normally distributed attribute and two normally correlated attributes.
2. **Normal curve foundations:** The paper defines and derives properties of the normal curve, including standardization, projection arguments, and moment relationships.
3. **Normal solid construction:** Sheppard uses geometric solids and projections to represent independent and correlated normal distributions.
4. **Error theory:** The paper derives sampling-error formulas for means, variances, class indices, and products of errors under normal assumptions.
5. **Application to normal distributions:** It applies the error formulas to tests of single-variable normality.
6. **Normal correlation geometry:** Part IV defines a correlation solid for two coexisting attributes and represents the dependence through a divergence angle D, with correlation expressed as cos D.
7. **Double median classification:** Section 27 shows how the four cells formed by splitting two normally correlated variables at their medians determine the divergence D.
8. **Classified-table calculation:** Section 28 extends the geometric construction from the double-median case to more general double-classification tables.
9. **Differential relationship:** Section 29 relates changes in the joint upper-tail proportion to changes in the divergence angle.
10. **Inference for normal correlation:** Sections 30-32 develop probable-error and discrepancy tests for estimating and testing normal correlation.

## Relevance to the Dissertation
Sheppard's double-median result is the classical source behind the zero-threshold bivariate-normal quadrant identity used in the RQ2 arcsine lemma. On article page 138 (PDF page 39), Sheppard defines the mean product of deviations as $ab\cos(D)$ and calls $D$ the divergence of the two distributions. In modern notation, for standardized jointly normal X and Y with correlation rho, this gives $\rho = \cos(D)$.

On article pages 140-141 (PDF pages 41-42), Sheppard's Section 27 arranges the normally correlated variables into four classes by their medians and states that the same-side and opposite-side median cells are in the ratio $\pi - D : D$. With total probability one across the four cells, this gives the same-sign cell mass $P = (\pi - D)/(2\pi)$. Substituting $D = \arccos(\rho)$ gives:

$$
P(X > 0, Y > 0) = \frac{1}{4} + \frac{\arcsin(\rho)}{2\pi}.
$$

This is the identity used to derive:

$$
\operatorname{Corr}(\operatorname{sign}(X), \operatorname{sign}(Y))
= \frac{2}{\pi}\arcsin(\rho).
$$

## Elements from This Paper to Use in the Dissertation
1. Cite Sheppard as the classical source for Lemma 1's zero-threshold bivariate-normal arcsine relation.
2. Use Section 27 as the historical bridge from median dichotomization to the quadrant probability formula.
3. Keep the dissertation derivation in modern notation, while noting that Sheppard's notation expresses the same result through the divergence angle D and rho = cos D.
4. Avoid citing later dissertation-line work as the authority for this classical identity; use later work only for method-lineage or application context.

## Competitive Method Assessment
This is not a competing prediction method. It is a classical mathematical statistics reference that supports the RQ2 theoretical derivation.

## Dissertation Citation Traceability

- Chapter: `Theoretical Analysis (RQ2)`; Section: `Formal Lemma Pathway`; Line: `Chapters/06_rq2.tex:88`; Relevance: Cited to support the statement that Then the transformed correlation follows the classical arcsine relation.
- Chapter: `Theoretical Analysis (RQ2)`; Section: `Formal Lemma Pathway`; Line: `Chapters/06_rq2.tex:95`; Relevance: Cited to support the statement that Because $(X,Y)$ is bivariate normal and centered, the classical quadrant formula gives.
- Chapter: `Lemmas`; Section: `Lemma 1`; Line: `Chapters/98_appendices.tex:59`; Relevance: Cited to support the statement that For jointly standard normal random variables thresholded at zero, the relationship between the pre-binarization correlation $ rho $ and the post-binarization correlation $ tilde rho $ is the classical arcsine relation.
- Chapter: `Lemmas`; Section: `Lemma 1`; Line: `Chapters/98_appendices.tex:66`; Relevance: Cited to support the statement that It follows the same median-classification argument underlying Sheppard's classical result.
- Chapter: `Lemmas`; Section: `Lemma 1`; Line: `Chapters/98_appendices.tex:116`; Relevance: Cited to support the statement that For standard normal variables $ X $ and $ Y $ with correlation $ rho $, the bivariate normal quadrant identity holds.
- Chapter: `Lemmas`; Section: `Lemma 3`; Line: `Chapters/98_appendices.tex:244`; Relevance: Cited to support the statement that For jointly standard normal variables, this joint probability is given by the same bivariate normal quadrant identity.
