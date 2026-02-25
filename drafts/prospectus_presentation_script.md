# Prospectus Presentation Script (Rev B)

Total planned runtime: **45:00** (slide timings below sum exactly to 45 minutes).
Audience: Dissertation committee (prospectus defense).

## Slide 1: Title
**Estimated time:** 0:52  
**Script:**  
Good afternoon, and thank you for being here. My prospectus is titled *Interpretable Sparse Modeling of Longitudinal Signals via Critical-Range Rectification and Anytime Rule Compression*. The central problem is that longitudinal, lag-expanded data are highly correlated, which makes sparse support selection unstable, while  many operational use cases still require transparent, auditable logic. My core claim is that a three-stage pipeline, rectification, sparse fitting, and anytime compression, can improve attribution reliability and produce compact rules without unacceptable loss in performance.

My committee chairmain is Dr. Sun, and additional members Dr. Zubair, Dr. Li, and Dr. Nguyen.

**Committee Q&A notes:**  
- If asked for a one-sentence thesis: rectification improves sparse recovery geometry in target regimes, and anytime compression makes results operationally interpretable.  
- If asked what is new vs prior papers: this dissertation integrates RQ1 empirical evidence, RQ2 mechanism, and RQ3 deployable compression in one scoped framework.

## Slide 2: Overview
**Estimated time:** 0:43  
**Script:**  
This talk has three sections. First, I will define the problem and knowledge gap. Secondly, I walk through the three research questions. Research question number 1 asks if critical-range binarization yields stable sparse baselines with reliable feature and lag attribution. Research question number 2 asks why that works and how far the mechanism may generalize beyond proof-of-concept assumptions. Research question number 3 asks whether we can compress sparse solutions into compact logical rules. Thirdly, I summarize contributions, future work, and my timeline to graduation.

**Committee Q&A notes:**  
- If asked why this sequencing: empirical behavior first, then theory, then deployment usability.  
- If asked expected committee feedback points: baseline choice, strongest real-world case study, and appropriate scope for RQ2 generalization.

## Slide 3: Section Divider - Background
**Estimated time:** 0:13  
**Script:**  
This section frames the core problem and the specific knowledge gap the dissertation addresses.

**Committee Q&A notes:**  
- If asked why keep this short: I am using section dividers only to orient the flow and preserve time for evidence.

## Slide 4: Core Problem
**Estimated time:** 1:02(a) +  0:48(b)
**Script:**  
Longitudinal modeling has two linked tensions. First, lag expansion increases dimensionality and consequently induces strong dependence, so sparse methods can swap among correlated lag terms and become unstable for support recovery by including elements from spurious correlations due to non-relevant variables. Secondly, many stakeholders ultimately need rules, not hundreds of coefficients. Think, clinical and financial sectors for good examples of high stakes arenas where the reasoning is as important as the answer. Additionally, in domains like ICS monitoring, clinical trajectories, and industrial controls, outcomes are often threshold-and-lag mediated. That structure is meaningful, but standard raw-feature sparse fitting often does not represent it in a way that is naturally auditable.

**Committee Q&A notes:**  
- If asked to separate prediction from attribution: prediction can remain good while support recovery is unstable under multicollinearity.  
- If asked why lag attribution matters: intervention and policy decisions often depend on when a variable becomes relevant, not only whether it is relevant.

## Slide 5: Knowledge Gap
**Estimated time:** 0:44  
**Script:**  
Next, we'll talk about the knowledge gap. The gap is not that sparse methods do not exist. The gap is that existing methods often satisfy only part of the requirement set. We need models that are accurate enough, sparse enough, interpretable enough, and efficient enough. Current alternatives usually trade one objective for another: either strong prediction with weak transparency, or transparent logic with heavy combinatorial search cost, or sparse models that remain unstable in strongly correlated lag spaces.

