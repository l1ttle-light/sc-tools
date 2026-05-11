# Scanpy 教程

Scanpy 是 Python 生态中最常用的单细胞 RNA-seq 分析框架之一。官方基础教程以 PBMC3k 数据为例，展示了从读取表达矩阵到聚类、marker gene 和细胞类型注释的完整路径。

本教程以官方教程为主线，同时补充一些实践判断：QC 阈值不要机械照抄、过滤最好按样本分布看、doublet 和低质量细胞要分开理解、归一化选择要服务下游任务。

<div class="scanpy-panel">
  <div>
    <span class="eyebrow">Scanpy Workflow</span>
    <h2>一个标准分析闭环</h2>
    <p>读入数据后，先确认 AnnData 结构，再计算 QC 指标、过滤低质量细胞和低表达基因，随后归一化、log 转换、选择高变基因，最后进入 PCA、邻居图、UMAP、Leiden 和 marker gene 注释。</p>
  </div>
  <div class="metrics">
    <span>数据容器 <strong>AnnData</strong></span>
    <span>主要矩阵 <strong>adata.X</strong></span>
    <span>细胞元数据 <strong>adata.obs</strong></span>
    <span>基因元数据 <strong>adata.var</strong></span>
    <span>降维结果 <strong>adata.obsm</strong></span>
  </div>
</div>

## 推荐阅读顺序

<div class="path-grid">
  <a href="/tools/scanpy/setup-anndata">
    <strong>环境与数据结构</strong>
    <span>安装 Scanpy，理解 AnnData 的核心字段，知道结果会被写到哪里。</span>
  </a>
  <a href="/tools/scanpy/qc-preprocessing">
    <strong>质控与预处理</strong>
    <span>计算 QC 指标、处理 doublet、归一化、log1p、高变基因选择和 scale。</span>
  </a>
  <a href="/tools/scanpy/clustering-annotation">
    <strong>降维、聚类与注释</strong>
    <span>PCA、neighbors、UMAP、Leiden、marker gene 和细胞类型命名。</span>
  </a>
  <a href="/tools/scanpy/practical-notes">
    <strong>经验与排坑</strong>
    <span>常见误区、参数记录、批次效应、保存结果和复现检查。</span>
  </a>
</div>

## 一条最小代码线

```python
import scanpy as sc

adata = sc.read_10x_mtx("data/filtered_gene_bc_matrices/hg19")
adata.var_names_make_unique()

adata.var["mt"] = adata.var_names.str.startswith("MT-")
sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True)

sc.pp.filter_cells(adata, min_genes=200)
sc.pp.filter_genes(adata, min_cells=3)
adata = adata[adata.obs.pct_counts_mt < 5].copy()

sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)
adata.raw = adata
adata = adata[:, adata.var.highly_variable].copy()
sc.pp.scale(adata, max_value=10)

sc.tl.pca(adata)
sc.pp.neighbors(adata, n_neighbors=10, n_pcs=40)
sc.tl.umap(adata)
sc.tl.leiden(adata)
sc.tl.rank_genes_groups(adata, "leiden", method="wilcoxon")
```

<div class="doc-callout warning">
  <strong>不要把这段代码当作万能模板</strong>
  <p>PBMC3k 的阈值和参数适合教学，不等于适合所有组织、平台、物种或疾病队列。真实项目必须回到每个样本的 QC 分布和实验设计。</p>
</div>

