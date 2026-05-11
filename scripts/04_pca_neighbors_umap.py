from __future__ import annotations

import matplotlib.pyplot as plt
import scanpy as sc

from common import DIRS, ensure_dirs, load_params


def main() -> None:
    ensure_dirs()
    params = load_params()
    adata = sc.read_h5ad(DIRS["data_interim"] / "03_normalized_hvg.h5ad")

    sc.tl.pca(
        adata,
        n_comps=params["pca"]["n_comps"],
        random_state=params["pca"]["random_state"],
    )
    sc.pp.neighbors(
        adata,
        n_neighbors=params["neighbors"]["n_neighbors"],
        n_pcs=params["neighbors"]["n_pcs"],
        random_state=params["neighbors"]["random_state"],
    )
    sc.tl.umap(adata, random_state=params["umap"]["random_state"])
    sc.tl.leiden(
        adata,
        resolution=params["clustering"]["resolution"],
        random_state=params["clustering"]["random_state"],
        key_added="leiden",
    )

    sc.pl.umap(adata, color=["leiden"], show=False)
    plt.savefig(DIRS["fig_umap"] / "umap_leiden.png", dpi=180, bbox_inches="tight")
    plt.close("all")

    sc.pl.umap(adata, color=["sample_id"], show=False)
    plt.savefig(DIRS["fig_umap"] / "umap_sample_id.png", dpi=180, bbox_inches="tight")
    plt.close("all")

    adata.write_h5ad(DIRS["data_interim"] / "04_clustered.h5ad")
    adata.write_h5ad(DIRS["data_processed"] / "processed_scanpy.h5ad")
    print(adata)


if __name__ == "__main__":
    main()