**Committee Q&A notes:**  
- If asked what "success" means: balanced performance across discrimination, attribution reliability, interpretability complexity, and compute cost.  
- If asked whether this is a universal gap: no, the gap is strongest in threshold-driven longitudinal settings with high lag correlation.

## Slide 6: Other Solutions
**Estimated time:** 1:14  
**Script:**  
That brings us to the other solutions in this space. This slide positions competing families in the context of the proposed method. Group and structured sparsity improve stability but still operate in raw, that is untransformed, covariance geometry. Rank-based and dependence-aware variants can help in specific regimes but do not directly yield threshold-native rule semantics. Wrapper methods are flexible but often heuristic and less transparent. Quadratic programming and direct logic learners are conceptually close but can be computationally expensive at scale and at best only provide indicators of relevant variables and lags, rather than encapsulating a candidate model. Deep learning is intentionally not the main comparator here because this dissertation targets inherently interpretable, auditable sparse models under constrained compute, all of which deep learning methods violate since they are universally black boxes with dense matrices that are very compute heavy by their very nature.

**Committee Q&A notes:**  
- If asked whether deep learning is excluded entirely: it is out of primary scope, but can be included as contextual baseline if the committee requests.  
- If asked closest comparator: Katrutsa-Strijov style relevance-redundancy optimization is closest in spirit for RQ1 comparisons.

## Slide 7: Section Divider - Approach and Research Questions
**Estimated time:** 0:13  
**Script:**  
I will now move from motivation to the proposed end-to-end approach and the three research questions.

**Committee Q&A notes:**  
- If asked why three RQs instead of one: each addresses a distinct validity layer: utility, mechanism, and usability.

## Slide 8: Proposed Solution (End-to-End)
**Estimated time:** 1:40  
**Script:**  
The proposed solution pipeline is conceptually simple: We will rectify the continuous data to produce a binarized matrix -> Fit Sparse Model on the rectified data -> and then Compress the ruleset. First, as I said, rectification will map continuous lagged features to event-relevant binary indicators, which will be stored in the matrix as a negative one or a positive one. Secondly, an L1-regularized logistic baseline identifies sparse support in that transformed space. Thirdly, anytime rule compression, or logic polishing, converts sparse coefficients into compact rule forms with explicit complexity-performance tradeoffs. The intervention point is the representation of the data itself first, not only penalty engineering as with a few of the other methods, and then a controlled post-fit compression stage for deployment.

**Committee Q&A notes:**  
- If asked why representation-first: it changes the statistical geometry before optimization, which can improve support behavior without changing solver internals.  
- If asked whether compression is required: not always; it is activated when operational interpretability demands simpler rule artifacts.

## Slide 9: Critical Range
**Estimated time:** 1:47  
**Script:**  
What we are calling a critical range is a condition where events have non-zero probability of occurring. This is how we will binarize the continuous input matrix. For each lagged feature, values inside the learned critical range become +1 and outside become -1, generating a binarized matrix with the same shape as the original design. The response remains binary event/non-event. We are distilling the relevant information into this binary indicator. In the implementation, and this is very important, ranges are learned on training folds only, then those ranges are applied to validation and test folds to avoid leakage. This gives an explicit threshold semantics, and that is easier to audit and while also supporting sparse learning in a dependence-reduced representation. In fact, the critical ranges themselves become a valuable training product since they potentially identify event triggers as real-world measurable values.

An example might be a radar return between x and y magnitude on a specific channel.  Instead of having to monitor all of the channels, submitting those values to a black box model, and then getting the result, you could monitor a specific channel for a specific result and even potentially encode an alarm into hardware.

**Committee Q&A notes:**  
- If asked about leakage control: critical ranges are fit only on training partitions, never on held-out data.  
- If asked about nonzero thresholds vs sign threshold theory: practice uses learned ranges; current closed-form theory is proof-of-concept for a tractable zero-threshold regime.

