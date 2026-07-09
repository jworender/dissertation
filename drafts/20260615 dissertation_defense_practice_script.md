# Dissertation Defense Practice Script

## Slide 1 — Title

Good afternoon, and thank you for being here.

My dissertation is titled **“Interpretable Sparse Modeling of Longitudinal Signals via Critical-Range Rectification and Anytime Rule Compression.”**

The central problem I address is how to build models for longitudinal signals that are not only predictive, but also interpretable, sparse, computationally practical, and usable in settings where humans need to understand the basis for a decision.

The work develops an end-to-end framework that begins with raw longitudinal sensor-style data, transforms it through critical-range rectification, fits a sparse model, and then optionally compresses that model into compact logical rules when doing so is justified by held-out validation.

---

## Slide 2 — Overview

This slide gives the roadmap for the defense.

The thesis is that **critical-range rectification improves the reliability and interpretability of sparse longitudinal modeling**, and that **anytime rule compression makes the result operationally usable**.

I will start with the problem and the knowledge gap. Then I will walk through the answers to the three research questions.

The first question is empirical: can rectification produce a stable sparse baseline with reliable feature and lag attribution?

The second question is theoretical: why does rectification work when it works, and how far does that explanation generalize?

The third question is operational: can the sparse solution be compressed into compact logical rules without unacceptable loss in discrimination?

After that, I will discuss scope boundaries and practical implications, and then close with the main dissertation contributions and future directions.

---

## Slide 3 — Section 1: Problem and Pipeline

I will begin with the motivation for the work.

The goal of this first section is to establish the setting: longitudinal, high-dimensional, correlated data where the outcome is often driven by threshold and lag behavior.

This is also where I will explain why the dissertation takes a representation-first approach rather than relying only on changes to the sparse-learning penalty or using a post-hoc interpretability method.

---

## Slide 4 — The Problem

The core problem is driven by three tensions.

First, high dimensionality and correlation create unstable sparse support. In longitudinal data, lag expansion means that neighboring time lags are often highly correlated. This makes it difficult for sparse models to select the right feature and the right lag reliably.

Second, operational settings often impose compute and model-complexity constraints. A model that is accurate but too large or too expensive may not be practical in some settings.

Third, high-stakes deployment often requires transparent and auditable rules rather than opaque scoring functions.

The details of the plots on the right are not important here. The point is that events can be associated with threshold regions at different lags, and those regions may differ by signal.

These three tensions motivate a representation-first pipeline for interpretable sparse longitudinal modeling.

---

## Slide 5 — Gaps in Prior Work

The related work addresses parts of this problem, but not the full combination.

Sparse penalties are mature and computationally useful, but they can be fragile under correlation and dependence. They may predict well while selecting unstable supports.

Structured and dependence-aware penalties help in some settings, but they often continue to operate in the raw correlated feature space.

Rule-learning methods are transparent, but direct rule search can become search-heavy and combinatorial in high-dimensional longitudinal settings.

So the gap is not that prior methods fail completely. The gap is that the field lacks an end-to-end, reproducible synthesis across these method families: a pipeline that handles representation, sparse attribution, compression, and deployment decision logic together.

---

## Slide 6 — Cross-Family Positioning

This slide positions the dissertation pipeline relative to the main competing method families.

Compared with L1, elastic net, and adaptive lasso, the key difference is that this work changes the representation before fitting, rather than relying only on penalty tuning in the original dependent feature space.

Compared with grouped and ordered sparsity, the pipeline targets threshold logic and lag semantics through feature redesign, not only through coefficient constraints.

Compared with dependence-aware methods and quadratic programming selectors, rectification couples redundancy reduction to explicit threshold semantics and a downstream rule path.

Compared with EBM and RuleFit-style approaches, this pipeline produces a shared rectified sparse baseline and, when justified, a smaller policy-screened rule artifact.

And compared with direct rule-list or LAD-style approaches, this method restricts logic compression to the active sparse support rather than searching the full lag-expanded space from scratch.

---

## Slide 7 — Section 2: Answers to Research Questions

I will now move into the main body of the dissertation: the answers to the three research questions.

The sequence is intentional. RQ1 tests whether rectification improves sparse attribution in practice. RQ2 explains why that improvement can occur under a scoped theoretical mechanism. RQ3 asks whether the resulting sparse structure can be converted into a simpler rule artifact for operational use.

