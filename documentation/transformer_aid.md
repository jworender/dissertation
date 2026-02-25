# Transformer Attention Warm-Start via Critical-Range Rectification

## Executive assessment
Based on the prospectus method (critical-range rectification -> sparse selection -> logic compression), using the rectification stage to create a **precomputed attention prior** for transformers is technically credible and worth pursuing as a post-doc direction.

The strongest version of the idea is **not** to hard-replace transformer learning with a fixed map, but to inject a rectification-derived prior as an additive bias at initialization and early training. That keeps the base transformer pipeline intact while giving optimization a better starting geometry.

## Why this is aligned with the current theory
Current RQ2 framing argues that binarization/rectification can contract harmful dependence and improve support behavior under multicollinearity. Translating that intuition to transformers:

1. A rectified representation can suppress noisy amplitude coupling and highlight threshold-trigger structure.
2. A prior built from that representation can bias attention toward plausible feature-lag interactions early.
3. The model can then refine away from the prior during training if data disagree.

This is conceptually similar to improving the initial search region of the optimizer without changing the downstream architecture.

## Recommended attachment point (minimal pipeline change)
Use a **Rectified Attention Prior (RAP)** as an additive attention-logit bias:

$$
\text{Attn}(Q,K,V)=\text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}} + \alpha B_{\text{rap}} + M\right)V
$$

- $ B_{\text{rap}} $: precomputed prior matrix (global or per-head)
- $ \alpha $: scalar gate (fixed small value, learnable, or annealed)
- $ M $: standard mask (causal/padding)

This is a one-step initialization add-on and does not require redesigning transformer blocks.

## How to build $ B_{\text{rap}} $ from your method
Use only the training split for each fold/run.

1. Estimate critical ranges per feature (your current rectification method).
2. Convert lag-expanded signals to $ \{-1,+1\} $ indicators.
3. Compute a dependency score matrix between tokens (or feature-lag tokens), for example:
   - signed co-activation difference between event and non-event windows, or
   - correlation/MI on rectified indicators, optionally class-conditional.
4. Regularize the prior:
   - clip/normalize to bounded range,
   - sparsify weak edges,
   - optionally force banded structure for lag locality.
5. Map to model shape:
   - temporal tokens: $ T \times T $ (or relative lag bias),
   - feature-lag tokens: $ P \times P $,
   - multi-head: same prior for all heads or specialized priors per head family.

## Two implementation modes
### Mode A (recommended first): Additive bias only
- Keep standard random init for $ W_Q, W_K, W_V $.
- Add $ B_{\text{rap}} $ with small $ \alpha $ at start.
- Optionally decay $ \alpha $ over epochs.

Pros: safest, stable, minimal code risk.

### Mode B (aggressive): Q/K warm-start from prior factorization
- Low-rank factorize $ B_{\text{rap}} \approx U_r \Sigma_r V_r^\top $.
- Initialize part of $ W_Q, W_K $ from factors so expected $ QK^\top $ reflects prior structure.

Pros: stronger non-random start.  
Cons: higher risk of brittle optimization and overconstraint.

## Transformational option: full-cycle seeded attention from polished outputs
This is a stronger variant: use the **entire** pipeline to build the prior, then let the transformer adapt if that prior is incomplete.

1. Run the full cycle on training data only:
   - critical-range rectification,
   - sparse fitting,
   - anytime polishing to produce a compact rule set $ R $.
2. Convert $ R $ into an attention prior matrix $ B_R $ over feature-lag or token pairs.
3. Train with:
$$
\text{Attn}(Q,K,V)=\text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}} + \alpha B_R + M\right)V
$$
4. Make escape paths explicit:
   - learnable or annealed $ \alpha $,
   - only bias a subset of heads,
   - keep unbiased heads fully free.

Why this can be transformational:
1. It narrows early search toward a compact, already-polished hypothesis set.
2. It links interpretable rule structure to deep model optimization directly.
3. It preserves neural flexibility because the prior is soft, not hard-masked.

Technical note on the threshold point: neural networks are not literal hard-threshold systems during gradient training, but they do learn nonlinear decision surfaces and gating-like behavior. That makes threshold-informed priors plausible, especially in event-triggered longitudinal domains.

## Where this is most likely to help
1. Event-driven longitudinal datasets with real threshold-and-lag mechanisms (your core regime).
2. Medium-data settings where random initialization variance is high.
3. High-collinearity multivariate time series where early training often chases spurious correlations.
4. Tasks where interpretability of attention patterns is valuable to domain experts.

