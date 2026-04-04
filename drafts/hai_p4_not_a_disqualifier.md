# Why the Residual P4 Block Is Not a Disqualifier for P2 Attribution in HAI

## Short Answer
The remaining `P4` coefficients in the HAI `attack_p2` analysis do not automatically invalidate sparse attribution to `P2`. In HAI 1.0, `P4` is the hardware-in-the-loop simulator that explicitly couples the turbine process (`P2`) to the rest of the testbed. A `P2` attack is therefore expected to create some legitimate downstream signal in `P4`, especially in simulator steam-side variables such as `P4_ST_PT01`.

The more important question is not "are there any nonzero `P4` coefficients?" but rather "does the sparse model still concentrate most of its support on the expected `P2` block while assigning only secondary weight to a physically plausible downstream effect?" On the current tuned CUTLASS result, the answer appears to be yes.

## Why the Shin et al. Paper Matters
The HAI paper is explicit that the dataset is not just three isolated subsystems. It is an *augmented* ICS dataset in which the real boiler (`P1`), turbine (`P2`), and water-treatment (`P3`) systems are coupled through an HIL simulator (`P4`) to create richer inter-process dynamics; see [shin2020.md](C:/Users/jason/ODU/dissertation/references/shin2020.md#L8), [shin2020.md](C:/Users/jason/ODU/dissertation/references/shin2020.md#L9), and [shin2020.md](C:/Users/jason/ODU/dissertation/references/shin2020.md#L10).

Section 2 of the paper further explains the mechanism:

- `P4` is the HIL simulator, not an unrelated auxiliary block.
- The turbine process remains synchronous with the rotating speed of the thermal power generator model in the HIL simulator.
- The HIL simulator exists specifically to enhance correlation among the real processes at the signal level.

That design means a `P2` attack can legitimately manifest in `P4`, because `P4` is part of the causal pathway through which the turbine process is represented and coupled.

## Why the Specific P4 Coefficients Are Plausible
The residual off-target block is not a random scattering of isolated features. It is mostly a coherent family:

- `P4_ST_PT01_01`
- `P4_ST_PT01_02`
- `P4_ST_PT01_04`
- `P4_ST_PT01_06`
- `P4_ST_PT01_07`
- `P4_ST_PT01_09`
- `P4_ST_PT01_10`

That matters because `P4_ST_PT01` appears to be a single simulator steam-side variable observed across lags. A coherent lag family in the simulator steam block is much easier to justify physically than a pattern in which support is sprayed across unrelated tags.

## What the Current Analysis Suggests
The recent notebook work improved the result in an important way:

- Duplicate rectified columns are now consolidated before fitting.
- Coefficients are expanded back with the `split_evenly` policy.
- The previous single large off-target spike was reduced into smaller secondary coefficients.
- The `P2` region now dominates the transformed fit rather than competing with one arbitrarily chosen duplicate feature.

This means the most obvious artifact, arbitrary allocation to identical columns, has already been addressed. What remains in `P4` is therefore more likely to reflect real coupling or label structure than a trivial optimization quirk.

## Additional Empirical Clues
Ad hoc checks on the HAI `attack_p2` data also point in the same direction.

### 1. The `P4` block is genuinely informative
On the processed `a1_sm` training split, the `P4_ST_PT01_*` lag family was substantially more correlated with the attack indicator than the `P2_VYT02_*` family:

- `P4_ST_PT01_*`: absolute correlation with `INDC` around `0.40` to `0.41`
- `P2_VYT02_*`: absolute correlation with `INDC` around `0.04` to `0.08`

Single-feature AUCs told the same story:

- `P4_ST_PT01_*`: about `0.70` to `0.75`
- `P2_VYT02_*`: about `0.52` to `0.53`

This does not prove `P4` is the causal source. It does show that the simulator steam-pressure block is a strong observable consequence of the `P2` attack scenarios as labeled in HAI.

### 2. Around pure `attack_P2` onsets, `P4_ST_PT01` moves more coherently than `P2_VYT02`
Using raw HAI windows centered on pure `attack_P2` starts, the average standardized post-onset shift was larger for `P4_ST_PT01` than for `P2_VYT02`:

- `P4_ST_PT01`: peak absolute mean z-shift about `3.06`
- `P2_VYT02`: peak absolute mean z-shift about `1.24`

Again, this suggests the simulator steam-side response is a real and consistent downstream marker of the `P2` attack condition.

## Why This Does Not Defeat Sparse Attribution
Sparse attribution in this project is being used to answer a process-level question: which lagged signals best characterize the `attack_p2` condition? That is not identical to the narrower question: which signals are direct turbine-local causes and nothing else?

For HAI, those two questions diverge because:

- the dataset is intentionally cross-coupled through `P4`
- the attack labels are process-level scenario labels
- the attack methodology includes stealth variants such as PV-response prevention; see [shin2020.md](C:/Users/jason/ODU/dissertation/references/shin2020.md#L12)
- the attack scenarios include repeated and combined control-loop manipulations; see [shin2020.md](C:/Users/jason/ODU/dissertation/references/shin2020.md#L13)

So a sparse model that gives primary weight to `P2` and secondary weight to the simulator steam block is still consistent with meaningful attribution. It may actually be the more faithful interpretation of the HAI benchmark.

## What Would Be More Concerning
The `P4` block would be more problematic if one or more of the following were true:

- `P2` support disappeared entirely and `P4` dominated the model.
- The off-target support were diffuse across unrelated tags with no physical linkage.
- The `P4` terms vanished under onset-centered or scenario-specific analysis, indicating they were only a train/test artifact.
- The same `P4` family appeared equally strongly for unrelated attack targets.

At the moment, the main residual block is coherent and physically plausible, and the tuned transformed model still concentrates its largest share in `P2`.

## Practical Interpretation
The safest interpretation is:

`P2` is the primary target block, and `P4_ST_PT01_*` is a legitimate secondary coupled-response block, not necessarily a false positive.

That is a stronger and more defensible claim than insisting that every nonzero coefficient outside `P2` must be an error.

## Recommended Next Checks
If tighter source attribution is needed, the next analyses should be designed around the HAI benchmark structure rather than around additional generic sparsity tuning.

1. Split `attack_p2` into `P2SC-SP` and `P2SC-SPRP` subsets and fit them separately.
2. Fit onset-centered windows rather than entire attack intervals.
3. Compare whether `P4_ST_PT01_*` remains strong when the target is restricted to pure `P2` attacks only.
4. Add a group-preference or hierarchy that favors direct `P2` variables over downstream `P4` variables when predictive value is nearly tied.

## Bottom Line
The residual `P4` block is not a disqualifier for sparse attribution in the `P2` block because HAI was engineered so that turbine behavior propagates into the HIL simulator. In this dataset, some `P4` support is expected. The right standard is not perfect exclusivity, but dominant concentration in `P2` with only limited, physically interpretable secondary support elsewhere.
