# Feature Selection Using Efficient Fusion of Fisher Score and Greedy Searching for Alzheimer's Classification (K.P. and Thiyagarajan, 2022)

## Dissertation Alignment Context
The dissertation proposal uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Clinical motivation and task framing (Section 1):** The paper targets early baseline-stage classification of Normal Control (NC), Mild Cognitive Impairment (MCI), and Alzheimer's Disease (AD), emphasizing practical value of detecting risk without waiting for long follow-up histories.
2. **Related-work positioning (Section 2):** It reviews multimodal AD studies (MRI/PET/CSF/cognitive tests) and argues that ranking-only feature selection can miss useful feature combinations, motivating a wrapper-style search on top of ranking.
3. **Core feature-selection proposal (Section 3.3.1):** The method fuses Fisher Score (FS) ranking with a greedy forward-add/remove check, keeping a feature only if LOOCV Balanced Classification Accuracy (BCA) improves.
4. **Algorithmic behavior and complexity claim (Section 4.5 discussion):** Features are traversed once in FS rank order, yielding a sub-optimal minimal set (not guaranteed global optimum) with claimed linear-time search behavior over ranked features.
5. **Data and preprocessing pipeline (Section 3):** Experiments use baseline-only cohorts from ADNI-TADPOLE and AIBL; reversed-progress cases are filtered, and records with missing selected-feature values are removed instead of imputed.
6. **Evaluation protocol (Section 4):** Performance is reported with both LOOCV and stratified 10-fold CV using SVM (RBF) and 1-NN, measured by BCA, precision, sensitivity, specificity, F1, and MAUC for multiclass settings.
7. **Main ADNI-TADPOLE findings (Sections 4.1 and 4.5):** The selected minimal set is four features (CDRSB, MMSE, ADAS-13, AV45), with reported multiclass performance around BCA 90-91% and MAUC 0.97-0.98 (LOOCV), plus strong binary results.
8. **Main AIBL findings (Section 4.2):** The selected minimal set is three features (LDELTOTAL, CDGLOBAL, MMSCORE), with lower LOOCV multiclass performance than ADNI but stronger stratified-10-fold results and competitive binary MCI-vs-AD sensitivity/specificity.
9. **Ablation and comparative analysis (Sections 4.4 and 4.5):** The paper reports substantial performance drops without the proposed feature-selection step and compares favorably with several prior ADNI/AIBL studies under its chosen metrics.
10. **Limitations and future work (Section 4.8 and 5):** Authors note reliance on preselected literature features, reduced sample size after missing-data removal, sub-optimal (not best) subset search, and plans for better imputation, larger cohorts, and clinical validation.

## Relevance to the Dissertation
Feature Selection Using Efficient Fusion of Fisher Score and Greedy Searching for Alzheimer's Classification (K.P. and Thiyagarajan, 2022) is relevant background that helps position the proposal among existing longitudinal, sparse, and interpretable modeling approaches.

## Elements from This Paper to Use in the Dissertation
1. Use this reference to strengthen the related-work bridge to the dissertation pipeline.
2. Extract terminology and assumptions that clarify modeling constraints in longitudinal settings.
3. Reuse details around cient, fusion, fisher to sharpen experiment design and discussion.
4. Tie this reference to ablations comparing raw, rectified, and compressed models.

## Competitive Method Assessment
This paper does not present the main competing algorithmic pipeline. It is most useful for problem framing, benchmark selection, and identifying contexts where interpretable lag-aware rules are preferable to opaque alternatives.


## Dissertation Citation Traceability

- Chapter: `Background`; Section: `Competing approaches`; Line: `Chapters/02_background.tex:38`; Relevance: Cited to support the statement that item Wrapper and filter selection methods remain pragmatic baselines, especially in domain pipelines where model families vary, but they are often heuristic and may provide weaker attribution consistency across resamples.
- Chapter: `Related Work`; Section: `Correlation-Aware and Alternative Feature Selection Families`; Line: `Chapters/03_relatedwork.tex:43`; Relevance: Cited to support the statement that Filter, wrapper, and embedded selection families remain widely used in practice because they are flexible and model-agnostic . Recent hybrid ranking-plus-search approaches also show good empirical performance in domain-specific pipelines . Still, these families can be sensitive to search heuristics, may yield unstable subsets under resampling, and usually do not produce direct temporal-threshold semantics without additional modeling layers.
