from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import scanpy as sc

from common import DIRS, ROOT, ensure_dirs, load_params


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def main() -> None:
    ensure_dirs()
    params = load_params()
    adata = sc.read_h5ad(DIRS["data_processed"] / "processed_scanpy.h5ad")
    markers_path = DIRS["tables_markers"] / "markers_leiden.tsv"
    qc_path = DIRS["tables_qc"] / "qc_summary.tsv"

    top_markers = "<p>Marker table not found.</p>"
    if markers_path.exists():
        markers = pd.read_csv(markers_path, sep="\t")
        top_markers = markers.groupby("cluster").head(5).to_html(index=False)

    qc_summary = "<p>QC summary not found.</p>"
    if qc_path.exists():
        qc_summary = pd.read_csv(qc_path, sep="\t").to_html(index=False)

    payload = {
        "n_cells": int(adata.n_obs),
        "n_genes": int(adata.n_vars),
        "clusters": adata.obs["leiden"].nunique() if "leiden" in adata.obs else None,
        "parameters": params,
    }
    (DIRS["reports"] / "run_summary.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>PBMC Scanpy QC Report</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 980px; margin: 40px auto; line-height: 1.65; color: #1f2937; }}
    h1, h2 {{ color: #0f766e; }}
    img {{ max-width: 100%; border: 1px solid #d1d5db; border-radius: 8px; }}
    table {{ border-collapse: collapse; width: 100%; font-size: 14px; }}
    th, td {{ border: 1px solid #d1d5db; padding: 6px 8px; text-align: left; }}
    code, pre {{ background: #f3f4f6; border-radius: 6px; }}
    pre {{ padding: 12px; overflow-x: auto; }}
  </style>
</head>
<body>
  <h1>PBMC Scanpy QC Report</h1>
  <p>Cells: <strong>{adata.n_obs}</strong>; genes in processed matrix: <strong>{adata.n_vars}</strong>.</p>

  <h2>QC Summary</h2>
  {qc_summary}

  <h2>QC Figures</h2>
  <p><img src="../../figures/qc/qc_violin.png" alt="QC violin"></p>
  <p><img src="../../figures/qc/qc_counts_vs_mt.png" alt="QC scatter"></p>

  <h2>UMAP</h2>
  <p><img src="../../figures/umap/umap_leiden.png" alt="UMAP Leiden"></p>
  <p><img src="../../figures/umap/umap_sample_id.png" alt="UMAP sample"></p>
  <p><img src="../../figures/umap/umap_cell_type_guess.png" alt="UMAP cell type guess"></p>

  <h2>Top Markers</h2>
  {top_markers}

  <h2>Key Files</h2>
  <ul>
    <li>{rel(DIRS["data_processed"] / "processed_scanpy.h5ad")}</li>
    <li>{rel(markers_path)}</li>
    <li>{rel(DIRS["reports"] / "run_summary.json")}</li>
  </ul>
</body>
</html>
"""
    (DIRS["reports"] / "qc_report.html").write_text(report, encoding="utf-8")
    print(f"Wrote {DIRS['reports'] / 'qc_report.html'}")


if __name__ == "__main__":
    main()
