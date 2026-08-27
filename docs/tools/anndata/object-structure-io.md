# 对象结构与读写

AnnData 可以理解为一个“矩阵 + 两张表 + 若干结果仓库”。如果把单细胞项目看成数据库，AnnData 就是最常用的数据表结构。

## 核心字段

<div class="check-grid">
  <article>
    <strong>X</strong>
    <span>主表达矩阵。常见形状是细胞 × 基因。注意它可能是原始计数、归一化值、对数转换值或标准化值。</span>
  </article>
  <article>
    <strong>obs</strong>
    <span>细胞元数据。sample_id、batch、percent_mito、leiden 和 cell_type 都常放在这里。</span>
  </article>
  <article>
    <strong>var</strong>
    <span>基因元数据。gene_ids、highly_variable、mean、dispersion 和 mt 标记常放在这里。</span>
  </article>
  <article>
    <strong>layers</strong>
    <span>同一批细胞 × 基因的备用矩阵。适合保存计数矩阵、归一化矩阵或插补矩阵。</span>
  </article>
  <article>
    <strong>obsm</strong>
    <span>细胞级多维结果。PCA、UMAP、t-SNE 和空间坐标通常在这里。</span>
  </article>
  <article>
    <strong>uns</strong>
    <span>非结构化结果。邻居图、标志基因排序、绘图颜色和参数经常在这里。</span>
  </article>
</div>

## 最小读写代码

```python
import scanpy as sc

adata = sc.read_10x_mtx("data/raw/sample_01/filtered_feature_bc_matrix")
adata.var_names_make_unique()

adata.layers["counts"] = adata.X.copy()
adata.obs["sample_id"] = "sample_01"

adata.write_h5ad("data/processed/sample_01_raw_counts.h5ad")
adata = sc.read_h5ad("data/processed/sample_01_raw_counts.h5ad")
```

## 切片与 copy

```python
filtered = adata[adata.obs["pct_counts_mt"] < 10, adata.var["highly_variable"]].copy()
```

AnnData 支持类似 pandas/numpy 的切片。实践中推荐在过滤后显式 `.copy()`，避免 view/copy 语义导致后续赋值出现警告或难以追踪。

## raw 和 layers 怎么选

<div class="doc-callout warning">
  <strong>raw 不是万能保险箱</strong>
  <p><code>adata.raw</code> 适合保存一个用于绘图或标志基因展示的快照，但不如 <code>layers</code> 灵活。需要长期追踪计数矩阵、归一化矩阵和标准化矩阵时，优先用 layers 并写清楚命名规则。</p>
</div>

## 和 Seurat 互转

Python 与 R 生态互转常用 `.h5ad`、`.h5seurat`、`.h5` 或 loom 等格式。真实项目中要特别检查：

1. 细胞条形码是否一致。
2. 基因符号和基因 ID 是否丢失。
3. 原始计数是否仍然存在。
4. 细胞群/细胞类型元数据是否保留。
5. UMAP/PCA 坐标是否被正确映射。

## 自检问题

1. `adata.obs` 和 `adata.var` 分别对应矩阵的哪个维度？
2. 为什么 scvi-tools 这类模型通常需要原始计数？
3. `obsm["X_umap"]` 和 `uns["rank_genes_groups"]` 分别是什么类型的结果？
4. 什么时候该用 `.copy()`？
