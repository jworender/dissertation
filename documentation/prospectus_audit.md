# Dissertation Prospectus Audit

**Author**: Jason Orender
**Title**: Interpretable Sparse Modeling of Longitudinal Signals via Critical-Range Rectification and Anytime Rule Compression

## 1. Executive Summary
Overall, the prospectus is exceptionally well-written, logically structured, and clearly bounds its claims. The problem statement—tackling the instability of sparse selection in lag-expanded longitudinal data (due to multicollinearity) and the need for operational interpretable models—is highly relevant to domains like industrial control and clinical monitoring. The proposed pipeline (rectification $\rightarrow$ sparse fitting $\rightarrow$ compression) is a pragmatic and cohesive approach.

## 2. Evaluation of Novelty
The novelty of this research lies primarily in its **integration and positioning** rather than the invention of an entirely new optimization algorithm.
*   **Representation-First Intervention**: While much of the literature focuses on penalty engineering (e.g., adaptive lasso, group lasso) to handle dependence, this work argues for representation-level preprocessing (critical-range rectification). 
*   **Theoretical Bridge**: Connecting zero-threshold sign binarization to the Irrepresentable Condition (IC) via correlation contraction (arcsine law) is an elegant proof-of-concept that establishes a structural mechanism for why the heuristic works.
*   **Anytime Rule Compression**: Creating a tunable complexity-performance Pareto frontier directly from lasso coefficients is a highly practical contribution for operational deployment. Treating interpretability as an explicit $m$-of-$K$ target rather than a post-hoc analysis is a strong philosophical stance.

## 3. Logical Flaws and Vulnerabilities
While the core argument is sound, there are a few areas where the logic could be challenged during a defense. These are not fatal flaws, but vulnerabilities that should be proactively fortified:

### 3.1 The Gap Between Theory (RQ2) and Practice (RQ1)
*   **The Issue**: The theoretical analysis in Chapter 6 depends on *zero-threshold sign binarization* under joint normality. However, the proposed empirical method relies on *critical-range rectification* (which often involves learned, non-zero thresholds or bounded intervals). 
*   **Logical Vulnerability**: The arcsine law (Lemma 1) $\tilde{\rho} = \frac{2}{\pi}\arcsin(\rho)$ specifically applies to zero-mean sign binarization. If the features are rectified into off-center intervals or asymmetric indicators, the covariance contraction behavior changes. In fact, thresholding far into the tails can sometimes *increase* the correlation of extreme events (tail dependence).
*   **Recommendation**: In the "Generalization roadmap" (Future Work, Section 8.3), explicitly commit to visualizing or bounding how sample covariance changes when using interval ranges rather than just zero-thresholds. 

### 3.2 The Performance-Interpretability Tradeoff in Non-Ideal Regimes
*   **The Issue**: In Chapter 5 (Preliminary Studies), the UNICEF dataset results show a massive drop in discrimination for the transformed model (AUC 0.865) compared to the untransformed mode (AUC 0.989). 
*   **Logical Vulnerability**: A drop of ~0.12 in AUC is often considered a material, sometimes unacceptable, degradation in many predictive domains. The text justifies this by saying the dataset may not be "threshold-and-lag aligned."
*   **Recommendation**: The dissertation needs an explicit diagnostic or heuristic to determine *a priori* if a dataset is "threshold-mediated". If the user cannot know beforehand whether the transformation will cause a catastrophic loss of AUC, the pipeline's practical utility decreases. Proposing a simple permutation or signal-to-noise test before adopting the pipeline would strengthen operational usability.

### 3.3 The Heuristic Nature of "Anytime" Compression (RQ3)
*   **The Issue**: The rule compression drops small coefficients, keeps the top $k$, and snaps them to a uniform magnitude $K$.
*   **Logical Vulnerability**: Sorting by marginal $|\beta_j|$ and snapping to a uniform magnitude in a multivariate logistic setting ignores conditional dependencies. Two features might have moderate $\beta$ values because they are slightly collinear and share the effect; snapping them to $K$ might over-inflate their combined odds ratio.
*   **Recommendation**: Clarify how the compression step validates conditional joint effects (e.g., does it re-fit the intercept or perform a quick constrained re-optimization of $K$, or is it purely a greedy thresholding?). 

## 4. Suggested Changes and Additions

1.  **Terminology Refinement**: The term "Anytime Rule Compression" might draw unwanted comparisons to traditional anytime search algorithms (like A* variants or Monte Carlo Tree Search) where a single objective improves monotonically with compute time. Consider clarifying that this is a "Complexity-Tunable Compression" or "Pareto-Frontier Extraction", though "Anytime" is acceptable if carefully caveated.
2.  **Expanded Baselines (Chapter 8)**: The proposed future work in Workstream A2 includes L1, elastic-net, group lasso, etc. It should also include **Explainable Boosting Machines (EBMs)** or **RuleFit**. Since the goal is interpretability and threshold-based learning, tree-based interpretable models are the most direct competitors to your $m$-of-$K$ logic rules.
3.  **Formalizing "Operational Loss"**: In RQ3, define "unacceptable operational loss" more rigorously. Consider defining an acceptable equivalence margin $\epsilon$ statistically (e.g., via non-inferiority testing).
4.  **Handling Continuous Magnitude Utility**: Add a brief discussion on hybrid features. If a continuous signal has a threshold trigger but also contains predictive power in its magnitude *beyond* the threshold, how does the pipeline accommodate this? (e.g., keeping both the indicator and a spline/continuous term).

## 5. Conclusion
This prospectus outlines a robust, defense-ready research plan. The separation of empirical behavior (RQ1), theoretical mechanism (RQ2), and operational deployment (RQ3) makes the scope extremely clear. By addressing the assumptions in the correlation-contraction theory and providing a framework for when *not* to use the method, the final dissertation will be computationally impactful and scientifically grounded.