## Slide 10: Measuring Success
**Estimated time:** 1:22  
**Script:**  
The question then becomes, how do we measure success? Evaluation is multi-objective. For discrimination, I use AUC and Youden's J, with J emphasized for operating-point relevance and class imbalance context. For interpretability, I track number of active features, rule count, and effective rule length. For efficiency, I include training and inference runtime, including transformation/compression overhead. The dissertation does not optimize one metric in isolation; it evaluates whether the full pipeline is a practical balance of reliability, transparency, and compute cost.

The plots to the right are intended to show the kind of evaluation metrics that I am using.  The left side shows a classic Receiver Operator Characteristic, or ROC, on top, as well as the number of rules in the final polished model. On the right hand side, we show the difference between the model generated from the raw untransformed data, using one of the synthetic data sets, to the output of the model generated by the transformed binarized data.

**Committee Q&A notes:**  
- If asked why J in addition to AUC: J reflects thresholded operational behavior, which matters for deployment decisions.  
- If asked how "no material loss" is defined: by predeclared tolerance policy and equivalence framing where appropriate.

## Slide 11: Research Questions
**Estimated time:** 1:16  
**Script:**  
Now we'll spend some time talking about the research questions that are intended to fill the knowledge gap.  

Research Question number one: can critical-range binarization produce a stable sparse baseline with reliable **feature and lag attribution**?  

Researrch Question number two: why does binarization work when it works, and how far can that mechanism be generalized?  

Research Question number three: can we compress the resulting sparse solution into compact logical rules without unacceptable operational loss?  

These research questions are intentionally linked. If research question number one fails, there is little value in downstream compression. If research question number one succeeds but research question number two is weak, claims are not scientifically durable. If research question number one and two hold but research question number three fails, deployment value remains limited.

The photo to the right is illustrative of the type of physical phenomena that might be modeled as a threshold-based phenomena.  It shows a newly commissioned warship from the Korean War which cracked in half when conditions were right for brittile fracture.

**Committee Q&A notes:**  
- If asked whether RQs are independent: no, they are staged dependencies by design.  
- If asked where limitations are handled: explicitly in RQ2 scope language and in cross-dataset RQ1/RQ3 evaluations.

## Slide 12: Section Divider - RQ1
**Estimated time:** 0:18  
**Script:**  
I will now present preliminary evidence for research question number one from synthetic and real-world studies. As you may recall, the research question is "can critical-range binarization produce a stable sparse baseline with reliable **feature and lag attribution**?"

**Committee Q&A notes:**  
- If asked what "preliminary" means: evidence is strong enough for directionality, but final defense work adds broader baselines and stability-first protocols.

## Slide 13: RQ1 Rectification Step
**Estimated time:** 1:05  
**Script:**  
The research question number one workflow begins by flattening longitudinal data into lagged design matrices. This creates the known multicollinearity problem that we already discussed. Next, critical ranges are estimated from event-aligned observations and mapped to binary indicators. Sparse fitting is then performed on the transformed matrix. This explicitly separates representation design from optimization design. The question is whether this representation shift improves support concentration and lag localization compared with fitting directly on untransformed lag-expanded inputs.

The algorithm to the right shows formally how this binarization task can be accomplished.  There is the possibility that the simple min/max procedure here can induce brittileness if there are outliers in the data, but by using a quantile rule this can be potentially remedied.

**Committee Q&A notes:**  
- If asked whether flattening loses temporal structure: temporal order is preserved through lag indexing; what changes is encoding.  
- If asked whether ranges are feature-specific: yes, range determination is per feature-lag channel under the training protocol.

## Slide 14: RQ1 Synthetic Data
**Estimated time:** 1:29  
**Script:**  
I started out with synthetic data because it provides known ground truth for feature-lag relevance. Under this controlled setup, rectification plus LASSO strongly improved both attribution clarity and metrics: Youden's J improved from 0.753 to 0.975, for instance, and F1 from 0.804 to 0.988, and relative runtime is almost half the time. Similar transformed-vs-untransformed gains appear for other methods in this table. The main point is not only better scores; it is closer alignment of nonzero coefficient support with true causal lag structure.

