from __future__ import annotations

import scanpy as sc

from common import DIRS, ensure_dirs, load_params


def main() -> None:
    ensure_dirs()
    params = load_params()
    adata = sc.read_h5ad(DIRS["data_interim"] / "02_qc_filtered.h5ad")

    sc.pp.normalize_total(adata, target_sum=params["normalization"]["target_sum"])
    if params["normalization"].get("log1p", True):
        sc.pp.log1p(adata)

    hvg = params["hvg"]
    sc.pp.highly_variable_genes(
        adata,
        flavor=hvg["flavor"],
        min_mean=hvg["min_mean"],
        max_mean=hvg["max_mean"],
        min_disp=hvg["min_disp"],
    )
    adata.raw = adata
    adata = adata[:, adata.var["highly_variable"]].copy()

    regress_vars = params.get("scale", {}).get("regress_out", [])
    if regress_vars:
        sc.pp.regress_out(adata, regress_vars)
    sc.pp.scale(adata, max_value=params["scale"]["max_value"])

    adata.write_h5ad(DIRS["data_interim"] / "03_normalized_hvg.h5ad")
    print(f"HVG matrix: {adata.n_obs} cells x {adata.n_vars} genes")


if __name__ == "__main__":
    main()