---

## Slide 8 — Final Pipeline

The final pipeline has three stages.

First, **rectification** converts lagged continuous measurements into critical-range indicators learned from training data only. The goal is to transform the representation before fitting, so that the model is operating on features that more directly encode threshold-event behavior.

Second, the method fits an **L1-regularized logistic baseline** on the rectified design. The sparse coefficient set identifies candidate feature-lag triggers.

Third, when a simpler artifact is needed, the active terms can be compressed into a **policy-controlled m-of-K anytime rule**. Compression is not automatic. It is accepted only when held-out deployment gates pass.

So the pipeline is not simply “transform, fit, deploy.” It is a branchable workflow with explicit checks at each stage.

---

## Slide 9 — Critical-Range Rectification

This slide defines the core representation.

A critical range is a train-only event-associated region of a feature’s values. In the simplest independent-feature case, it is the minimum-to-maximum interval observed during event-positive training times.

The original continuous feature is then converted into a logical indicator: +1 when the measurement is within the critical range, and -1 when it is outside the critical range.

The important methodological safeguard is shown at the bottom: **ranges are learned on training folds only**. That prevents the test data from contaminating the representation.

This slide describes the empirical pipeline. Later, in the theory section, I narrow to zero-threshold sign binarization because that special case is analytically tractable.

---

## Slide 10 — Measuring Success

The goal is not only predictive accuracy.

The dissertation evaluates four kinds of success.

The first is performance: AUC, Youden’s J-index, and exact-lag F1.

The second is attribution quality and stability: active support size, pairwise Jaccard support stability, and feature-lag localization.

The third is compression and deployment quality: held-out non-inferiority gates, rule length, and number of rules.

The fourth is efficiency: training and inference runtime.

The plots on the right are illustrative. The point is that rectification and compression should not only preserve discrimination; they should also make the model more interpretable, more stable, and more usable.

---

## Slide 11 — Research Questions

This slide restates the three research questions in the context of the full workflow.

The motivation is that selecting relevant features in high-dimensional, strongly correlated longitudinal data is challenging when thresholds and lags drive outcomes.

Critical-range rectification maps continuous measurements to logical indicators defined by train-only critical ranges. That can simplify correlation structure and stabilize sparse model fitting.

The three questions then follow naturally.

RQ1 asks whether critical-range rectification can produce a stable sparse baseline with reliable feature and lag attribution.

RQ2 asks why rectification works, and how far the theoretical explanation generalizes.

RQ3 asks whether the resulting sparse solution can be compressed into compact logical rules without unacceptable loss in operational discrimination.

The figure on the right is the operational playbook: raw baseline, threshold diagnostic, rectified baseline, optional compression, or fallback if the gates fail.

---

## Slide 12 — Research Question 1

The first research question is:

**Can critical-range rectification produce a stable sparse baseline with reliable feature and lag attribution?**

This question is empirical. It asks whether the representation change actually improves sparse longitudinal selection in practice.

The evidence comes from synthetic data with known ground truth, comparative baseline studies, and real-world data.

---

## Slide 13 — RQ1: Rectification Workflow

This slide shows the RQ1 workflow.

First, longitudinal data are collected and flattened into lagged examples. Each measurement is offset across candidate time lags. This lag expansion is useful because it lets us model delayed effects, but it also creates many highly correlated columns.

Second, critical ranges are estimated using training data only. For each feature-lag column, event-positive training rows define the candidate critical range.

Third, an L1-regularized logistic model is fit on the rectified design to determine the sparse coefficient set.

The algorithm on the right is the formal version of these three boxes: lag-expanded inputs, train-only critical ranges, and rectified L1-logistic fitting.

---

## Slide 14 — RQ1: Synthetic Data

The synthetic data provide a controlled test because the ground-truth feature-lag structure is known.

The table compares raw sparse fitting, rectified sparse fitting, and the compressed rule.

The raw model already has high AUC, but the exact-lag F1 is very low, around 0.048. That means prediction can look good while attribution is poor.

After rectification, AUC improves to about 0.998, Youden’s J improves, exact-lag F1 rises to about 0.619, and pairwise support stability also improves.

The compressed rule preserves most of the discrimination while reducing the active support to about six terms on average and improving exact-lag F1 further.

