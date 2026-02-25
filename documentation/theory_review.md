# Theory Review: `Chapters/06_concordia.tex` and `Chapters/98_appendices.tex`

## Scope and comparison basis
This review checks theoretical correctness, internal consistency, and consistency with prior work, especially:

- `references/JOrender2025Efficient.pdf` (via extracted text snapshot: `references/_JOrender2025Efficient_extracted.txt`)
- `references/JOrender2025Efficient.md`

## Findings (ordered by severity)

1. **High - sign error in Lemma 3 negative-correlation bound**
File reference: `Chapters/98_appendices.tex:362`
The line states
`1/4 <= arcsin(rho_ij)/(2pi) <= 0` for `rho_ij <= 0`.
This is incorrect in sign; it should be `-1/4 <= ... <= 0`.
This is a mathematical error (the left bound cannot be positive while the right bound is non-positive).
Suggested fix: replace `\frac{1}{4}` with `-\frac{1}{4}` at `Chapters/98_appendices.tex:362`.

2. **High - monotonicity domain mismatch in Lemma 4 derivation**
File reference: `Chapters/98_appendices.tex:517`
The appendix states `f(x)` is increasing on `(-1, 1)`, while the same section acknowledges a discontinuity at `-1/(s-1)` (`Chapters/98_appendices.tex:520`).
Prior paper defines the domain as `(-1/(s-1), 1)` for this monotonicity argument (`references/_JOrender2025Efficient_extracted.txt:516`-`references/_JOrender2025Efficient_extracted.txt:519`).
Suggested fix: change the monotonicity interval to the domain excluding the pole and align text with the discontinuity caveat.

3. **Medium - theorem strength in Chapter 06 is stricter than prior work**
File reference: `Chapters/06_concordia.tex:111`
Chapter 06 states a strict probability inequality:
`P(Theta(X)<1) < P(Theta(X_tilde)<1)`.
Prior work states a weak inequality (`>=`) and explicitly says strict ordering is only in stylized equicorrelation settings:
`references/_JOrender2025Efficient_extracted.txt:536`-`references/_JOrender2025Efficient_extracted.txt:548`.
Suggested fix: use weak inequality in the main theorem statement, and reserve strict improvement language for explicitly stated stylized regimes.

4. **Medium - arcsin mapping presented as approximate where PoC result is exact**
File references: `Chapters/06_concordia.tex:74`, `Chapters/98_appendices.tex:63`
Both sections use `\approx` for the zero-threshold jointly normal arcsin relation.
Prior work states this mapping as exact in the PoC setup (`references/_JOrender2025Efficient_extracted.txt:409`-`references/_JOrender2025Efficient_extracted.txt:411`).
Suggested fix: use `=` in PoC lemma statements and reserve approximation wording for nonzero-threshold or non-Gaussian extensions.

5. **Medium - representation mismatch (+/-1 vs 0/1) is under-explained across chapter and appendix**
File references: `Chapters/06_concordia.tex:35`-`Chapters/06_concordia.tex:38`, `Chapters/98_appendices.tex:84`-`Chapters/98_appendices.tex:92`, `Chapters/98_appendices.tex:281`-`Chapters/98_appendices.tex:284`
Chapter 06 defines sign binarization as `{-1,+1}`, while appendix proofs use `0/1` variables.
This can be correct (affine equivalent after centering), and prior work explicitly notes this equivalence (`references/_JOrender2025Efficient_extracted.txt:406`-`references/_JOrender2025Efficient_extracted.txt:407`), but the dissertation text does not make that bridge explicit where needed.
Suggested fix: add one explicit sentence in Chapter 06 lemma pathway (or appendix intro) clarifying affine equivalence and its impact on covariance/correlation constants.

