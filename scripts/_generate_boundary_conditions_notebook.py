from __future__ import annotations

import json
import textwrap
from pathlib import Path


def md_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": textwrap.dedent(source).strip() + "\n",
    }


def code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": textwrap.dedent(source).strip() + "\n",
    }


cells = [
    md_cell(
        """
        # Boundary Conditions Notebook

        This notebook is designed to fill **deficiency D003** for the dissertation. It translates the notes in `documentation/deficiencies.md`, `documentation/prospectus_audit.md`, and `documentation/theory_review.md` into one empirical boundary-condition package for **RQ2**.

        The goal is not to replace the Chapter 06 proof. The goal is to map where the proof-of-concept mechanism holds strongly, where it remains directionally useful but weaker, and where the chapter should explicitly treat the result as out of scope.
        """
    ),
    md_cell(
        """
        ## Experiment Design

        The notebook produces four deliverables tied directly to D003:

        1. **A zero-threshold IC boundary sweep** over positive and negative correlation settings, using Gaussian draws plus an empirical IC proxy.
        2. **A threshold bridge study** that starts from the exact zero-threshold sign case, then shifts to practical one-sided and interval critical ranges.
        3. **A negative-correlation complement check** showing why complement features are the practical repair when the chapter leaves the positive-correlation regime.
        4. **A final strong/weak/fail summary table** that can be translated directly into one Chapter 06 subsection.

        The one-sided bridge is intentional. As noted in the theory review, many learned practical ranges collapse one bound to an observed extreme, so the deployed rectifier often behaves like a shifted single-threshold rule rather than a perfectly symmetric interval.
        """
    ),
    md_cell(
        """
        ## How the Empirical Results Are Calculated

        This notebook does **not** estimate the Chapter 06 quantities from one real dataset. Instead, it builds a controlled family of synthetic covariance settings so the boundary conditions can be probed directly and repeatably.

        ### Calculation workflow

        1. **Construct a toy covariance model.**
           The main IC sweeps use an equicorrelated active block of size `s = 4` plus one inactive feature. The active block is controlled by `rho_active`, which determines how strongly the relevant features correlate with one another.

        2. **Set the inactive-active coupling.**
           The inactive feature is linked to the active block through the notebook's `cross_scale` parameter. Internally this is converted into an actual inactive-active correlation `rho_cross`, scaled to remain inside a positive-definite covariance construction.

        3. **Sample Gaussian data from that covariance.**
           For each `(rho_active, cross_scale)` setting and each random seed, the notebook draws multivariate normal samples. The baseline IC sweep uses a fixed moderate `cross_scale`, while the harder stress sweep varies it over a grid to expose where the proxy crosses its failure threshold.

        4. **Create the rectified view by sign binarization.**
           The raw draws are converted into `{-1, +1}` indicators using a zero threshold. This is the exact proof-of-concept transformation analyzed in Chapter 06.

        5. **Convert both views to empirical correlation matrices.**
           The notebook computes the sample correlation matrix for the raw Gaussian draws and for the sign-binarized version. Those matrices are the direct inputs to the IC proxy.

        6. **Evaluate the IC proxy.**
           For each correlation matrix, the notebook computes
           `Theta = max_i |c_i G^{-1} 1|`,
           where:
           - `G` is the active-block correlation matrix,
           - `c_i` is the inactive-active correlation vector for inactive feature `i`,
           - `1` is a fixed all-positive sign vector used as a simplified stand-in for `sign(beta_S)`.

        7. **Aggregate over seeds and summarize the boundary.**
           The notebook averages `Theta` over repeated seeds and also records the empirical fraction of runs satisfying `Theta < 1`. The heatmaps and crossing tables are derived from those aggregated summaries.

        8. **Run two additional empirical bridges.**
           The threshold-bridge section keeps the raw Gaussian correlation fixed and changes only the threshold rule, comparing zero-threshold signs, shifted one-sided thresholds, and interval ranges. The complement section uses a negatively correlated Gaussian pair and compares the original sign pair against a complemented feature view.

        ### Assumptions built into these calculations

        - **Joint normality:** the IC sweeps are based on multivariate Gaussian draws so the zero-threshold sign-binarization story remains tied to the proof-of-concept theory.
        - **Known support:** the notebook assumes the active set is known in advance. It is studying the geometry of the IC proxy, not performing support discovery from unknown truth.
        - **Equicorrelated active block:** all active features share the same within-support correlation in the toy construction. This keeps the boundary maps interpretable, but it is still a stylized regime.
        - **One explicit inactive feature in the baseline covariance toy model:** the main boundary sweeps start with a single inactive feature so the role of off-support leakage is easy to isolate. A later section then relaxes that simplification by fixing `s=4` and increasing the inactive pool from `1` to `10`.
        - **Fixed positive sign pattern:** the proxy uses an all-ones sign vector rather than estimating `sign(beta_S)` from fitted sparse models. This makes the notebook an IC-oriented stress test rather than a full end-to-end selection experiment.
        - **Sample correlation as a proxy for population structure:** the notebook uses finite-sample empirical correlation matrices, then averages across seeds to stabilize the result. It is therefore an empirical approximation to the theory, not a symbolic derivation.
        - **Pseudoinverse instead of exact inverse:** `G^{-1}` is implemented with a pseudoinverse for numerical robustness, especially near difficult conditioning regimes.
        - **Positive-correlation theorem scope:** the chapter's clean theorem is only meant to be interpreted to the right of the negative-side discontinuity marker. Left of that boundary, the notebook reports empirical stress behavior only.
        - **Threshold bridge is empirical, not closed-form theory:** once the threshold moves away from zero or becomes an interval, the notebook is documenting directional behavior rather than claiming an exact arcsin mapping.

        The safest way to read the notebook is therefore: it is a controlled empirical stress package that tests whether the chapter's mechanism survives when dependence strength, threshold placement, and sign structure are varied, while keeping the assumptions explicit enough that the resulting plots remain interpretable.
        """
    ),
    code_cell(
        """
        from __future__ import annotations

        import math
        from pathlib import Path

        import matplotlib.pyplot as plt
        from matplotlib.lines import Line2D
        import numpy as np
        import pandas as pd

        try:
            import seaborn as sns
        except Exception:
            sns = None

        try:
            from IPython.display import Markdown, display
        except Exception:
            Markdown = None
            display = None

        plt.rcParams["figure.figsize"] = (10, 5)
        plt.rcParams["axes.grid"] = True
        if sns is not None:
            sns.set_theme(style="whitegrid")
        """
    ),
    code_cell(
        """
        def _find_repo_root() -> Path:
            anchors = [Path.cwd().resolve()]
            if "__file__" in globals():
                anchors.insert(0, Path(__file__).resolve().parent)
            for anchor in anchors:
                for candidate in (anchor, *anchor.parents):
                    if (candidate / "documentation").is_dir() and (candidate / "notebooks").is_dir():
                        return candidate
            raise FileNotFoundError("Could not locate the dissertation repository root.")


        REPO_ROOT = _find_repo_root()
        NOTEBOOKS_DIR = REPO_ROOT / "notebooks"
        FIGURES_DIR = NOTEBOOKS_DIR / "Figures"
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        RUN_DIR = NOTEBOOKS_DIR / "runs_new" / "boundary_conditions"
        RUN_DIR.mkdir(parents=True, exist_ok=True)

        SUPPORT_SIZE = 4
        SUPPORT_INDEX = tuple(range(SUPPORT_SIZE))
        POLE = -1.0 / (SUPPORT_SIZE - 1)
        IC_RHO_GRID = np.array([-0.30, -0.25, -0.20, -0.15, -0.10, -0.05, 0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90])
        IC_SEEDS = [1201, 1202, 1203, 1204, 1205]
        IC_N = 6000
        DEFAULT_CROSS_SCALE = 0.60
        STRESS_RHO_GRID = np.round(np.arange(-0.25, 0.91, 0.05), 2)
        STRESS_SCALE_GRID = np.round(np.arange(0.45, 0.96, 0.05), 2)
        STRESS_SEEDS = [2201, 2202, 2203]
        STRESS_N = 5000
        PROFILE_RHOS = [-0.20, 0.00, 0.20, 0.60]
        INACTIVE_COUNT_GRID = np.arange(1, 11)
        INACTIVE_SWEEP_RHOS = [0.00, 0.20, 0.60]
        INACTIVE_SWEEP_CROSS_SCALE = 0.80
        INACTIVE_SWEEP_SEEDS = [3301, 3302, 3303, 3304, 3305]
        INACTIVE_SWEEP_N = 5000

        THRESHOLD_BRIDGE_RHO = 0.60
        THRESHOLD_BRIDGE_N = 250000
        THRESHOLD_GRID = np.linspace(-1.5, 1.5, 13)
        INTERVAL_SCENARIOS = [
            {"scenario_id": "centered_wide", "label": "Centered wide [-1.0, 1.0]", "lo": -1.0, "hi": 1.0},
            {"scenario_id": "centered_narrow", "label": "Centered narrow [-0.35, 0.35]", "lo": -0.35, "hi": 0.35},
            {"scenario_id": "shifted_mid", "label": "Shifted mid [0.25, 1.25]", "lo": 0.25, "hi": 1.25},
            {"scenario_id": "tail_band", "label": "Tail band [1.0, 2.0]", "lo": 1.0, "hi": 2.0},
        ]
        NEG_COMPLEMENT_RHO = -0.60
        NEG_COMPLEMENT_N = 250000
        OVERWRITE_CACHE = False

        config_view = pd.DataFrame(
            [
                {"Parameter": "Support size", "Value": SUPPORT_SIZE},
                {"Parameter": "Negative-side pole", "Value": f"{POLE:.3f}"},
                {"Parameter": "IC rho grid", "Value": ", ".join(f"{value:.2f}" for value in IC_RHO_GRID)},
                {"Parameter": "IC seeds", "Value": ", ".join(map(str, IC_SEEDS))},
                {"Parameter": "Default cross-scale", "Value": DEFAULT_CROSS_SCALE},
                {"Parameter": "Stress cross-scale grid", "Value": ", ".join(f"{value:.2f}" for value in STRESS_SCALE_GRID)},
                {"Parameter": "Inactive-count grid", "Value": ", ".join(map(str, INACTIVE_COUNT_GRID))},
                {"Parameter": "Inactive sweep rhos", "Value": ", ".join(f"{value:.2f}" for value in INACTIVE_SWEEP_RHOS)},
                {"Parameter": "Inactive sweep cross-scale", "Value": f"{INACTIVE_SWEEP_CROSS_SCALE:.2f}"},
                {"Parameter": "Threshold bridge rho", "Value": THRESHOLD_BRIDGE_RHO},
                {"Parameter": "Threshold grid", "Value": ", ".join(f"{value:.2f}" for value in THRESHOLD_GRID)},
            ]
        )
        if display is not None:
            display(config_view)
        else:
            print(config_view.to_string(index=False))

        print("Repository root:", REPO_ROOT)
        print("Figures directory:", FIGURES_DIR)
        print("Run directory:", RUN_DIR)
        """
    ),
    code_cell(
        """
        def safe_corr(a, b) -> float:
            x = np.asarray(a, dtype=float)
            y = np.asarray(b, dtype=float)
            if x.ndim != 1:
                x = x.reshape(-1)
            if y.ndim != 1:
                y = y.reshape(-1)
            if x.size != y.size:
                raise ValueError("safe_corr expects vectors of equal length.")
            if np.std(x) < 1e-12 or np.std(y) < 1e-12:
                return float("nan")
            return float(np.corrcoef(x, y)[0, 1])


        def pm1(values, threshold: float = 0.0) -> np.ndarray:
            arr = np.asarray(values, dtype=float)
            return np.where(arr >= threshold, 1.0, -1.0)


        def pm1_from_mask(mask) -> np.ndarray:
            arr = np.asarray(mask, dtype=bool)
            return np.where(arr, 1.0, -1.0)


        def correlation_matrix(X) -> np.ndarray:
            arr = np.asarray(X, dtype=float)
            corr = np.corrcoef(arr, rowvar=False)
            return np.nan_to_num(corr, nan=0.0, posinf=1.0, neginf=-1.0)


        def pairwise_mean(corr: np.ndarray, width: int) -> float:
            tri = np.triu_indices(width, k=1)
            values = corr[np.ix_(range(width), range(width))][tri]
            return float(np.mean(values))


        def pivot_surface(df: pd.DataFrame, value_col: str, *, index: str = "cross_scale", columns: str = "rho_active") -> pd.DataFrame:
            return df.pivot(index=index, columns=columns, values=value_col).sort_index().sort_index(axis=1)


        def ic_score(corr: np.ndarray, support) -> float:
            support = list(support)
            inactive = [index for index in range(corr.shape[0]) if index not in support]
            if not inactive:
                return 0.0
            G = corr[np.ix_(support, support)]
            inv_G = np.linalg.pinv(G)
            sign_vec = np.ones(len(support), dtype=float)
            values = []
            for index in inactive:
                c_vec = corr[index, support]
                values.append(abs(float(c_vec @ inv_G @ sign_vec)))
            return float(max(values))


        def first_crossing_scale(df: pd.DataFrame, value_col: str, cutoff: float = 1.0) -> float:
            ordered = df.sort_values("cross_scale")
            crossed = ordered.loc[ordered[value_col] > cutoff, "cross_scale"]
            if crossed.empty:
                return float("nan")
            return float(crossed.iloc[0])


        def inverse_inf_norm(corr: np.ndarray, support) -> float:
            G = corr[np.ix_(list(support), list(support))]
            return float(np.linalg.norm(np.linalg.pinv(G), ord=np.inf))


        def active_block_covariance(s: int, rho_active: float) -> np.ndarray:
            if s < 2:
                raise ValueError("Support size must be at least 2.")
            pole = -1.0 / (s - 1)
            if not (pole < rho_active < 0.999):
                raise ValueError(f"rho_active must lie in ({pole}, 1).")

            active_block = np.full((s, s), rho_active, dtype=float)
            np.fill_diagonal(active_block, 1.0)
            return active_block


        def block_covariance(s: int, rho_active: float, cross_scale: float = 0.60) -> tuple[np.ndarray, float]:
            active_block = active_block_covariance(s, rho_active)

            cross_cap = math.sqrt(max(1e-12, (1.0 + (s - 1) * rho_active) / s))
            sign = 1.0 if abs(rho_active) < 1e-12 else math.copysign(1.0, rho_active)
            rho_cross = float(sign * cross_scale * cross_cap)

            cov = np.eye(s + 1, dtype=float)
            cov[:s, :s] = active_block
            cov[:s, s] = rho_cross
            cov[s, :s] = rho_cross

            eigvals = np.linalg.eigvalsh(cov)
            if eigvals.min() <= 1e-9:
                raise ValueError(f"Constructed covariance is not positive definite: {eigvals.min():.6g}")
            return cov, rho_cross


        def sample_multi_inactive_design(
            n: int,
            s: int,
            inactive_count: int,
            rho_active: float,
            cross_scale: float,
            seed: int,
        ) -> np.ndarray:
            if inactive_count < 1:
                raise ValueError("inactive_count must be at least 1.")
            if not (0.0 <= cross_scale < 1.0):
                raise ValueError("cross_scale must lie in [0, 1).")

            rng = np.random.default_rng(int(seed))
            active_cov = active_block_covariance(s, rho_active)
            X_active = rng.multivariate_normal(np.zeros(s), active_cov, size=n)

            sign = 1.0 if abs(rho_active) < 1e-12 else math.copysign(1.0, rho_active)
            inactive_cols = []
            noise_scale = math.sqrt(max(1e-12, 1.0 - cross_scale**2))
            for _ in range(inactive_count):
                weights = rng.dirichlet(np.ones(s))
                mixture = X_active @ weights
                mixture_std = float(np.std(mixture))
                if mixture_std < 1e-12:
                    raise ValueError("Degenerate inactive mixture encountered.")
                mixture = mixture / mixture_std
                noise = rng.normal(size=n)
                inactive_cols.append(sign * cross_scale * mixture + noise_scale * noise)

            X_inactive = np.column_stack(inactive_cols)
            return np.column_stack([X_active, X_inactive])


        def classify_ic_regime(rho_active: float, delta_theta: float, delta_ic_rate: float) -> str:
            if rho_active < 0:
                return "out_of_scope"
            if delta_theta <= -0.15 and delta_ic_rate >= 0.10:
                return "strong"
            if delta_theta < 0.0:
                return "weak"
            return "fragile"


        def render_markdown(text: str) -> None:
            if display is not None and Markdown is not None:
                display(Markdown(text))
            else:
                print(text)
        """
    ),
    code_cell(
        """
        def run_or_load_ic_boundary(overwrite_cache: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
            runs_path = RUN_DIR / "ic_boundary_runs.csv"
            summary_path = RUN_DIR / "ic_boundary_summary.csv"
            if runs_path.exists() and summary_path.exists() and not overwrite_cache:
                runs_df = pd.read_csv(runs_path)
                summary_df = pd.read_csv(summary_path)
                print("Loaded cached IC boundary results from:", RUN_DIR)
                return runs_df, summary_df

            rows = []
            for rho_active in IC_RHO_GRID:
                cov, rho_cross = block_covariance(SUPPORT_SIZE, float(rho_active))
                for seed in IC_SEEDS:
                    rng = np.random.default_rng(int(seed))
                    X = rng.multivariate_normal(np.zeros(SUPPORT_SIZE + 1), cov, size=IC_N)
                    X_bin = pm1(X, threshold=0.0)

                    corr_raw = correlation_matrix(X)
                    corr_bin = correlation_matrix(X_bin)

                    theta_raw = ic_score(corr_raw, SUPPORT_INDEX)
                    theta_bin = ic_score(corr_bin, SUPPORT_INDEX)
                    inv_raw = inverse_inf_norm(corr_raw, SUPPORT_INDEX)
                    inv_bin = inverse_inf_norm(corr_bin, SUPPORT_INDEX)
                    active_raw = pairwise_mean(corr_raw, SUPPORT_SIZE)
                    active_bin = pairwise_mean(corr_bin, SUPPORT_SIZE)
                    cross_raw = float(np.mean(corr_raw[SUPPORT_SIZE, :SUPPORT_SIZE]))
                    cross_bin = float(np.mean(corr_bin[SUPPORT_SIZE, :SUPPORT_SIZE]))

                    rows.append(
                        {
                            "rho_active": float(rho_active),
                            "rho_cross": float(rho_cross),
                            "seed": int(seed),
                            "active_corr_raw": active_raw,
                            "active_corr_bin": active_bin,
                            "cross_corr_raw": cross_raw,
                            "cross_corr_bin": cross_bin,
                            "theta_raw": theta_raw,
                            "theta_bin": theta_bin,
                            "ic_rate_raw": float(theta_raw < 1.0),
                            "ic_rate_bin": float(theta_bin < 1.0),
                            "inv_raw": inv_raw,
                            "inv_bin": inv_bin,
                        }
                    )

            runs_df = pd.DataFrame(rows)
            summary_df = (
                runs_df.groupby(["rho_active", "rho_cross"], as_index=False)
                .agg(
                    active_corr_raw=("active_corr_raw", "mean"),
                    active_corr_bin=("active_corr_bin", "mean"),
                    cross_corr_raw=("cross_corr_raw", "mean"),
                    cross_corr_bin=("cross_corr_bin", "mean"),
                    theta_raw=("theta_raw", "mean"),
                    theta_bin=("theta_bin", "mean"),
                    ic_rate_raw=("ic_rate_raw", "mean"),
                    ic_rate_bin=("ic_rate_bin", "mean"),
                    inv_raw=("inv_raw", "mean"),
                    inv_bin=("inv_bin", "mean"),
                )
                .sort_values("rho_active")
                .reset_index(drop=True)
            )
            summary_df["delta_theta"] = summary_df["theta_bin"] - summary_df["theta_raw"]
            summary_df["delta_ic_rate"] = summary_df["ic_rate_bin"] - summary_df["ic_rate_raw"]
            summary_df["delta_inv"] = summary_df["inv_bin"] - summary_df["inv_raw"]
            summary_df["theoretical_active_sign_corr"] = (2.0 / np.pi) * np.arcsin(summary_df["rho_active"].clip(-1.0, 1.0))
            summary_df["theoretical_cross_sign_corr"] = (2.0 / np.pi) * np.arcsin(summary_df["rho_cross"].clip(-1.0, 1.0))
            summary_df["regime"] = [
                classify_ic_regime(rho_active, delta_theta, delta_ic_rate)
                for rho_active, delta_theta, delta_ic_rate in zip(
                    summary_df["rho_active"],
                    summary_df["delta_theta"],
                    summary_df["delta_ic_rate"],
                )
            ]

            runs_df.to_csv(runs_path, index=False)
            summary_df.to_csv(summary_path, index=False)
            print("Saved IC boundary results to:", RUN_DIR)
            return runs_df, summary_df


        ic_runs, ic_summary = run_or_load_ic_boundary(overwrite_cache=OVERWRITE_CACHE)
        if display is not None:
            display(ic_summary)
        else:
            print(ic_summary.to_string(index=False))
        """
    ),
    code_cell(
        """
        ic_plot = ic_summary.sort_values("rho_active").reset_index(drop=True)

        fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True)

        axes[0, 0].plot(ic_plot["rho_active"], ic_plot["active_corr_raw"], marker="o", linewidth=2, label="Raw active corr")
        axes[0, 0].plot(ic_plot["rho_active"], ic_plot["active_corr_bin"], marker="o", linewidth=2, label="Rectified active corr")
        axes[0, 0].plot(
            ic_plot["rho_active"],
            ic_plot["theoretical_active_sign_corr"],
            linestyle="--",
            linewidth=2,
            color="#2d6a4f",
            label="Theory: 2/pi * arcsin(rho)",
        )
        axes[0, 0].set_ylabel("Pairwise active correlation")
        axes[0, 0].set_title("Pairwise Correlation Contraction")
        axes[0, 0].legend()

        axes[0, 1].plot(ic_plot["rho_active"], ic_plot["theta_raw"], marker="o", linewidth=2, label="Raw Theta")
        axes[0, 1].plot(ic_plot["rho_active"], ic_plot["theta_bin"], marker="o", linewidth=2, label="Rectified Theta")
        axes[0, 1].set_yscale("log")
        axes[0, 1].set_ylabel("IC proxy Theta (log scale)")
        axes[0, 1].set_title("Inactive-Active Leakage Proxy")
        axes[0, 1].legend()

        axes[1, 0].plot(ic_plot["rho_active"], ic_plot["ic_rate_raw"], marker="o", linewidth=2, label="Raw P(Theta < 1)")
        axes[1, 0].plot(ic_plot["rho_active"], ic_plot["ic_rate_bin"], marker="o", linewidth=2, label="Rectified P(Theta < 1)")
        axes[1, 0].set_xlabel("Active-block rho")
        axes[1, 0].set_ylabel("Empirical IC satisfaction rate")
        axes[1, 0].set_title("IC-Favorable Region Frequency")
        axes[1, 0].legend()

        axes[1, 1].plot(ic_plot["rho_active"], ic_plot["inv_raw"], marker="o", linewidth=2, label="Raw ||G^-1||_inf")
        axes[1, 1].plot(ic_plot["rho_active"], ic_plot["inv_bin"], marker="o", linewidth=2, label="Rectified ||G^-1||_inf")
        axes[1, 1].set_yscale("log")
        axes[1, 1].set_xlabel("Active-block rho")
        axes[1, 1].set_ylabel("Inverse norm (log scale)")
        axes[1, 1].set_title("Active-Block Conditioning Proxy")
        axes[1, 1].legend()

        for ax in axes.ravel():
            ax.axvline(POLE, linestyle=":", linewidth=1.5, color="crimson")
            ax.grid(True, alpha=0.3)

        fig.suptitle("D003 Boundary Sweep Around the Positive and Negative Regimes", y=1.02)
        fig.tight_layout()
        out_path = FIGURES_DIR / "boundary_ic_sweep.png"
        fig.savefig(out_path, dpi=150, bbox_inches="tight")
        plt.show()
        print("Saved:", out_path)
        """
    ),
    code_cell(
        """
        positive_rows = ic_summary.loc[ic_summary["rho_active"] > 0].copy()
        strong_rows = positive_rows.loc[positive_rows["regime"] == "strong"].copy()
        if strong_rows.empty:
            strong_rows = positive_rows.nsmallest(1, "theta_bin")
        strongest_row = strong_rows.iloc[0]
        negative_edge_row = ic_summary.loc[ic_summary["rho_active"].idxmin()]

        render_markdown(
            f'''
        ### Reading the IC Boundary Sweep

        The four-panel figure is the notebook's main visual check on the Chapter 06 mechanism.

        - **Upper-left panel:** the rectified active-feature correlations sit below the raw correlations across the whole sweep, and on the nonnegative side they closely track the dashed theoretical `2/pi * arcsin(rho)` curve. This is the cleanest visual confirmation that the zero-threshold proof-of-concept behaves as expected.
        - **Upper-right panel:** the IC leakage proxy `Theta` drops after rectification. In the strongest positive regime highlighted by this run, `Theta` falls from `{strongest_row["theta_raw"]:.3f}` to `{strongest_row["theta_bin"]:.3f}` at `rho={strongest_row["rho_active"]:.2f}`. That is the direct operational meaning of "less inactive-active interference."
        - **Lower-left panel:** the empirical rate of satisfying `Theta < 1` rises sharply once rectification is applied near the weak-to-moderate positive settings. This is the panel that connects the proof language to a recoverability story rather than just a correlation story.
        - **Lower-right panel:** the inverse-norm proxy for the active block also drops after rectification, which means the transformed active block is easier to invert and less likely to amplify small nuisance correlations.

        The crimson vertical line marks the negative-side pole at `rho={POLE:.3f}`. To the right of that line, the plot supports the chapter's positive-correlation mechanism. To the left, the transformed proxy can still look numerically better, but that evidence should be read as a **stress test**, not as confirmation of the monotone theorem, because the proof no longer cleanly applies there. At the most negative point in this sweep (`rho={negative_edge_row["rho_active"]:.2f}`), `Theta` still drops from `{negative_edge_row["theta_raw"]:.3f}` to `{negative_edge_row["theta_bin"]:.3f}`, but the interpretation is empirical-only.

        One limitation of this baseline panel is that it fixes the inactive-active coupling at `cross_scale={DEFAULT_CROSS_SCALE:.2f}`. In that default setting, rectified `Theta` stays below `1` across the whole sweep. That is useful as a baseline, but it does **not** mean rectification is universally IC-safe. The next section increases coupling strength explicitly so the notebook can show where the orange curve really does cross the boundary.
        '''
        )
        """
    ),
    md_cell(
        """
        ## Harder IC Boundary Sweeps

        The baseline sweep above keeps `cross_scale` fixed at `0.60`, which is deliberately moderate. To expose a real rectified failure region, the next section sweeps both:

        - the active-block correlation `rho`, and
        - the inactive-active coupling multiplier `cross_scale`.

        This produces a genuine boundary map rather than a single favorable slice through the parameter space.
        """
    ),
    code_cell(
        """
        def run_or_load_ic_stress(overwrite_cache: bool = False) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
            runs_path = RUN_DIR / "ic_stress_runs.csv"
            summary_path = RUN_DIR / "ic_stress_summary.csv"
            crossing_path = RUN_DIR / "ic_stress_crossing_summary.csv"
            if runs_path.exists() and summary_path.exists() and crossing_path.exists() and not overwrite_cache:
                runs_df = pd.read_csv(runs_path)
                summary_df = pd.read_csv(summary_path)
                crossing_df = pd.read_csv(crossing_path)
                print("Loaded cached IC stress results from:", RUN_DIR)
                return runs_df, summary_df, crossing_df

            rows = []
            for rho_active in STRESS_RHO_GRID:
                for cross_scale in STRESS_SCALE_GRID:
                    cov, rho_cross = block_covariance(SUPPORT_SIZE, float(rho_active), cross_scale=float(cross_scale))
                    for seed in STRESS_SEEDS:
                        rng = np.random.default_rng(int(seed))
                        X = rng.multivariate_normal(np.zeros(SUPPORT_SIZE + 1), cov, size=STRESS_N)
                        X_bin = pm1(X, threshold=0.0)

                        corr_raw = correlation_matrix(X)
                        corr_bin = correlation_matrix(X_bin)

                        theta_raw = ic_score(corr_raw, SUPPORT_INDEX)
                        theta_bin = ic_score(corr_bin, SUPPORT_INDEX)

                        rows.append(
                            {
                                "rho_active": float(rho_active),
                                "cross_scale": float(cross_scale),
                                "rho_cross": float(rho_cross),
                                "seed": int(seed),
                                "theta_raw": theta_raw,
                                "theta_bin": theta_bin,
                                "safe_raw": float(theta_raw < 1.0),
                                "safe_bin": float(theta_bin < 1.0),
                            }
                        )

            runs_df = pd.DataFrame(rows)
            summary_df = (
                runs_df.groupby(["rho_active", "cross_scale", "rho_cross"], as_index=False)
                .agg(
                    theta_raw=("theta_raw", "mean"),
                    theta_bin=("theta_bin", "mean"),
                    safe_raw=("safe_raw", "mean"),
                    safe_bin=("safe_bin", "mean"),
                )
                .sort_values(["rho_active", "cross_scale"])
                .reset_index(drop=True)
            )
            summary_df["delta_theta"] = summary_df["theta_bin"] - summary_df["theta_raw"]
            summary_df["delta_safe"] = summary_df["safe_bin"] - summary_df["safe_raw"]
            summary_df["raw_over_one"] = summary_df["theta_raw"] > 1.0
            summary_df["rect_over_one"] = summary_df["theta_bin"] > 1.0

            crossing_rows = []
            for rho_active in np.sort(summary_df["rho_active"].unique()):
                subset = summary_df.loc[np.isclose(summary_df["rho_active"], rho_active)].copy()
                raw_cross = first_crossing_scale(subset, "theta_raw", cutoff=1.0)
                rect_cross = first_crossing_scale(subset, "theta_bin", cutoff=1.0)
                crossing_rows.append(
                    {
                        "rho_active": float(rho_active),
                        "raw_cross_scale": raw_cross,
                        "rect_cross_scale": rect_cross,
                        "extra_rectified_margin": rect_cross - raw_cross if np.isfinite(raw_cross) and np.isfinite(rect_cross) else float("nan"),
                    }
                )

            crossing_df = pd.DataFrame(crossing_rows).sort_values("rho_active").reset_index(drop=True)
            crossing_df["rho_active"] = crossing_df["rho_active"].round(2)
            crossing_df.loc[crossing_df["rho_active"].abs() < 1e-12, "rho_active"] = 0.0

            runs_df.to_csv(runs_path, index=False)
            summary_df.to_csv(summary_path, index=False)
            crossing_df.to_csv(crossing_path, index=False)
            print("Saved IC stress results to:", RUN_DIR)
            return runs_df, summary_df, crossing_df


        stress_runs, stress_summary, stress_crossings = run_or_load_ic_stress(overwrite_cache=OVERWRITE_CACHE)
        if display is not None:
            display(stress_crossings)
        else:
            print(stress_crossings.to_string(index=False))
        """
    ),
    code_cell(
        """
        raw_theta_surface = pivot_surface(stress_summary, "theta_raw")
        rect_theta_surface = pivot_surface(stress_summary, "theta_bin")
        raw_safe_surface = pivot_surface(stress_summary, "safe_raw")
        rect_safe_surface = pivot_surface(stress_summary, "safe_bin")

        rho_vals = raw_theta_surface.columns.to_numpy(dtype=float)
        scale_vals = raw_theta_surface.index.to_numpy(dtype=float)
        Xg, Yg = np.meshgrid(rho_vals, scale_vals)

        fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=True, constrained_layout=True)

        theta_levels = np.linspace(0.5, 2.5, 17)
        rate_levels = np.linspace(0.0, 1.0, 11)

        theta_maps = [
            (axes[0, 0], raw_theta_surface.to_numpy(dtype=float), "Raw Theta", "magma"),
            (axes[0, 1], rect_theta_surface.to_numpy(dtype=float), "Rectified Theta", "magma"),
        ]
        theta_mappable = None
        for ax, Z, title, cmap in theta_maps:
            theta_mappable = ax.contourf(Xg, Yg, Z, levels=theta_levels, cmap=cmap, extend="both")
            ax.contour(Xg, Yg, Z, levels=[1.0], colors="white", linewidths=2)
            ax.axvline(POLE, linestyle=":", linewidth=1.5, color="crimson")
            ax.axhline(DEFAULT_CROSS_SCALE, linestyle="--", linewidth=1.5, color="#8c564b")
            ax.set_title(title)
            ax.grid(True, alpha=0.2)

        rate_maps = [
            (axes[1, 0], raw_safe_surface.to_numpy(dtype=float), "Raw P(Theta < 1)", "viridis"),
            (axes[1, 1], rect_safe_surface.to_numpy(dtype=float), "Rectified P(Theta < 1)", "viridis"),
        ]
        rate_mappable = None
        for ax, Z, title, cmap in rate_maps:
            rate_mappable = ax.contourf(Xg, Yg, Z, levels=rate_levels, cmap=cmap, vmin=0.0, vmax=1.0)
            ax.axvline(POLE, linestyle=":", linewidth=1.5, color="crimson")
            ax.axhline(DEFAULT_CROSS_SCALE, linestyle="--", linewidth=1.5, color="#8c564b")
            ax.set_title(title)
            ax.grid(True, alpha=0.2)

        axes[1, 0].set_xlabel("Active-block rho")
        axes[1, 1].set_xlabel("Active-block rho")
        axes[0, 0].set_ylabel("Cross-scale")
        axes[1, 0].set_ylabel("Cross-scale")

        fig.colorbar(theta_mappable, ax=axes[0, :], shrink=0.9, label="Mean Theta")
        fig.colorbar(rate_mappable, ax=axes[1, :], shrink=0.9, label="Empirical safe frequency")
        fig.suptitle("Harder IC Boundary Maps Over rho and Cross-Scale", y=1.02)
        out_path = FIGURES_DIR / "boundary_ic_stress_heatmaps.png"
        fig.savefig(out_path, dpi=150, bbox_inches="tight")
        plt.show()
        print("Saved:", out_path)
        """
    ),
    code_cell(
        """
        crossing_zero = stress_crossings.loc[np.isclose(stress_crossings["rho_active"], 0.00)].iloc[0]
        crossing_two = stress_crossings.loc[np.isclose(stress_crossings["rho_active"], 0.20)].iloc[0]
        crossing_six = stress_crossings.loc[np.isclose(stress_crossings["rho_active"], 0.60)].iloc[0]
        crossing_neg = stress_crossings.loc[np.isclose(stress_crossings["rho_active"], -0.20)].iloc[0]

        render_markdown(
            f'''
        ### Reading the Harder Boundary Heatmaps

        These heatmaps answer the specific concern that the baseline sweep was too forgiving.

        - The **top row** shows mean `Theta` itself. The white contour is the actual `Theta = 1` boundary. Once `cross_scale` is allowed to grow, the rectified surface also crosses that contour.
        - The **bottom row** translates the same information into an empirical safe-frequency view. Unlike the earlier one-dimensional panel, the rectified map is no longer flat at `1.0`; its safe region shrinks as inactive-active coupling becomes stronger.
        - The **horizontal dashed line** marks the original baseline choice `cross_scale={DEFAULT_CROSS_SCALE:.2f}`. You can read the earlier sweep as a single horizontal slice through this larger map.

        The crossing table quantifies the gap between raw and rectified failure. In this run:

        - at `rho=0.00`, raw `Theta` first crosses `1` near `cross_scale={crossing_zero["raw_cross_scale"]:.2f}`, while rectified `Theta` does not cross until about `{crossing_zero["rect_cross_scale"]:.2f}`;
        - at `rho=0.20`, the corresponding crossings are `{crossing_two["raw_cross_scale"]:.2f}` and `{crossing_two["rect_cross_scale"]:.2f}`;
        - at `rho=0.60`, they shift to `{crossing_six["raw_cross_scale"]:.2f}` and `{crossing_six["rect_cross_scale"]:.2f}`.

        So the stronger claim supported by these plots is not "rectification never fails." The stronger claim is that, in the positive-correlation regime, rectification **pushes the failure boundary outward**. The negative case (`rho=-0.20`) is more brittle: raw crosses at `{crossing_neg["raw_cross_scale"]:.2f}`, while rectified still waits until about `{crossing_neg["rect_cross_scale"]:.2f}`, but that should still be interpreted as stress-test behavior rather than theorem-level support.
        '''
        )
        """
    ),
    code_cell(
        """
        fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=True)

        for ax, target_rho in zip(axes.ravel(), PROFILE_RHOS):
            subset = stress_summary.loc[np.isclose(stress_summary["rho_active"], target_rho)].sort_values("cross_scale")
            crossing = stress_crossings.loc[np.isclose(stress_crossings["rho_active"], target_rho)].iloc[0]

            ax.plot(subset["cross_scale"], subset["theta_raw"], marker="o", linewidth=2, label="Raw Theta")
            ax.plot(subset["cross_scale"], subset["theta_bin"], marker="o", linewidth=2, label="Rectified Theta")
            ax.axhline(1.0, linestyle="--", linewidth=1.5, color="black")
            ax.axvline(DEFAULT_CROSS_SCALE, linestyle=":", linewidth=1.5, color="#8c564b")
            ax.set_yscale("log")
            ax.set_title(f"rho = {target_rho:.2f}")
            raw_cross = crossing["raw_cross_scale"]
            rect_cross = crossing["rect_cross_scale"]
            raw_text = f"{raw_cross:.2f}" if np.isfinite(raw_cross) else "none"
            rect_text = f"{rect_cross:.2f}" if np.isfinite(rect_cross) else "none"
            ax.text(
                0.03,
                0.97,
                f"raw > 1 at {raw_text}\\nrect > 1 at {rect_text}",
                transform=ax.transAxes,
                va="top",
                ha="left",
                fontsize=8,
                bbox=dict(facecolor="white", edgecolor="#cccccc", alpha=0.9),
            )
            ax.grid(True, alpha=0.25)

        axes[1, 0].set_xlabel("Cross-scale")
        axes[1, 1].set_xlabel("Cross-scale")
        axes[0, 0].set_ylabel("Theta (log scale)")
        axes[1, 0].set_ylabel("Theta (log scale)")
        axes[0, 0].legend()
        fig.suptitle("Representative Cross-Scale Boundary Profiles", y=1.02)
        fig.tight_layout()
        out_path = FIGURES_DIR / "boundary_ic_stress_profiles.png"
        fig.savefig(out_path, dpi=150, bbox_inches="tight")
        plt.show()
        print("Saved:", out_path)
        """
    ),
    code_cell(
        """
        render_markdown(
            f'''
        ### Reading the Cross-Scale Profiles

        The profile panels make the heatmap story easier to read one slice at a time.

        - Each panel fixes `rho` and increases only the inactive-active coupling multiplier.
        - The black dashed line is the operative IC threshold `Theta = 1`.
        - The brown vertical marker is the original baseline `cross_scale={DEFAULT_CROSS_SCALE:.2f}`.

        These slices show the intended dissertation interpretation very clearly:

        - raw `Theta` crosses the boundary first,
        - rectified `Theta` crosses later,
        - and the delay between those crossings is largest in the central positive-correlation region where the chapter's mechanism is supposed to be most relevant.

        This is the missing robustness check that the original upper-right panel did not provide. The baseline slice showed one favorable setting; these profiles show the **distance to failure** as coupling strength increases.
        '''
        )
        """
    ),
    code_cell(
        """
        render_markdown(
            '''
        ### Interpreting Within-Support vs Off-Support Correlation

        The harder boundary plots are useful because they separate two different sources of difficulty inside the IC proxy:

        - the **active-block correlation** `rho`, which controls how entangled the relevant features are with one another, and
        - the **cross-scale** parameter, which controls how strongly a non-relevant feature aligns with the relevant block.

        In the proxy
        `Theta = max_i |c_i G^{-1} 1|`,
        these play different roles:

        - `c_i` is the inactive-active leakage term,
        - `G^{-1}` is the active-block amplification term.

        That means the plots should be read as follows:

        - when relevant features are strongly correlated among themselves but non-relevant features are only weakly tied to them, the system can still remain relatively safe because off-support leakage is limited;
        - when relevant features are not especially correlated among themselves but non-relevant features are strongly tied to them, the leakage term dominates and rectification becomes more important;
        - when both effects are large, the problem is hardest, and the question becomes how far rectification can push the failure boundary outward before `Theta` crosses `1`.

        So the main contribution of the rectification procedure in this notebook is best understood as **shrinking off-support interference**. It can also help active-block conditioning, but these stress plots show that the largest practical gain appears when inactive features are too correlated with the true support.
        '''
        )
        """
    ),
    md_cell(
        """
        ## Fixed Support, Growing Inactive Pool

        The earlier IC sweeps use one explicit inactive feature so the geometry is easy to read. The next section keeps the active support fixed at `s=4`, then increases the number of inactive features from `1` to `10`.

        This matters because the proxy is a **maximum over inactive features**. Even if each nuisance feature is only moderately aligned with the active block, a larger off-support pool creates more chances for one of them to become the worst-case leakage direction.
        """
    ),
    code_cell(
        """
        def run_or_load_inactive_count_sweep(overwrite_cache: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
            runs_path = RUN_DIR / "inactive_count_runs.csv"
            summary_path = RUN_DIR / "inactive_count_summary.csv"
            if runs_path.exists() and summary_path.exists() and not overwrite_cache:
                runs_df = pd.read_csv(runs_path)
                summary_df = pd.read_csv(summary_path)
                print("Loaded cached inactive-count sweep results from:", RUN_DIR)
                return runs_df, summary_df

            rows = []
            for rho_active in INACTIVE_SWEEP_RHOS:
                for inactive_count in INACTIVE_COUNT_GRID:
                    for seed in INACTIVE_SWEEP_SEEDS:
                        X = sample_multi_inactive_design(
                            n=INACTIVE_SWEEP_N,
                            s=SUPPORT_SIZE,
                            inactive_count=int(inactive_count),
                            rho_active=float(rho_active),
                            cross_scale=INACTIVE_SWEEP_CROSS_SCALE,
                            seed=int(seed),
                        )
                        X_bin = pm1(X, threshold=0.0)

                        corr_raw = correlation_matrix(X)
                        corr_bin = correlation_matrix(X_bin)

                        theta_raw = ic_score(corr_raw, SUPPORT_INDEX)
                        theta_bin = ic_score(corr_bin, SUPPORT_INDEX)
                        mean_cross_raw = float(np.mean(np.abs(corr_raw[SUPPORT_SIZE:, :SUPPORT_SIZE])))
                        mean_cross_bin = float(np.mean(np.abs(corr_bin[SUPPORT_SIZE:, :SUPPORT_SIZE])))

                        rows.append(
                            {
                                "rho_active": float(rho_active),
                                "inactive_count": int(inactive_count),
                                "seed": int(seed),
                                "theta_raw": theta_raw,
                                "theta_bin": theta_bin,
                                "safe_raw": float(theta_raw < 1.0),
                                "safe_bin": float(theta_bin < 1.0),
                                "mean_cross_raw": mean_cross_raw,
                                "mean_cross_bin": mean_cross_bin,
                            }
                        )

            runs_df = pd.DataFrame(rows)
            summary_df = (
                runs_df.groupby(["rho_active", "inactive_count"], as_index=False)
                .agg(
                    theta_raw=("theta_raw", "mean"),
                    theta_bin=("theta_bin", "mean"),
                    safe_raw=("safe_raw", "mean"),
                    safe_bin=("safe_bin", "mean"),
                    mean_cross_raw=("mean_cross_raw", "mean"),
                    mean_cross_bin=("mean_cross_bin", "mean"),
                )
                .sort_values(["rho_active", "inactive_count"])
                .reset_index(drop=True)
            )
            summary_df["delta_theta"] = summary_df["theta_bin"] - summary_df["theta_raw"]
            summary_df["delta_safe"] = summary_df["safe_bin"] - summary_df["safe_raw"]

            runs_df.to_csv(runs_path, index=False)
            summary_df.to_csv(summary_path, index=False)
            print("Saved inactive-count sweep results to:", RUN_DIR)
            return runs_df, summary_df


        inactive_count_runs, inactive_count_summary = run_or_load_inactive_count_sweep(overwrite_cache=OVERWRITE_CACHE)
        if display is not None:
            display(inactive_count_summary)
        else:
            print(inactive_count_summary.to_string(index=False))
        """
    ),
    code_cell(
        """
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharex=True)
        color_map = {
            0.00: "#4c78a8",
            0.20: "#f58518",
            0.60: "#54a24b",
        }
        safety_plot_offsets = {
            ("raw", 0.00): 0.004,
            ("rectified", 0.00): -0.004,
            ("raw", 0.20): 0.008,
            ("rectified", 0.20): -0.008,
            ("raw", 0.60): -0.012,
            ("rectified", 0.60): -0.016,
        }

        for rho_active in INACTIVE_SWEEP_RHOS:
            subset = inactive_count_summary.loc[np.isclose(inactive_count_summary["rho_active"], rho_active)].sort_values("inactive_count")
            color = color_map[float(rho_active)]
            label_suffix = f"rho={rho_active:.2f}"
            safe_raw_plot = subset["safe_raw"].to_numpy(dtype=float).copy()
            safe_bin_plot = subset["safe_bin"].to_numpy(dtype=float).copy()
            raw_offset = safety_plot_offsets[("raw", float(rho_active))]
            rect_offset = safety_plot_offsets[("rectified", float(rho_active))]

            # Display-only epsilon shifts keep coincident 0/1 safety curves visible in the plot.
            safe_raw_plot[np.isclose(safe_raw_plot, 0.0)] += raw_offset
            safe_raw_plot[np.isclose(safe_raw_plot, 1.0)] += raw_offset
            safe_bin_plot[np.isclose(safe_bin_plot, 0.0)] += rect_offset
            safe_bin_plot[np.isclose(safe_bin_plot, 1.0)] += rect_offset

            axes[0].plot(subset["inactive_count"], subset["theta_raw"], marker="o", linewidth=2, color=color, label=f"Raw {label_suffix}")
            axes[0].plot(subset["inactive_count"], subset["theta_bin"], marker="o", linewidth=2, linestyle="--", color=color, label=f"Rectified {label_suffix}")

            axes[1].plot(subset["inactive_count"], safe_raw_plot, marker="o", linewidth=2, color=color, label=f"Raw {label_suffix}")
            axes[1].plot(subset["inactive_count"], safe_bin_plot, marker="o", linewidth=2, linestyle="--", color=color, label=f"Rectified {label_suffix}")

        legend_handles = []
        for rho_active in INACTIVE_SWEEP_RHOS:
            color = color_map[float(rho_active)]
            legend_handles.append(Line2D([0], [0], color=color, linewidth=2, linestyle="-", label=f"Raw rho={rho_active:.2f}"))
            legend_handles.append(Line2D([0], [0], color=color, linewidth=2, linestyle="--", label=f"Rectified rho={rho_active:.2f}"))

        axes[0].axhline(1.0, linestyle="--", linewidth=1.5, color="black")
        axes[0].set_yscale("log")
        axes[0].set_xlabel("Number of inactive features")
        axes[0].set_ylabel("Mean Theta (log scale)")
        axes[0].set_title("Worst-Case Leakage vs Inactive Count")
        axes[0].legend(handles=legend_handles, ncol=2, fontsize=8)

        axes[1].set_xlabel("Number of inactive features")
        axes[1].set_ylabel("Empirical P(Theta < 1)")
        axes[1].set_title("IC Safety vs Inactive Count")
        axes[1].set_ylim(-0.02, 1.02)
        axes[1].legend(handles=legend_handles, ncol=2, fontsize=8)

        for ax in axes:
            ax.grid(True, alpha=0.25)

        fig.suptitle("Fixed s=4 Sweep Over the Size of the Inactive Pool", y=1.02)
        fig.tight_layout()
        out_path = FIGURES_DIR / "boundary_inactive_count_sweep.png"
        fig.savefig(out_path, dpi=150, bbox_inches="tight")
        plt.show()
        print("Saved:", out_path)
        """
    ),
    code_cell(
        """
        strongest_rho = inactive_count_summary.loc[np.isclose(inactive_count_summary["rho_active"], 0.20)].copy()
        first_row = strongest_rho.loc[strongest_rho["inactive_count"] == int(INACTIVE_COUNT_GRID.min())].iloc[0]
        last_row = strongest_rho.loc[strongest_rho["inactive_count"] == int(INACTIVE_COUNT_GRID.max())].iloc[0]

        render_markdown(
            f'''
        ### Reading the Inactive-Count Sweep

        This section isolates a simple but important fact about the IC proxy: `Theta` is a **maximum over inactive features**. Holding the active support fixed at `s=4` means the active-side geometry is unchanged, so any deterioration here is coming from a larger nuisance pool rather than from a bigger support block.

        - Each new inactive feature is generated as a noisy positive mixture of the active block, using the same coupling strength `cross_scale={INACTIVE_SWEEP_CROSS_SCALE:.2f}`.
        - The x-axis therefore does **not** mean the support is changing. It means the number of opportunities for off-support leakage is changing.
        - That is why the mean `Theta` curves rise as the inactive pool grows: with more nuisance features, the worst offending `c_i` tends to get worse.

        The raw-versus-rectified comparison still goes in the expected direction. At `rho=0.20`, mean raw `Theta` rises from `{first_row["theta_raw"]:.3f}` with one inactive feature to `{last_row["theta_raw"]:.3f}` with ten, while rectified `Theta` moves from `{first_row["theta_bin"]:.3f}` to `{last_row["theta_bin"]:.3f}`. So rectification does not remove the max-over-inactives effect; it **compresses it**.

        The practical interpretation is straightforward: if the relevant set stays small but the candidate feature pool grows, recovery becomes harder because there are more ways for non-relevant features to shadow the true support. Rectification still helps, but the notebook should not present that help as independent of dimensionality on the inactive side.
        '''
        )
        """
    ),
    md_cell(
        """
        ## Threshold Bridge: From Zero-Threshold Signs to Practical Critical Ranges

        The next section keeps the data-generating distribution fixed and changes only the threshold rule. This isolates the bridge question raised in the prospectus audit:

        - zero-threshold sign binarization has an exact arcsin mapping,
        - shifted one-sided cutoffs are the closest practical extension when one bound collapses to an observed extreme,
        - interval ranges are still useful empirically, but the exact closed-form theory is no longer available.
        """
    ),
    code_cell(
        """
        def run_or_load_threshold_bridge(overwrite_cache: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
            threshold_path = RUN_DIR / "threshold_bridge_sweep.csv"
            interval_path = RUN_DIR / "interval_bridge_summary.csv"
            if threshold_path.exists() and interval_path.exists() and not overwrite_cache:
                threshold_df = pd.read_csv(threshold_path)
                interval_df = pd.read_csv(interval_path)
                print("Loaded cached threshold bridge results from:", RUN_DIR)
                return threshold_df, interval_df

            rng = np.random.default_rng(314159)
            cov = np.array(
                [
                    [1.0, THRESHOLD_BRIDGE_RHO],
                    [THRESHOLD_BRIDGE_RHO, 1.0],
                ],
                dtype=float,
            )
            X = rng.multivariate_normal(np.zeros(2), cov, size=THRESHOLD_BRIDGE_N)
            raw_rho = safe_corr(X[:, 0], X[:, 1])

            threshold_rows = []
            for threshold in THRESHOLD_GRID:
                mask_a = X[:, 0] > threshold
                mask_b = X[:, 1] > threshold
                corr_indicator = safe_corr(pm1_from_mask(mask_a), pm1_from_mask(mask_b))
                threshold_rows.append(
                    {
                        "threshold": float(threshold),
                        "raw_rho": raw_rho,
                        "indicator_corr": corr_indicator,
                        "prevalence": float(np.mean(mask_a)),
                    }
                )

            threshold_df = pd.DataFrame(threshold_rows)
            zero_corr = float(threshold_df.loc[np.isclose(threshold_df["threshold"], 0.0), "indicator_corr"].iloc[0])
            threshold_df["delta_vs_raw"] = threshold_df["indicator_corr"] - threshold_df["raw_rho"]
            threshold_df["delta_vs_zero_sign"] = threshold_df["indicator_corr"] - zero_corr

            interval_rows = []
            for scenario in INTERVAL_SCENARIOS:
                lo = float(scenario["lo"])
                hi = float(scenario["hi"])
                mask_a = (X[:, 0] > lo) & (X[:, 0] < hi)
                mask_b = (X[:, 1] > lo) & (X[:, 1] < hi)
                corr_indicator = safe_corr(pm1_from_mask(mask_a), pm1_from_mask(mask_b))
                interval_rows.append(
                    {
                        "scenario_id": scenario["scenario_id"],
                        "label": scenario["label"],
                        "lo": lo,
                        "hi": hi,
                        "raw_rho": raw_rho,
                        "indicator_corr": corr_indicator,
                        "prevalence": float(np.mean(mask_a)),
                        "delta_vs_raw": corr_indicator - raw_rho,
                        "delta_vs_zero_sign": corr_indicator - zero_corr,
                    }
                )

            interval_df = pd.DataFrame(interval_rows)
            threshold_df.to_csv(threshold_path, index=False)
            interval_df.to_csv(interval_path, index=False)
            print("Saved threshold bridge results to:", RUN_DIR)
            return threshold_df, interval_df


        threshold_bridge_df, interval_bridge_df = run_or_load_threshold_bridge(overwrite_cache=OVERWRITE_CACHE)
        if display is not None:
            display(threshold_bridge_df)
            display(interval_bridge_df)
        else:
            print(threshold_bridge_df.to_string(index=False))
            print(interval_bridge_df.to_string(index=False))
        """
    ),
    code_cell(
        """
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

        axes[0].plot(
            threshold_bridge_df["threshold"],
            threshold_bridge_df["indicator_corr"],
            marker="o",
            linewidth=2,
            label="One-sided indicator corr",
        )
        axes[0].axhline(
            float(threshold_bridge_df["raw_rho"].iloc[0]),
            linestyle="--",
            linewidth=2,
            color="#7f8c8d",
            label="Raw Pearson rho",
        )
        axes[0].axvline(0.0, linestyle=":", linewidth=1.5, color="crimson")
        axes[0].set_xlabel("Threshold t in 1{x > t}")
        axes[0].set_ylabel("Indicator correlation")
        axes[0].set_title("One-Sided Threshold Bridge")
        axes[0].legend()

        interval_plot = interval_bridge_df.sort_values("indicator_corr", ascending=True).reset_index(drop=True)
        axes[1].barh(interval_plot["label"], interval_plot["indicator_corr"], color="#4c78a8")
        axes[1].axvline(
            float(interval_plot["raw_rho"].iloc[0]),
            linestyle="--",
            linewidth=2,
            color="#7f8c8d",
            label="Raw Pearson rho",
        )
        axes[1].set_xlabel("Indicator correlation")
        axes[1].set_title("Interval Critical-Range Bridge")
        axes[1].legend()

        fig.tight_layout()
        out_path = FIGURES_DIR / "boundary_threshold_bridge.png"
        fig.savefig(out_path, dpi=150, bbox_inches="tight")
        plt.show()
        print("Saved:", out_path)
        """
    ),
    code_cell(
        """
        zero_threshold_row = threshold_bridge_df.loc[np.isclose(threshold_bridge_df["threshold"], 0.0)].iloc[0]
        shifted_threshold_row = threshold_bridge_df.loc[np.isclose(threshold_bridge_df["threshold"], 0.75)].iloc[0]
        shifted_interval_row = interval_bridge_df.loc[interval_bridge_df["scenario_id"] == "shifted_mid"].iloc[0]
        tail_interval_row = interval_bridge_df.loc[interval_bridge_df["scenario_id"] == "tail_band"].iloc[0]

        render_markdown(
            f'''
        ### Reading the Threshold Bridge Plot

        This figure asks a narrower question than the IC sweep: if the theorem is exact only at zero threshold, how much of its direction survives once the cutoff is moved?

        - **Left panel:** the one-sided threshold curve peaks near the zero-threshold sign case and then tapers as the threshold moves into either tail. That shape means the cleanest bridge from theory to practice is not "any arbitrary threshold"; it is specifically a **moderately shifted one-sided cutoff**.
        - At `t=0.00`, the indicator correlation is `{zero_threshold_row["indicator_corr"]:.3f}` against raw `rho={zero_threshold_row["raw_rho"]:.3f}`. This is the direct empirical analogue of the arcsin contraction.
        - At `t=0.75`, the indicator correlation is still only `{shifted_threshold_row["indicator_corr"]:.3f}`, which remains well below the raw `{shifted_threshold_row["raw_rho"]:.3f}`. That is why the notebook classifies shifted one-sided rules as a **strong bridge** even though the exact formula is no longer available.
        - **Right panel:** the interval rules all remain below the raw Pearson correlation, but they are noticeably weaker than the one-sided cases. The shifted interval `[0.25, 1.25]` lands at `{shifted_interval_row["indicator_corr"]:.3f}`, while the tail band `[1.0, 2.0]` lands at `{tail_interval_row["indicator_corr"]:.3f}`.

        The practical message is that interval critical ranges can still be directionally useful, but they should be described more cautiously in Chapter 06. Once the rule becomes a bounded interval, range placement and prevalence start to matter almost as much as the original covariance geometry.
        '''
        )
        """
    ),
    md_cell(
        """
        ## Negative Correlation and Complement Features

        Chapter 06 and the theory review both flag negative-correlation settings as the main place where the clean positive-correlation monotonicity story breaks. The practical mitigation in the manuscript is to add complement features so that an "outside-range" relation can be represented as a positive association in the transformed design.
        """
    ),
    code_cell(
        """
        def run_or_load_negative_complement(overwrite_cache: bool = False) -> pd.DataFrame:
            out_path = RUN_DIR / "negative_complement_summary.csv"
            if out_path.exists() and not overwrite_cache:
                df = pd.read_csv(out_path)
                print("Loaded cached complement summary from:", out_path)
                return df

            rng = np.random.default_rng(271828)
            cov = np.array(
                [
                    [1.0, NEG_COMPLEMENT_RHO],
                    [NEG_COMPLEMENT_RHO, 1.0],
                ],
                dtype=float,
            )
            X = rng.multivariate_normal(np.zeros(2), cov, size=NEG_COMPLEMENT_N)
            sign_a = pm1(X[:, 0], threshold=0.0)
            sign_b = pm1(X[:, 1], threshold=0.0)

            df = pd.DataFrame(
                [
                    {
                        "view": "Original sign pair",
                        "correlation": safe_corr(sign_a, sign_b),
                        "note": "Negative pair remains negative and sits outside the positive-correlation proof path.",
                    },
                    {
                        "view": "Complemented second feature",
                        "correlation": safe_corr(sign_a, -sign_b),
                        "note": "Adding the complement flips the relation back into a positive-correlation view.",
                    },
                ]
            )
            df.to_csv(out_path, index=False)
            print("Saved complement summary to:", out_path)
            return df


        negative_complement_df = run_or_load_negative_complement(overwrite_cache=OVERWRITE_CACHE)
        if display is not None:
            display(negative_complement_df)
        else:
            print(negative_complement_df.to_string(index=False))
        """
    ),
    code_cell(
        """
        original_corr = float(negative_complement_df.loc[negative_complement_df["view"] == "Original sign pair", "correlation"].iloc[0])
        complemented_corr = float(negative_complement_df.loc[negative_complement_df["view"] == "Complemented second feature", "correlation"].iloc[0])

        render_markdown(
            f'''
        ### Reading the Complement Check

        This table is small, but it carries the main practical lesson for the negative-correlation edge case.

        - Without complements, the sign pair stays negatively associated at `{original_corr:.3f}`. That leaves the example outside the chapter's clean positive-correlation proof path.
        - After complementing the second feature, the same relationship becomes positively associated at `{complemented_corr:.3f}`.

        In other words, complement features do not "fix" the theorem. They **re-express** the problematic relation in a form that the rectified representation can use more naturally. That is why the dissertation should frame complements as a practical engineering repair rather than as an extension of the closed-form proof.
        '''
        )
        """
    ),
    code_cell(
        """
        def nearest_ic_row(target_rho: float) -> pd.Series:
            idx = (ic_summary["rho_active"] - target_rho).abs().idxmin()
            return ic_summary.loc[idx]


        def threshold_row(target_threshold: float) -> pd.Series:
            mask = np.isclose(threshold_bridge_df["threshold"], target_threshold)
            return threshold_bridge_df.loc[mask].iloc[0]


        def interval_row(scenario_id: str) -> pd.Series:
            return interval_bridge_df.loc[interval_bridge_df["scenario_id"] == scenario_id].iloc[0]


        positive_row = nearest_ic_row(0.60)
        negative_row = nearest_ic_row(-0.30)
        shifted_one_sided = threshold_row(0.75)
        shifted_interval = interval_row("shifted_mid")
        tail_interval = interval_row("tail_band")
        complement_rows = negative_complement_df.set_index("view")

        boundary_summary = pd.DataFrame(
            [
                {
                    "setting": "Positive zero-threshold sign (rho=0.60)",
                    "status": "strong",
                    "raw_metric": positive_row["theta_raw"],
                    "rectified_metric": positive_row["theta_bin"],
                    "delta": positive_row["delta_theta"],
                    "interpretation": "The exact arcsin regime holds: pairwise correlations contract and the empirical IC proxy drops.",
                },
                {
                    "setting": "Shifted one-sided cutoff t=0.75",
                    "status": "strong",
                    "raw_metric": shifted_one_sided["raw_rho"],
                    "rectified_metric": shifted_one_sided["indicator_corr"],
                    "delta": shifted_one_sided["delta_vs_raw"],
                    "interpretation": "This is the cleanest bridge to practice because many fitted ranges collapse to a one-sided cutoff.",
                },
                {
                    "setting": "Shifted interval [0.25, 1.25]",
                    "status": "weak",
                    "raw_metric": shifted_interval["raw_rho"],
                    "rectified_metric": shifted_interval["indicator_corr"],
                    "delta": shifted_interval["delta_vs_raw"],
                    "interpretation": "Correlation still contracts, but the exact zero-threshold mapping is gone and range placement becomes feature-specific.",
                },
                {
                    "setting": "Tail interval [1.0, 2.0]",
                    "status": "weak",
                    "raw_metric": tail_interval["raw_rho"],
                    "rectified_metric": tail_interval["indicator_corr"],
                    "delta": tail_interval["delta_vs_raw"],
                    "interpretation": "The range is still contractive here, but low prevalence makes the practical bridge sample-fragile.",
                },
                {
                    "setting": "Negative-side IC sweep near pole (rho=-0.30)",
                    "status": "fail",
                    "raw_metric": negative_row["theta_raw"],
                    "rectified_metric": negative_row["theta_bin"],
                    "delta": negative_row["delta_theta"],
                    "interpretation": "The empirical proxy may still improve, but the chapter's monotone positive-correlation proof no longer applies on this side of the discontinuity.",
                },
                {
                    "setting": "Negative pair with complement feature",
                    "status": "recovered",
                    "raw_metric": complement_rows.loc["Original sign pair", "correlation"],
                    "rectified_metric": complement_rows.loc["Complemented second feature", "correlation"],
                    "delta": complement_rows.loc["Complemented second feature", "correlation"] - complement_rows.loc["Original sign pair", "correlation"],
                    "interpretation": "Complement features convert the negative pair back into a positive-correlation representation, which is the practical repair noted in Chapter 06.",
                },
            ]
        )

        summary_path = RUN_DIR / "boundary_conditions_summary.csv"
        boundary_summary.to_csv(summary_path, index=False)

        takeaways = [
            "In the positive zero-threshold regime, sign binarization reproduces the expected arcsin contraction and lowers the empirical IC leakage proxy.",
            "Harder cross-scale sweeps show that rectification does not eliminate failure; it pushes the Theta=1 boundary outward so stronger inactive-active coupling is required before the proxy breaks.",
            "With support fixed at s=4, enlarging the inactive pool from 1 to 10 raises the max-based IC proxy because more nuisance features create more chances for a worst-case leakage direction.",
            "Moderate one-sided nonzero thresholds preserve the same directional contraction, making them the clearest empirical bridge from the theorem to practical critical-range rules.",
            "Shifted and tail intervals remain directionally useful but weaker because the exact mapping disappears and low-prevalence ranges become sample-sensitive.",
            "Negative-correlation settings should be described as out of scope for the clean theorem; complement features are the practical repair when those relations matter.",
        ]
        takeaways_path = RUN_DIR / "boundary_takeaways.txt"
        takeaways_path.write_text("\\n".join(takeaways) + "\\n", encoding="utf-8")

        if display is not None:
            display(boundary_summary)
        else:
            print(boundary_summary.to_string(index=False))
        print("Saved:", summary_path)
        print("Saved:", takeaways_path)
        """
    ),
    code_cell(
        """
        status_counts = boundary_summary["status"].value_counts().to_dict()

        render_markdown(
            f'''
        ### What the Final Summary Table Says

        The last table is the notebook's manuscript-ready synthesis.

        - It identifies **where the theorem is strongest**: the positive zero-threshold sign case and its nearby one-sided practical extensions.
        - It marks **where the theory becomes weaker but still directionally useful**: shifted and tail interval rules, where contraction remains visible but the exact mapping disappears.
        - It marks **where the chapter should stop claiming theorem-level support**: negative-side covariance settings. Those cases can still be studied empirically, but they should be written up as boundary conditions or stress tests.
        - It also records **the repair path**: complement features recover a positive association view when the native sign relation is negative.
        - The harder cross-scale plots above qualify the word **strong**: it means the failure boundary moves outward, not that rectified `Theta` can never exceed `1`.

        In this run, the final tally is `{status_counts}`. Read that as a chapter-writing guide: emphasize the strong cases, acknowledge the weak bridge cases, and explicitly fence off the fail/out-of-scope cases so the RQ2 claim stays precise.
        '''
        )
        """
    ),
    md_cell(
        """
        ## Artifact Summary

        The notebook writes the D003 support artifacts to:

        - `notebooks/runs_new/boundary_conditions/ic_boundary_runs.csv`
        - `notebooks/runs_new/boundary_conditions/ic_boundary_summary.csv`
        - `notebooks/runs_new/boundary_conditions/ic_stress_runs.csv`
        - `notebooks/runs_new/boundary_conditions/ic_stress_summary.csv`
        - `notebooks/runs_new/boundary_conditions/ic_stress_crossing_summary.csv`
        - `notebooks/runs_new/boundary_conditions/inactive_count_runs.csv`
        - `notebooks/runs_new/boundary_conditions/inactive_count_summary.csv`
        - `notebooks/runs_new/boundary_conditions/threshold_bridge_sweep.csv`
        - `notebooks/runs_new/boundary_conditions/interval_bridge_summary.csv`
        - `notebooks/runs_new/boundary_conditions/negative_complement_summary.csv`
        - `notebooks/runs_new/boundary_conditions/boundary_conditions_summary.csv`
        - `notebooks/runs_new/boundary_conditions/boundary_takeaways.txt`

        and saves figures into `notebooks/Figures/`:

        - `boundary_ic_sweep.png`
        - `boundary_ic_stress_heatmaps.png`
        - `boundary_ic_stress_profiles.png`
        - `boundary_inactive_count_sweep.png`
        - `boundary_threshold_bridge.png`

        This is the minimal empirical package needed to replace the D003 placeholder with one regime-scoped subsection plus one figure/table pair.
        """
    ),
]

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "cutlass",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.11",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

out_path = Path(__file__).resolve().parents[1] / "notebooks" / "boundary_conditions.ipynb"
out_path.write_text(json.dumps(notebook, indent=2), encoding="utf-8")
print(f"Wrote notebook to {out_path}")
