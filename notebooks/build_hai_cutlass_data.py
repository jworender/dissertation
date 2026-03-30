#!/usr/bin/env python3
"""
Build cutlass-ready HAI datasets from the raw CSV files.

This script mirrors the saved outputs produced by ``hai_20.07.R``:

- training split  = ``test1.csv`` + ``train1.csv``
- test split      = ``test2.csv`` + ``train2.csv``
- condition code  = ``attack + 2*attack_P1 + 4*attack_P2 + 8*attack_P3``
- flattened rows  = 10-step rolling windows over rows filtered to
  ``cond in {0, target_cond}``
- label column    = ``INDC`` (0/1), defined from the last row in each window
- balanced output = positives first, then a random sample of negatives whose
  count matches the number of positives

Parquet is the default output format because the flattened HAI matrices are
large. The generated files can be loaded into pandas and passed directly to
``cutlass``:

    python cases/HAI/build_hai_cutlass_data.py
"""

from __future__ import annotations

import argparse
import gc
import json
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view

TIME_COL = "time"
ATTACK_COLS = ("attack", "attack_P1", "attack_P2", "attack_P3")
WINDOW = 10
DEFAULT_FORMAT = "parquet"
TARGET_CONDS = {
    "a0": 3,
    "a1": 5,
    "a2": 7,
    "a3": 9,
    "a4": 11,
}
SPLIT_FILES = {
    # This odd mapping is intentional; it reproduces hai_20.07.R exactly.
    "train": ("test1.csv", "train1.csv"),
    "test": ("test2.csv", "train2.csv"),
}


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Build flattened HAI datasets for cutlass.",
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=script_dir / "raw_data",
        help="Directory containing the raw HAI CSV files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=script_dir / "processed_data",
        help="Directory for the generated cutlass-ready CSV files.",
    )
    parser.add_argument(
        "--window",
        type=int,
        default=WINDOW,
        help="Number of time steps to flatten per example.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed used for the balanced *_sm outputs.",
    )
    parser.add_argument(
        "--block-rows",
        type=int,
        default=5000,
        help="Number of flattened rows written per CSV append block.",
    )
    parser.add_argument(
        "--format",
        choices=("parquet", "csv"),
        default=DEFAULT_FORMAT,
        help="Output file format for the generated datasets.",
    )
    parser.add_argument(
        "--write-anomaly",
        action="store_true",
        help="Also write train_ad_hai.csv and test_ad_hai.csv.",
    )
    return parser.parse_args()


def log(message: str) -> None:
    print(message, flush=True)


def parquet_modules():
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
    except ImportError as exc:
        raise RuntimeError(
            "Parquet output requires pyarrow. Install pyarrow or rerun with --format csv."
        ) from exc
    return pa, pq


def sensor_columns(columns: Iterable[str]) -> list[str]:
    exclude = {TIME_COL, "cond", *ATTACK_COLS}
    return [str(col) for col in columns if col not in exclude]


def flattened_columns(features: list[str], window: int) -> list[str]:
    return [f"{feature}_{step:02d}" for feature in features for step in range(1, window + 1)]


def load_split(raw_dir: Path, split_name: str) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for file_name in SPLIT_FILES[split_name]:
        path = raw_dir / file_name
        log(f"Reading {path.name} for {split_name} split...")
        frame = pd.read_csv(
            path,
            sep=";",
            usecols=lambda col: col != TIME_COL,
            low_memory=False,
        )
        frames.append(frame)

    data = pd.concat(frames, ignore_index=True)
    data["cond"] = (
        data["attack"].astype(np.int16)
        + 2 * data["attack_P1"].astype(np.int16)
        + 4 * data["attack_P2"].astype(np.int16)
        + 8 * data["attack_P3"].astype(np.int16)
    ).astype(np.int16)
    return data


def write_empty_table(path: Path, columns: list[str], file_format: str) -> None:
    empty_df = pd.DataFrame(columns=columns)
    if file_format == "csv":
        empty_df.to_csv(path, index=False)
    else:
        empty_df.to_parquet(path, index=False)


