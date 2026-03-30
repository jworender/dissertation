# Event-Triggered Communication and H-Infinity Control Co-Design for Networked Control Systems (Peng and Yang, 2013)

## Dissertation Alignment Context
The dissertation proposal uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Paper
1. **Problem framing and motivation (Section 1):** The paper targets networked control systems where communication delay and packet loss create lagged and reliability-constrained closed-loop behavior.
2. **Gap in prior approaches (Section 1):** It argues that many existing event-triggered methods are two-step (controller then trigger) and seeks a unified co-design approach for control performance and communication efficiency.
3. **Core communication scheme (Section 2.1):** A periodic-sampling, event-triggered transmission rule is proposed, where sampled-state error thresholds determine whether data are sent at each sampling instant.
4. **Lag-aware system modeling (Section 2.2):** The closed-loop networked controller is modeled as a time-delay system, explicitly capturing communication-induced delays and zero-order-hold behavior.
5. **Performance objective (Section 2):** The design target is asymptotic stability with prescribed H-infinity disturbance attenuation under imperfect networked signal transfer.
6. **Stability theory without packet loss (Section 3.1):** A theorem based on a Lyapunov-Krasovskii functional provides matrix-inequality conditions guaranteeing stability/performance under bounded delay.
7. **Stability theory with packet loss (Section 3.2):** A second theorem extends guarantees to successive packet losses and provides bounds through maximum allowable communication-delay and packet-loss limits.
8. **Co-design algorithm (Section 3.4):** The paper presents a one-step algorithm to jointly compute triggering-condition parameters and controller gain, rather than tuning them separately.
9. **Numerical demonstrations (Section 4):** Two examples show reduced communication occupancy while preserving control performance, and quantify transmission-period improvements relative to comparator schemes.
10. **Main conclusion (Section 5):** Threshold-triggered communication combined with lag-aware controller co-design can maintain robust performance under delay/loss while significantly reducing network usage.

## Relevance to the Dissertation
Event-Triggered Communication and H-Infinity Control Co-Design for Networked Control Systems (Peng and Yang, 2013) is relevant as direct control-systems evidence for threshold-driven lagged behavior under real communication constraints.

## Elements from This Paper to Use in the Dissertation
1. Use this source to support the control-systems motivation sentence in Chapter 1.
2. Reuse the framing that delays and packet losses induce lagged responses that must be modeled directly.
3. Borrow terminology around event-triggered thresholds, maximum allowable delay bound, and packet-loss limits.
4. Cite the co-design perspective as a concrete example of threshold-driven engineering behavior under constrained networks.

## Competitive Method Assessment
This paper does not present the dissertation's main competing algorithmic pipeline. It is most useful as domain grounding that control applications often involve explicit threshold triggers plus lag effects.


## Dissertation Citation Traceability

- Chapter: `Introduction`; Section: `Chapter context (no explicit section)`; Line: `Chapters/01_introduction.tex:11`; Relevance: Cited to support the statement that control systems frequently exhibit threshold-driven lagged behavior in response to inputs and environmental conditions.