So the main synthetic result is not just better prediction. It is better attribution, stability, compactness, and efficiency.

---

## Slide 15 — RQ1: Quadratic Programming Comparison

This slide compares rectification with a close parallel method in intent: the Katrutsa-Strijov quadratic-programming feature-selection approach.

The QP method provides feature-importance weights, but it does not directly produce a predictive model for metrics like AUC, Youden’s J, or F1. So for comparison, an L1 fit was applied to the selected feature set.

The QP importance values often came close to identifying the correct variables, but in several cases they selected an incorrect lag.

The table shows the key result. QP plus L1 had AUC of 0.894, Youden’s J of 0.603, and exact-lag F1 of 0.000. Rectified L1 had AUC of 0.997, Youden’s J of 0.946, and exact-lag F1 of 0.571.

The bottom note addresses runtime fairness: the original QP implementation was in R, so it was reimplemented in Python. After that, runtime was comparable, so the difference here is not just an implementation artifact.

---

## Slide 16 — RQ1: Real-World Data

This slide shows the real-world evidence using HAI as the main exemplar and UNICEF as a cross-domain check.

In the HAI case, rectification concentrated coefficient mass on the turbine-loop P2 instruments while suppressing unrelated features. That is exactly the kind of attribution behavior we want.

The smaller P4 response is plausible because P4 is the HIL simulator block and contains signals coupled to the P2 turbine-loop response.

The table also includes UNICEF. There, raw metrics were higher, but the raw model used a less compact feature set: 16 categories versus 5. That is an important scope point.

So the conclusion is not that rectification is universally superior on every metric. The conclusion is that rectification must be judged against attribution, compactness, and complexity goals, not only raw discrimination.

---

## Slide 17 — RQ1 Answer

The answer to RQ1 is **yes, conditionally**.

Critical-range rectification improved support concentration, lag localization, compactness, and often runtime in threshold-and-lag aligned regimes.

The cross-domain checks show that it should be used when threshold structure is meaningful and held-out performance is preserved.

The efficiency note is also important. In the synthetic studies, rectification reduced runtime even after transformation overhead, while producing more compact and stable sparse supports.

This leads naturally to RQ2. The empirical results are strong in the target regime, but we still need to ask what mechanism explains the gains, under what assumptions rectification improves sparse recovery, and where the theoretical and empirical boundaries appear.

---

## Slide 18 — Research Question 2

The second research question is:

**Why does rectification work, and how far does the theoretical explanation generalize?**

This section gives a scoped theoretical explanation. The goal is not to prove that every possible critical-range rectifier always helps.

Instead, the goal is to show a tractable mechanism: under explicit assumptions, a threshold transformation can contract dependence and improve sparse-recovery conditions.

---

## Slide 19 — RQ2: Irrepresentable Condition

The theoretical lens we will use is the LASSO irrepresentable condition.

The IC gives a formal way to reason about when LASSO can recover the true sparse support. In high-dimensional lag-expanded longitudinal data, raw features often violate this condition because of high collinearity.

RQ2 uses zero-threshold sign binarization as a tractable special case. In that setting, we can show how rectification can contract dependence and improve IC behavior.

The important qualifier is that this is a scoped, mechanistic result. It is not a universal guarantee for every rectifier or dataset.

The bottom box captures the scope: practical critical-range rectification is broader, so the later boundary checks test how far this mechanism appears to extend.

---

## Slide 20 — RQ2: The Arcsin Relation

The key mathematical tool is the arcsin relation.

For standardized, jointly normal variables with correlation rho, zero-threshold sign binarization induces a closed-form mapping.

The transformed correlation is:

${\rho}_{tilde} = (2 / pi) * arcsin(\rho)$

Under these assumptions, the magnitude of the transformed pairwise correlation is no larger than the original correlation.

The important intuition is at the bottom: **sign binarization contracts pairwise correlations**, and that reduces harmful dependence among lag-expanded features.

This is the bridge from the representation change to improved sparse-selection behavior.

---

## Slide 21 — RQ2: Gram Matrix Bounds

The next step is to connect pairwise correlation contraction to the Gram matrix.

In the equicorrelated case, the active-set Gram matrix and its inverse have closed-form expressions. Similar expressions can be obtained for the binarized version by substituting the transformed correlation for the raw correlation.

