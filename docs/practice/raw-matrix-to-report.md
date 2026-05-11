# raw matrix 到 h5ad、marker 表、UMAP 图和 QC 报告

这个模板默认使用 Scanpy 内置的公开 PBMC3k 数据集，方便快速验证环境和流程。真实项目中也可以把 `config/parameters.yaml` 的 `dataset.source` 改成 `tenx_mtx`，再在 `config/samples.tsv` 指向 10x Genomics 输出的 `raw_feature_bc_matrix` 或 `filtered_feature_bc_matrix`。

## 推荐目录结构

```text
single-cell-project/
  README.md
  environment.yml
  config/
    parameters.yaml
    samples.tsv
  data/
    raw/
      sample_01/raw_feature_bc_matrix/
      sample_02/raw_feature_bc_matrix/
    interim/
    processed/
  scripts/
    00_check_inputs.py
    01_create_h5ad.py
    02_qc_filter.py
    03_normalize_hvg.py
    04_pca_neighbors_umap.py
    05_markers_annotation.py
    06_export_report_assets.py
  notebooks/
    01_qc_exploration.ipynb
    02_annotation_review.ipynb
  results/
    figures/
      qc/
      umap/
    tables/
      markers/
      qc/
    reports/
  logs/
```

当前仓库已经创建了对应的 `config/`、`scripts/`、`data/`、`results/`、`logs/` 和 `notebooks/` 目录。

<div class="doc-callout important">
  <strong>raw 不可改，processed 可再生</strong>
  <p>`data/raw` 应该只读保存；中间文件和结果都应该能由脚本重新生成。这样参数调整不会污染原始数据。</p>
</div>

## 配置文件

`config/samples.tsv`

```text
sample_id	group	batch	path
sample_01	control	batch1	data/raw/sample_01/raw_feature_bc_matrix
sample_02	treatment	batch1	data/raw/sample_02/raw_feature_bc_matrix
```

`config/parameters.yaml` 已经放在项目根目录。默认配置如下：

```yaml
qc:
  min_genes: 200
  min_cells: 3
  max_pct_mt: 5
  max_genes_by_counts: 2500
normalization:
  target_sum: 10000
  log1p: true
hvg:
  flavor: seurat
  min_mean: 0.0125
  max_mean: 3
  min_disp: 0.5
pca:
  n_comps: 50
neighbors:
  n_neighbors: 10
  n_pcs: 40
clustering:
  method: leiden
  resolution: 1.0
  random_state: 0
markers:
  groupby: leiden
  method: wilcoxon
```

## 脚本职责

<div class="flow-strip">
  <span>检查输入和样本表</span>
  <span>读取 10x 并合并样本</span>
  <span>计算 QC 并过滤</span>
  <span>归一化和 HVG</span>
  <span>PCA、neighbors、UMAP、Leiden</span>
  <span>计算 marker genes</span>
  <span>导出图表</span>
  <span>生成报告素材</span>
</div>

## 最小脚本骨架

```python
# scripts/01_create_h5ad.py
from pathlib import Path
import pandas as pd
import scanpy as sc

samples = pd.read_csv("config/samples.tsv", sep="\t")
adatas = []

for row in samples.itertuples(index=False):
    adata = sc.read_10x_mtx(row.path, var_names="gene_symbols")
    adata.var_names_make_unique()
    adata.obs["sample_id"] = row.sample_id
    adata.obs["group"] = row.group
    adata.obs["batch"] = row.batch
    adata.obs_names = [f"{row.sample_id}_{x}" for x in adata.obs_names]
    adatas.append(adata)

combined = sc.concat(adatas, join="outer", label="sample_id_from_concat", fill_value=0)
Path("data/interim").mkdir(parents=True, exist_ok=True)
combined.write_h5ad("data/interim/01_raw_counts.h5ad")
```

```python
# scripts/02_qc_filter.py
import scanpy as sc

adata = sc.read_h5ad("data/interim/01_raw_counts.h5ad")
adata.layers["counts"] = adata.X.copy()

adata.var["mt"] = adata.var_names.str.startswith(("MT-", "mt-"))
sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True)

sc.pp.filter_cells(adata, min_genes=200)
sc.pp.filter_genes(adata, min_cells=3)
adata = adata[adata.obs["pct_counts_mt"] < 15].copy()

adata.write_h5ad("data/interim/02_qc_filtered.h5ad")
```

```python
# scripts/04_pca_neighbors_umap.py
import scanpy as sc

adata = sc.read_h5ad("data/interim/03_normalized_hvg.h5ad")
sc.tl.pca(adata, n_comps=50, random_state=0)
sc.pp.neighbors(adata, n_neighbors=10, n_pcs=40, random_state=0)
sc.tl.umap(adata, random_state=0)
sc.tl.leiden(adata, resolution=1.0, random_state=0)

adata.write_h5ad("data/processed/processed_scanpy.h5ad")
```

## 输出物清单

<div class="check-grid">
  <article>
    <strong>processed h5ad</strong>
    <span><code>data/processed/processed_scanpy.h5ad</code>, contains QC, normalization, PCA, UMAP, cluster, and marker results.</span>
  </article>
  <article>
    <strong>marker 表</strong>
    <span><code>results/tables/markers/markers_leiden.tsv</code>, with gene, score, logfoldchange, p-value, and adjusted p-value for each cluster.</span>
  </article>
  <article>
    <strong>UMAP 图</strong>
    <span><code>results/figures/umap/umap_leiden.png</code>, <code>umap_sample_id.png</code>, and <code>umap_cell_type_guess.png</code>.</span>
  </article>
  <article>
    <strong>QC 报告</strong>
    <span><code>results/reports/qc_report.html</code>, records cell counts before and after filtering, QC distributions, parameters, and software versions.</span>
  </article>
</div>

## 一条命令线

```bash
conda env create -f environment.yml
conda activate sc-tools-pbmc
bash scripts/run_pbmc_pipeline.sh
```

这条命令会按顺序生成：

```text
data/interim/01_raw_counts.h5ad
data/interim/02_qc_filtered.h5ad
data/interim/03_normalized_hvg.h5ad
data/interim/04_clustered.h5ad
data/processed/processed_scanpy.h5ad
results/tables/qc/qc_summary.tsv
results/tables/markers/markers_leiden.tsv
results/figures/qc/qc_violin.png
results/figures/qc/qc_counts_vs_mt.png
results/figures/umap/umap_leiden.png
results/figures/umap/umap_sample_id.png
results/figures/umap/umap_cell_type_guess.png
results/reports/qc_report.html
```

## QC 报告应该包含什么

<div class="flow-strip">
  <span>每个样本原始细胞数</span>
  <span>过滤后细胞数</span>
  <span>n_genes 分布</span>
  <span>total_counts 分布</span>
  <span>pct_counts_mt 分布</span>
  <span>样本/批次 UMAP</span>
  <span>cluster marker 摘要</span>
  <span>参数和软件版本</span>
</div>

## 判断流程是否成功

1. 每个样本都有合理数量的细胞保留，没有某个样本被阈值整体清空。
2. QC 指标的过滤前后分布能解释，不只是“因为教程这么写”。
3. UMAP 不应只按测序批次分开；如果分开，要先考虑批次或样本差异。
4. marker gene 与 cluster 命名有一致证据，不能只靠一个 marker。
5. 所有输出都能由脚本从 raw 数据重新生成。