The blue bars on the figure to the left show the coefficients for the model based on the untransformed data on top, with the true support shown by the multicolored bars. What we can see is that even though the true support is not shown by the coefficients in the model, it can still perform relatively well by using relationships that are nearly there in adjacent time steps and enlisting spurious relationships for non-relevant variables.  However, when we binarize the data, the plot on the bottom shows how the coefficients can snap to the correct support and ignore the other spurious relationships.

**Committee Q&A notes:**  
- If asked whether synthetic design is favorable by construction: yes, it is threshold-and-lag aligned by design, and that is precisely the target regime claim.  
- If asked what remains uncertain: transferability to regimes with weaker threshold structure, addressed via expanded real-data validation.

## Slide 15: RQ1 Quadratic Programming Comparison
**Estimated time:** 1:19  
**Script:**  
I compared against the Katrutsa-Strijov relevance-redundancy quadratic programming selector as a close conceptual baseline. It often identifies related variables but misses precise lag localization and is substantially slower in these tests, typically about 100 to 200 times slower than rectification plus LASSO combined. It also outputs importance scores rather than a full predictive model, so AUC plus Youden's-J comparisons are less direct. For this work, practical repeatability across folds and ablations makes runtime and accurate identification of true lags the primary criteria for comparison.

From the figure you can see that in many cases the true support is almost identified, but in all but one case, the lag identified is several time steps off. Consistently with the previous figures, the blue bars in this figure show the feature importance values where before we were using coefficient values for that purpose, and the multicolored bars show the ground truth support. I actually used their published R-code to generate these results for comparison.

**Committee Q&A notes:**  
- If asked whether implementation differences explain runtime gaps: I will provide reproducibility artifacts and config details for a fair comparison package. 
- The original code that I used for these comparisons was written in R-code as well, so this is an apples-to-apples comparison.
- If asked why keep this comparator despite output mismatch: it tests redundancy-aware selection in a methodologically relevant way.

## Slide 16: RQ1 Real-World Data
**Estimated time:** 1:36  
**Script:**  
On the Hardware-in-Loop-based Augmented Industrial Controls Systems data set, also known has the HAI ICS security dataset, transformed models outperformed untransformed models across accuracy, AUC, F1, and Youden's-J, and coefficient concentration also aligns with turbine-related channels, which represents ground truth support, and this in turn improves interpretability and domain plausibility. 

Conversely, on UNICEF data, untransformed models show stronger raw discrimination, while transformed models are far simpler in active feature categories. This cross-dataset pattern supports a conditional claim: rectification is strongest in threshold-and-lag aligned regimes, while other regimes can present a discrimination-interpretability tradeoff.

I show the UNICEF data to acknowledge that this method does not improve all regimes, but even in areas where it does not necessarily produce the best overall model, it can still produce simple rules that potentially capture almost all of the variation in the data. 

The plot to the left shows the modeling results for transformed vs. untransformed data in the HAI ICS dataset.  Notice that for the transformed data, the coefficients are all clustered on the turbine instrument readings, which tracks with the ground truth that the casualty being recorded is originating in the turbine component.

**Committee Q&A notes:**  
- If asked why keep UNICEF if raw wins there: it demonstrates boundary conditions and prevents overclaiming.  
- If asked what "better interpretability" means quantitatively: fewer active categories and cleaner lag support concentration.

## Slide 17: RQ1 Takeaway
**Estimated time:** 1:35  
**Script:**  
So, what do we take away from this discussion? The interim answer for research question number one is yes, conditionally. When we reframe the problem into boolean logic, rectification tends to improve support concentration, lag attribution reliability, and often runtime in the target regime. In the experiments I've already showed you today, transformed fitting leveraging the LASSO algorithm is nearly twice as fast even including transformation overhead, and the transformation itself is linear-time and parallelizable. We have reframed continuous signals into explicit logic-like indicators, which produces sparse coefficients ultimately to to human-auditable logical hypotheses. 