When the transformed correlation is smaller, the inverse-Gram contribution can also be bounded.

The reason this matters is that the inverse Gram matrix appears directly inside the IC term. So the correlation contraction is not just an isolated fact about pairwise features. It affects the stability of the active-set inverse and the support-recovery condition.

The key bridge is that, in this scoped equicorrelated case, sign binarization can reduce the inverse-Gram contribution, making support recovery more favorable.

---

## Slide 22 — RQ2: Parsing the Results

This slide decomposes the IC term.

The IC expression combines three components: inactive-active covariance, inverse active-set covariance, and the sign direction of the active coefficients.

The sign vector has infinity norm 1 on the active support, so the important changes occur in the covariance terms.

The arcsin relation attenuates positive correlations after zero-threshold sign binarization. Under the scoped assumptions, inactive-active covariance terms shrink.

That means inactive lag features are less able to imitate active lag features in the IC expression.

So this slide explains the mechanism: rectification can make sparse recovery easier because it reduces the dependence pathways that allow irrelevant features to masquerade as relevant ones.

---

## Slide 23 — RQ2: Boundary Checks Beyond the Theorem

This slide is important because it states the limits of the theory.

The theorem gives a scoped mechanism, not a universal guarantee. To test how far the mechanism extends, I used empirical boundary checks.

The contour plots show the HAI real-world data overlaid on the same kind of IC-boundary framework used in the theorem. Before and after rectification, we can see how the empirical distribution shifts into a more favorable region and increases contrast between active and inactive dependence structure.

The table summarizes the broader boundary package.

The positive zero-threshold sign case is strong and matches the theorem assumptions.

A shifted one-sided cutoff is also strong, suggesting practical thresholds can preserve the mechanism.

Shifted interval rules are weaker, meaning broader rectifiers need empirical validation.

The negative-side IC sweep did not hold, showing that not all correlation structures benefit.

And the negative pair with a complement feature shows that representation design can repair some failures.

The takeaway is that RQ2 provides a defensible scoped mechanism, while the boundary checks define when caution or hybrid features are needed.

---

## Slide 24 — Research Question 3

The third research question is:

**Can the resulting sparse solution be compressed into compact logical rules without unacceptable loss in operational discrimination?**

This question moves from sparse attribution to deployment usability.

Even a sparse model may still have too many small coefficients for direct human use. RQ3 asks whether the rectified sparse model can be turned into a simpler rule artifact, and whether we can decide when that simplification is safe.

---

## Slide 25 — RQ3: Policy-Controlled Rule Compression

L1-regularized logistic models provide sparsity and computational simplicity, but they can still leave small residual coefficients that obscure the underlying event logic.

Rule compression converts the rectified sparse support into a compact m-of-K rule candidate. The key word is **candidate**.

The flow diagram shows the process.

First, fit the rectified sparse model. Then sort active features by coefficient magnitude. Then scan ordered prefixes. For each prefix, optimize the m-of-K vote threshold. Then nominate a candidate k-star.

Finally, the candidate is accepted only if held-out deployment gates pass.

So compression is not a post-hoc simplification chosen by preference. It is a policy-controlled procedure with an explicit accept-or-reject decision.

---

## Slide 26 — RQ3: HAI Compression Policy Results

This slide shows the HAI compression policy results.

The Youden’s J versus K plot shows the anytime frontier: as we retain more features, performance changes along the ordered feature path.

The frontier identifies compact m-of-K rule candidates, but compression is adopted only when the candidate passes the held-out deployment gates.

The table shows the result.

For HAI Attack P2 and HAI Attack P1/P2, the policy selected compressed rules. These give roughly 2.8x and 3.1x compression.

For HAI Attack P3 and HAI Attack P1/P3, the policy rejected the candidates, so the upstream rectified sparse baseline is retained.

P3 is a useful example of why the policy gate matters. Even though the candidate improved Youden’s J, its 95% confidence interval exceeded the allowed delta-AUC gate, so the compressed rule was rejected. The deployment decision is governed by the full held-out policy, not by a single improved metric.

---

## Slide 27 — Section 3: Boundaries and Implications

I will now step back from the individual research questions and discuss the boundaries and practical implications.

