# 整合与潜空间

这一页给出 scvi-tools 最常见的一条路径：从 AnnData 中读取 raw counts 和 batch 信息，训练 SCVI 模型，导出 latent representation，再回到 Scanpy 做 neighbors, UMAP, and clustering。

## 数据准备

```python
import scanpy as sc
import scvi

adata = sc.read_h5ad("data/interim/02_qc_filtered.h5ad")
adata.layers["counts"] = adata.layers.get("counts", adata.X.copy())
```

scvi-tools 通常希望输入 raw counts，而不是已经 log-normalized 或 scaled 的矩阵。因此建议在 Scanpy QC 阶段就把 counts 存入 `adata.layers["counts"]`。

## 注册 AnnData

```python
scvi.model.SCVI.setup_anndata(
    adata,
    layer="counts",
    batch_key="batch",
    categorical_covariate_keys=["sample_id"],
)
```

`setup_anndata()` 不是训练模型，而是告诉 scvi-tools：表达矩阵在哪里，batch 在哪里，哪些 obs 字段是协变量。这里写错，后面的模型解释都会偏。

## 训练模型并导出潜空间

```python
model = scvi.model.SCVI(adata, n_latent=30)
model.train(max_epochs=100)

adata.obsm["X_scVI"] = model.get_latent_representation()
```

## 回到 Scanpy 做图

```python
sc.pp.neighbors(adata, use_rep="X_scVI")
sc.tl.umap(adata)
sc.tl.leiden(adata, key_added="leiden_scvi")
sc.pl.umap(adata, color=["batch", "sample_id", "leiden_scvi"])
```

<div class="doc-callout important">
  <strong>整合不是把差异都抹平</strong>
  <p>好的 integration 应该减少技术批次驱动的分离，同时保留真实 biological condition, cell type, and cell state 差异。整合后必须检查 batch mixing 和 marker preservation。</p>
</div>

## 常见排坑

<div class="check-grid">
  <article>
    <strong>输入矩阵不对</strong>
    <span>把 log-normalized matrix 当 counts 输入，会破坏模型假设。优先使用 counts layer。</span>
  </article>
  <article>
    <strong>batch_key 过粗或过细</strong>
    <span>batch_key 应该表示技术批次或需要建模的来源，不应随便把 biological condition 当成 batch。</span>
  </article>
  <article>
    <strong>只看 UMAP</strong>
    <span>UMAP mixing 好看不代表整合正确，还要看 known markers, sample composition, and differential states。</span>
  </article>
  <article>
    <strong>缺少随机种子和版本</strong>
    <span>深度模型受版本、GPU 和随机性影响更明显，报告要记录 scvi-tools, PyTorch, and CUDA 版本。</span>
  </article>
</div>

## 自检问题

1. 为什么 SCVI 通常需要 raw counts？
2. `batch_key` 和 `categorical_covariate_keys` 的区别是什么？
3. 为什么整合后还要检查 marker gene？
4. `X_scVI` 和 `X_pca` 在下游 neighbors 中扮演什么角色？

