from __future__ import annotations

import importlib.metadata as metadata
from pathlib import Path

import pandas as pd

from common import DIRS, ROOT, ensure_dirs, load_params, write_json


def main() -> None:
    ensure_dirs()
    params = load_params()
    samples_path = ROOT / "config" / "samples.tsv"

    if not samples_path.exists():
        raise FileNotFoundError("Missing config/samples.tsv")

    samples = pd.read_csv(samples_path, sep="\t")
    required = {"sample_id", "group", "batch", "path"}
    missing = required.difference(samples.columns)
    if missing:
        raise ValueError(f"config/samples.tsv missing columns: {sorted(missing)}")

    source = params["dataset"]["source"]
    if source not in {"scanpy_pbmc3k", "tenx_mtx"}:
        raise ValueError("dataset.source must be 'scanpy_pbmc3k' or 'tenx_mtx'")

    if source == "tenx_mtx":
        missing_paths = [p for p in samples["path"] if not (ROOT / p).exists()]
        if missing_paths:
            raise FileNotFoundError(f"Missing 10x matrix paths: {missing_paths}")

    versions = {}
    for package in ["scanpy", "anndata", "pandas", "numpy", "scipy", "matplotlib"]:
        try:
            versions[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            versions[package] = "not-installed"

    write_json(DIRS["logs"] / "environment_versions.json", versions)
    print(f"Input check passed. Dataset source: {source}")


if __name__ == "__main__":
    main()