Remaining open questions become the focus of research question number two: mechanism, generalization, and failure modes.

So next, when we talk about why this works and whether it may generalize, remember that already saw with the UNICEF data that there may be limitations in the form of tradeoffs when we deviate from the main regime that we are modeling while acknowleging that even when the final answer does not necessarily provide the same fidelity as the raw data that the answer itself may be far more useful.

**Committee Q&A notes:**  
- If asked whether this is just feature engineering: it is feature engineering with a theoretical recovery lens and explicit downstream interpretability target.  
- If asked what could fail: non-threshold-mediated regimes or adverse dependence structures may reduce gains.

## Slide 18: Section Divider - RQ2
**Estimated time:** 0:25  
**Script:**  
Next I address research question number two, in which we will lay the theoretical foundation for why binarization helps and what can be claimed rigorously.

**Committee Q&A notes:**  
- If asked expected rigor level: proof-of-concept theorem with explicit assumptions and boundaries, not universal guarantees.

## Slide 19: RQ2 Irrepresentable Condition (IC)
**Estimated time:** 2:04  
**Script:**  
The irrepresentable condition or IC, as studied by Zhao and Yu in 2006, is the support-recovery lens that we will use to frame the problem. Through this lens, inactive features should not be too well represented by active features after accounting for active-block geometry. 

The inequality shown formalizes this concept by limiting the product shown to less than one.  In this context, "X" is the feature matrix, the subset of the relevant features is denoted by "S", and the non-relevant features are denoted by S superscript c, with the "c" indicating the complement.  Beta in this context is the coefficient vector.  The central term is the inverse gram matrix of the relevant features, and we will exploit certain properties in the proof sketch that follows. For the full proof and the detail for each lemma, look in the appendices for the prospectus document that I sent out previously.

In computer science terms, this is an interference bound on worst-case leakage between relevant and non-relevant features. High collinearity in lag-expanded designs often violates this condition and yields unstable support. The research question number two objective is to show, under tractable assumptions, that binarization increases the probability of satisfying irrepresentable-condition-related bounds, linking observed  behavior that we noted in the discussion for research question number one to a mechanistic explanation.

It should be emphasized that what I am presenting is a tractable proof-of-concept meant to prove the mechanism by which binarization achieves a higher probability of meeting the irrepresentable condition under simplifying assumptions.

**Committee Q&A notes:**  
- If asked why IC instead of another condition: IC directly connects to LASSO support recovery consistency literature.  
- If asked about practical relevance: even when exact consistency assumptions fail, IC-oriented analysis predicts where false inclusions become likely.

## Slide 20: RQ2 Arcsin Relation
**Estimated time:** 2:02  
**Script:**  
Now we will discuss one of the major elements of the proof.

Under standardized joint normal distribution assumptions and zero-threshold sign binarization, transformed correlation follows the closed-form mapping $ \tilde{\rho} = (2/\pi) arcsin(\rho) $. This contracts correlation magnitude through most of the interior while preserving sign and endpoints. Intuitively, sign mapping keeps direction information and discards amplitude, which can reduce linear coupling that drives support ambiguity. This is the proof-of-concept scope to which I was referring: it is analytically tractable and explanatory, but it does not necessarily constitute the final claim for arbitrary nonzero thresholds.  However, it does provide a reasonable mechanism.

The tilde will be used to distinguish the parameters calculated on binarized data from the continuous counterparts.  So rho-tilde in this case is the pearson correlation coefficient for the binarized feature matrix, whereas rho will be the pearson correlation coefficient for the original continuous matrix.

What this shows, is that under these conditions and assumptions is that all pairwise correlations must be less than or equal to the original but never greater.  In fact, because the arcsin relation is strictly convex on the interval from 0 to 1 and strictly concave on the interval from negative one to zero, equality only occurs at negative one, zero, and one.