## Where it may fail or underperform
1. Tasks without threshold-trigger structure (prior injects wrong bias).
2. Very large-scale pretraining where learned representations dominate initialization quickly.
3. Highly nonstationary environments (static prior becomes stale).
4. Cases where attention patterns are highly context-specific per sample, not global.

## Competing methods and RAP tradeoffs
Several existing approaches can provide a similar "better-than-random" start or efficiency gain for transformers.

| Competing approach | What it targets | RAP advantages | RAP disadvantages | Expected computational complexity vs proposed RAP |
| --- | --- | --- | --- | --- |
| Raw correlation / MI attention bias (from continuous inputs) | Precomputed statistical prior for attention | Better aligned with threshold-and-lag event logic; less driven by raw amplitude outliers | Can discard useful magnitude information that raw priors retain | Similar or slightly lower (skips rectification/rule-generation steps) |
| Learned positional bias (relative bias, ALiBi/RoPE-style temporal inductive bias) | Improves temporal/lag handling inside attention | Encodes data-specific feature-lag event structure, not just distance | Less flexible than fully learned bias when lag structure is complex or non-thresholded | Lower (small parameter/compute overhead, no offline prior construction) |
| Graph-constrained attention (adjacency masks or graph priors) | Injects domain topology/causal structure | Data-derived from observed event behavior; no manual graph specification required | Weaker when a high-quality expert graph exists; may encode spurious data artifacts | Similar for fixed masks; higher if graph structure is learned or updated online |
| Sparse/local attention variants (Longformer-style windows, linear attention) | Compute/memory efficiency at long sequence length | Keeps full attention expressivity while improving optimization starting point | Does not solve quadratic attention cost by itself | Lower for long sequences (better asymptotic attention cost than full-attention RAP) |
| Large-scale self-supervised pretraining then finetune | Strong non-random initialization and representation reuse | Lower setup cost; highly targeted to your exact event regime and attribution goals | Usually lower ceiling than very large pretrained models with broad transfer signal | Much higher end-to-end (dominant pretraining cost, then finetuning) |

Practical interpretation: RAP is strongest when you need a **targeted inductive bias for threshold-mediated longitudinal events** with minimal architectural change. It is weaker as a universal replacement for long-context efficiency methods or foundation-model pretraining.

## Main risks and mitigations
1. **Leakage risk**: prior accidentally uses validation/test labels.
   - Mitigation: strict train-only prior computation per split, with audit logs.
2. **Over-biasing early training**: model stuck near handcrafted structure.
   - Mitigation: small $ \alpha $, annealing schedule, per-head learnable gate with regularization.
3. **Head collapse / reduced diversity**:
   - Mitigation: apply prior to subset of heads only; leave others fully free.
4. **Quadratic memory for long sequences**:
   - Mitigation: relative-lag prior (vector over $ \Delta t $) or low-rank/banded approximation.
5. **False confidence from faster convergence**:
   - Mitigation: compare final generalization, calibration, and stability, not only speed.

## Proposed post-doc experiment program
### Phase 1: Feasibility
- Baselines:
  - vanilla transformer (random init),
  - transformer + raw-correlation bias,
  - transformer + RAP bias (rectification-only prior),
  - transformer + full-cycle seeded bias (polished-rule prior).
- Endpoints:
  - steps/time to reach fixed validation target,
  - final AUC/F1/Youden's $ J $,
  - seed variance.

### Phase 2: Ablation and mechanism checks
- $ \alpha $: fixed vs learnable vs annealed.
- Prior source: class-conditional vs unconditional.
- Prior granularity: global vs per-head.
- Sparsity level of $ B_{\text{rap}} $.
- Prior generator: rectification-only vs full-cycle polished rules.

### Phase 3: Robustness and transfer
- Domain shift splits.
- Negative-correlation stress settings.
- Non-threshold datasets as falsification controls.

## Go/no-go criteria
Treat this as promising if RAP shows, across multiple seeds/datasets:
1. Meaningful efficiency gain (for example 10-20% less wall-clock to target metric),
2. No material degradation in final discrimination/calibration,
3. Improved training stability (lower seed variance),
4. Interpretable attention patterns aligned with known lag logic.

If gains appear only on one dataset or vanish under leakage-safe splits, do not scale the direction.

## Bottom line
Your intuition is sound: this can give transformers a more informative start than purely random attention structure, while preserving the standard pipeline. A pragmatic strategy is two-track: start with the easier rectification-only prior for quick validation, then push the full-cycle seeded prior as the potentially most transformational direction.
