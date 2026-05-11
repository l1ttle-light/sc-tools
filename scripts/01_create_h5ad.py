from __future__ import annotations

import pandas as pd
import scanpy as sc

from common import DIRS, ROOT, ensure_dirs, load_params


def load_scanpy_pbmc3k():
    adata = sc.datasets.pbmc3k()
    adata.var_names_make_unique()
    adata.obs["sample_id"] = "pbmc3k"
    adata.obs["group"] = "public_pbmc"
    adata.obs["batch"] = "batch1"
    adata.obs_names = [f"pbmc3k_{x}" for x in adata.obs_names]
    return adata


def load_tenx_from_samples():
    samples = pd.read_csv(ROOT / "config" / "samples.tsv", sep="\t")
    adatas = []
    for row in samples.itertuples(index=False):
        adata = sc.read_10x_mtx(ROOT / row.path, var_names="gene_symbols")
        adata.var_names_make_unique()
        adata.obs["sample_id"] = row.sample_id
        adata.obs["group"] = row.group
        adata.obs["batch"] = row.batch
        adata.obs_names = [f"{row.sample_id}_{x}" for x in adata.obs_names]
        adatas.append(adata)
    return sc.concat(adatas, join="outer", fill_value=0)


def main() -> None:
    ensure_dirs()
    params = load_params()
    source = params["dataset"]["source"]
    adata = load_scanpy_pbmc3k() if source == "scanpy_pbmc3k" else load_tenx_from_samples()
    adata.write_h5ad(DIRS["data_interim"] / "01_raw_counts.h5ad")
    print(adata)


if __name__ == "__main__":
    main()
