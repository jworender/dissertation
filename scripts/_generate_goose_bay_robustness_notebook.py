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
        # Goose Bay Robustness Notebook

        This notebook addresses the ionosphere discrepancy raised during the D002 cross-domain analysis. Its purpose is to determine whether the difference between the 2022 Goose Bay result and the newer generic transfer probe is primarily due to:

        1. train/test split choice,
        2. rectification rule, or
        3. sparse-penalty strength.
        """
    ),
    md_cell(
        """
        ## Experiment Design

        The notebook uses the UCI ionosphere dataset in four protocol variants:

        1. **Generic probe**: the same standardized protocol used in `cross_domain.ipynb` (`70/30` split, `cutlass` rectification, `C=0.1`).
        2. **Split-matched cutlass**: same rectification and penalty as the generic probe, but with a Goose Bay style `67/33` class-stratified split.
        3. **Legacy rectifier bridge**: same Goose Bay style split, but replacing the generic quantile rectifier with a legacy-style positive-range min/max rectifier while keeping `C=0.1`.
        4. **Published-like legacy**: same Goose Bay style split and legacy rectifier, but using a much weaker penalty (`C=10`) that better mimics the least-penalized behavior of the original LLE pipeline.

        The repeated-split experiment runs all four protocols over a fixed seed set, then summarizes:

        - `delta_j = rectified_j - raw_j`
        - `delta_tpr = rectified_tpr - raw_tpr`
        - `delta_tnr = rectified_tnr - raw_tnr`
        - the fraction of seeds where rectification beats raw

        The 2022 paper values are also recorded as a separate reference point rather than being conflated with the standardized generic probe.
        """
    ),
    code_cell(
        """
        from __future__ import annotations

        import importlib
        import json
        from pathlib import Path
        from time import perf_counter

        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler

        try:
            from IPython.display import display
        except Exception:
            display = None

        for module_name in [name for name in list(globals()) if name == "cutlass" or str(name).startswith("cutlass.")]:
            pass

        cutlass = importlib.import_module("cutlass")
        DuplicateColumnConsolidator = cutlass.DuplicateColumnConsolidator
        Rectifier = cutlass.Rectifier

        plt.rcParams["figure.figsize"] = (10, 5)
        plt.rcParams["axes.grid"] = True
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
                    if (candidate / "scripts").is_dir() and (candidate / "notebooks").is_dir():
                        return candidate
            raise FileNotFoundError("Could not locate the dissertation repository root.")


        REPO_ROOT = _find_repo_root()
        NOTEBOOKS_DIR = REPO_ROOT / "notebooks"
        RAW_DATA_DIR = NOTEBOOKS_DIR / "raw_data"
        FIGURES_DIR = NOTEBOOKS_DIR / "Figures"
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        RUN_DIR = NOTEBOOKS_DIR / "runs_new" / "goose_bay_robustness"
        RUN_DIR.mkdir(parents=True, exist_ok=True)

        print("Repository root:", REPO_ROOT)
        print("Figures directory:", FIGURES_DIR)
        print("Run directory:", RUN_DIR)
        """
    ),
    code_cell(
        """
        DATA_PATH = RAW_DATA_DIR / "ionosphere.data"
        PAPER_REFERENCE = {
            "raw_tpr": 0.933,
            "raw_tnr": 0.762,
            "rect_tpr": 0.973,
            "rect_tnr": 0.881,
        }
        PAPER_REFERENCE["raw_j"] = PAPER_REFERENCE["raw_tpr"] + PAPER_REFERENCE["raw_tnr"] - 1.0
        PAPER_REFERENCE["rect_j"] = PAPER_REFERENCE["rect_tpr"] + PAPER_REFERENCE["rect_tnr"] - 1.0
        PAPER_REFERENCE["delta_j"] = PAPER_REFERENCE["rect_j"] - PAPER_REFERENCE["raw_j"]

        PROTOCOLS = [
            {
                "id": "generic_probe",
                "label": "Generic probe",
                "split": "generic70",
                "raw_c": 0.1,
                "rectifier": "cutlass",
                "rect_c": 0.1,
            },
            {
                "id": "matched_split_cutlass",
                "label": "Split-matched cutlass",
                "split": "legacy67",
                "raw_c": 0.1,
                "rectifier": "cutlass",
                "rect_c": 0.1,
            },
            {
                "id": "legacy_rectifier_bridge",
                "label": "Legacy rectifier bridge",
                "split": "legacy67",
                "raw_c": 0.1,
                "rectifier": "legacy",
                "rect_c": 0.1,
            },
            {
                "id": "published_like_legacy",
                "label": "Published-like legacy",
                "split": "legacy67",
                "raw_c": 10.0,
                "rectifier": "legacy",
                "rect_c": 10.0,
            },
        ]
        PROTOCOL_ORDER = [item["id"] for item in PROTOCOLS]
        PROTOCOL_LABELS = {item["id"]: item["label"] for item in PROTOCOLS}
        PROTOCOL_DISPLAY = {
            "generic_probe": "Generic probe\\n70/30, cutlass, C=0.1",
            "matched_split_cutlass": "Split-matched cutlass\\n67/33, cutlass, C=0.1",
            "legacy_rectifier_bridge": "Legacy rectifier bridge\\n67/33, min/max, C=0.1",
            "published_like_legacy": "Published-like legacy\\n67/33, min/max, C=10",
        }
        PROTOCOL_COLORS = {
            "generic_probe": "#7f8c8d",
            "matched_split_cutlass": "#4c78a8",
            "legacy_rectifier_bridge": "#f28e2b",
            "published_like_legacy": "#2ca02c",
        }
        EVAL_SEEDS = list(range(100)) + [2345]
        CUTLASS_RECTIFIER_KW = dict(sdfilter=None, snap=0.001, quantile_bounds=(0.25, 0.75))

        ionosphere_raw = pd.read_csv(DATA_PATH, header=None)
        X_FULL = ionosphere_raw.iloc[:, :-1].copy()
        X_FULL.columns = [f"F{i:02d}" for i in range(X_FULL.shape[1])]
        Y_FULL = (ionosphere_raw.iloc[:, -1] == "g").astype(int).to_numpy()

        config_view = pd.DataFrame(
            [
                {"Parameter": "Dataset", "Value": str(DATA_PATH)},
                {"Parameter": "Seed count", "Value": len(EVAL_SEEDS)},
                {"Parameter": "Special seed", "Value": 2345},
                {"Parameter": "Protocols", "Value": ", ".join(item["id"] for item in PROTOCOLS)},
                {"Parameter": "Paper reference delta J", "Value": f"{PAPER_REFERENCE['delta_j']:.3f}"},
            ]
        )
        if display is not None:
            display(config_view)
        else:
            print(config_view.to_string(index=False))
        """
    ),
    code_cell(
        """
        def format_numeric(value: float, digits: int = 3) -> str:
            if pd.isna(value):
                return "n/a"
            return f"{float(value):.{digits}f}"


        def split_r_like(seed: int, train_frac: float = 0.67):
            pos_idx = np.flatnonzero(Y_FULL == 1)
            neg_idx = np.flatnonzero(Y_FULL == 0)
            rng = np.random.RandomState(seed)
            pos_train = rng.choice(pos_idx, size=int(train_frac * len(pos_idx)), replace=False)
            neg_train = rng.choice(neg_idx, size=int(train_frac * len(neg_idx)), replace=False)
            train_idx = np.sort(np.concatenate([pos_train, neg_train]))
            test_mask = np.ones(len(Y_FULL), dtype=bool)
            test_mask[train_idx] = False
            test_idx = np.flatnonzero(test_mask)
            return (
                X_FULL.iloc[train_idx].reset_index(drop=True),
                X_FULL.iloc[test_idx].reset_index(drop=True),
                Y_FULL[train_idx],
                Y_FULL[test_idx],
            )


        def split_generic(seed: int, test_size: float = 0.30):
            X_train, X_test, y_train, y_test = train_test_split(
                X_FULL,
                Y_FULL,
                test_size=test_size,
                stratify=Y_FULL,
                random_state=seed,
            )
            return X_train.reset_index(drop=True), X_test.reset_index(drop=True), y_train, y_test


        def score_at_threshold(y_true, prob, threshold: float = 0.5) -> dict:
            y_arr = np.asarray(y_true).astype(int)
            prob_arr = np.asarray(prob, dtype=float)
            pred = (prob_arr >= threshold).astype(int)
            positives = y_arr == 1
            negatives = y_arr == 0
            tpr = float(np.mean(pred[positives] == 1))
            tnr = float(np.mean(pred[negatives] == 0))
            return {
                "j": float(tpr + tnr - 1.0),
                "tpr": tpr,
                "tnr": tnr,
            }


        def fit_sparse_logistic(X_train, y_train, X_test, y_test, *, C: float, standardize: bool) -> dict:
            Xtr = X_train
            Xte = X_test
            if standardize:
                scaler = StandardScaler().fit(X_train)
                Xtr = scaler.transform(X_train)
                Xte = scaler.transform(X_test)

            model = LogisticRegression(
                penalty="l1",
                solver="saga",
                C=float(C),
                max_iter=12000,
                tol=1e-4,
                random_state=42,
            )
            model.fit(Xtr, y_train)
            prob = model.predict_proba(Xte)[:, 1]
            threshold_metrics = score_at_threshold(y_test, prob, threshold=0.5)
            return {
                "j": threshold_metrics["j"],
                "tpr": threshold_metrics["tpr"],
                "tnr": threshold_metrics["tnr"],
                "nonzero_total": int((model.coef_.ravel() != 0).sum()),
            }


        def legacy_rectify(X_train: pd.DataFrame, y_train: np.ndarray, X_test: pd.DataFrame):
            positive_rows = X_train.loc[y_train == 1]
            lower = positive_rows.min(axis=0)
            upper = positive_rows.max(axis=0)
            X_train_rect = np.where((X_train >= lower) & (X_train <= upper), 1.0, -1.0)
            X_test_rect = np.where((X_test >= lower) & (X_test <= upper), 1.0, -1.0)
            return pd.DataFrame(X_train_rect, columns=X_train.columns), pd.DataFrame(X_test_rect, columns=X_train.columns)


        def cutlass_rectify(X_train: pd.DataFrame, y_train: np.ndarray, X_test: pd.DataFrame):
            rectifier = Rectifier(groups=None, **CUTLASS_RECTIFIER_KW)
            X_train_rect = rectifier.fit_transform(X_train, y_train)
            X_test_rect = rectifier.transform(X_test)
            consolidator = DuplicateColumnConsolidator(mode="none", expansion="split_evenly")
            X_train_fit = consolidator.fit_transform(X_train_rect, feature_names=rectifier.feature_names_)
            X_test_fit = consolidator.transform(X_test_rect, feature_names=rectifier.feature_names_)
            return X_train_fit, X_test_fit
        """
    ),
    code_cell(
        """
        def run_or_load_repeated_protocol_ablation(overwrite_cache: bool = False) -> pd.DataFrame:
            cache_path = RUN_DIR / "goose_bay_repeated_protocol_runs.csv"
            if cache_path.exists() and not overwrite_cache:
                df = pd.read_csv(cache_path)
                required_cols = {
                    "seed",
                    "protocol",
                    "protocol_label",
                    "split",
                    "rectifier",
                    "raw_c",
                    "rect_c",
                    "raw_j",
                    "rect_j",
                    "delta_j",
                    "raw_tpr",
                    "rect_tpr",
                    "delta_tpr",
                    "raw_tnr",
                    "rect_tnr",
                    "delta_tnr",
                    "raw_nonzero",
                    "rect_nonzero",
                }
                if required_cols.issubset(df.columns):
                    print("Loaded repeated protocol ablation from:", cache_path)
                    return df
                print("Repeated-protocol cache is missing required columns. Recomputing:", cache_path)

            rows = []
            start = perf_counter()

            for index, seed in enumerate(EVAL_SEEDS):
                split_cache = {}
                for protocol in PROTOCOLS:
                    split_key = protocol["split"]
                    if split_key not in split_cache:
                        if split_key == "legacy67":
                            split_cache[split_key] = split_r_like(seed, train_frac=0.67)
                        else:
                            split_cache[split_key] = split_generic(seed, test_size=0.30)
                    X_train, X_test, y_train, y_test = split_cache[split_key]

                    raw_result = fit_sparse_logistic(
                        X_train,
                        y_train,
                        X_test,
                        y_test,
                        C=protocol["raw_c"],
                        standardize=True,
                    )

                    if protocol["rectifier"] == "legacy":
                        X_train_rect, X_test_rect = legacy_rectify(X_train, y_train, X_test)
                    else:
                        X_train_rect, X_test_rect = cutlass_rectify(X_train, y_train, X_test)

                    rect_result = fit_sparse_logistic(
                        X_train_rect,
                        y_train,
                        X_test_rect,
                        y_test,
                        C=protocol["rect_c"],
                        standardize=False,
                    )

                    rows.append(
                        {
                            "seed": int(seed),
                            "protocol": protocol["id"],
                            "protocol_label": protocol["label"],
                            "split": protocol["split"],
                            "rectifier": protocol["rectifier"],
                            "raw_c": float(protocol["raw_c"]),
                            "rect_c": float(protocol["rect_c"]),
                            "raw_j": raw_result["j"],
                            "rect_j": rect_result["j"],
                            "delta_j": rect_result["j"] - raw_result["j"],
                            "raw_tpr": raw_result["tpr"],
                            "rect_tpr": rect_result["tpr"],
                            "delta_tpr": rect_result["tpr"] - raw_result["tpr"],
                            "raw_tnr": raw_result["tnr"],
                            "rect_tnr": rect_result["tnr"],
                            "delta_tnr": rect_result["tnr"] - raw_result["tnr"],
                            "raw_nonzero": raw_result["nonzero_total"],
                            "rect_nonzero": rect_result["nonzero_total"],
                        }
                    )

                if index % 20 == 0:
                    print(f"Completed seed {index + 1} / {len(EVAL_SEEDS)}")

            df = pd.DataFrame(rows)
            df.to_csv(cache_path, index=False)
            print(f"Saved repeated protocol ablation to: {cache_path} ({perf_counter() - start:.2f}s)")
            return df


        repeated_runs = run_or_load_repeated_protocol_ablation(overwrite_cache=False)
        if display is not None:
            display(repeated_runs.head())
        else:
            print(repeated_runs.head().to_string(index=False))
        """
    ),
    code_cell(
        """
        protocol_summary = (
            repeated_runs.groupby(["protocol", "protocol_label"], as_index=False)
            .agg(
                mean_delta_j=("delta_j", "mean"),
                median_delta_j=("delta_j", "median"),
                p05_delta_j=("delta_j", lambda s: float(np.quantile(s, 0.05))),
                p95_delta_j=("delta_j", lambda s: float(np.quantile(s, 0.95))),
                positive_fraction=("delta_j", lambda s: float((s > 0).mean())),
                mean_delta_tpr=("delta_tpr", "mean"),
                mean_delta_tnr=("delta_tnr", "mean"),
                mean_raw_j=("raw_j", "mean"),
                mean_rect_j=("rect_j", "mean"),
                mean_raw_nonzero=("raw_nonzero", "mean"),
                mean_rect_nonzero=("rect_nonzero", "mean"),
            )
        )
        protocol_summary["protocol"] = pd.Categorical(protocol_summary["protocol"], categories=PROTOCOL_ORDER, ordered=True)
        protocol_summary = protocol_summary.sort_values("protocol").reset_index(drop=True)
        protocol_summary.to_csv(RUN_DIR / "goose_bay_protocol_summary.csv", index=False)

        protocol_summary_formatted = protocol_summary.copy()
        for column in [
            "mean_delta_j",
            "median_delta_j",
            "p05_delta_j",
            "p95_delta_j",
            "positive_fraction",
            "mean_delta_tpr",
            "mean_delta_tnr",
            "mean_raw_j",
            "mean_rect_j",
            "mean_raw_nonzero",
            "mean_rect_nonzero",
        ]:
            protocol_summary_formatted[column] = protocol_summary_formatted[column].map(lambda value: format_numeric(value, 3))
        protocol_summary_formatted.to_csv(RUN_DIR / "goose_bay_protocol_summary_formatted.csv", index=False)

        if display is not None:
            display(protocol_summary_formatted)
        else:
            print(protocol_summary_formatted.to_string(index=False))
        """
    ),
    code_cell(
        """
        seed_2345 = repeated_runs[repeated_runs["seed"] == 2345].copy()
        seed_2345["protocol"] = pd.Categorical(seed_2345["protocol"], categories=PROTOCOL_ORDER, ordered=True)
        seed_2345 = seed_2345.sort_values("protocol").reset_index(drop=True)
        seed_2345.to_csv(RUN_DIR / "goose_bay_seed2345_decomposition.csv", index=False)

        seed_2345_table = seed_2345[
            [
                "protocol_label",
                "raw_j",
                "rect_j",
                "delta_j",
                "raw_tpr",
                "rect_tpr",
                "delta_tpr",
                "raw_tnr",
                "rect_tnr",
                "delta_tnr",
            ]
        ].copy()
        for column in seed_2345_table.columns[1:]:
            seed_2345_table[column] = seed_2345_table[column].map(lambda value: format_numeric(value, 3))
        seed_2345_table.to_csv(RUN_DIR / "goose_bay_seed2345_decomposition_formatted.csv", index=False)

        paper_reference_table = pd.DataFrame(
            [
                {
                    "source": "orender2022 paper",
                    "raw_tpr": PAPER_REFERENCE["raw_tpr"],
                    "raw_tnr": PAPER_REFERENCE["raw_tnr"],
                    "raw_j": PAPER_REFERENCE["raw_j"],
                    "rect_tpr": PAPER_REFERENCE["rect_tpr"],
                    "rect_tnr": PAPER_REFERENCE["rect_tnr"],
                    "rect_j": PAPER_REFERENCE["rect_j"],
                    "delta_j": PAPER_REFERENCE["delta_j"],
                }
            ]
        )
        paper_reference_table.to_csv(RUN_DIR / "goose_bay_paper_reference.csv", index=False)

        paper_reference_formatted = paper_reference_table.copy()
        for column in paper_reference_formatted.columns[1:]:
            paper_reference_formatted[column] = paper_reference_formatted[column].map(lambda value: format_numeric(value, 3))
        paper_reference_formatted.to_csv(RUN_DIR / "goose_bay_paper_reference_formatted.csv", index=False)

        if display is not None:
            display(seed_2345_table)
            display(paper_reference_formatted)
        else:
            print(seed_2345_table.to_string(index=False))
            print(paper_reference_formatted.to_string(index=False))
        """
    ),
    code_cell(
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        data = [
            repeated_runs.loc[repeated_runs["protocol"] == protocol_id, "delta_j"].to_numpy()
            for protocol_id in PROTOCOL_ORDER
        ]
        box = ax.boxplot(data, patch_artist=True, tick_labels=[PROTOCOL_DISPLAY[protocol_id] for protocol_id in PROTOCOL_ORDER])
        for patch, protocol_id in zip(box["boxes"], PROTOCOL_ORDER):
            patch.set_facecolor(PROTOCOL_COLORS[protocol_id])
            patch.set_alpha(0.65)

        ax.axhline(0.0, color="black", linewidth=1.0)
        published_x = PROTOCOL_ORDER.index("published_like_legacy") + 1
        ax.scatter(
            [published_x],
            [PAPER_REFERENCE["delta_j"]],
            marker="*",
            s=220,
            color="black",
            label="2022 paper delta J",
            zorder=5,
        )
        ax.set_ylabel("Delta Youden's J (rectified - raw)")
        ax.set_title("Goose Bay Repeated-Split Robustness Across Protocol Variants")
        ax.tick_params(axis="x", rotation=18)
        ax.legend(loc="upper left")
        fig.tight_layout()
        out_path = FIGURES_DIR / "goose_bay_delta_j_protocols.png"
        fig.savefig(out_path, dpi=160, bbox_inches="tight")
        plt.show(block=False)
        print("Saved:", out_path)
        """
    ),
    code_cell(
        """
        x = np.arange(len(PROTOCOL_ORDER))
        width = 0.36
        summary_indexed = protocol_summary.set_index("protocol")

        fig, ax = plt.subplots(figsize=(12, 5.8))
        delta_tpr = [summary_indexed.loc[protocol_id, "mean_delta_tpr"] for protocol_id in PROTOCOL_ORDER]
        delta_tnr = [summary_indexed.loc[protocol_id, "mean_delta_tnr"] for protocol_id in PROTOCOL_ORDER]
        ax.bar(x - width / 2, delta_tpr, width=width, color="#d62728", label="Mean delta TPR")
        ax.bar(x + width / 2, delta_tnr, width=width, color="#1f77b4", label="Mean delta TNR")
        ax.axhline(0.0, color="black", linewidth=1.0)
        ax.set_xticks(x)
        ax.set_xticklabels([PROTOCOL_DISPLAY[protocol_id] for protocol_id in PROTOCOL_ORDER], rotation=18, ha="right")
        ax.set_ylabel("Mean rectified - raw rate change")
        ax.set_title("Why the Goose Bay Result Moves: TPR vs TNR Effects")
        ax.legend(loc="upper left")
        fig.tight_layout()
        out_path = FIGURES_DIR / "goose_bay_delta_components.png"
        fig.savefig(out_path, dpi=160, bbox_inches="tight")
        plt.show(block=False)
        print("Saved:", out_path)
        """
    ),
    code_cell(
        """
        seed_indexed = seed_2345.set_index("protocol")

        fig, ax = plt.subplots(figsize=(12, 5.8))
        seed_delta = [seed_indexed.loc[protocol_id, "delta_j"] for protocol_id in PROTOCOL_ORDER]
        ax.bar(x, seed_delta, color=[PROTOCOL_COLORS[protocol_id] for protocol_id in PROTOCOL_ORDER])
        ax.axhline(0.0, color="black", linewidth=1.0)
        ax.scatter(
            [PROTOCOL_ORDER.index("published_like_legacy")],
            [PAPER_REFERENCE["delta_j"]],
            marker="*",
            s=220,
            color="black",
            label="2022 paper delta J",
            zorder=5,
        )
        ax.set_xticks(x)
        ax.set_xticklabels([PROTOCOL_DISPLAY[protocol_id] for protocol_id in PROTOCOL_ORDER], rotation=18, ha="right")
        ax.set_ylabel("Seed 2345 delta Youden's J")
        ax.set_title("Seed 2345 Decomposition: Split, Rectifier, and Penalty Effects")
        ax.legend(loc="upper left")
        fig.tight_layout()
        out_path = FIGURES_DIR / "goose_bay_seed2345_decomposition.png"
        fig.savefig(out_path, dpi=160, bbox_inches="tight")
        plt.show(block=False)
        print("Saved:", out_path)
        """
    ),
    code_cell(
        """
        summary_indexed = protocol_summary.set_index("protocol")
        takeaways = [
            (
                "Changing the split alone is not enough: the mean delta J stays near zero when moving from the generic probe "
                f"({summary_indexed.loc['generic_probe', 'mean_delta_j']:.3f}) to split-matched cutlass "
                f"({summary_indexed.loc['matched_split_cutlass', 'mean_delta_j']:.3f})."
            ),
            (
                "Changing the rectifier matters: under the same 67/33 split and C=0.1, the mean delta J rises to "
                f"{summary_indexed.loc['legacy_rectifier_bridge', 'mean_delta_j']:.3f} and is positive on "
                f"{100.0 * summary_indexed.loc['legacy_rectifier_bridge', 'positive_fraction']:.1f}% of seeds."
            ),
            (
                "The published-like protocol is robust in this approximation: mean delta J is "
                f"{summary_indexed.loc['published_like_legacy', 'mean_delta_j']:.3f}, positive on "
                f"{100.0 * summary_indexed.loc['published_like_legacy', 'positive_fraction']:.1f}% of seeds, and close to the paper's delta J of "
                f"{PAPER_REFERENCE['delta_j']:.3f}."
            ),
            (
                "On seed 2345 specifically, the delta J progression is "
                f"{seed_indexed.loc['generic_probe', 'delta_j']:.3f} -> "
                f"{seed_indexed.loc['matched_split_cutlass', 'delta_j']:.3f} -> "
                f"{seed_indexed.loc['legacy_rectifier_bridge', 'delta_j']:.3f} -> "
                f"{seed_indexed.loc['published_like_legacy', 'delta_j']:.3f}, "
                "which indicates that rectification rule and penalty strength matter more than split matching alone."
            ),
        ]

        takeaways_path = RUN_DIR / "goose_bay_takeaways.txt"
        takeaways_path.write_text("\\n".join(takeaways) + "\\n", encoding="utf-8")

        print("Goose Bay robustness takeaways:")
        for line in takeaways:
            print("-", line)
        print("Saved:", takeaways_path)
        """
    ),
    md_cell(
        """
        ## Artifact Summary

        The notebook writes the main tabular artifacts to:

        - `notebooks/runs_new/goose_bay_robustness/goose_bay_repeated_protocol_runs.csv`
        - `notebooks/runs_new/goose_bay_robustness/goose_bay_protocol_summary.csv`
        - `notebooks/runs_new/goose_bay_robustness/goose_bay_protocol_summary_formatted.csv`
        - `notebooks/runs_new/goose_bay_robustness/goose_bay_seed2345_decomposition.csv`
        - `notebooks/runs_new/goose_bay_robustness/goose_bay_seed2345_decomposition_formatted.csv`
        - `notebooks/runs_new/goose_bay_robustness/goose_bay_paper_reference.csv`
        - `notebooks/runs_new/goose_bay_robustness/goose_bay_paper_reference_formatted.csv`
        - `notebooks/runs_new/goose_bay_robustness/goose_bay_takeaways.txt`

        and saves figures into `notebooks/Figures/`:

        - `goose_bay_delta_j_protocols.png`
        - `goose_bay_delta_components.png`
        - `goose_bay_seed2345_decomposition.png`
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

out_path = Path(__file__).resolve().parents[1] / "notebooks" / "goose_bay_robustness.ipynb"
out_path.write_text(json.dumps(notebook, indent=2), encoding="utf-8")
print(f"Wrote notebook to {out_path}")
