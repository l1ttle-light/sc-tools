# 自动注释流程

这一页给出 CellTypist 接入 Scanpy/AnnData 项目的常规流程。核心思路是：准备一个表达矩阵，选择合适 reference model，运行 cell-level prediction，再把预测结果写回 `adata.obs`。

## 安装与模型查看

```bash
pip install celltypist
```

```python
import celltypist

celltypist.models.download_models()
celltypist.models.models_description()
```

模型选择要和物种、组织、平台和研究问题匹配。不要用一个过宽泛或不相关的模型直接下最终结论。

## 输入 AnnData

```python
import scanpy as sc
import celltypist

adata = sc.read_h5ad("data/processed/processed_scanpy.h5ad")
```

CellTypist 通常使用 normalized/log-transformed expression。若你的 `adata.X` 是 scaled matrix 或只保留 HVGs，要回到更合适的表达矩阵。实践中建议保留一个用于 annotation 的 log-normalized full gene matrix。

<div class="doc-callout warning">
  <strong>输入矩阵要检查清楚</strong>
  <p>如果 <code>adata.X</code> 已经 scale 到均值 0 方差 1，或只剩高变基因，自动注释会更容易偏。保留 full genes 的 log-normalized matrix 更稳。</p>
</div>

## 运行预测

```python
pred = celltypist.annotate(
    adata,
    model="Immune_All_Low.pkl",
    majority_voting=True,
)

adata = pred.to_adata()
```

常见输出包括 predicted labels、confidence scores 和 majority voting labels。majority voting 会结合邻域/聚类信息平滑 cell-level prediction，通常更适合展示。

## 写回现有对象

如果不想让 `pred.to_adata()` 替换你的对象，可以手动写回：

```python
result = pred.predicted_labels
adata.obs["celltypist_label"] = result["predicted_labels"]
adata.obs["celltypist_majority"] = result["majority_voting"]
```

## 和 marker gene 对照

```python
sc.pl.umap(adata, color=["leiden", "celltypist_majority"])
sc.tl.rank_genes_groups(adata, "leiden", method="wilcoxon")
```

<div class="check-grid">
  <article>
    <strong>一致 cluster</strong>
    <span>一个 cluster 的 CellTypist 标签、marker genes 和组织背景一致，可以作为强证据。</span>
  </article>
  <article>
    <strong>混合 cluster</strong>
    <span>一个 cluster 内有多个强标签，要检查 resolution, doublet, batch, and cell state。</span>
  </article>
  <article>
    <strong>低置信度细胞</strong>
    <span>低 score 不一定是错，可能是参考模型没有覆盖该状态或组织。</span>
  </article>
  <article>
    <strong>罕见细胞</strong>
    <span>罕见细胞更需要 marker 和文献支持，不能只靠自动注释。</span>
  </article>
</div>

## 自检问题

1. CellTypist 的 reference model 是否匹配你的物种和组织？
2. 输入矩阵是 raw counts, log-normalized, scaled, or HVG-only？
3. majority voting 和 predicted labels 有什么区别？
4. 哪些 cluster 需要手工复核？