This section is important because the dissertation does not claim that rectification and compression are universally appropriate.

Instead, the contribution is a pipeline with diagnostics, gates, and fallback decisions.

---

## Slide 28 — Scope Boundaries

This slide summarizes when the method is most appropriate and when caution is needed.

The best-fit regime has threshold-mediated event structure, meaningful lagged dependencies, and raw sparse models that remain predictive but unstable.

Rectification is especially useful when it improves attribution, compactness, or stability without harming held-out fit.

Caution is needed when threshold structure is weak or unstable, when small threshold changes produce erratic results, when post-threshold magnitude still carries important signal, or when compression fails held-out non-inferiority gates.

The takeaway is that rectification is a representation strategy, not a universal replacement for raw continuous modeling.

The correct decision may be to stay raw, use hybrid features, or stop before compression.

---

## Slide 29 — Practical Implications

This slide translates the dissertation into a deployment playbook.

The workflow is simple.

Start with a raw sparse baseline. Screen for threshold-and-lag structure. Estimate critical ranges on training data only. Compare raw and rectified attribution and held-out discrimination. Compress only when a simpler rule is needed and justified. Deploy compressed rules only when held-out gates pass.

What the user gets is more stable feature-lag attribution, smaller and more auditable sparse supports, optional compact m-of-K rules, and explicit fallback decisions when simplification is unsafe or unnecessary.

The practical contribution is not just a model. It is a decision policy for interpretable longitudinal modeling.

---

## Slide 30 — Section 4: Contributions

I will close by summarizing the dissertation contributions.

The key point is that the work is not just a collection of experiments. It contributes an integrated framework: a representation-first pipeline, a scoped theoretical bridge, an anytime compression method, an empirical validation package, and a reproducible implementation pathway.

---

## Slide 31 — Contributions

The dissertation makes five main contributions.

First, it provides a unified rectification-first pipeline: a complete workflow from raw longitudinal data to sparse models and optional rules.

Second, it provides a scoped theoretical bridge: a mechanistic explanation for why rectification can improve sparse recovery under explicit assumptions.

Third, it provides an anytime rule-compression stage that converts active rectified support into compact m-of-K rule candidates when policy gates justify simplification.

Fourth, it provides an empirical validation package, including synthetic studies, benchmark comparisons, HAI, UNICEF, ablation, and boundary studies that characterize both gains and limits.

Fifth, it provides a reproducible implementation pathway through the CUTLASS package and notebooks that connect the dissertation artifacts to reusable analyses.

Taken together, the dissertation contributes both a theoretical framing and a usable implementation pathway for interpretable longitudinal modeling.

---

## Slide 32 — Thank You / Questions

Thank you.

The final message is that critical-range rectification can improve sparse longitudinal attribution when the event structure is threshold-and-lag aligned; the theoretical analysis provides a scoped mechanism for why this can happen; and anytime rule compression makes the result operationally usable when held-out policy gates justify simplification.

I’m happy to take questions.

---

# Backup Slides

## Slide 33 — Backup Slides

These are backup slides for technical questions.

The main deck intentionally keeps the proof and administrative details at a higher level. These slides are available if the committee wants more detail on the RQ2 proof synthesis or the timeline.

---

## Slide 34 — Backup: RQ2 Putting the Pieces Together

This backup slide shows the proof synthesis in one place.

The left side starts from the IC decomposition. The key terms are inactive-active covariance and the inverse active-set Gram matrix.

Under the stated assumptions, the previous lemmas show that sign binarization contracts the relevant covariance terms and improves the inverse-Gram behavior.

The result is a bound showing that the binarized version is more likely to satisfy the IC-related condition than the raw version in the theorem-scoped setting.

The important point is that the proof isolates three mechanisms: pairwise contraction, improved conditioning, and smaller off-support covariance.

Together, those mechanisms explain why rectification can promote sparse, stable selections under the scoped assumptions.

---

## Slide 35 — Backup: Timeline to Graduation

This is an administrative backup slide.

The dissertation prospectus, D3 form, defense presentation, assessment survey, and COS review are all part of the required process.

The only reason I would use this slide is if there is a procedural question about the remaining graduation steps or submission timeline.

For the scientific argument, the important conclusion has already been presented: the framework is complete, evaluated, scoped, and tied to a reproducible implementation pathway.
