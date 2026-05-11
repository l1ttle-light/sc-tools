#!/usr/bin/env bash
set -euo pipefail

python scripts/00_check_inputs.py
python scripts/01_create_h5ad.py
python scripts/02_qc_filter.py
python scripts/03_normalize_hvg.py
python scripts/04_pca_neighbors_umap.py
python scripts/05_markers_annotation.py
python scripts/06_export_report_assets.py
