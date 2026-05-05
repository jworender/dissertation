#!/usr/bin/env python3
"""Smoke-check the dissertation reproduction environment and cached artifacts."""

from __future__ import annotations

import argparse
import csv
import importlib
import json
import sys
from importlib import metadata
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = ROOT / "requirements.txt"
KERNEL_NAME = "cutlass"

CORE_IMPORTS = {
    "cutlass": "cutlass",
    "numpy": "numpy",
    "pandas": "pandas",
    "scikit-learn": "sklearn",
    "scipy": "scipy",
    "pyarrow": "pyarrow",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "copt": "copt",
    "groupyr": "groupyr",
    "imodels": "imodels",
    "interpret-core": "interpret",
    "mlxtend": "mlxtend",
    "qp-feature-selection": "qp_feature_selection",
    "scikit-optimize": "skopt",
    "jupyter": "jupyter",
    "ipykernel": "ipykernel",
    "nbconvert": "nbconvert",
    "notebook": "notebook",
}

CACHED_OUTPUTS = (
    "notebooks/runs_new/summary.csv",
    "notebooks/runs_new/stability_ablation/stability_ablation_summary_numeric.csv",
    "notebooks/runs_new/cross_domain/cross_domain_transfer_summary.csv",
    "notebooks/runs_new/goose_bay_robustness/goose_bay_protocol_summary.csv",
    "notebooks/runs_new/interpretable_baselines/case1_interpretable_summary.csv",
    "notebooks/runs_new/boundary_conditions/boundary_conditions_summary.csv",
    "notebooks/runs_new/compression_validation/strict_policy_noninferiority_summary.csv",
    "notebooks/runs_new/walkthrough/hai_a1_walkthrough_summary.json",
    "notebooks/runs_new/walkthrough/hai_a1_walkthrough_selected_rule.csv",
)

RAW_DATA_FILES = (
    "notebooks/raw_data/train1.csv",
    "notebooks/raw_data/train2.csv",
    "notebooks/raw_data/test1.csv",
    "notebooks/raw_data/test2.csv",
    "notebooks/raw_data/ionosphere.data",
)

PROCESSED_HAI_FILES = (
    "notebooks/processed_data/hai_manifest.json",
    "notebooks/processed_data/train_a1_sm_hai.parquet",
    "notebooks/processed_data/test_a1_sm_hai.parquet",
    "notebooks/processed_data/train_a2_sm_hai.parquet",
    "notebooks/processed_data/test_a2_sm_hai.parquet",
    "notebooks/processed_data/train_a3_sm_hai.parquet",
    "notebooks/processed_data/test_a3_sm_hai.parquet",
    "notebooks/processed_data/train_a4_sm_hai.parquet",
    "notebooks/processed_data/test_a4_sm_hai.parquet",
)


