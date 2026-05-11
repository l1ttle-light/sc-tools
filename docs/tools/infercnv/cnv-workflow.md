# CNV 推断流程

inferCNV 通常在 R 中运行，需要三个核心输入：raw counts matrix、cell annotation file 和 gene order file。最关键的设计选择是 reference groups，即哪些细胞被当作相对正常的基线。

## 输入文件

<div class="check-grid">
  <article>
    <strong>counts matrix</strong>
    <span>genes × cells 的 raw counts 或接近 raw counts 的表达矩阵。</span>
  </article>
  <article>
    <strong>cell annotation</strong>
    <span>每个 cell barcode 对应一个 group，例如 Tumor_Epithelial, T_cells, Myeloid, Fibroblast。</span>
  </article>
  <article>
    <strong>gene order file</strong>
    <span>每个 gene 的 chromosome, start, and end，用于按染色体位置排序和平滑。</span>
  </article>
  <article>
    <strong>reference groups</strong>
    <span>通常选择 immune/stromal/normal epithelial 等相对正常细胞作为背景。</span>
  </article>
</div>

## R 代码骨架

```r
library(infercnv)

infercnv_obj <- CreateInfercnvObject(
  raw_counts_matrix = "counts_matrix.tsv",
  annotations_file = "cell_annotations.tsv",
  delim = "\t",
  gene_order_file = "gene_order.tsv",
  ref_group_names = c("T_cells", "Myeloid", "Fibroblast")
)

infercnv_obj <- infercnv::run(
  infercnv_obj,
  cutoff = 0.1,
  out_dir = "results/infercnv",
  cluster_by_groups = TRUE,
  denoise = TRUE,
  HMM = TRUE
)
```

## 从 AnnData/Scanpy 导出输入

```python
import pandas as pd
import scanpy as sc

adata = sc.read_h5ad("data/processed/processed_scanpy.h5ad")
counts = adata.layers["counts"].T

pd.DataFrame(
    counts.toarray() if hasattr(counts, "toarray") else counts,
    index=adata.var_names,
    columns=adata.obs_names,
).to_csv("results/infercnv/counts_matrix.tsv", sep="\t")

adata.obs[["cell_type"]].to_csv(
    "results/infercnv/cell_annotations.tsv",
    sep="\t",
    header=False,
)
```

gene order file 需要根据物种和 gene annotation 生成，不能随便拼。常见来源包括 GTF/GFF annotation、biomaRt 或官方参考文件。

## reference group 选择

<div class="doc-callout warning">
  <strong>reference 选错，CNV 图会整体偏</strong>
  <p>inferCNV 是相对比较。若 reference 里混入 malignant cells，或目标组织没有真正正常对照，推断结果会偏弱或产生假信号。</p>
</div>

## 结果解释

1. 看 chromosome arm-level 的一致 gain/loss，而不是单个基因。
2. 看同一 cluster 内是否有一致模式。
3. 看 tumor-like cells 是否和 reference cells 明显分开。
4. 与 marker genes、样本来源、病理信息和 DNA 层证据互相验证。
5. 不要把 inferCNV 当作精确断点或小片段 CNV calling。

## 自检问题

1. 你的 reference groups 是否足够可信？
2. counts matrix 是否保留了原始表达信息？
3. gene order file 是否和 gene symbols/IDs 匹配？
4. CNV pattern 是否在细胞群内一致，而不是由低质量细胞驱动？