def write_flattened_dataset(
    filtered: pd.DataFrame,
    feature_cols: list[str],
    target_cond: int,
    window: int,
    output_path: Path,
    block_rows: int,
    file_format: str,
) -> tuple[dict[str, int | str], np.ndarray, np.ndarray]:
    data_rows = len(filtered)
    output_cols = flattened_columns(feature_cols, window) + ["INDC"]
    if data_rows <= window:
        write_empty_table(output_path, output_cols, file_format)
        return (
            {
                "rows_in_filtered_stream": int(data_rows),
                "rows_written": 0,
                "positives": 0,
                "negatives": 0,
                "target_cond": int(target_cond),
                "output": str(output_path),
            },
            np.empty(0, dtype=np.int64),
            np.empty(0, dtype=np.int64),
        )

    feature_matrix = filtered.loc[:, feature_cols].to_numpy(dtype=np.float64, copy=False)
    cond = filtered["cond"].to_numpy(dtype=np.int16, copy=False)
    windows = sliding_window_view(feature_matrix, window_shape=window, axis=0)[:-1]
    labels = (cond[window - 1 : -1] == target_cond).astype(np.int8, copy=False)

    positive_parts: list[np.ndarray] = []
    negative_parts: list[np.ndarray] = []
    total_rows = labels.shape[0]
    writer = None

    if file_format == "parquet":
        pa, pq = parquet_modules()

    try:
        for start in range(0, total_rows, block_rows):
            stop = min(start + block_rows, total_rows)
            flat_block = windows[start:stop].reshape(stop - start, -1)
            block_df = pd.DataFrame(flat_block, columns=output_cols[:-1])
            block_df["INDC"] = labels[start:stop]

            if file_format == "csv":
                block_df.to_csv(
                    output_path,
                    mode="w" if start == 0 else "a",
                    header=start == 0,
                    index=False,
                )
            else:
                table = pa.Table.from_pandas(block_df, preserve_index=False)
                if writer is None:
                    writer = pq.ParquetWriter(str(output_path), table.schema, compression="snappy")
                writer.write_table(table)

            block_labels = labels[start:stop]
            pos = np.flatnonzero(block_labels == 1)
            neg = np.flatnonzero(block_labels == 0)
            if pos.size:
                positive_parts.append((pos + start).astype(np.int64, copy=False))
            if neg.size:
                negative_parts.append((neg + start).astype(np.int64, copy=False))
    finally:
        if writer is not None:
            writer.close()

    positive_idx = (
        np.concatenate(positive_parts) if positive_parts else np.empty(0, dtype=np.int64)
    )
    negative_idx = (
        np.concatenate(negative_parts) if negative_parts else np.empty(0, dtype=np.int64)
    )
    stats = {
        "rows_in_filtered_stream": int(data_rows),
        "rows_written": int(total_rows),
        "positives": int(positive_idx.size),
        "negatives": int(negative_idx.size),
        "target_cond": int(target_cond),
        "output": str(output_path),
    }
    return stats, positive_idx, negative_idx


def write_balanced_dataset(
    full_path: Path,
    output_path: Path,
    positive_idx: np.ndarray,
    negative_idx: np.ndarray,
    seed: int,
    file_format: str,
) -> dict[str, int | str]:
    if positive_idx.size == 0:
        if file_format == "csv":
            header = pd.read_csv(full_path, nrows=0)
            header.to_csv(output_path, index=False)
        else:
            _, pq = parquet_modules()
            columns = pq.ParquetFile(str(full_path)).schema.names
            pd.DataFrame(columns=columns).to_parquet(output_path, index=False)
        return {
            "rows_written": 0,
            "positives": 0,
            "negatives_sampled": 0,
            "output": str(output_path),
        }

    if negative_idx.size < positive_idx.size:
        raise ValueError(
            f"Cannot create balanced dataset from {full_path.name}: "
            f"{negative_idx.size} negatives available for {positive_idx.size} positives."
        )

    rng = np.random.default_rng(seed)
    sampled_neg = rng.choice(negative_idx, size=positive_idx.size, replace=False)
    sampled_neg_order = {int(idx): order for order, idx in enumerate(sampled_neg.tolist())}
    positive_lookup = set(map(int, positive_idx.tolist()))
    negative_lookup = set(map(int, sampled_neg.tolist()))

    positive_chunks: list[pd.DataFrame] = []
    negative_chunks: list[pd.DataFrame] = []
    row_start = 0

    if file_format == "csv":
        chunk_iter = pd.read_csv(full_path, chunksize=50000, low_memory=False)
    else:
        _, pq = parquet_modules()
        parquet_file = pq.ParquetFile(str(full_path))
        chunk_iter = (
            batch.to_pandas(types_mapper=None)
            for batch in parquet_file.iter_batches(batch_size=50000)
        )

    for chunk in chunk_iter:
        row_numbers = np.arange(row_start, row_start + len(chunk), dtype=np.int64)

        pos_mask = np.fromiter((int(row) in positive_lookup for row in row_numbers), dtype=bool)
        if pos_mask.any():
            positive_chunks.append(chunk.loc[pos_mask].copy())

        neg_mask = np.fromiter((int(row) in negative_lookup for row in row_numbers), dtype=bool)
        if neg_mask.any():
            selected = chunk.loc[neg_mask].copy()
            selected["_sample_order"] = [
                sampled_neg_order[int(row)] for row in row_numbers[neg_mask]
            ]
            negative_chunks.append(selected)

        row_start += len(chunk)

    positive_df = pd.concat(positive_chunks, ignore_index=True)
    negative_df = (
        pd.concat(negative_chunks, ignore_index=True)
        .sort_values("_sample_order", kind="stable")
        .drop(columns="_sample_order")
        .reset_index(drop=True)
    )
    balanced = pd.concat([positive_df, negative_df], ignore_index=True)
    if file_format == "csv":
        balanced.to_csv(output_path, index=False)
    else:
        balanced.to_parquet(output_path, index=False)

    return {
        "rows_written": int(len(balanced)),
        "positives": int(len(positive_df)),
        "negatives_sampled": int(len(negative_df)),
        "output": str(output_path),
    }