**Committee Q&A notes:**  
- If asked whether the arcsin relation is exact here: yes, in the zero-threshold jointly normal setup.  
- If asked about non-Gaussian or nonzero-threshold cases: those are explicit extension targets in future-work workstream B.

## Slide 21: RQ2 Gram Matrix Bounds
**Estimated time:** 1:35
**Script:**  
The second part of the mechanism is active-block conditioning. In an equicorrelated tractable case, we can write Gram and inverse Gram forms explicitly, using standard matrix identities. Under these stated conditions, binarization yields a smaller infinity norm for the inverse active block, reducing amplification during de-mixing. Combined with pairwise contraction, this shrinks the irrepresentable condition interference term. I frame this as a regime-scoped bound, especially strongest in the positive-correlation settings used in the proof.

In this representation, G is the gram matrix, n is the number of examples, I is the identity matrix, and J is a matrix of ones.  S indicates the shape of the relevant feature matrix, and $ \rho $ is again the pearson correlation coefficient.

We can show that when zero is less than the original pearson correlation coefficient, which is less than the binarized data pearson correlation coefficient, which is less than one, the infinity norm of the binarized gram matrix should be less than or equal to the infinity norm of the gram matrix of the original continuous feature matrix.

This is the center term of the irrepresentable condition.

**Committee Q&A notes:**  
- If asked whether this holds for all covariance geometries: no, this is a scoped tractable regime result.  
- If asked why infinity norm: IC is expressed in worst-case leakage terms, so infinity norm is the relevant induced norm.

## Slide 22: RQ2 Parsing the Results
**Estimated time:** 1:23
**Script:**  
This slide decomposes the interference expression term-by-term. The sign vector norm is fixed for nonzero coefficients, while inactive-active covariance magnitudes contract under binarization in the PoC setting. Using submultiplicative norm bounds, which allows us to break up the individual components of the irrepresentable condition, the transformed interference upper bound becomes tighter than the raw bound under the lemma assumptions. 

Practically speaking, that means fewer inactive features are likely to mimic the active span, which should translate to improved sparse support stability and clearer lag attribution.

For these purposes, I am defining a theta sub-J term which is a scalar representation of the result of individual relevant feature vector multiplication within the irrepresentable condition. Hang on to this definition for the next slide.

**Committee Q&A notes:**  
- If asked if this proves strict dominance: generally no; the main claim is weak probabilistic improvement, with strict gains in stylized regimes.  
- If asked where full derivations live: appendix proofs and theorem path in the RQ2 chapter.

## Slide 23: RQ2 Putting the Pieces Together
**Estimated time:** 1:42
**Script:**  
Putting the lemmas together, the theorem-level claim is probability-based: transformed designs are at least as likely to satisfy IC margin conditions as raw designs in the PoC regime. The interpretation is mechanistic, not a universal claim: correlation contraction, inverse-block control, and reduced off-support leakage show a mechanism which combines to improve support recoverability odds. This explains why research question number one gains appear where threshold-and-lag structure is aligned, while we also must preserve explicit caveats about scope and assumptions.

At the top, you see the definition for theta sub-J which we defined on the last slide.  We define the B-star terms based on this, in which we are selecting the specific value which will comprise the infinity norm result.

The final result shows a mechanism which explains why a binarized matrix has a greater probability of satisfying the irrepresentable condition than its continuous counterpart.

It helps pairwise contraction keep off-diagonals from saturating, it provides better conditioning of gram matrices which bounds inverse norms, and encourages smaller off-support covariances which further reduce the irrepresentable condition term.  Altogether, these raise the cance of true support recovery and promotes sparse and stable selections.

**Committee Q&A notes:**  
- If asked for the exact claim strength: mechanistic bridge with scoped assumptions, not a universal theorem over all thresholding schemes.  
- If asked how this informs experiments: it predicts where gains should appear and where failure modes should cluster.

## Slide 24: Section Divider - RQ3
**Estimated time:** 0:12  
**Script:**  
I now move to research question number three: converting sparse rectified models into compact, deployable logical rules.

