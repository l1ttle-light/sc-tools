# 整合与潜空间

这一页给出 scvi-tools 最常见的一条路径：从 AnnData 中读取原始计数和批次信息，训练 SCVI 模型，导出潜在表示，再回到 Scanpy 做邻居图、UMAP 和聚类。

## 数据准备

```python
import scanpy as sc
import scvi

adata = sc.read_h5ad("data/interim/02_qc_filtered.h5ad")
adata.layers["counts"] = adata.layers.get("counts", adata.X.copy())
```

scvi-tools 通常希望输入原始计数，而不是已经对数归一化或标准化的矩阵。因此建议在 Scanpy QC 阶段就把计数矩阵存入 `adata.layers["counts"]`。

## 注册 AnnData

```python
scvi.model.SCVI.setup_anndata(
    adata,
    layer="counts",
    batch_key="batch",
    categorical_covariate_keys=["sample_id"],
)
```

`setup_anndata()` 不是训练模型，而是告诉 scvi-tools：表达矩阵在哪里，批次字段在哪里，哪些 obs 字段是协变量。这里写错，后面的模型解释都会偏。

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
  <p>好的整合应该减少技术批次驱动的分离，同时保留真实生物条件、细胞类型和细胞状态差异。整合后必须检查批次混合和标志基因保留情况。</p>
</div>

## 常见排坑

<div class="check-grid">
  <article>
    <strong>输入矩阵不对</strong>
    <span>把对数归一化矩阵当计数输入，会破坏模型假设。优先使用计数层。</span>
  </article>
  <article>
    <strong>batch_key 过粗或过细</strong>
    <span>batch_key 应该表示技术批次或需要建模的来源，不应随便把生物条件当成批次。</span>
  </article>
  <article>
    <strong>只看 UMAP</strong>
    <span>UMAP 上混合得好看不代表整合正确，还要看已知标志基因、样本组成和差异状态。</span>
  </article>
  <article>
    <strong>缺少随机种子和版本</strong>
    <span>深度模型受版本、GPU 和随机性影响更明显，报告要记录 scvi-tools、PyTorch 和 CUDA 版本。</span>
  </article>
</div>

## 自检问题

1. 为什么 SCVI 通常需要原始计数？
2. `batch_key` 和 `categorical_covariate_keys` 的区别是什么？
3. 为什么整合后还要检查标志基因？
4. `X_scVI` 和 `X_pca` 在下游邻居图中扮演什么角色？
