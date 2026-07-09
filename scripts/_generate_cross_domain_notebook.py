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
        # Cross-Domain Benchmark Notebook

        This notebook is designed to fill **deficiency D002** for the dissertation. It extends the RQ1 evidence in two directions:

        1. a **synthetic baseline-expansion benchmark** that compares the rectification-first sparse pipeline against additional correlated-feature baselines on the raw lag-expanded design, and
        2. a **cross-domain transfer panel** that checks whether the raw-versus-rectified pattern persists outside the synthetic Case 1 setting.
        """
    ),
    md_cell(
        """
        ## Experiment Design

        The notebook produces four deliverables tied directly to D002:

        1. **One consolidated synthetic benchmark table** covering:
           - raw L1 logistic,
           - rectified L1 logistic,
           - raw elastic net,
           - raw adaptive L1,
           - raw grouped sparse logistic,
           - a practical ordered-lag prefix proxy,
           - quadratic-programming feature ranking plus sparse logistic refit,
           - raw random forest.
        2. **One synthetic comparison figure suite** showing discrimination, attribution fidelity, and runtime tradeoffs.
        3. **One cross-domain transfer summary** across multiple HAI attack subsets plus the UCI ionosphere radar benchmark.
        4. **A concise transferability narrative** derived from the measured domain-by-domain deltas.

        Notes:

        - The ordered comparator is implemented here as an **ordered prefix proxy baseline** because the repository does not bundle a dedicated ordered-lasso solver.
        - The HAI real-data path reuses the same `cutlass`-environment rectification ideas as the existing HAI notebook: robust quantile rectification plus duplicate-column consolidation before sparse fitting.
        - The ionosphere dataset is intentionally shown in **two separate views**:
          1. a published Goose Bay reference view taken from the 2022 paper, and
          2. a standardized generic transfer probe used only for the D002 cross-domain panel.
        """
    ),
    code_cell(
        """
        from __future__ import annotations

        import importlib
        import importlib.util
        import json
        import math
        import re
        import sys
        import warnings
        from pathlib import Path
        from time import perf_counter

        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        from groupyr import LogisticSGL
        from qp_feature_selection import create_opt_problem, normalize_design_and_target, solve_opt_problem
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import precision_recall_curve, roc_auc_score
        from sklearn.model_selection import StratifiedKFold, train_test_split
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler as SkStandardScaler

        try:
            import seaborn as sns
        except Exception:
            sns = None

        try:
            from IPython.display import display
        except Exception:
            display = None

        for module_name in [name for name in list(sys.modules) if name == "cutlass" or name.startswith("cutlass.")]:
            del sys.modules[module_name]

        cutlass = importlib.import_module("cutlass")
        DuplicateColumnConsolidator = cutlass.DuplicateColumnConsolidator
        Rectifier = cutlass.Rectifier
        calculate_youden_j = cutlass.calculate_youden_j

        plt.rcParams["figure.figsize"] = (10, 5)
        plt.rcParams["axes.grid"] = True
        if sns is not None:
            sns.set(style="whitegrid")
        warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn.linear_model._logistic")
        warnings.filterwarnings("ignore", message=r"Inconsistent values: penalty=.*", category=UserWarning)
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


        def _load_module(name: str, path: Path):
            spec = importlib.util.spec_from_file_location(name, str(path))
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            assert spec.loader is not None
            spec.loader.exec_module(module)
            return module


        REPO_ROOT = _find_repo_root()
        SCRIPTS_DIR = REPO_ROOT / "scripts"
        NOTEBOOKS_DIR = REPO_ROOT / "notebooks"
        RAW_DATA_DIR = NOTEBOOKS_DIR / "raw_data"
        PROCESSED_DIR = NOTEBOOKS_DIR / "processed_data"
        FIGURES_DIR = NOTEBOOKS_DIR / "Figures"
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        RUN_DIR = NOTEBOOKS_DIR / "runs_new" / "cross_domain"
        RUN_DIR.mkdir(parents=True, exist_ok=True)

        syn = _load_module("cross_domain_syn", SCRIPTS_DIR / "sensor_generate - commented.py")
        skcase = _load_module("cross_domain_skcase", SCRIPTS_DIR / "case_1_simple_script_scikit_fast_v6.py")

        print("Repository root:", REPO_ROOT)
        print("Figures directory:", FIGURES_DIR)
        print("Run directory:", RUN_DIR)
        """
    ),
    code_cell(
        """
        SYN_CONFIG = dict(
            num_examples=900,
            N=100,
            S=40,
            R=(5, 6, 9, 10, 15, 25, 30),
            AB=("a", "a", "b", "b", "a", "b", "n"),
            gp=(1, 1, 1, 1, 1, 1, 1),
            H=10,
            train_fr=0.70,
            disp=(
                0, 0, 0, 0, 10, 6, 0, 10, 1, 0,
                0, 0, 2, 0, 5, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 3, 0, 0, 0, 0, 7,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            ),
            thresh_a=0.30,
            thresh_b=0.65,
            tr_frac=0.25,
            pos_tol=5e-3,
            max_cycle_iters=10,
            max_thresh_iters=24,
            verbose=False,
            rseed=1234,
        )
        TRUE_FEATURES = [f"V{r}TM{SYN_CONFIG['disp'][r - 1]}" for r in SYN_CONFIG["R"]]

        SYN_BENCHMARK_PROTOCOL_VERSION = "synthetic-aa-v3-20260622"
        SYN_RANDOM_STATE = 1234
        SYN_CV = 3
        SYN_C_GRID = np.logspace(-2, 1, 3).astype(float)
        SYN_CV_RULE = "1se"
        SYN_SOLVER = "saga"
        SYN_TOL = 1e-3
        SYN_MAX_ITER = 800
        SYN_L1_KW = dict(
            cv=SYN_CV,
            cs=len(SYN_C_GRID),
            c_lo=float(np.log10(SYN_C_GRID[0])),
            c_hi=float(np.log10(SYN_C_GRID[-1])),
            solver=SYN_SOLVER,
            tol=SYN_TOL,
            max_iter=SYN_MAX_ITER,
            cv_rule=SYN_CV_RULE,
        )
        ENET_L1_RATIOS = [0.5]
        ADAPTIVE_EPS = 1e-3
        GROUP_ALPHA_GRID = [0.05, 0.01, 0.001]
        QP_K_GRID = [5, 10, 15]
        RAW_RF_BASE_KW = dict(
            n_estimators=500,
            class_weight="balanced_subsample",
            random_state=SYN_RANDOM_STATE,
            n_jobs=1,
        )
        RAW_RF_CANDIDATES = [
            {"max_features": "sqrt", "min_samples_leaf": 8},
            {"max_features": "sqrt", "min_samples_leaf": 4},
            {"max_features": "sqrt", "min_samples_leaf": 2},
        ]

        SYN_FAMILY_ORDER = [
            "l1",
            "enet",
            "adaptive_l1",
            "group_lasso",
            "ordered_prefix",
            "qp_selector",
            "random_forest",
        ]
        SYN_FAMILY_LABELS = {
            "l1": "L1",
            "enet": "Elastic Net",
            "adaptive_l1": "Adaptive L1",
            "group_lasso": "Group Lasso",
            "ordered_prefix": "Ordered Prefix",
            "qp_selector": "QP + L1",
            "random_forest": "Random Forest",
        }
        SYN_VIEW_ORDER = ["raw", "rectified"]
        SYN_VIEW_LABELS = {"raw": "Raw", "rectified": "Rectified"}
        SYN_VIEW_COLORS = {"raw": "#7f8c8d", "rectified": "#1f77b4"}
        SYN_METHOD_ORDER = [
            f"{view}_{family}"
            for family in SYN_FAMILY_ORDER
            for view in SYN_VIEW_ORDER
        ]
        SYN_METHOD_FAMILY = {
            method: family
            for family in SYN_FAMILY_ORDER
            for method in (f"raw_{family}", f"rectified_{family}")
        }
        SYN_METHOD_VIEW = {
            method: view
            for family in SYN_FAMILY_ORDER
            for view, method in (("raw", f"raw_{family}"), ("rectified", f"rectified_{family}"))
        }
        SYN_METHOD_LABELS = {
            method: f"{SYN_VIEW_LABELS[SYN_METHOD_VIEW[method]]} {SYN_FAMILY_LABELS[SYN_METHOD_FAMILY[method]]}"
            for method in SYN_METHOD_ORDER
        }
        SYN_METHOD_COLORS = {
            method: SYN_VIEW_COLORS[SYN_METHOD_VIEW[method]]
            for method in SYN_METHOD_ORDER
        }

        HAI_TARGETS = {
            "HAI attack_p2 (a1)": dict(tag="a1"),
            "HAI attack_p1p2 (a2)": dict(tag="a2"),
            "HAI attack_p3 (a3)": dict(tag="a3"),
            "HAI attack_p1p3 (a4)": dict(tag="a4"),
        }

        RAW_HAI_C = 0.012
        RECT_HAI_C = 0.012
        HAI_RECTIFIER_KW = dict(sdfilter=None, snap=0.001, quantile_bounds=(0.35, 0.65))
        HAI_DUPLICATE_MODE = "within_group"

        IONO_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/ionosphere/ionosphere.data"
        IONO_CACHE = RAW_DATA_DIR / "ionosphere.data"
        IONO_RAW_C = 0.1
        IONO_RECT_C = 0.1
        IONO_RECTIFIER_KW = dict(sdfilter=None, snap=0.001, quantile_bounds=(0.25, 0.75))
        PUBLISHED_GOOSE_BAY = {
            "rectified_l1": {"tpr_test": 0.973, "tnr_test": 0.881},
            "raw_l1": {"tpr_test": 0.933, "tnr_test": 0.762},
        }

        OVERWRITE_CACHE = False

        config_view = pd.DataFrame(
            [
                {"Parameter": "Synthetic true features", "Value": ", ".join(TRUE_FEATURES)},
                {"Parameter": "Synthetic methods", "Value": ", ".join(SYN_METHOD_ORDER)},
                {"Parameter": "HAI targets", "Value": ", ".join(f"{label}:{spec['tag']}" for label, spec in HAI_TARGETS.items())},
                {"Parameter": "Ionosphere cache", "Value": str(IONO_CACHE)},
                {"Parameter": "Ionosphere published reference", "Value": "orender2022 Goose Bay case"},
                {"Parameter": "Notebook kernel", "Value": "cutlass"},
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
        SYN_FEATURE_RE = re.compile(r"^V(\\d+)TM(\\d+)$")


        def parse_synthetic_feature(name: str):
            match = SYN_FEATURE_RE.match(str(name))
            if not match:
                return None
            return int(match.group(1)), int(match.group(2))


        def lag_metrics(selected: list[str], truth: list[str], tol: int = 0) -> tuple[float, float, float]:
            selected_parsed = [item for item in (parse_synthetic_feature(x) for x in selected) if item is not None]
            truth_parsed = [item for item in (parse_synthetic_feature(x) for x in truth) if item is not None]
            matched_truth = set()
            hits = 0
            for variable, lag in selected_parsed:
                for j, (truth_variable, truth_lag) in enumerate(truth_parsed):
                    if j in matched_truth:
                        continue
                    if variable == truth_variable and abs(lag - truth_lag) <= tol:
                        matched_truth.add(j)
                        hits += 1
                        break
            precision = hits / max(len(selected_parsed), 1)
            recall = hits / max(len(truth_parsed), 1)
            f1 = 2 * precision * recall / max(precision + recall, 1e-9)
            return precision, recall, f1


        def top_features_from_series(beta: pd.Series, k: int = 7) -> tuple[list[str], pd.Series]:
            beta = beta[beta != 0].copy()
            if beta.empty:
                return [], beta
            beta = beta.reindex(beta.abs().sort_values(ascending=False).index)
            return beta.index[: min(k, len(beta))].tolist(), beta


        def metric_row(y_true, prob, *, threshold: float = 0.5) -> dict:
            y_arr = np.asarray(y_true).astype(int)
            prob_arr = np.asarray(prob, dtype=float)
            pred = (prob_arr >= threshold).astype(int)
            precision, recall, _ = precision_recall_curve(y_arr, prob_arr)
            f1 = 2 * precision * recall / np.clip(precision + recall, 1e-9, None)
            return {
                "auc_test": float(roc_auc_score(y_arr, prob_arr)),
                "j_test": float(calculate_youden_j(y_arr, pred)),
                "f1max_test": float(np.nanmax(f1)),
            }


        def threshold_rates(y_true, prob, *, threshold: float = 0.5) -> dict:
            y_arr = np.asarray(y_true).astype(int)
            prob_arr = np.asarray(prob, dtype=float)
            pred = (prob_arr >= threshold).astype(int)
            positives = y_arr == 1
            negatives = y_arr == 0
            tp = int(np.sum((pred == 1) & positives))
            tn = int(np.sum((pred == 0) & negatives))
            fp = int(np.sum((pred == 1) & negatives))
            fn = int(np.sum((pred == 0) & positives))
            tpr = tp / max(int(np.sum(positives)), 1)
            tnr = tn / max(int(np.sum(negatives)), 1)
            return {
                "tp": tp,
                "tn": tn,
                "fp": fp,
                "fn": fn,
                "tpr_test": float(tpr),
                "tnr_test": float(tnr),
            }


        def synthetic_group_arrays(feature_names: list[str]) -> list[np.ndarray]:
            mapping: dict[int | str, list[int]] = {}
            for idx, name in enumerate(feature_names):
                parsed = parse_synthetic_feature(name)
                key = parsed[0] if parsed is not None else name
                mapping.setdefault(key, []).append(idx)
            return [np.asarray(mapping[key], dtype=int) for key in sorted(mapping)]


        def format_numeric(value: float, digits: int = 3) -> str:
            if pd.isna(value):
                return "n/a"
            return f"{float(value):.{digits}f}"


        def domain_transfer_takeaways(summary_df: pd.DataFrame) -> list[str]:
            improved = summary_df.loc[(summary_df["delta_auc"] > 0) & (summary_df["delta_j"] > 0), "domain"].tolist()
            mixed = summary_df.loc[(summary_df["delta_auc"] > 0) ^ (summary_df["delta_j"] > 0), "domain"].tolist()
            declined = summary_df.loc[(summary_df["delta_auc"] <= 0) & (summary_df["delta_j"] <= 0), "domain"].tolist()
            lines = []
            if improved:
                lines.append("Under the standardized generic protocol, rectification improves both AUC and J on: " + ", ".join(improved))
            if mixed:
                lines.append("Under the standardized generic protocol, rectification is mixed across metrics on: " + ", ".join(mixed))
            if declined:
                lines.append("Under the standardized generic protocol, rectification does not dominate on: " + ", ".join(declined))
            return lines
        """
    ),
    code_cell(
        """
        def _raw_synthetic_xy(train_df: pd.DataFrame, test_df: pd.DataFrame) -> tuple[pd.DataFrame, np.ndarray, pd.DataFrame, np.ndarray]:
            raw_train = train_df[[c for c in train_df.columns if c not in skcase.EXCLUDE_COLS]].copy()
            raw_test = test_df[[c for c in test_df.columns if c not in skcase.EXCLUDE_COLS]].copy()
            X_train = raw_train.drop(columns=["INDC"])
            y_train = raw_train["INDC"].astype(int).to_numpy()
            X_test = raw_test.drop(columns=["INDC"])
            y_test = raw_test["INDC"].astype(int).to_numpy()
            return X_train, y_train, X_test, y_test


        def _rectified_synthetic_xy(train_df: pd.DataFrame, test_df: pd.DataFrame) -> tuple[pd.DataFrame, np.ndarray, pd.DataFrame, np.ndarray]:
            groups = skcase.organize(train_df)
            rt_train, limits = skcase.rectify_fast(train_df, groups, limits=None, sdfilter=3.0, snap=0.001)
            rt_test, _ = skcase.rectify_fast(test_df, groups, limits=limits, sdfilter=3.0, snap=0.001)
            X_train = rt_train.drop(columns=["INDC"])
            y_train = rt_train["INDC"].astype(int).to_numpy()
            X_test = rt_test.drop(columns=["INDC"])
            y_test = rt_test["INDC"].astype(int).to_numpy()
            return X_train, y_train, X_test, y_test


        def _synthetic_xy(
            train_df: pd.DataFrame,
            test_df: pd.DataFrame,
            *,
            view: str,
        ) -> tuple[pd.DataFrame, np.ndarray, pd.DataFrame, np.ndarray]:
            if view == "raw":
                return _raw_synthetic_xy(train_df, test_df)
            if view == "rectified":
                return _rectified_synthetic_xy(train_df, test_df)
            raise ValueError(f"Unknown synthetic representation: {view}")


        def _binary_log_loss(y_true: np.ndarray, prob: np.ndarray) -> float:
            y_arr = np.asarray(y_true, dtype=float)
            prob_arr = np.clip(np.asarray(prob, dtype=float), 1e-12, 1.0 - 1e-12)
            return float(-(y_arr * np.log(prob_arr) + (1.0 - y_arr) * np.log(1.0 - prob_arr)).mean())


        def _synthetic_cv_splits(y: np.ndarray) -> list[tuple[np.ndarray, np.ndarray]]:
            splitter = StratifiedKFold(n_splits=SYN_CV, shuffle=True, random_state=SYN_RANDOM_STATE)
            return list(splitter.split(np.zeros(len(y)), y))


        def _select_loss_candidate(losses: np.ndarray) -> tuple[int, np.ndarray, np.ndarray]:
            mean_losses = losses.mean(axis=0)
            se_losses = losses.std(axis=0, ddof=1) / np.sqrt(losses.shape[0]) if losses.shape[0] > 1 else np.zeros_like(mean_losses)
            best_idx = int(np.argmin(mean_losses))
            if SYN_CV_RULE == "1se":
                threshold = mean_losses[best_idx] + se_losses[best_idx]
                eligible = np.flatnonzero(mean_losses <= threshold)
                selected_idx = int(eligible[0]) if eligible.size else best_idx
            else:
                selected_idx = best_idx
            return selected_idx, mean_losses, se_losses


        def _make_logistic(C: float, *, penalty: str = "l1", l1_ratio: float | None = None, max_iter: int = SYN_MAX_ITER) -> LogisticRegression:
            kwargs = dict(
                penalty=penalty,
                solver=SYN_SOLVER,
                C=float(C),
                tol=SYN_TOL,
                max_iter=int(max_iter),
                random_state=SYN_RANDOM_STATE,
                warm_start=False,
                fit_intercept=True,
            )
            if penalty == "elasticnet":
                kwargs["l1_ratio"] = float(l1_ratio)
            return LogisticRegression(**kwargs)


        def _scaled_pair(X_fit, X_apply):
            scaler = SkStandardScaler().fit(X_fit)
            return scaler.transform(X_fit), scaler.transform(X_apply), scaler


        def _fit_linear_external_cv(
            X_train: pd.DataFrame,
            y_train: np.ndarray,
            X_test: pd.DataFrame,
            *,
            penalty: str = "l1",
            l1_ratios: list[float | None] | None = None,
            use_scaler: bool = True,
        ) -> tuple[np.ndarray, pd.Series, dict]:
            ratios = [None] if l1_ratios is None else list(l1_ratios)
            candidates = [{"C": float(C), "l1_ratio": ratio} for C in SYN_C_GRID for ratio in ratios]
            folds = _synthetic_cv_splits(y_train)
            losses = np.empty((len(folds), len(candidates)), dtype=float)

            X_arr = X_train.to_numpy(dtype=float)
            X_test_arr = X_test.to_numpy(dtype=float)
            for fold_idx, (train_idx, valid_idx) in enumerate(folds):
                X_fold_train = X_arr[train_idx]
                X_fold_valid = X_arr[valid_idx]
                if use_scaler:
                    X_fold_train, X_fold_valid, _ = _scaled_pair(X_fold_train, X_fold_valid)
                for cand_idx, candidate in enumerate(candidates):
                    model = _make_logistic(candidate["C"], penalty=penalty, l1_ratio=candidate["l1_ratio"])
                    model.fit(X_fold_train, y_train[train_idx])
                    losses[fold_idx, cand_idx] = _binary_log_loss(y_train[valid_idx], model.predict_proba(X_fold_valid)[:, 1])

            selected_idx, mean_losses, se_losses = _select_loss_candidate(losses)
            selected = candidates[selected_idx]
            X_final = X_arr
            X_test_final = X_test_arr
            if use_scaler:
                X_final, X_test_final, _ = _scaled_pair(X_final, X_test_final)
            final_model = _make_logistic(selected["C"], penalty=penalty, l1_ratio=selected["l1_ratio"])
            final_model.fit(X_final, y_train)
            prob = final_model.predict_proba(X_test_final)[:, 1]
            beta = pd.Series(final_model.coef_.ravel(), index=X_train.columns, name="coef")
            info = {
                "selected_C": float(selected["C"]),
                "selected_l1_ratio": np.nan if selected["l1_ratio"] is None else float(selected["l1_ratio"]),
                "cv_candidate_count": int(len(candidates)),
                "fit_count": int(len(folds) * len(candidates) + 1),
                "iteration_budget": int(SYN_MAX_ITER),
                "cv_mean_loss": float(mean_losses[selected_idx]),
                "cv_se_loss": float(se_losses[selected_idx]),
            }
            return prob, beta, info


        def _finish_synthetic_row(method: str, y_test: np.ndarray, prob: np.ndarray, scores: pd.Series, start: float, info: dict | None = None) -> dict:
            selected_topk, _ = top_features_from_series(scores, k=len(TRUE_FEATURES))
            metrics = metric_row(y_test, prob)
            _, _, exact_f1 = lag_metrics(selected_topk, TRUE_FEATURES, tol=0)
            row = {
                "method": method,
                "method_family": SYN_METHOD_FAMILY[method],
                "family_label": SYN_FAMILY_LABELS[SYN_METHOD_FAMILY[method]],
                "representation": SYN_METHOD_VIEW[method],
                "representation_label": SYN_VIEW_LABELS[SYN_METHOD_VIEW[method]],
                "protocol_version": SYN_BENCHMARK_PROTOCOL_VERSION,
                **metrics,
                "lag_f1_exact": float(exact_f1),
                "nonzero_total": int((scores != 0).sum()),
                "selected_features": "|".join(selected_topk),
                "runtime_seconds": float(perf_counter() - start),
            }
            if info:
                row.update(info)
            return row


        def _view_uses_scaler(view: str) -> bool:
            return view == "raw"


        def _maybe_scaled_pair(X_fit, X_apply, *, use_scaler: bool):
            if use_scaler:
                return _scaled_pair(X_fit, X_apply)
            return np.asarray(X_fit, dtype=float), np.asarray(X_apply, dtype=float), None


        def _add_view_info(info: dict, view: str) -> dict:
            return {**info, "rectification_included": bool(view == "rectified")}


        def fit_l1_synthetic(train_df: pd.DataFrame, test_df: pd.DataFrame, *, view: str) -> dict:
            start = perf_counter()
            X_train, y_train, X_test, y_test = _synthetic_xy(train_df, test_df, view=view)
            prob, beta, info = _fit_linear_external_cv(
                X_train,
                y_train,
                X_test,
                penalty="l1",
                use_scaler=_view_uses_scaler(view),
            )
            return _finish_synthetic_row(f"{view}_l1", y_test, prob, beta, start, _add_view_info(info, view))


        def fit_enet_synthetic(train_df: pd.DataFrame, test_df: pd.DataFrame, *, view: str) -> dict:
            start = perf_counter()
            X_train, y_train, X_test, y_test = _synthetic_xy(train_df, test_df, view=view)
            prob, beta, info = _fit_linear_external_cv(
                X_train,
                y_train,
                X_test,
                penalty="elasticnet",
                l1_ratios=ENET_L1_RATIOS,
                use_scaler=_view_uses_scaler(view),
            )
            return _finish_synthetic_row(f"{view}_enet", y_test, prob, beta, start, _add_view_info(info, view))


        def fit_adaptive_l1_synthetic(train_df: pd.DataFrame, test_df: pd.DataFrame, *, view: str) -> dict:
            start = perf_counter()
            use_scaler = _view_uses_scaler(view)
            X_train, y_train, X_test, y_test = _synthetic_xy(train_df, test_df, view=view)
            X_arr = X_train.to_numpy(dtype=float)
            X_test_arr = X_test.to_numpy(dtype=float)
            folds = _synthetic_cv_splits(y_train)
            losses = np.empty((len(folds), len(SYN_C_GRID)), dtype=float)

            for fold_idx, (train_idx, valid_idx) in enumerate(folds):
                X_fold_train, X_fold_valid, _ = _maybe_scaled_pair(
                    X_arr[train_idx],
                    X_arr[valid_idx],
                    use_scaler=use_scaler,
                )
                pilot = LogisticRegression(C=1.0, penalty="l2", solver="lbfgs", max_iter=SYN_MAX_ITER, tol=SYN_TOL, random_state=SYN_RANDOM_STATE)
                pilot.fit(X_fold_train, y_train[train_idx])
                weights = 1.0 / (np.abs(pilot.coef_.ravel()) + ADAPTIVE_EPS)
                X_weighted_train = X_fold_train / weights
                X_weighted_valid = X_fold_valid / weights
                for cand_idx, C in enumerate(SYN_C_GRID):
                    model = _make_logistic(float(C), penalty="l1")
                    model.fit(X_weighted_train, y_train[train_idx])
                    losses[fold_idx, cand_idx] = _binary_log_loss(y_train[valid_idx], model.predict_proba(X_weighted_valid)[:, 1])

            selected_idx, mean_losses, se_losses = _select_loss_candidate(losses)
            selected_C = float(SYN_C_GRID[selected_idx])
            X_final, X_test_final, _ = _maybe_scaled_pair(X_arr, X_test_arr, use_scaler=use_scaler)
            pilot = LogisticRegression(C=1.0, penalty="l2", solver="lbfgs", max_iter=SYN_MAX_ITER, tol=SYN_TOL, random_state=SYN_RANDOM_STATE)
            pilot.fit(X_final, y_train)
            weights = 1.0 / (np.abs(pilot.coef_.ravel()) + ADAPTIVE_EPS)
            final_model = _make_logistic(selected_C, penalty="l1")
            final_model.fit(X_final / weights, y_train)
            prob = final_model.predict_proba(X_test_final / weights)[:, 1]
            beta = pd.Series(final_model.coef_.ravel() / weights, index=X_train.columns, name="coef")
            info = {
                "selected_C": selected_C,
                "selected_l1_ratio": np.nan,
                "cv_candidate_count": int(len(SYN_C_GRID)),
                "fit_count": int(len(folds) * (len(SYN_C_GRID) + 1) + 2),
                "iteration_budget": int(SYN_MAX_ITER),
                "cv_mean_loss": float(mean_losses[selected_idx]),
                "cv_se_loss": float(se_losses[selected_idx]),
                "pilot_fit_count": int(len(folds) + 1),
            }
            return _finish_synthetic_row(f"{view}_adaptive_l1", y_test, prob, beta, start, _add_view_info(info, view))


        def fit_group_lasso_synthetic(train_df: pd.DataFrame, test_df: pd.DataFrame, *, view: str) -> dict:
            start = perf_counter()
            use_scaler = _view_uses_scaler(view)
            X_train, y_train, X_test, y_test = _synthetic_xy(train_df, test_df, view=view)
            X_arr = X_train.to_numpy(dtype=float)
            X_test_arr = X_test.to_numpy(dtype=float)
            groups = synthetic_group_arrays(X_train.columns.tolist())
            folds = _synthetic_cv_splits(y_train)
            losses = np.empty((len(folds), len(GROUP_ALPHA_GRID)), dtype=float)

            for fold_idx, (train_idx, valid_idx) in enumerate(folds):
                X_fold_train, X_fold_valid, _ = _maybe_scaled_pair(
                    X_arr[train_idx],
                    X_arr[valid_idx],
                    use_scaler=use_scaler,
                )
                for cand_idx, alpha in enumerate(GROUP_ALPHA_GRID):
                    model = LogisticSGL(
                        l1_ratio=0.0,
                        alpha=float(alpha),
                        groups=groups,
                        scale_l2_by="group_length",
                        max_iter=SYN_MAX_ITER,
                        tol=SYN_TOL,
                        suppress_solver_warnings=True,
                    )
                    model.fit(X_fold_train, y_train[train_idx])
                    losses[fold_idx, cand_idx] = _binary_log_loss(y_train[valid_idx], model.predict_proba(X_fold_valid)[:, 1])

            selected_idx, mean_losses, se_losses = _select_loss_candidate(losses)
            selected_alpha = float(GROUP_ALPHA_GRID[selected_idx])
            X_final, X_test_final, _ = _maybe_scaled_pair(X_arr, X_test_arr, use_scaler=use_scaler)
            final_model = LogisticSGL(
                l1_ratio=0.0,
                alpha=selected_alpha,
                groups=groups,
                scale_l2_by="group_length",
                max_iter=SYN_MAX_ITER,
                tol=SYN_TOL,
                suppress_solver_warnings=True,
            )
            final_model.fit(X_final, y_train)
            prob = final_model.predict_proba(X_test_final)[:, 1]
            beta = pd.Series(np.asarray(final_model.coef_).ravel(), index=X_train.columns, name="coef")
            info = {
                "selected_alpha": selected_alpha,
                "tuned_alpha": selected_alpha,
                "cv_candidate_count": int(len(GROUP_ALPHA_GRID)),
                "fit_count": int(len(folds) * len(GROUP_ALPHA_GRID) + 1),
                "iteration_budget": int(SYN_MAX_ITER),
                "cv_mean_loss": float(mean_losses[selected_idx]),
                "cv_se_loss": float(se_losses[selected_idx]),
            }
            return _finish_synthetic_row(f"{view}_group_lasso", y_test, prob, beta, start, _add_view_info(info, view))


        def _ordered_prefix_design(X_fit: pd.DataFrame, y_fit: np.ndarray, X_apply: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
            train_features = {}
            apply_features = {}
            for variable in range(1, SYN_CONFIG["S"] + 1):
                lag_cols = [f"V{variable}TM{lag}" for lag in range(SYN_CONFIG["H"] + 1)]
                lag_cols = [col for col in lag_cols if col in X_fit.columns]
                best_auc = -np.inf
                best_label = None
                best_train_feature = None
                best_apply_feature = None
                for idx in range(len(lag_cols)):
                    cols = lag_cols[: idx + 1]
                    train_feature = X_fit[cols].mean(axis=1).to_numpy()
                    apply_feature = X_apply[cols].mean(axis=1).to_numpy()
                    auc = roc_auc_score(y_fit, train_feature)
                    if auc < 0.5:
                        auc = 1.0 - auc
                        train_feature = -train_feature
                        apply_feature = -apply_feature
                    if auc > best_auc:
                        best_auc = auc
                        best_label = f"V{variable}TM{idx}"
                        best_train_feature = train_feature
                        best_apply_feature = apply_feature
                train_features[best_label] = best_train_feature
                apply_features[best_label] = best_apply_feature
            return pd.DataFrame(train_features), pd.DataFrame(apply_features)


        def fit_ordered_prefix_synthetic(train_df: pd.DataFrame, test_df: pd.DataFrame, *, view: str) -> dict:
            start = perf_counter()
            use_scaler = _view_uses_scaler(view)
            X_train, y_train, X_test, y_test = _synthetic_xy(train_df, test_df, view=view)
            folds = _synthetic_cv_splits(y_train)
            losses = np.empty((len(folds), len(SYN_C_GRID)), dtype=float)

            for fold_idx, (train_idx, valid_idx) in enumerate(folds):
                X_prefix_train, X_prefix_valid = _ordered_prefix_design(X_train.iloc[train_idx], y_train[train_idx], X_train.iloc[valid_idx])
                X_fold_train = X_prefix_train.to_numpy(dtype=float)
                X_fold_valid = X_prefix_valid.to_numpy(dtype=float)
                X_fold_train, X_fold_valid, _ = _maybe_scaled_pair(
                    X_fold_train,
                    X_fold_valid,
                    use_scaler=use_scaler,
                )
                for cand_idx, C in enumerate(SYN_C_GRID):
                    model = _make_logistic(float(C), penalty="l1")
                    model.fit(X_fold_train, y_train[train_idx])
                    losses[fold_idx, cand_idx] = _binary_log_loss(y_train[valid_idx], model.predict_proba(X_fold_valid)[:, 1])

            selected_idx, mean_losses, se_losses = _select_loss_candidate(losses)
            selected_C = float(SYN_C_GRID[selected_idx])
            X_prefix_train, X_prefix_test = _ordered_prefix_design(X_train, y_train, X_test)
            X_final, X_test_final, _ = _maybe_scaled_pair(
                X_prefix_train.to_numpy(dtype=float),
                X_prefix_test.to_numpy(dtype=float),
                use_scaler=use_scaler,
            )
            final_model = _make_logistic(selected_C, penalty="l1")
            final_model.fit(X_final, y_train)
            prob = final_model.predict_proba(X_test_final)[:, 1]
            beta = pd.Series(final_model.coef_.ravel(), index=X_prefix_train.columns, name="coef")
            info = {
                "selected_C": selected_C,
                "selected_l1_ratio": np.nan,
                "cv_candidate_count": int(len(SYN_C_GRID)),
                "fit_count": int(len(folds) * len(SYN_C_GRID) + 1),
                "iteration_budget": int(SYN_MAX_ITER),
                "cv_mean_loss": float(mean_losses[selected_idx]),
                "cv_se_loss": float(se_losses[selected_idx]),
            }
            return _finish_synthetic_row(f"{view}_ordered_prefix", y_test, prob, beta, start, _add_view_info(info, view))


        def _qp_feature_ranking(X_fit: pd.DataFrame, y_fit: np.ndarray) -> np.ndarray:
            X_norm, y_norm = normalize_design_and_target(X_fit.to_numpy(dtype=float), y_fit.astype(float))
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in divide")
                Q, b = create_opt_problem(X_norm, y_norm, sim="correl", rel="correl")
            qp_weights = solve_opt_problem(Q, b)
            return np.argsort(np.abs(qp_weights))[::-1]


        def fit_qp_selector_synthetic(train_df: pd.DataFrame, test_df: pd.DataFrame, *, view: str) -> dict:
            start = perf_counter()
            use_scaler = _view_uses_scaler(view)
            X_train, y_train, X_test, y_test = _synthetic_xy(train_df, test_df, view=view)
            candidate_pairs = [(int(k), float(C)) for k in QP_K_GRID for C in SYN_C_GRID]
            folds = _synthetic_cv_splits(y_train)
            losses = np.empty((len(folds), len(candidate_pairs)), dtype=float)

            for fold_idx, (train_idx, valid_idx) in enumerate(folds):
                X_fold_df = X_train.iloc[train_idx]
                X_valid_df = X_train.iloc[valid_idx]
                ranking = _qp_feature_ranking(X_fold_df, y_train[train_idx])
                for cand_idx, (k, C) in enumerate(candidate_pairs):
                    cols = X_train.columns[ranking[:k]].tolist()
                    X_fold_train, X_fold_valid, _ = _maybe_scaled_pair(
                        X_fold_df[cols].to_numpy(dtype=float),
                        X_valid_df[cols].to_numpy(dtype=float),
                        use_scaler=use_scaler,
                    )
                    model = _make_logistic(C, penalty="l1")
                    model.fit(X_fold_train, y_train[train_idx])
                    losses[fold_idx, cand_idx] = _binary_log_loss(y_train[valid_idx], model.predict_proba(X_fold_valid)[:, 1])

            selected_idx, mean_losses, se_losses = _select_loss_candidate(losses)
            selected_k, selected_C = candidate_pairs[selected_idx]
            ranking = _qp_feature_ranking(X_train, y_train)
            best_cols = X_train.columns[ranking[:selected_k]].tolist()
            X_final, X_test_final, _ = _maybe_scaled_pair(
                X_train[best_cols].to_numpy(dtype=float),
                X_test[best_cols].to_numpy(dtype=float),
                use_scaler=use_scaler,
            )
            final_model = _make_logistic(selected_C, penalty="l1")
            final_model.fit(X_final, y_train)
            prob = final_model.predict_proba(X_test_final)[:, 1]
            beta = pd.Series(final_model.coef_.ravel(), index=best_cols, name="coef")
            info = {
                "selected_C": float(selected_C),
                "selected_l1_ratio": np.nan,
                "chosen_k": int(selected_k),
                "cv_candidate_count": int(len(candidate_pairs)),
                "fit_count": int(len(folds) * len(candidate_pairs) + 1),
                "qp_solve_count": int(len(folds) + 1),
                "iteration_budget": int(SYN_MAX_ITER),
                "cv_mean_loss": float(mean_losses[selected_idx]),
                "cv_se_loss": float(se_losses[selected_idx]),
            }
            return _finish_synthetic_row(f"{view}_qp_selector", y_test, prob, beta, start, _add_view_info(info, view))


        def fit_random_forest_synthetic(train_df: pd.DataFrame, test_df: pd.DataFrame, *, view: str) -> dict:
            start = perf_counter()
            X_train, y_train, X_test, y_test = _synthetic_xy(train_df, test_df, view=view)
            folds = _synthetic_cv_splits(y_train)
            losses = np.empty((len(folds), len(RAW_RF_CANDIDATES)), dtype=float)

            for fold_idx, (train_idx, valid_idx) in enumerate(folds):
                for cand_idx, candidate in enumerate(RAW_RF_CANDIDATES):
                    params = {**RAW_RF_BASE_KW, **candidate}
                    model = RandomForestClassifier(**params)
                    model.fit(X_train.iloc[train_idx], y_train[train_idx])
                    losses[fold_idx, cand_idx] = _binary_log_loss(y_train[valid_idx], model.predict_proba(X_train.iloc[valid_idx])[:, 1])

            selected_idx, mean_losses, se_losses = _select_loss_candidate(losses)
            selected_params = {**RAW_RF_BASE_KW, **RAW_RF_CANDIDATES[selected_idx]}
            final_model = RandomForestClassifier(**selected_params)
            final_model.fit(X_train, y_train)
            prob = final_model.predict_proba(X_test)[:, 1]
            importance = pd.Series(final_model.feature_importances_, index=X_train.columns, name="importance")
            info = {
                "cv_candidate_count": int(len(RAW_RF_CANDIDATES)),
                "fit_count": int(len(folds) * len(RAW_RF_CANDIDATES) + 1),
                "iteration_budget": int(RAW_RF_BASE_KW["n_estimators"]),
                "selected_min_samples_leaf": int(selected_params["min_samples_leaf"]),
                "cv_mean_loss": float(mean_losses[selected_idx]),
                "cv_se_loss": float(se_losses[selected_idx]),
            }
            return _finish_synthetic_row(f"{view}_random_forest", y_test, prob, importance, start, _add_view_info(info, view))
        """
    ),
    md_cell(
        """
        ## Synthetic Baseline Expansion

        This section expands the baseline set on the synthetic Case 1 generator. The goal is to test whether stronger penalty design on the **raw** lag-expanded representation can match the attribution behavior of a simpler **rectification-first** sparse model.

        Runtime is measured as end-to-end wall time for each method-specific calculation after the common synthetic train/test split has been generated. That includes method-specific preprocessing, rectification where applicable, feature construction or ranking, cross-validation, final refit, prediction, metric extraction, and support extraction. Logistic-family comparisons use the same stratified folds, log-loss selection rule, `C` grid, tolerance, max-iteration budget, and no-warm-start fits; method-specific extra stages such as adaptive-L1 pilot fits or QP ranking are counted in the method's runtime.
        """
    ),
    code_cell(
        """
        def run_or_load_synthetic_benchmark(overwrite_cache: bool = False) -> pd.DataFrame:
            cache_path = RUN_DIR / "synthetic_baseline_runs.csv"
            expected_methods = set(SYN_METHOD_ORDER)
            if cache_path.exists() and not overwrite_cache:
                df = pd.read_csv(cache_path)
                cached_methods = set(df.get("method", pd.Series(dtype=str)).astype(str))
                missing_methods = sorted(expected_methods.difference(cached_methods))
                protocol_ok = (
                    "protocol_version" in df.columns
                    and set(df["protocol_version"].dropna().astype(str)) == {SYN_BENCHMARK_PROTOCOL_VERSION}
                )
                if not missing_methods and protocol_ok:
                    print("Loaded synthetic benchmark from:", cache_path)
                    return df
                reasons = []
                if missing_methods:
                    reasons.append("missing methods: " + ", ".join(missing_methods))
                if not protocol_ok:
                    reasons.append("stale protocol")
                print("Synthetic benchmark cache is stale; recomputing (" + "; ".join(reasons) + ")")

            cfg = dict(SYN_CONFIG)
            full_df, train_df, test_df = syn.generate_synthetic_dataset_nexamples(**cfg)

            rows = [
                fit_l1_synthetic(train_df, test_df, view="raw"),
                fit_l1_synthetic(train_df, test_df, view="rectified"),
                fit_enet_synthetic(train_df, test_df, view="raw"),
                fit_enet_synthetic(train_df, test_df, view="rectified"),
                fit_adaptive_l1_synthetic(train_df, test_df, view="raw"),
                fit_adaptive_l1_synthetic(train_df, test_df, view="rectified"),
                fit_group_lasso_synthetic(train_df, test_df, view="raw"),
                fit_group_lasso_synthetic(train_df, test_df, view="rectified"),
                fit_ordered_prefix_synthetic(train_df, test_df, view="raw"),
                fit_ordered_prefix_synthetic(train_df, test_df, view="rectified"),
                fit_qp_selector_synthetic(train_df, test_df, view="raw"),
                fit_qp_selector_synthetic(train_df, test_df, view="rectified"),
                fit_random_forest_synthetic(train_df, test_df, view="raw"),
                fit_random_forest_synthetic(train_df, test_df, view="rectified"),
            ]

            df = pd.DataFrame(rows)
            df.to_csv(cache_path, index=False)
            print("Saved synthetic benchmark to:", cache_path)
            return df


        synthetic_runs = run_or_load_synthetic_benchmark(overwrite_cache=OVERWRITE_CACHE)
        synthetic_runs["method_label"] = synthetic_runs["method"].map(SYN_METHOD_LABELS)
        synthetic_runs = synthetic_runs.set_index("method").loc[SYN_METHOD_ORDER].reset_index()
        if display is not None:
            display(synthetic_runs)
        else:
            print(synthetic_runs.to_string(index=False))
        """
    ),
    code_cell(
        """
        synthetic_summary = synthetic_runs[
            [
                "method",
                "method_label",
                "family_label",
                "representation_label",
                "auc_test",
                "j_test",
                "lag_f1_exact",
                "nonzero_total",
                "runtime_seconds",
                "fit_count",
                "cv_candidate_count",
                "iteration_budget",
                "selected_features",
            ]
        ].copy()
        synthetic_summary.to_csv(RUN_DIR / "synthetic_baseline_summary.csv", index=False)

        synthetic_table = synthetic_summary.copy()
        for col in ["auc_test", "j_test", "lag_f1_exact", "runtime_seconds"]:
            synthetic_table[col] = synthetic_table[col].map(lambda value: format_numeric(value, 3))
        for col in ["nonzero_total", "fit_count", "cv_candidate_count", "iteration_budget"]:
            synthetic_table[col] = synthetic_table[col].astype(int)
        synthetic_table.to_csv(RUN_DIR / "synthetic_baseline_summary_formatted.csv", index=False)

        if display is not None:
            display(synthetic_table)
        else:
            print(synthetic_table.to_string(index=False))
        """
    ),
    code_cell(
        """
        def _latex_text(value) -> str:
            text = str(value)
            replacements = {
                "&": r"\\&",
                "%": r"\\%",
                "#": r"\\#",
                "_": r"\\_",
            }
            for old, new in replacements.items():
                text = text.replace(old, new)
            return text


        def _latex_num(value: float, digits: int = 3) -> str:
            return f"${float(value):.{digits}f}$"


        latex_source = synthetic_runs.copy()
        latex_source["latex_family_order"] = latex_source["method_family"].map(
            {family: idx for idx, family in enumerate(SYN_FAMILY_ORDER)}
        )
        latex_source["latex_status_order"] = latex_source["representation"].map({"rectified": 0, "raw": 1})
        latex_source = latex_source.sort_values(["latex_family_order", "latex_status_order"])
        rectified_l1_time = float(latex_source.loc[latex_source["method"] == "rectified_l1", "runtime_seconds"].iloc[0])

        latex_rows = []
        for row in latex_source.itertuples(index=False):
            latex_rows.append(
                " & ".join(
                    [
                        _latex_text(row.family_label),
                        _latex_text(row.representation_label),
                        _latex_num(row.runtime_seconds / rectified_l1_time, 1),
                        _latex_num(row.auc_test, 3),
                        _latex_num(row.j_test, 3),
                        _latex_num(row.f1max_test, 3),
                        _latex_num(row.lag_f1_exact, 3),
                    ]
                )
                + r" \\\\"
            )

        synthetic_latex_table = "\\n".join(
            [
                r"\\begin{tabular}{llccccc}",
                r"\\toprule",
                r"Method & Status & Rel. Time & AUC & Youden's $J$ & $F_1$ Max & $F_1$ Exact Lag \\\\",
                r"\\midrule",
                *latex_rows,
                r"\\bottomrule",
                r"\\end{tabular}",
            ]
        )

        print(synthetic_latex_table)
        """
    ),
    code_cell(
        """
        plot_metrics = [
            ("auc_test", "Test AUC"),
            ("j_test", "Test Youden's J"),
            ("lag_f1_exact", "Exact-Lag F1"),
            ("runtime_seconds", "Runtime (s)"),
        ]

        fig, axes = plt.subplots(2, 2, figsize=(13, 8))
        axes = axes.ravel()
        x = np.arange(len(SYN_FAMILY_ORDER))
        family_labels = [SYN_FAMILY_LABELS[family] for family in SYN_FAMILY_ORDER]
        width = 0.38

        for ax, (metric, title) in zip(axes, plot_metrics):
            for view_idx, view in enumerate(SYN_VIEW_ORDER):
                view_df = (
                    synthetic_runs[synthetic_runs["representation"] == view]
                    .set_index("method_family")
                    .reindex(SYN_FAMILY_ORDER)
                )
                offset = (view_idx - 0.5) * width
                ax.bar(
                    x + offset,
                    view_df[metric].to_numpy(),
                    width=width,
                    color=SYN_VIEW_COLORS[view],
                    label=SYN_VIEW_LABELS[view],
                )
            ax.set_xticks(x)
            ax.set_xticklabels(family_labels, rotation=25, ha="right")
            ax.set_title(title)
            if metric == "runtime_seconds":
                ax.set_yscale("log")
            ax.grid(True, axis="y", alpha=0.3)
        axes[0].legend(frameon=False, ncol=2, loc="lower right")

        fig.suptitle("D002 Synthetic Baseline Expansion", fontsize=16, y=0.98)
        fig.tight_layout()
        out_path = FIGURES_DIR / "cross_domain_synthetic_benchmark.png"
        fig.savefig(out_path, dpi=160, bbox_inches="tight")
        plt.show(block=False)
        print("Saved:", out_path)
        """
    ),
    code_cell(
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        label_offsets = {
            "l1": (1.03, 0.018),
            "enet": (1.06, -0.002),
            "adaptive_l1": (1.03, 0.0),
            "group_lasso": (1.04, 0.0),
            "ordered_prefix": (1.04, 0.0),
            "qp_selector": (1.03, -0.012),
            "random_forest": (1.08, 0.012),
        }
        for family in SYN_FAMILY_ORDER:
            pair = (
                synthetic_runs[synthetic_runs["method_family"] == family]
                .set_index("representation")
                .reindex(SYN_VIEW_ORDER)
            )
            ax.plot(
                pair["runtime_seconds"].to_numpy(),
                pair["lag_f1_exact"].to_numpy(),
                color="#b0b0b0",
                linewidth=1.2,
                zorder=1,
            )
            for row in pair.itertuples():
                ax.scatter(
                    row.runtime_seconds,
                    row.lag_f1_exact,
                    s=110,
                    color=SYN_VIEW_COLORS[row.Index],
                    alpha=0.9,
                label=SYN_VIEW_LABELS[row.Index],
                zorder=2,
            )
            rect_row = pair.loc["rectified"]
            x_mult, y_delta = label_offsets.get(family, (1.03, 0.0))
            ax.text(
                rect_row["runtime_seconds"] * x_mult,
                rect_row["lag_f1_exact"] + y_delta,
                SYN_FAMILY_LABELS[family],
                fontsize=9,
                va="center",
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.75, pad=1.5),
            )

        ax.set_xscale("log")
        ax.set_xlabel("Runtime (s, log scale)")
        ax.set_ylabel("Exact-Lag F1")
        ax.set_title("Synthetic Baseline Frontier: Runtime vs Attribution Fidelity")
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), frameon=False, loc="upper right")
        ax.margins(x=0.12, y=0.08)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        out_path = FIGURES_DIR / "cross_domain_synthetic_frontier.png"
        fig.savefig(out_path, dpi=160, bbox_inches="tight")
        plt.show(block=False)
        print("Saved:", out_path)
        """
    ),
    md_cell(
        """
        ## Cross-Domain Transfer Panel

        The second half of D002 asks whether the representation-first pattern transfers beyond the core synthetic comparison. This section evaluates a lighter core comparison, **raw L1 vs. rectified L1**, across multiple HAI attack subsets and the UCI ionosphere radar benchmark.

        Important distinction:

        - The HAI domains and the ionosphere row below are part of one **standardized generic transfer protocol** used for cross-domain comparison.
        - The ionosphere result in this panel is **not** a replication of the 2022 Goose Bay case study.
        - A separate section later in the notebook reconstructs the **published Goose Bay reference view** directly from the reported 2022 paper values and places it beside the generic probe so the two should not be conflated.
        """
    ),
    code_cell(
        """
        def prepare_cutlass_rectified_design(
            X_train: pd.DataFrame,
            y_train: np.ndarray,
            X_test: pd.DataFrame,
            *,
            rectifier_kw: dict,
            duplicate_mode: str = "within_group",
        ) -> dict:
            rectifier = Rectifier(groups=None, **rectifier_kw)
            X_train_rect = rectifier.fit_transform(X_train, y_train)
            X_test_rect = rectifier.transform(X_test)
            consolidator = DuplicateColumnConsolidator(mode=duplicate_mode, expansion="split_evenly")
            X_train_fit = consolidator.fit_transform(X_train_rect, feature_names=rectifier.feature_names_)
            X_test_fit = consolidator.transform(X_test_rect, feature_names=rectifier.feature_names_)
            return {
                "rectifier": rectifier,
                "consolidator": consolidator,
                "X_train_fit": X_train_fit,
                "X_test_fit": X_test_fit,
                "rectified_feature_names": list(rectifier.feature_names_),
                "fit_feature_names": list(consolidator.feature_names_),
            }


        def expanded_cutlass_coefficients(design: dict, coef_fit: np.ndarray) -> pd.Series:
            coef_fit_series = pd.Series(np.asarray(coef_fit).ravel(), index=design["fit_feature_names"], name="coef")
            coef_full = design["consolidator"].expand_coefficients(coef_fit_series)
            return pd.Series(np.asarray(coef_full).ravel(), index=design["rectified_feature_names"], name="coef")


        def fit_cutlass_raw_fixed_l1(
            X_train: pd.DataFrame,
            y_train: np.ndarray,
            X_test: pd.DataFrame,
            y_test: np.ndarray,
            *,
            fixed_c: float,
            max_iter: int = 6000,
            tol: float = 1e-4,
        ) -> dict:
            start = perf_counter()
            scaler = SkStandardScaler().fit(X_train)
            X_train_scaled = scaler.transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            lr = LogisticRegression(
                penalty="l1",
                solver="saga",
                C=float(fixed_c),
                max_iter=max_iter,
                tol=tol,
                random_state=42,
            )
            lr.fit(X_train_scaled, y_train)
            prob = lr.predict_proba(X_test_scaled)[:, 1]
            metrics = {**metric_row(y_test, prob), **threshold_rates(y_test, prob)}
            coef = pd.Series(lr.coef_.ravel(), index=X_train.columns, name="coef")
            return {
                "coef": coef,
                "prob": prob,
                "metrics": {
                    **metrics,
                    "nonzero_total": int((coef != 0).sum()),
                    "runtime_seconds": float(perf_counter() - start),
                    "chosen_C": float(fixed_c),
                },
            }


        def fit_cutlass_rectified_fixed_l1(
            X_train: pd.DataFrame,
            y_train: np.ndarray,
            X_test: pd.DataFrame,
            y_test: np.ndarray,
            *,
            fixed_c: float,
            rectifier_kw: dict,
            duplicate_mode: str,
            max_iter: int = 12000,
            tol: float = 1e-4,
        ) -> dict:
            start = perf_counter()
            design = prepare_cutlass_rectified_design(
                X_train,
                y_train,
                X_test,
                rectifier_kw=rectifier_kw,
                duplicate_mode=duplicate_mode,
            )
            lr = LogisticRegression(
                penalty="l1",
                solver="saga",
                C=float(fixed_c),
                max_iter=max_iter,
                tol=tol,
                random_state=42,
            )
            lr.fit(design["X_train_fit"], y_train)
            prob = lr.predict_proba(design["X_test_fit"])[:, 1]
            metrics = {**metric_row(y_test, prob), **threshold_rates(y_test, prob)}
            coef = expanded_cutlass_coefficients(design, lr.coef_)
            return {
                "coef": coef,
                "prob": prob,
                "metrics": {
                    **metrics,
                    "nonzero_total": int((coef != 0).sum()),
                    "runtime_seconds": float(perf_counter() - start),
                    "chosen_C": float(fixed_c),
                    "fit_features": int(design["X_train_fit"].shape[1]),
                },
            }


        def load_or_cache_ionosphere() -> pd.DataFrame:
            if IONO_CACHE.exists():
                df = pd.read_csv(IONO_CACHE, header=None)
            else:
                df = pd.read_csv(IONO_URL, header=None)
                IONO_CACHE.parent.mkdir(parents=True, exist_ok=True)
                df.to_csv(IONO_CACHE, header=False, index=False)
            return df


        def run_or_load_cross_domain_panel(overwrite_cache: bool = False) -> pd.DataFrame:
            cache_path = RUN_DIR / "cross_domain_transfer_runs.csv"
            if cache_path.exists() and not overwrite_cache:
                df = pd.read_csv(cache_path)
                required_columns = {
                    "domain",
                    "dataset_family",
                    "method",
                    "sample_train",
                    "sample_test",
                    "auc_test",
                    "j_test",
                    "f1max_test",
                    "tpr_test",
                    "tnr_test",
                    "nonzero_total",
                    "runtime_seconds",
                    "chosen_C",
                }
                if required_columns.issubset(df.columns):
                    print("Loaded cross-domain panel from:", cache_path)
                    return df
                print("Cross-domain cache is missing required columns. Recomputing:", cache_path)

            rows = []

            for domain_label, spec in HAI_TARGETS.items():
                tag = spec["tag"]
                train_df = pd.read_parquet(PROCESSED_DIR / f"train_{tag}_sm_hai.parquet")
                test_df = pd.read_parquet(PROCESSED_DIR / f"test_{tag}_sm_hai.parquet")

                X_train = train_df.drop(columns=["INDC"])
                y_train = train_df["INDC"].astype(int).to_numpy()
                X_test = test_df.drop(columns=["INDC"])
                y_test = test_df["INDC"].astype(int).to_numpy()

                raw_result = fit_cutlass_raw_fixed_l1(X_train, y_train, X_test, y_test, fixed_c=RAW_HAI_C)
                rect_result = fit_cutlass_rectified_fixed_l1(
                    X_train,
                    y_train,
                    X_test,
                    y_test,
                    fixed_c=RECT_HAI_C,
                    rectifier_kw=HAI_RECTIFIER_KW,
                    duplicate_mode=HAI_DUPLICATE_MODE,
                )

                rows.append(
                    {
                        "domain": domain_label,
                        "dataset_family": "HAI",
                        "method": "raw_l1",
                        "sample_train": int(len(X_train)),
                        "sample_test": int(len(X_test)),
                        **raw_result["metrics"],
                    }
                )
                rows.append(
                    {
                        "domain": domain_label,
                        "dataset_family": "HAI",
                        "method": "rectified_l1",
                        "sample_train": int(len(X_train)),
                        "sample_test": int(len(X_test)),
                        **rect_result["metrics"],
                    }
                )
                print(f"Completed HAI panel for {domain_label}")

            iono_raw = load_or_cache_ionosphere()
            X_iono = iono_raw.iloc[:, :-1].copy()
            X_iono.columns = [f"F{i:02d}" for i in range(X_iono.shape[1])]
            y_iono = (iono_raw.iloc[:, -1] == "g").astype(int).to_numpy()
            X_train, X_test, y_train, y_test = train_test_split(
                X_iono,
                y_iono,
                test_size=0.30,
                stratify=y_iono,
                random_state=42,
            )

            raw_result = fit_cutlass_raw_fixed_l1(X_train, y_train, X_test, y_test, fixed_c=IONO_RAW_C)
            rect_result = fit_cutlass_rectified_fixed_l1(
                X_train,
                y_train,
                X_test,
                y_test,
                fixed_c=IONO_RECT_C,
                rectifier_kw=IONO_RECTIFIER_KW,
                duplicate_mode="none",
            )

            rows.append(
                {
                    "domain": "Ionosphere radar",
                    "dataset_family": "Radar",
                    "method": "raw_l1",
                    "sample_train": int(len(X_train)),
                    "sample_test": int(len(X_test)),
                    **raw_result["metrics"],
                }
            )
            rows.append(
                {
                    "domain": "Ionosphere radar",
                    "dataset_family": "Radar",
                    "method": "rectified_l1",
                    "sample_train": int(len(X_train)),
                    "sample_test": int(len(X_test)),
                    **rect_result["metrics"],
                }
            )

            df = pd.DataFrame(rows)
            df.to_csv(cache_path, index=False)
            print("Saved cross-domain panel to:", cache_path)
            return df


        cross_domain_runs = run_or_load_cross_domain_panel(overwrite_cache=OVERWRITE_CACHE)
        if display is not None:
            display(cross_domain_runs)
        else:
            print(cross_domain_runs.to_string(index=False))
        """
    ),
    code_cell(
        """
        domain_order = list(HAI_TARGETS.keys()) + ["Ionosphere radar"]
        summary_rows = []
        for domain in domain_order:
            domain_df = cross_domain_runs[cross_domain_runs["domain"] == domain].set_index("method")
            raw_row = domain_df.loc["raw_l1"]
            rect_row = domain_df.loc["rectified_l1"]
            summary_rows.append(
                {
                    "domain": domain,
                    "dataset_family": raw_row["dataset_family"],
                    "sample_train": int(raw_row["sample_train"]),
                    "sample_test": int(raw_row["sample_test"]),
                    "raw_auc": float(raw_row["auc_test"]),
                    "rectified_auc": float(rect_row["auc_test"]),
                    "delta_auc": float(rect_row["auc_test"] - raw_row["auc_test"]),
                    "raw_j": float(raw_row["j_test"]),
                    "rectified_j": float(rect_row["j_test"]),
                    "delta_j": float(rect_row["j_test"] - raw_row["j_test"]),
                    "raw_tpr": float(raw_row["tpr_test"]),
                    "rectified_tpr": float(rect_row["tpr_test"]),
                    "raw_tnr": float(raw_row["tnr_test"]),
                    "rectified_tnr": float(rect_row["tnr_test"]),
                    "raw_nonzero": int(raw_row["nonzero_total"]),
                    "rectified_nonzero": int(rect_row["nonzero_total"]),
                    "raw_runtime": float(raw_row["runtime_seconds"]),
                    "rectified_runtime": float(rect_row["runtime_seconds"]),
                }
            )

        transfer_summary = pd.DataFrame(summary_rows)
        transfer_summary.to_csv(RUN_DIR / "cross_domain_transfer_summary.csv", index=False)

        transfer_summary_formatted = transfer_summary.copy()
        for column in [
            "raw_auc",
            "rectified_auc",
            "delta_auc",
            "raw_j",
            "rectified_j",
            "delta_j",
            "raw_tpr",
            "rectified_tpr",
            "raw_tnr",
            "rectified_tnr",
            "raw_runtime",
            "rectified_runtime",
        ]:
            transfer_summary_formatted[column] = transfer_summary_formatted[column].map(lambda value: format_numeric(value, 3))
        transfer_summary_formatted.to_csv(RUN_DIR / "cross_domain_transfer_summary_formatted.csv", index=False)

        if display is not None:
            display(transfer_summary_formatted)
        else:
            print(transfer_summary_formatted.to_string(index=False))
        """
    ),
    code_cell(
        """
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharex=True)
        x = np.arange(len(transfer_summary))

        axes[0].bar(x, transfer_summary["delta_auc"].to_numpy(), color="#1f77b4")
        axes[0].axhline(0.0, color="black", linewidth=1.0)
        axes[0].set_title("Rectified minus Raw AUC")
        axes[0].set_xticks(x)
        axes[0].set_xticklabels(transfer_summary["domain"], rotation=30, ha="right")
        axes[0].grid(True, axis="y", alpha=0.3)

        axes[1].bar(x, transfer_summary["delta_j"].to_numpy(), color="#d62728")
        axes[1].axhline(0.0, color="black", linewidth=1.0)
        axes[1].set_title("Rectified minus Raw Youden's J")
        axes[1].set_xticks(x)
        axes[1].set_xticklabels(transfer_summary["domain"], rotation=30, ha="right")
        axes[1].grid(True, axis="y", alpha=0.3)

        fig.suptitle("Cross-Domain Transfer Deltas (Generic Protocol)", fontsize=16, y=0.98)
        fig.tight_layout()
        out_path = FIGURES_DIR / "cross_domain_transfer_deltas.png"
        fig.savefig(out_path, dpi=160, bbox_inches="tight")
        plt.show(block=False)
        print("Saved:", out_path)
        """
    ),
    code_cell(
        """
        fig, ax = plt.subplots(figsize=(10, 5.5))
        x = np.arange(len(transfer_summary))
        width = 0.35
        ax.bar(x - width / 2, transfer_summary["raw_nonzero"].to_numpy(), width=width, label="Raw L1", color="#7f8c8d")
        ax.bar(x + width / 2, transfer_summary["rectified_nonzero"].to_numpy(), width=width, label="Rectified L1", color="#1f77b4")
        ax.set_xticks(x)
        ax.set_xticklabels(transfer_summary["domain"], rotation=30, ha="right")
        ax.set_ylabel("Nonzero coefficients")
        ax.set_title("Cross-Domain Sparsity Comparison (Generic Protocol)")
        ax.legend()
        ax.grid(True, axis="y", alpha=0.3)
        fig.tight_layout()
        out_path = FIGURES_DIR / "cross_domain_sparsity.png"
        fig.savefig(out_path, dpi=160, bbox_inches="tight")
        plt.show(block=False)
        print("Saved:", out_path)
        """
    ),
    md_cell(
        """
        ## Ionosphere Protocol Distinction

        The ionosphere dataset appears in this notebook for two different reasons:

        1. **Published Goose Bay reference view**: the values reported in the 2022 paper, retained for continuity with the original publication.
        2. **Generic transfer probe**: the standardized `cutlass`-based protocol used in this notebook so ionosphere can participate in the same D002 transfer panel as the HAI domains.

        These are not the same experiment. The published Goose Bay view uses the original LLE study protocol, while the generic transfer probe uses the standardized cross-domain notebook protocol. The comparison below keeps both views visible while preventing the negative delta in the generic probe from being misread as a contradiction of the published result.
        """
    ),
    code_cell(
        """
        generic_ionosphere = cross_domain_runs[cross_domain_runs["domain"] == "Ionosphere radar"].copy()
        generic_ionosphere["view"] = "Generic transfer probe"
        generic_ionosphere["source"] = "cross_domain.ipynb standardized protocol"
        generic_ionosphere["notes"] = "70/30 stratified split, random_state=42, fixed-C cutlass sparse logistic"

        published_rows = []
        for method, rates in PUBLISHED_GOOSE_BAY.items():
            published_rows.append(
                {
                    "view": "Published 2022 Goose Bay reference",
                    "source": "orender2022 paper",
                    "notes": "Original LLE R pipeline, 67/33 class-stratified split, rseed=2345",
                    "method": method,
                    "dataset_family": "Radar",
                    "domain": "Ionosphere radar",
                    "sample_train": np.nan,
                    "sample_test": np.nan,
                    "auc_test": np.nan,
                    "j_test": float(rates["tpr_test"] + rates["tnr_test"] - 1.0),
                    "f1max_test": np.nan,
                    "tpr_test": float(rates["tpr_test"]),
                    "tnr_test": float(rates["tnr_test"]),
                    "nonzero_total": np.nan,
                    "runtime_seconds": np.nan,
                    "chosen_C": np.nan,
                    "fit_features": np.nan,
                }
            )

        published_ionosphere = pd.DataFrame(published_rows)
        ionosphere_protocol_comparison = pd.concat([published_ionosphere, generic_ionosphere], ignore_index=True, sort=False)
        ionosphere_protocol_comparison["method_label"] = ionosphere_protocol_comparison["method"].map(
            {"raw_l1": "Raw L1", "rectified_l1": "Rectified L1"}
        )
        ionosphere_protocol_comparison = ionosphere_protocol_comparison[
            ["view", "method", "method_label", "tpr_test", "tnr_test", "j_test", "auc_test", "source", "notes"]
        ].copy()
        ionosphere_protocol_comparison.to_csv(RUN_DIR / "ionosphere_protocol_comparison.csv", index=False)

        ionosphere_protocol_table = ionosphere_protocol_comparison.copy()
        for column in ["tpr_test", "tnr_test", "j_test", "auc_test"]:
            ionosphere_protocol_table[column] = ionosphere_protocol_table[column].map(lambda value: format_numeric(value, 3))
        ionosphere_protocol_table.to_csv(RUN_DIR / "ionosphere_protocol_comparison_formatted.csv", index=False)

        if display is not None:
            display(ionosphere_protocol_table)
        else:
            print(ionosphere_protocol_table.to_string(index=False))
        """
    ),
    code_cell(
        """
        view_order = ["Published 2022 Goose Bay reference", "Generic transfer probe"]
        method_order = ["raw_l1", "rectified_l1"]
        method_colors = {"raw_l1": "#7f8c8d", "rectified_l1": "#1f77b4"}
        metric_specs = [
            ("tpr_test", "True Positive Rate"),
            ("tnr_test", "True Negative Rate"),
            ("j_test", "Youden's J"),
        ]

        fig, axes = plt.subplots(1, 3, figsize=(15, 4.8))
        x = np.arange(len(view_order))
        width = 0.32

        for ax, (metric, title) in zip(axes, metric_specs):
            for offset, method in [(-width / 2, "raw_l1"), (width / 2, "rectified_l1")]:
                values = []
                for view in view_order:
                    row = ionosphere_protocol_comparison[
                        (ionosphere_protocol_comparison["view"] == view)
                        & (ionosphere_protocol_comparison["method"] == method)
                    ].iloc[0]
                    values.append(float(row[metric]))
                ax.bar(
                    x + offset,
                    values,
                    width=width,
                    color=method_colors[method],
                    label={"raw_l1": "Raw L1", "rectified_l1": "Rectified L1"}[method] if metric == "tpr_test" else None,
                )
            ax.set_xticks(x)
            ax.set_xticklabels(["Published 2022\\nreference", "Generic\\nprobe"])
            ax.set_title(title)
            ax.grid(True, axis="y", alpha=0.3)
            if metric in {"tpr_test", "tnr_test"}:
                ax.set_ylim(0.65, 1.0)

        axes[0].legend(loc="lower right")
        fig.suptitle("Ionosphere: Published Goose Bay Reference vs Generic Transfer Probe", fontsize=16, y=0.98)
        fig.tight_layout()
        out_path = FIGURES_DIR / "cross_domain_ionosphere_protocol_comparison.png"
        fig.savefig(out_path, dpi=160, bbox_inches="tight")
        plt.show(block=False)
        print("Saved:", out_path)
        """
    ),
    code_cell(
        """
        takeaways = domain_transfer_takeaways(transfer_summary)
        takeaways_path = RUN_DIR / "cross_domain_takeaways.txt"
        takeaways_path.write_text("\\n".join(takeaways) + "\\n", encoding="utf-8")

        print("Transferability summary for the standardized generic protocol:")
        for line in takeaways:
            print("-", line)
        print("Saved:", takeaways_path)
        """
    ),
    md_cell(
        """
        ## Artifact Summary

        The notebook writes the core artifacts to:

        - `notebooks/runs_new/cross_domain/synthetic_baseline_runs.csv`
        - `notebooks/runs_new/cross_domain/synthetic_baseline_summary.csv`
        - `notebooks/runs_new/cross_domain/synthetic_baseline_summary_formatted.csv`
        - `notebooks/runs_new/cross_domain/cross_domain_transfer_runs.csv`
        - `notebooks/runs_new/cross_domain/cross_domain_transfer_summary.csv`
        - `notebooks/runs_new/cross_domain/cross_domain_transfer_summary_formatted.csv`
        - `notebooks/runs_new/cross_domain/ionosphere_protocol_comparison.csv`
        - `notebooks/runs_new/cross_domain/ionosphere_protocol_comparison_formatted.csv`
        - `notebooks/runs_new/cross_domain/cross_domain_takeaways.txt`

        and saves figures into `notebooks/Figures/`:

        - `cross_domain_synthetic_benchmark.png`
        - `cross_domain_synthetic_frontier.png`
        - `cross_domain_transfer_deltas.png`
        - `cross_domain_sparsity.png`
        - `cross_domain_ionosphere_protocol_comparison.png`
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

out_path = Path(__file__).resolve().parents[1] / "notebooks" / "cross_domain.ipynb"
out_path.write_text(json.dumps(notebook, indent=2), encoding="utf-8")
print(f"Wrote notebook to {out_path}")