**Committee Q&A notes:**  
- If asked why this is separate from RQ1: sparsity alone is not equivalent to operational interpretability.

## Slide 25: RQ3 Rule Compression (Logic Polishing)
**Estimated time:** 1:30  
**Script:**  
The L1-logistic method provides both sparsity and computational simplicity, but small residual coefficients can obscure clear logic. Logic polishing maps active coefficients to a shared magnitude or zero while preserving sign, then builds ordered top-k prefixes. Each prefix yields a candidate m-of-k rule. This creates a structured path from model-centric coefficients to human-auditable decision logic. The key is policy control: we can choose simpler rules when performance stays within a declared tolerance of baseline behavior.

To the right, we see three plots stacked on top of one another which show the value which each step in the process provides.  The top plot shows the result just from the raw data, the middle plot shows the result after rectification, a great improvement, and then the bottom plot shows the result of the final step, in which we eliminate the coefficients which are not contributing to the final result.

**Committee Q&A notes:**  
- If asked whether K choice is arbitrary: sensitivity to K is part of planned validation; current evidence suggests robustness once K is sufficiently above noise scale.  
- If asked what rule family this resembles: compressed signed-vote m-of-k logic derived from sparse convex front-end fits.

## Slide 26: RQ3 Results
**Estimated time:** 1:52  
**Script:**  
Finally, results are presented as anytime tradeoff curves, typically J versus retained rule size k. As k grows, we get a controlled quality frontier and can stop at the first rule meeting the policy that we have predefined. Statistical framing is equivalence-first: practical non-loss is assessed with predefined margins, such as two-one-sided-tests-style 90 percent confidence interval within plus or minus 0.01 AUC, while pairwise p-values are also measured. Prior results show large complexity reductions, including near 50x fewer non-zero coefficients in some settings, with very little little practical degradation.

The plot to the right shows how Youden's-J varies with the number of logical rules.  The value collapses to zero after the maximum because the algorithm quits after the preselected Youden's J-value target is reached.

Below, we see that the paired t-test AUC P-value comparison indicates that the results of the binarized, rule-based, and raw values are essentially the same on the dataset shown while retaining much more explainability.  Note that I used the scikit-learn python package as a comparison against my own algorithm which takes advantage of the binarization to converge faster and seamlessly transition to the logic polishing stage.  This will be available with the python package that will be published with the dissertation and be the foundation of the repeatable results notebooks.

**Committee Q&A notes:**  
- If asked why equivalence framing matters: "not significantly different" is not evidence of practical non-loss.  
- If asked whether compression ever hurts: yes, over-compression can degrade; the anytime policy explicitly avoids adopting those points.

## Slide 27: Section Divider - Contributions
**Estimated time:** 0:07  
**Script:**  
I will now summarize integrated contributions and then discuss the completion plan.

**Committee Q&A notes:**  
- If asked for summary format: one slide for contributions, one for conclusions/positioning, then future work and timeline.

## Slide 28: Contributions
**Estimated time:** 1:53  
**Script:**  

I will now discuss contributions.

Contribution one: an end-to-end rectification-first sparse longitudinal pipeline.  

- Critical-range rectification yields more reliable feature/lag attribution in longitudinal, correlated settings (synthetic + real-world).
- In addition, it often improves interpretability and efficiency (fewer feature categories; faster fits).

Contribution two: a scoped theoretical bridge from binarization to IC-favorability mechanism.  

- Proof-of-concept shows binarization can increase the probability of satisfying IC under tractable assumptions.
- The key mechanism is correlation contraction plus improved conditioning yielding smaller off-support influence

Contribution three: anytime rule compression that operationalizes interpretability with policy-based adoption.  

- “Logic polishing” compresses sparse models into compact rule forms without materially degrading AUC / J (equivalence framing).
- Anytime behavior: stop once desired J reached (complexity-performance tradeoff).

Contribution four: a unified evaluation perspective balancing discrimination, attribution stability, complexity, and runtime.  

