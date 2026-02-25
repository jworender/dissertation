# Matrix Analysis, Second Edition (Horn and Johnson, 2012)

## Dissertation Alignment Context
The dissertation proposal uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Purpose and scope (Preface):** The book presents a broad, modern treatment of matrix analysis using canonical forms and invariance principles as unifying ideas across theory and applications.
2. **Foundational review (Chapter 0):** It consolidates core linear-algebra prerequisites (vector spaces, rank, determinants, nonsingularity, basis changes, block matrices, matrix classes) used throughout later chapters.
3. **Eigenstructure and similarity (Chapter 1):** The text develops eigenvalues/eigenvectors, characteristic and minimal polynomials, algebraic/geometric multiplicity, and similarity invariants.
4. **Unitary frameworks (Chapter 2):** It covers unitary similarity/equivalence, Schur triangularization, normal matrices, and key decompositions including SVD and CS decomposition.
5. **Canonical-form machinery (Chapter 3):** Jordan, real Jordan, and Weyr canonical forms are treated in detail, with consequences for structure, factorization, and matrix-function analysis.
6. **Hermitian/symmetric and congruence theory (Chapter 4):** The chapter focuses on spectral/variational results, eigenvalue inequalities, and congruence-based classifications for structured matrices.
7. **Norms and conditioning (Chapter 5):** Vector and matrix norms, duality, induced norms, and condition numbers are developed for stability/error analysis of linear systems and algorithms.
8. **Eigenvalue localization and perturbation (Chapter 6):** Gersgorin-type inclusion sets and perturbation theorems provide tools for sensitivity analysis under model/data changes.
9. **Positive semidefinite and nonnegative matrices (Chapters 7-8):** Positive-definite theory (Loewner order, Schur product, inequalities, block-matrix results) and Perron-Frobenius theory for nonnegative matrices are presented.
10. **Reference infrastructure (Appendices):** Supplementary material (complex numbers, convexity, continuity of polynomial roots/eigenvalues, canonical pairs, extensive hints/index) supports rigorous proof work and practical lookup.

## Relevance to the Dissertation
Matrix Analysis, Second Edition (Horn and Johnson, 2012) is relevant as theoretical foundation for dependence, conditioning, and inference arguments used in the dissertation.

## Elements from This Paper to Use in the Dissertation
1. Use this source for theoretical statements and notation in the dissertation theory chapters.
2. Apply relevant results to conditioning, dependence, or uncertainty arguments.
3. Link matrix, second, edition to the proposal's correlation-contraction and support-recovery claims.
4. Cite this reference when formalizing proof steps and assumptions.

## Competitive Method Assessment
This is not a competing prediction method. It provides mathematical/inferential foundations that can strengthen or weaken claims depending on assumption fit to the dissertation data.


## Dissertation Citation Traceability

- Chapter: `Background`; Section: `Support recovery and the irrepresentable condition`; Line: `Chapters/02_background.tex:19`; Relevance: Cited to support the statement that From a linear-algebra perspective, the issue is closely tied to conditioning and inverse-Gram stability, which govern how sensitive selected supports are to perturbations in data and tuning . For this reason, the dissertation treats representation-level correlation contraction as a first-class objective before sparse fitting, and uses IC-oriented reasoning as the theoretical lens for interpreting support behavior.
- Chapter: `Related Work`; Section: `Support Recovery Under Dependence`; Line: `Chapters/03_relatedwork.tex:25`; Relevance: Cited to support the statement that From a matrix-analysis viewpoint, these selection instabilities reflect conditioning and inverse-Gram sensitivity, which directly affect sparse-support perturbation behavior . This perspective motivates representation-level interventions before sparse fitting, rather than relying only on penalty redesign in the original feature space.
- Chapter: `Research Questions`; Section: `Why RQ2 matters`; Line: `Chapters/04_resquestions.tex:28`; Relevance: Cited to support the statement that At a high level, the motivating hypothesis is that rectification can contract harmful dependence structure in ways that improve sparse-support conditions related to IC-style reasoning . Prior proof-of-concept analysis in this line supports this direction under explicit assumptions, but does not yet establish universal guarantees across all threshold settings and dependence regimes . RQ2 is therefore critical: it separates durable methodological insight from dataset-specific heuristic success.
- Chapter: `Theoretical Analysis (RQ2)`; Section: `Why sign binarization can reduce dependence`; Line: `Chapters/06_rq2.tex:71`; Relevance: Cited to support the statement that The second point should not be read as a universal monotone guarantee for every design. It is a regime-level effect supported in the PoC analysis and tied to matrix-conditioning arguments.
- Chapter: `Appendices`; Section: `Lemma 2`; Line: `Chapters/98_appendices.tex:256`; Relevance: Cited to support the statement that item If all off-diagonal entries of a correlation matrix are strictly bounded away from , then the matrix's smallest eigenvalue is always positive.
