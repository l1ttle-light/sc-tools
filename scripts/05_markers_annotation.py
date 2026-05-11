from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import scanpy as sc

from common import DIRS, ensure_dirs, load_params


PBMC_MARKERS = {
    "IL7R": "CD4 T cells",
    "CD3D": "T cells",
    "CD3E": "T cells",
    "NKG7": "NK cells",
    "GNLY": "NK cells",
    "MS4A1": "B cells",
    "CD79A": "B cells",
    "LYZ": "monocytes",
    "S100A8": "monocytes",
    "FCGR3A": "FCGR3A monocytes",
    "MS4A7": "FCGR3A monocytes",
    "FCER1A": "dendritic cells",
    "CST3": "dendritic cells",
    "PPBP": "megakaryocytes",
}


def export_rank_genes(adata, groupby: str, n_genes: int) -> pd.DataFrame:
    result = adata.uns["rank_genes_groups"]
    groups = result["names"].dtype.names
    rows = []
    for group in groups:
        for rank in range(min(n_genes, len(result["names"][group]))):
            rows.append(
                {
                    "cluster": group,
                    "rank": rank + 1,
                    "gene": result["names"][group][rank],
                    "score": result["scores"][group][rank],
                    "logfoldchange": result["logfoldchanges"][group][rank],
                    "pval": result["pvals"][group][rank],
                    "pval_adj": result["pvals_adj"][group][rank],
                    "groupby": groupby,
                }
            )
    return pd.DataFrame(rows)


def infer_simple_labels(markers: pd.DataFrame) -> dict[str, str]:
    labels = {}
    for cluster, table in markers.groupby("cluster"):
        top = table.head(30)
        votes = {}
        for gene in top["gene"]:
            label = PBMC_MARKERS.get(gene)
            if label:
                votes[label] = votes.get(label, 0) + 1
        labels[cluster] = max(votes, key=votes.get) if votes else f"cluster {cluster}"
    return labels


def main() -> None:
    ensure_dirs()
    params = load_params()
    marker_params = params["markers"]
    adata = sc.read_h5ad(DIRS["data_interim"] / "04_clustered.h5ad")

    groupby = marker_params["groupby"]
    sc.tl.rank_genes_groups(adata, groupby, method=marker_params["method"])
    markers = export_rank_genes(adata, groupby, marker_params["n_genes"])
    markers.to_csv(DIRS["tables_markers"] / f"markers_{groupby}.tsv", sep="\t", index=False)

    labels = infer_simple_labels(markers)
    adata.obs["cell_type_guess"] = adata.obs[groupby].map(labels).astype("category")
    pd.Series(labels, name="cell_type_guess").to_csv(
        DIRS["tables_markers"] / "cluster_cell_type_guess.tsv",
        sep="\t",
        header=True,
    )

    sc.pl.umap(adata, color=["cell_type_guess"], legend_loc="on data", show=False)
    plt.savefig(DIRS["fig_umap"] / "umap_cell_type_guess.png", dpi=180, bbox_inches="tight")
    plt.close("all")

    adata.write_h5ad(DIRS["data_processed"] / "processed_scanpy.h5ad")
    print(f"Exported markers for {markers['cluster'].nunique()} clusters")


if __name__ == "__main__":
    main()
