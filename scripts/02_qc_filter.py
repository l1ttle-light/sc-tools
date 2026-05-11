from __future__ import annotations

import matplotlib.pyplot as plt
import scanpy as sc

from common import DIRS, ensure_dirs, load_params


def main() -> None:
    ensure_dirs()
    params = load_params()
    qc = params["qc"]

    adata = sc.read_h5ad(DIRS["data_interim"] / "01_raw_counts.h5ad")
    adata.layers["counts"] = adata.X.copy()
    adata.var["mt"] = adata.var_names.str.upper().str.startswith("MT-")
    sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True)

    before = adata.n_obs
    sc.pp.filter_cells(adata, min_genes=qc["min_genes"])
    sc.pp.filter_genes(adata, min_cells=qc["min_cells"])

    keep = adata.obs["pct_counts_mt"] < qc["max_pct_mt"]
    if qc.get("max_genes_by_counts") is not None:
        keep &= adata.obs["n_genes_by_counts"] < qc["max_genes_by_counts"]
    adata = adata[keep].copy()

    summary = adata.obs.groupby("sample_id", observed=True).agg(
        cells_after=("sample_id", "size"),
        median_genes=("n_genes_by_counts", "median"),
        median_counts=("total_counts", "median"),
        median_pct_mt=("pct_counts_mt", "median"),
    )
    summary.loc["__all__", "cells_before"] = before
    summary.loc["__all__", "cells_after"] = adata.n_obs
    summary.to_csv(DIRS["tables_qc"] / "qc_summary.tsv", sep="\t")

    sc.pl.violin(
        adata,
        ["n_genes_by_counts", "total_counts", "pct_counts_mt"],
        groupby="sample_id",
        rotation=45,
        show=False,
    )
    plt.savefig(DIRS["fig_qc"] / "qc_violin.png", dpi=160, bbox_inches="tight")
    plt.close("all")

    sc.pl.scatter(adata, x="total_counts", y="pct_counts_mt", show=False)
    plt.savefig(DIRS["fig_qc"] / "qc_counts_vs_mt.png", dpi=160, bbox_inches="tight")
    plt.close("all")

    adata.write_h5ad(DIRS["data_interim"] / "02_qc_filtered.h5ad")
    print(f"Cells before QC: {before}; after QC: {adata.n_obs}")


if __name__ == "__main__":
    main()