Across synthetic and real data, this package will support a conditional but coherent claim for threshold-and-lag aligned longitudinal problems.

**Committee Q&A notes:**  
- If asked what is most novel: integration and explicit linkage across utility, mechanism, and deployment usability.  
- If asked what is most risky: theoretical extension beyond PoC assumptions and cross-domain robustness under weaker threshold structure.

## Slide 29: Conclusions and Positioning
**Estimated time:** 1:55 
**Script:**  
Conclusions will be discussed by research question: 

Research question number one is conditionally positive, 

In threshold-and-lag aligned settings, critical-range rectification tends to improve support concentration, lag localization, and sparse-model usability under multicollinearity stress.

Research question number two is mechanistically positive but scoped, 

This work provides a proof-of-concept theoretical argument: in a tractable regime with zero-threshold sign binarization with explicit normality assumptions.
Dependence contraction can improve the likelihood of satisfying irrepresentable-condition-related sparse-recovery conditions.

And research question number three is operationally positive under tolerance policy. 

Sparse rectified models can often be compressed into substantially smaller rule representations while preserving practical discrimination quality under predefined tolerance policies.
This directly addresses deployment requirements in settings where explanation, auditability, and compact decision logic are non-negotiable.

Positioning relative to prior work is by intervention point. Compared to classic L1 or elastic net, this work modifies representation before sparse optimization. 

Compared to grouped or ordered penalties, it emphasizes threshold logic and lag-level interpretability. Compared to direct combinatorial rule learners, it demonstrates scalable sparse fitting then structured compression at a much lower computational cost.



**Committee Q&A notes:**  
- If asked whether this replaces prior methods: no, this is a bridge architecture with explicit scope, not a universal replacement claim.  
- If asked what "conditional" means in practice: strongest gains in threshold-mediated, lag-dependent regimes with multicollinearity pressure.

## Slide 30: Future Work (Prospectus Plan)
**Estimated time:** 1:06  
**Script:**  
The completion plan has three workstreams.  
Workstream A strengthens RQ1 with stability-first evaluation, broader correlated baselines, and cross-domain validation.  
Workstream B strengthens RQ2 by extending beyond zero-threshold PoC where justified, plus assumption stress tests and explicit failure modes.  
Workstream C validates RQ3 with real-data anytime curves, equivalence-style comparisons, and interpretability audits.  
Cross-cutting ablations isolate contribution of each stage. This slide also marks where committee feedback is most valuable: baseline priority, flagship real dataset, and desired depth of RQ2 generalization.

**Committee Q&A notes:**  
- If asked what is mandatory before defense: stability package, expanded baselines, RQ2 scope-accurate theorem narrative, RQ3 real-data anytime/equivalence evidence.  
- If asked what can be stretch goals: broader non-independence extensions and additional rule-learner comparator breadth.

## Slide 31: Timeline to Graduation
**Estimated time:** 0:46  
**Script:**  
This timeline maps deliverables to decision gates. Prospectus defense is today, February 23, 2026, and D3 submission target is March 6, 2026. Core technical milestones then run through spring and early summer, with full draft to committee by July 3, 2026, formal defense target July 17, 2026, and graduation target August 28, 2026. Administrative milestones, including graduation application and ProQuest deadlines, are aligned to avoid bottlenecks after technical completion.

**Committee Q&A notes:**  
- If asked where schedule risk is highest: expanded benchmarking and RQ2 stress-testing integration.  
- If asked mitigation plan: milestone gates with required outputs, reproducibility automation, and early committee check-ins on scope decisions.

## Slide 32: Thank You
**Estimated time:** 0:40  
**Script:**  
Thank you for your time and guidance. I welcome questions, especially on baseline prioritization, RQ2 scope boundaries, and what evidence would most increase your confidence before final defense.

**Committee Q&A notes:**  
- If discussion opens broadly: steer first to claim boundaries, then to concrete artifact and timeline commitments.