class SmokeFailure(Exception):
    """Raised when one smoke-check group fails."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Check imports, pinned package versions, the cutlass Jupyter kernel, "
            "cached study outputs, and optionally real-data inputs."
        ),
    )
    parser.add_argument(
        "--with-real-data",
        action="store_true",
        help=(
            "Also require HAI and ionosphere raw inputs plus the processed HAI "
            "parquet files used by real-data notebooks."
        ),
    )
    parser.add_argument(
        "--allow-version-drift",
        action="store_true",
        help="Report package-version mismatches as warnings instead of failures.",
    )
    parser.add_argument(
        "--skip-kernel",
        action="store_true",
        help="Skip the Jupyter kernelspec check.",
    )
    return parser.parse_args()


def pinned_requirements(path: Path) -> dict[str, str]:
    pins: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "==" not in stripped:
            continue
        name, version = stripped.split("==", 1)
        pins[name.lower()] = version.strip()
    return pins


def readable_size(path: Path) -> str:
    size = path.stat().st_size
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.1f} {unit}" if unit != "B" else f"{size} B"
        size /= 1024
    return f"{size:.1f} GB"


def require_files(paths: Iterable[str]) -> list[str]:
    missing: list[str] = []
    empty: list[str] = []
    for relative in paths:
        path = ROOT / relative
        if not path.exists():
            missing.append(relative)
        elif path.is_file() and path.stat().st_size == 0:
            empty.append(relative)
    failures = []
    if missing:
        failures.append("missing files: " + ", ".join(missing))
    if empty:
        failures.append("empty files: " + ", ".join(empty))
    return failures


def check_imports() -> list[str]:
    failures: list[str] = []
    for package, module_name in CORE_IMPORTS.items():
        try:
            importlib.import_module(module_name)
        except Exception as exc:  # noqa: BLE001 - smoke check should show exact import breakage.
            failures.append(f"{package} import failed via {module_name}: {exc}")
    return failures


def check_versions(allow_drift: bool) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []
    pins = pinned_requirements(REQUIREMENTS)
    for package, expected in sorted(pins.items()):
        try:
            actual = metadata.version(package)
        except metadata.PackageNotFoundError:
            failures.append(f"{package} is not installed")
            continue
        if actual != expected:
            message = f"{package} version {actual} does not match pinned {expected}"
            if allow_drift:
                warnings.append(message)
            else:
                failures.append(message)
    return failures, warnings


def check_kernel() -> list[str]:
    try:
        from jupyter_client.kernelspec import KernelSpecManager
    except Exception as exc:  # noqa: BLE001
        return [f"could not import Jupyter kernelspec manager: {exc}"]

    kernels = KernelSpecManager().find_kernel_specs()
    if KERNEL_NAME not in kernels:
        available = ", ".join(sorted(kernels)) or "(none)"
        return [
            f"kernel '{KERNEL_NAME}' is not registered; available kernels: {available}. "
            "Run: python -m ipykernel install --user --name cutlass --display-name cutlass"
        ]
    return []


def check_cached_outputs() -> list[str]:
    failures = require_files(CACHED_OUTPUTS)
    if failures:
        return failures

    for relative in CACHED_OUTPUTS:
        path = ROOT / relative
        try:
            if path.suffix == ".json":
                with path.open("r", encoding="utf-8") as handle:
                    payload = json.load(handle)
                if not payload:
                    failures.append(f"{relative} is readable but empty")
            elif path.suffix == ".csv":
                with path.open("r", encoding="utf-8", newline="") as handle:
                    reader = csv.reader(handle)
                    header = next(reader, None)
                    row = next(reader, None)
                if not header or row is None:
                    failures.append(f"{relative} does not contain a header and at least one data row")
            elif path.suffix == ".txt" or path.suffix == ".md":
                text = path.read_text(encoding="utf-8").strip()
                if not text:
                    failures.append(f"{relative} is readable but blank")
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{relative} is not readable: {exc}")
    return failures


def check_real_data() -> list[str]:
    failures = require_files(RAW_DATA_FILES)
    failures.extend(require_files(PROCESSED_HAI_FILES))
    if failures:
        return failures

    manifest = ROOT / "notebooks/processed_data/hai_manifest.json"
    try:
        with manifest.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if not payload:
            failures.append("notebooks/processed_data/hai_manifest.json is readable but empty")
    except Exception as exc:  # noqa: BLE001
        failures.append(f"notebooks/processed_data/hai_manifest.json is not readable: {exc}")

    try:
        import pyarrow.parquet as pq

        for relative in PROCESSED_HAI_FILES:
            if not relative.endswith(".parquet"):
                continue
            metadata_obj = pq.ParquetFile(ROOT / relative).metadata
            if metadata_obj.num_rows <= 0:
                failures.append(f"{relative} contains no rows")
    except Exception as exc:  # noqa: BLE001
        failures.append(f"processed HAI parquet metadata check failed: {exc}")

    return failures


def print_group(title: str, failures: list[str], warnings: list[str] | None = None) -> None:
    warnings = warnings or []
    if not failures and not warnings:
        print(f"[OK] {title}")
        return
    if failures:
        print(f"[FAIL] {title}")
        for failure in failures:
            print(f"  - {failure}")
    if warnings:
        print(f"[WARN] {title}")
        for warning in warnings:
            print(f"  - {warning}")


def main() -> int:
    args = parse_args()
    all_failures: list[str] = []

    import_failures = check_imports()
    print_group("core imports", import_failures)
    all_failures.extend(import_failures)

    version_failures, version_warnings = check_versions(args.allow_version_drift)
    print_group("requirements.txt package versions", version_failures, version_warnings)
    all_failures.extend(version_failures)

    if args.skip_kernel:
        print("[SKIP] cutlass Jupyter kernel")
    else:
        kernel_failures = check_kernel()
        print_group("cutlass Jupyter kernel", kernel_failures)
        all_failures.extend(kernel_failures)

    cached_failures = check_cached_outputs()
    print_group("cached notebooks/runs_new outputs", cached_failures)
    all_failures.extend(cached_failures)

    if args.with_real_data:
        real_data_failures = check_real_data()
        print_group("real-data inputs and processed HAI outputs", real_data_failures)
        all_failures.extend(real_data_failures)
    else:
        print("[SKIP] real-data inputs; rerun with --with-real-data before full real-data regeneration")

    if all_failures:
        print(f"\nSmoke check failed with {len(all_failures)} issue(s).", file=sys.stderr)
        return 1

    print("\nSmoke check passed.")
    print(f"Repository root: {ROOT}")
    print("Cached artifact sample:")
    for relative in CACHED_OUTPUTS[:3]:
        path = ROOT / relative
        print(f"  - {relative} ({readable_size(path)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