6. **Low - over-strong narrative language exceeds stated caveats**
File reference: `Chapters/98_appendices.tex:568`
The phrase "unequivocally enhances positive correlation relationships" is stronger than prior caveat language, which is careful about weak improvement and negative-correlation discontinuity (`references/_JOrender2025Efficient_extracted.txt:539`-`references/_JOrender2025Efficient_extracted.txt:560`).
Suggested fix: soften to regime-scoped wording (for example, "in the positive-correlation PoC regime").

## Areas where theory is intentionally limited (PoC scope)

These are not defects; they are expected scope limits and should remain explicit:

1. Zero-threshold, jointly normal assumptions for closed-form arcsin contraction.
References: `Chapters/06_concordia.tex:43`-`Chapters/06_concordia.tex:50`, `references/_JOrender2025Efficient_extracted.txt:399`-`references/_JOrender2025Efficient_extracted.txt:403`.

2. Large-`n` population-covariance replacement in the main theorem chain.
References: `Chapters/06_concordia.tex:127`, `references/_JOrender2025Efficient_extracted.txt:535`.

3. Negative-correlation edge cases near `-1/(s-1)` and non-monotonic behavior outside safe intervals.
References: `Chapters/98_appendices.tex:520`, `references/_JOrender2025Efficient_extracted.txt:556`-`references/_JOrender2025Efficient_extracted.txt:560`.

4. Nonzero critical-range thresholds used in practice do not yet have a closed-form theory in this chapter.
References: `Chapters/06_concordia.tex:174`-`Chapters/06_concordia.tex:177`, `references/_JOrender2025Efficient_extracted.txt:722`-`references/_JOrender2025Efficient_extracted.txt:726`.

## Validity of Assumptions in `Chapters/06_concordia.tex`

Assumptions reviewed from `Chapters/06_concordia.tex:43`-`Chapters/06_concordia.tex:48`:

1. **Joint normality after standardization**
Assessment: Reasonable as a PoC analytical device, but generally not realistic for many longitudinal sensing datasets (heavy tails, bounded sensors, mixed regimes). Valid for tractability, weak for external validity.

2. **Fixed support set `S` in local analysis**
Assessment: Standard and acceptable for IC-theory exposition. It is theoretically coherent, but practical support uncertainty should be acknowledged when translating to finite-sample model selection outcomes.

3. **Large-sample covariance approximations**
Assessment: Valid asymptotically and aligned with prior work. In finite samples (especially high `d/n`), this can materially overstate stability; practical claims should remain probabilistic and weak-form.

4. **Comparative objective (raw vs transformed IC-satisfaction probability)**
Assessment: Valid and well-posed for PoC theory. It correctly frames the contribution as a relative mechanism claim rather than a universal optimality claim.

5. **Zero-threshold meaningfulness**
Assessment: Domain-dependent and potentially fragile. It is valid for sign-theory derivation and threshold-triggered phenomena, but not generally guaranteed for all domains or all features.

Overall assumption validity judgment: **acceptable for a proof-of-concept theorem**, provided claims remain scoped to the PoC regime and do not imply general nonzero-threshold guarantees.

Recommended strengthening edits (optional):
1. Add one sentence that joint normality and threshold meaningfulness are modeling assumptions, not empirically verified prerequisites.
2. Add one sentence that finite-sample/high-dimensional settings may violate population-approximation behavior.
3. Keep theorem wording in weak-probability form unless an explicit stylized regime is invoked.

## Overall assessment

The chapter and appendix are directionally consistent with the prior paper's PoC theory chain (correlation contraction -> inverse-Gram control -> IC-bound tightening), but there are two correctness-level math issues in the appendix and a theorem-strength mismatch in Chapter 06 that should be corrected to maintain rigorous alignment with prior work.

## Notes

1. Any arbitrary threshold could be remapped to a zero threshold, and if those mapping parameters are retained, the results could be remapped to the original domain at the conclusion of the analysis.  This applies to single-threshold problems only.
2. In many fitted features, one bound collapses to an observed extreme (near min or max), so the active rule behaves like a one-sided cutoff in practice.