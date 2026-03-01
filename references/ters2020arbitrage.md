# Estimating Unknown Arbitrage Costs: Evidence from a 3-Regime Threshold Vector Error Correction Model (Ters and Urban, 2018)

## Dissertation Alignment Context
The dissertation proposal uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Problem framing and motivation (Section 1):** The paper studies persistent non-zero basis between spot and derivative instruments, where market frictions make arbitrage costly and produce nonlinear adjustment.
2. **Literature gap (Section 1):** Prior threshold approaches either assume known cointegration or handle only two regimes; the paper targets the unresolved case of multiple thresholds with unknown cointegrating vector.
3. **Core model contribution (Section 2):** It develops a 3-regime TVECM (two thresholds) with unknown cointegration and an intercept term in the error-correction relation to capture persistent parity distortions.
4. **Economic regime interpretation (Section 2):** The middle regime is a no-arbitrage band (insufficient basis to cover costs), while upper/lower regimes represent profitable arbitrage on basis-weakening and basis-strengthening sides.
5. **Estimation strategy (Sections 2.1-2.2):** Parameters are estimated via maximum likelihood with sequential threshold search and dynamic grid evaluation to handle non-differentiable objective surfaces.
6. **Testing framework (Section 2.2):** Threshold significance is evaluated with sup-LM style procedures using fixed-regressor and residual bootstrap approaches for finite-sample inference.
7. **Simulation evidence for one-threshold case (Section 2.3.1):** The slope parameter and transaction-cost combination are estimated precisely, while individual threshold/intercept estimates can be noisy.
8. **Simulation evidence for two-threshold case (Sections 2.3.2 and 2.4):** Dynamic grid settings and fixing the first threshold-search slope in the second search improve robustness and computational efficiency.
9. **Empirical applications (Section 3):** Applications to S&P 500 spot-futures and palladium show significant threshold behavior and estimate two-sided transaction-cost bands consistent with nonlinear arbitrage dynamics.
10. **Main conclusion (Section 4):** Financial parity adjustment is often multi-threshold; estimating transaction-cost bands via regime-switching cointegrated dynamics is feasible even when key costs are not directly observable.

## Relevance to the Dissertation
Estimating Unknown Arbitrage Costs: Evidence from a 3-Regime Threshold Vector Error Correction Model (Ters and Urban, 2018) is relevant as domain evidence that financial-market dynamics can depend on multiple thresholds and regime-specific delayed adjustments.

## Elements from This Paper to Use in the Dissertation
1. Use this source to support the financial-markets motivation for multiple thresholds in Chapter 1.
2. Reuse the neutral-band versus arbitrage-regime framing when discussing threshold-dependent response dynamics.
3. Borrow the interpretation that transaction costs map to threshold bands around parity, not a single trigger point.
4. Cite the S&P 500 and palladium applications as concrete examples of multi-threshold behavior in real markets.

## Competitive Method Assessment
This paper does not present the dissertation's main competing algorithmic pipeline. It is most useful for domain grounding and for supporting the claim that financial responses can be governed by multiple threshold regimes.


## Dissertation Citation Traceability

- Chapter: `Introduction`; Section: `Chapter context (no explicit section)`; Line: `Chapters/01_introduction.tex:12`; Relevance: Cited to support the statement that financial-market reactions can follow multiple threshold effects with delayed responses.
