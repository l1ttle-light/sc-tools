# 自动注释流程

这一页给出 CellTypist 接入 Scanpy/AnnData 项目的常规流程。核心思路是：准备一个表达矩阵，选择合适参考模型，运行细胞级预测，再把预测结果写回 `adata.obs`。

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

CellTypist 通常使用归一化并做过对数转换的表达矩阵。若你的 `adata.X` 是标准化矩阵或只保留高变基因，要回到更合适的表达矩阵。实践中建议保留一个用于注释的全基因对数归一化矩阵。

<div class="doc-callout warning">
  <strong>输入矩阵要检查清楚</strong>
  <p>如果 <code>adata.X</code> 已经标准化到均值 0 方差 1，或只剩高变基因，自动注释会更容易偏。保留全基因的对数归一化矩阵更稳。</p>
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

常见输出包括预测标签、置信度分数和多数投票标签。多数投票会结合邻域/聚类信息平滑细胞级预测，通常更适合展示。

## 写回现有对象

如果不想让 `pred.to_adata()` 替换你的对象，可以手动写回：

```python
result = pred.predicted_labels
adata.obs["celltypist_label"] = result["predicted_labels"]
adata.obs["celltypist_majority"] = result["majority_voting"]
```

## 和标志基因对照

```python
sc.pl.umap(adata, color=["leiden", "celltypist_majority"])
sc.tl.rank_genes_groups(adata, "leiden", method="wilcoxon")
```

<div class="check-grid">
  <article>
    <strong>一致细胞群</strong>
    <span>一个细胞群的 CellTypist 标签、标志基因和组织背景一致，可以作为强证据。</span>
  </article>
  <article>
    <strong>混合细胞群</strong>
    <span>一个细胞群内有多个强标签，要检查分辨率、双细胞、批次和细胞状态。</span>
  </article>
  <article>
    <strong>低置信度细胞</strong>
    <span>低分数不一定是错，可能是参考模型没有覆盖该状态或组织。</span>
  </article>
  <article>
    <strong>罕见细胞</strong>
    <span>罕见细胞更需要标志基因和文献支持，不能只靠自动注释。</span>
  </article>
</div>

## 自检问题

1. CellTypist 的参考模型是否匹配你的物种和组织？
2. 输入矩阵是原始计数、对数归一化矩阵、标准化矩阵，还是只包含高变基因？
3. 多数投票标签和原始预测标签有什么区别？
4. 哪些细胞群需要手工复核？