def write_anomaly_dataset(
    split_name: str,
    data: pd.DataFrame,
    feature_cols: list[str],
    output_dir: Path,
    file_format: str,
) -> dict[str, int | str]:
    suffix = "csv" if file_format == "csv" else "parquet"
    output_path = output_dir / f"{split_name}_ad_hai.{suffix}"
    anomaly_df = data.loc[:, feature_cols].copy()
    anomaly_df["INDC"] = (data["cond"] == 0).astype(np.int8)
    if file_format == "csv":
        anomaly_df.to_csv(output_path, index=False)
    else:
        anomaly_df.to_parquet(output_path, index=False)
    return {
        "rows_written": int(len(anomaly_df)),
        "positives": int(anomaly_df["INDC"].sum()),
        "negatives": int((1 - anomaly_df["INDC"]).sum()),
        "output": str(output_path),
    }


def process_split(
    split_name: str,
    raw_dir: Path,
    output_dir: Path,
    window: int,
    seed: int,
    block_rows: int,
    file_format: str,
    write_anomaly: bool,
) -> dict[str, object]:
    data = load_split(raw_dir, split_name)
    feature_cols = sensor_columns(data.columns)
    summary: dict[str, object] = {
        "source_files": list(SPLIT_FILES[split_name]),
        "raw_rows": int(len(data)),
        "feature_count": int(len(feature_cols)),
        "targets": {},
    }

    if write_anomaly:
        suffix = "csv" if file_format == "csv" else "parquet"
        log(f"Writing anomaly-style {split_name}_ad_hai.{suffix}...")
        summary["anomaly"] = write_anomaly_dataset(
            split_name,
            data,
            feature_cols,
            output_dir,
            file_format,
        )

    for target_name, target_cond in TARGET_CONDS.items():
        suffix = "csv" if file_format == "csv" else "parquet"
        full_name = f"{split_name}_{target_name}_hai.{suffix}"
        balanced_name = f"{split_name}_{target_name}_sm_hai.{suffix}"
        full_path = output_dir / full_name
        balanced_path = output_dir / balanced_name

        log(
            f"Building {full_name} "
            f"(cond in {{0, {target_cond}}}, window={window})..."
        )
        filtered = data.loc[data["cond"].isin((0, target_cond))].reset_index(drop=True)
        full_stats, positive_idx, negative_idx = write_flattened_dataset(
            filtered=filtered,
            feature_cols=feature_cols,
            target_cond=target_cond,
            window=window,
            output_path=full_path,
            block_rows=block_rows,
            file_format=file_format,
        )

        log(f"Building {balanced_name}...")
        balanced_stats = write_balanced_dataset(
            full_path=full_path,
            output_path=balanced_path,
            positive_idx=positive_idx,
            negative_idx=negative_idx,
            seed=seed,
            file_format=file_format,
        )

        summary["targets"][target_name] = {
            "full": full_stats,
            "balanced": balanced_stats,
        }
        del filtered, positive_idx, negative_idx
        gc.collect()

    del data
    gc.collect()
    return summary


def main() -> None:
    args = parse_args()
    raw_dir = args.raw_dir.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "raw_dir": str(raw_dir),
        "output_dir": str(output_dir),
        "window": int(args.window),
        "seed": int(args.seed),
        "block_rows": int(args.block_rows),
        "format": str(args.format),
        "splits": {},
    }

    for split_name in ("train", "test"):
        log(f"=== Processing {split_name} split ===")
        manifest["splits"][split_name] = process_split(
            split_name=split_name,
            raw_dir=raw_dir,
            output_dir=output_dir,
            window=args.window,
            seed=args.seed,
            block_rows=args.block_rows,
            file_format=args.format,
            write_anomaly=args.write_anomaly,
        )

    manifest_path = output_dir / "hai_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    log(f"Wrote manifest to {manifest_path}")


if __name__ == "__main__":
    main()
