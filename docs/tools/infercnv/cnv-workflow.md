# CNV 推断流程

inferCNV 通常在 R 中运行，需要三个核心输入：原始计数矩阵、细胞注释文件和基因排序文件。最关键的设计选择是参考细胞群，即哪些细胞被当作相对正常的基线。

## 输入文件

<div class="check-grid">
  <article>
    <strong>计数矩阵</strong>
    <span>基因 × 细胞的原始计数或接近原始计数的表达矩阵。</span>
  </article>
  <article>
    <strong>细胞注释</strong>
    <span>每个细胞条形码对应一个分组，例如 Tumor_Epithelial、T_cells、Myeloid、Fibroblast。</span>
  </article>
  <article>
    <strong>基因排序文件</strong>
    <span>记录每个基因的染色体、起点和终点，用于按染色体位置排序和平滑。</span>
  </article>
  <article>
    <strong>参考细胞群</strong>
    <span>通常选择免疫、基质、正常上皮等相对正常细胞作为背景。</span>
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

基因排序文件需要根据物种和基因注释生成，不能随便拼。常见来源包括 GTF/GFF 注释、biomaRt 或官方参考文件。

## 参考细胞群选择

<div class="doc-callout warning">
  <strong>参考细胞群选错，CNV 图会整体偏</strong>
  <p>inferCNV 是相对比较。若参考细胞群里混入恶性细胞，或目标组织没有真正正常对照，推断结果会偏弱或产生假信号。</p>
</div>

## 结果解释

1. 看染色体臂级别的一致增益/缺失，而不是单个基因。
2. 看同一细胞群内是否有一致模式。
3. 看肿瘤样细胞是否和参考细胞明显分开。
4. 与标志基因、样本来源、病理信息和 DNA 层证据互相验证。
5. 不要把 inferCNV 当作精确断点或小片段 CNV 检测。

## 自检问题

1. 你的参考细胞群是否足够可信？
2. 计数矩阵是否保留了原始表达信息？
3. 基因排序文件是否和基因符号/基因 ID 匹配？
4. CNV 模式是否在细胞群内一致，而不是由低质量细胞驱动？
