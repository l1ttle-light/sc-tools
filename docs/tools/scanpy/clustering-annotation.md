# 降维、聚类与注释

Scanpy 的聚类流程可以理解成：先用 PCA 压缩主要变化，再在 PCA 空间构建邻居图，随后用 UMAP 展示局部结构，并用 Leiden 在图上找社区。

## PCA

```python
sc.tl.pca(adata, svd_solver="arpack")
sc.pl.pca_variance_ratio(adata, log=True)
```

PCA 不只是为了画图，它决定了后续邻居图看到的主要变化。`n_pcs` 太小可能丢掉细胞类型差异，太大可能引入噪声。

## 邻居图、UMAP 和 Leiden

```python
sc.pp.neighbors(adata, n_neighbors=10, n_pcs=40)
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=1.0)

sc.pl.umap(adata, color=["leiden"])
```

<div class="check-grid">
  <article>
    <strong>n_neighbors</strong>
    <span>控制局部结构尺度。小值更强调细碎局部差异，大值更平滑。</span>
  </article>
  <article>
    <strong>n_pcs</strong>
    <span>决定邻居图使用多少 PCA 维度。需要结合方差解释和结果稳定性判断。</span>
  </article>
  <article>
    <strong>resolution</strong>
    <span>控制 Leiden 聚类颗粒度。它不是生物学真相，只是图社区划分参数。</span>
  </article>
  <article>
    <strong>random_state</strong>
    <span>UMAP 和部分算法受随机性影响。报告中应固定随机种子。</span>
  </article>
</div>

## Marker gene

```python
sc.tl.rank_genes_groups(adata, "leiden", method="wilcoxon")
sc.pl.rank_genes_groups(adata, n_genes=25, sharey=False)
```

Marker gene 是注释细胞类型的证据，而不是直接答案。更可靠的注释通常来自多种证据：经典 marker、差异基因、样本来源、已知组织结构、参考图谱和自动注释工具。

## 命名细胞类型

```python
cluster_to_cell_type = {
    "0": "CD4 T cells",
    "1": "CD14 monocytes",
    "2": "B cells",
}

adata.obs["cell_type"] = adata.obs["leiden"].map(cluster_to_cell_type)
sc.pl.umap(adata, color=["cell_type"])
```

<div class="doc-callout example">
  <strong>注释时要保留不确定性</strong>
  <p>如果一个 cluster 同时表达多个谱系 marker，先标成 ambiguous 或 mixed，比强行命名更诚实。后续可以回查 doublet、批次、细胞周期或亚群分辨率。</p>
</div>

## 自检问题

1. PCA、neighbors、UMAP、Leiden 之间是什么关系？
2. 为什么 UMAP 上看起来分开的点群不一定等于真实细胞类型？
3. `resolution` 变大后 cluster 变多，应该如何判断是否合理？
4. marker gene 注释为什么需要结合组织背景？

