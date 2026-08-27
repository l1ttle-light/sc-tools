# Harmony

Harmony 是一个用于整合单细胞数据的无监督算法。它的核心思想很明确：不直接修改基因表达矩阵，而是在 PCA 等低维表示上学习批次/协变量校正，让细胞在低维空间中更多按生物状态聚集，而不是按实验批次、供体、测序平台或组织来源分开 [1]。

这篇页面基于论文 *Fast, sensitive and accurate integration of single-cell data with Harmony* 和官方 GitHub 仓库代码整理。

## 1. 算法基本信息

| 项目 | 内容 |
|---|---|
| 算法名称 | Harmony |
| 论文标题 | Fast, sensitive and accurate integration of single-cell data with Harmony |
| 发表信息 | *Nature Methods*, 2019 |
| DOI | `10.1038/s41592-019-0619-0` |
| GitHub 仓库 | `https://github.com/immunogenomics/harmony` |
| 任务类型 | 批次整合 / 多数据集整合 / 协变量校正 |
| 适用数据 | scRNA-seq 低维表示；论文也展示了跨模态整合场景 |
| 主要输出 | 校正后的低维表示，通常保存为 `harmony`、`X_harmony` 或 `reducedDim(..., "HARMONY")` |

## 2. 算法作用

Harmony 解决的是“多个单细胞数据集放在一起时，低维空间被批次/协变量主导”的问题。它把 PCA 低维表示和细胞元数据作为输入，输出一个校正后的低维表示。后续的邻居图、UMAP、聚类、轨迹分析都应基于这个校正结果运行。

它不输出校正后的计数，也不应该把 Harmony 低维表示当作新的表达矩阵去做基因层面的差异表达。论文讨论里明确建议：差异表达这类问题应使用能显式处理批次的统计模型，例如包含批次/协变量的线性模型或混合效应模型 [1]。

<div class="doc-callout important">
  <strong>一句话理解</strong>
  <p>Harmony 做的是低维表示校正，不是表达插补。它让低维空间更适合联合聚类和可视化，但不创造新的基因表达值。</p>
</div>

## 3. 输入与输出

### 输入文件

| 输入 | 格式 | 形状/字段 | 必需 | 说明 |
|---|---|---|---|---|
| 表达矩阵 | `.h5ad`, `.rds`, `.mtx`, `.loom`, `.csv`, `.tsv` | 细胞 x 基因 | 上游需要 | Harmony 通常不直接从原始计数开始，而是先归一化、找高变基因、PCA。 |
| PCA/细胞低维表示 | matrix, `adata.obsm["X_pca"]`, Seurat `pca`, SCE `PCA` | 细胞 x PC | 是 | 论文记作 `Z`，实现内部转成 `d x N`。 |
| 细胞元数据 | `.csv`, `.tsv`, `adata.obs`, Seurat `meta.data`, SCE `colData` | 细胞 x 协变量 | 是 | 必须包含要校正的分类变量，例如 `batch`, `donor`, `platform`, `chemistry`。 |
| 协变量列表 | string/list | 列名 | 是 | R 接口为 `group.by.vars` 或 `vars_use`。 |

### 输出文件

| 输出 | 格式 | 形状/字段 | 用途 |
|---|---|---|---|
| 校正后的低维表示 | matrix, `adata.obsm["X_harmony"]`, Seurat reduction, SCE reducedDim | 细胞 x PC | 下游邻居图/UMAP/聚类 |
| 收敛轨迹 | 对象中的图或数据 | 目标函数值 | 检查优化是否稳定。 |
| 软聚类分配 | `return_object=TRUE` 时的 R6 对象字段 `R` | 细胞群 x 细胞 | 解释每个细胞属于多个细胞群的权重。 |
| 共现统计量 | R6 对象字段 `O`, `E` | 细胞群 x 批次 | 理解多样性惩罚中的观测/期望批次组成。 |

## 4. 算法流程图

![Harmony algorithm flow](/algorithms/harmony-flow.svg)

## 5. 模型结构详解

Harmony 不是 VAE、Transformer 或 GNN，而是一个迭代优化算法。论文里的 Algorithm 1 可以概括为：

```text
function harmonize(Z, Phi)
    Z_corr <- Z
    repeat
        R <- maximum_diversity_clustering(Z_corr, Phi)
        Z_corr <- mixture_model_linear_correction(Z, R, Phi)
    until convergence
    return Z_corr
```

### 5.1 数据结构

| 符号 | 代码中对应 | 形状 | 含义 |
|---|---|---|---|
| `Z` | `Z_orig` | `d x N` | 原始 PCA/细胞低维表示。 |
| `Z_hat`, `Z_corr` | `Z_corr` | `d x N` | 当前校正后的低维表示。 |
| `Phi` | `Phi` | `B x N` | 批次/协变量的独热设计矩阵。 |
| `R` | `R` | `K x N` | 软聚类分配，每个细胞可同时属于多个细胞群。 |
| `Y` | `Y` | `d x K` | 细胞群中心。 |
| `O` | `O` | `K x B` | 观测到的细胞群-批次共现。 |
| `E` | `E` | `K x B` | 独立假设下期望的共现。 |
| `theta` | `theta` | 每个协变量水平 | 控制批次多样性惩罚强度。 |
| `sigma` | `sigma` | 每个细胞群 | 控制软 k-means 的软硬程度。 |
| `lambda` | `lambda` | 每个协变量水平 | 岭惩罚，越大越保守，越不容易过度校正。 |

### 5.2 第一步：最大多样性聚类

Harmony 先在当前低维表示上做软 k-means。与普通 k-means 不同，`R` 是概率分配矩阵，而不是每个细胞只有一个硬标签。这样做的好处是保留连续状态，例如分化轨迹或激活梯度。

论文在软 k-means 的距离项之外加入多样性惩罚。直观上，如果某个细胞群里某个批次明显过多，Harmony 会降低这个批次的细胞继续进入该细胞群的概率；如果某个批次在该细胞群中不足，则会提高它进入的机会。代码中对应：

```text
dist_mat = 2 * (1 - Y.t() * Z_corr)
E = sum(R, 1) * Pr_b.t()
O = R * Phi_t
Rcells = exp(-dist / sigma) * diversity_score
```

实际实现入口在 `src/harmony.cpp` 的 `cluster_cpp()` 和 `update_R()`。其中 `update_R()` 会分块更新细胞，先暂时移除一批细胞对 `O` 和 `E` 的贡献，再用新的多样性分数更新这些细胞的 `R`，最后把它们加回统计量。

### 5.3 第二步：混合专家岭回归校正

聚类后，Harmony 在每个细胞群内估计批次效应。这里可以理解为“每个细胞群是一个专家”，每个专家都学习一组批次/协变量的线性校正项；细胞最终的校正值是多个专家按 `R` 加权后的结果。

论文强调校正步骤使用原始 `Z` 估计校正，而不是持续在已经校正过的 `Z_corr` 上叠加回归。这样可以减少过度校正风险。代码中 `moe_correct_ridge_cpp()` 一开始就执行：

```text
Z_corr = Z_orig
```

随后对每个细胞群 `k` 拟合岭回归：

```text
W_k = (Phi* diag(R_k) Phi*^T + lambda I)^-1 Phi* diag(R_k) Z_orig^T
```

其中 `Phi*` 是带截距的设计矩阵。实现里会保留截距，不从低维表示中移除全局细胞群中心，只移除批次/协变量相关项：

```text
Y.col(k) = W.row(0).t()
W.row(0).zeros()
Z_corr -= W.t() * Phi_Rk
```

### 5.4 收敛判断

Harmony 有两层收敛：聚类内部用 k-means 目标函数的窗口变化判断；外层整合用校正前后的目标函数变化判断。R 层 `harmonize()` 每轮调用：

```text
harmonyObj$cluster_cpp()
harmonyObj$moe_correct_ridge_cpp()
harmonyObj$check_convergence(1)
```

默认 `max_iter=10`，`early_stop=TRUE`。如果 `plot_convergence=TRUE`，R 包会根据 `objective_kmeans` 画出收敛曲线。

## 6. GitHub 代码阅读记录

| 模块 | 文件路径 | 作用 | 重点函数/类 |
|---|---|---|---|
| 用户入口 | `R/RunHarmony.R` | Seurat、SingleCellExperiment 和 default API。 | `RunHarmony.Seurat()`, `RunHarmony.SingleCellExperiment()` |
| 参数与主入口 | `R/ui.R` | 检查输入、构造 `Phi`、设置 `theta`, `sigma`, `lambda`, `nclust`。 | `RunHarmony.default()` |
| 外层循环 | `R/utils.R` | 执行每轮聚类和校正。 | `harmonize()` |
| C++ 对象定义 | `src/harmony.h` | 保存 `Z_orig`, `Z_corr`, `R`, `Y`, `O`, `E` 等核心状态。 | `class harmony` |
| 初始化与目标函数 | `src/harmony.cpp` | 初始化中心点、计算目标函数。 | `setup()`, `init_cluster_cpp()`, `compute_objective()` |
| 聚类 | `src/harmony.cpp` | 软 k-means + 多样性惩罚。 | `cluster_cpp()`, `update_R()` |
| 校正 | `src/harmony.cpp` | 混合专家岭回归校正。 | `moe_correct_ridge_cpp()` |

## 7. 最小使用流程

### Seurat

```r
library(Seurat)
library(harmony)

obj <- NormalizeData(obj)
obj <- FindVariableFeatures(obj)
obj <- ScaleData(obj)
obj <- RunPCA(obj, npcs = 30)

obj <- RunHarmony(
  object = obj,
  group.by.vars = c("batch"),
  reduction.use = "pca",
  reduction.save = "harmony"
)

obj <- FindNeighbors(obj, reduction = "harmony", dims = 1:30)
obj <- FindClusters(obj)
obj <- RunUMAP(obj, reduction = "harmony", dims = 1:30)
```

### Scanpy 生态

```python
import scanpy as sc
import scanpy.external as sce

sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, batch_key="batch")
adata = adata[:, adata.var["highly_variable"]].copy()
sc.pp.scale(adata)
sc.tl.pca(adata)

sce.pp.harmony_integrate(adata, key="batch")
sc.pp.neighbors(adata, use_rep="X_pca_harmony")
sc.tl.umap(adata)
sc.tl.leiden(adata)
```

## 8. 参数解释

| 参数 | 作用 | 实用建议 |
|---|---|---|
| `group.by.vars` / `vars_use` | 指定要校正的协变量。 | 可以传多个变量，例如 `donor` 和 `chemistry`。 |
| `nclust` | Harmony 内部混合专家数量。 | 默认 `min(round(N / 30), 100)`；太小会接近简单线性回归。 |
| `theta` | 多样性惩罚。 | `theta=0` 等于不鼓励批次混合；过大可能过度混合。 |
| `sigma` | 软 k-means 宽度。 | 小值更接近硬聚类；大值让细胞分配更分散。 |
| `lambda` | 岭惩罚。 | 大值更保守，减少过度校正；小值校正更强。 |
| `max_iter` | 外层 Harmony 迭代次数。 | 默认通常够用；检查收敛曲线更稳。 |

## 9. 结果解释与质控

Harmony 的结果要同时看批次混合和生物学保留。论文提出 LISI 指标：iLISI 用于衡量局部邻域中的数据集混合程度，cLISI 用于衡量细胞类型是否被错误混合 [1]。直观检查时，可以画：

1. 按 `batch`、`donor`、`platform` 着色的 UMAP。
2. 按已知 `cell_type` 或经典标志基因着色的 UMAP。
3. 每个细胞群内不同批次的比例。
4. Harmony 前后 PCA/UMAP 对比。
5. 已知标志基因表达是否仍符合生物学预期。

如果批次看起来完全混合但标志基因/细胞类型也被混掉了，这不是好结果；如果细胞类型很清晰但批次仍分层，也说明校正不足或批次与生物学差异混杂。

## 10. 常见问题与风险

<div class="check-grid">
  <article>
    <strong>把 Harmony 当成校正后的表达矩阵</strong>
    <span>Harmony 输出的是低维表示。不要把它当作基因表达矩阵做标志基因或差异表达。</span>
  </article>
  <article>
    <strong>校正真实生物差异</strong>
    <span>如果批次与疾病分组完全混杂，任何整合方法都可能把真实差异当作批次去掉。</span>
  </article>
  <article>
    <strong>只看 UMAP</strong>
    <span>UMAP 好看不等于整合正确。需要结合标志基因、细胞群组成、已知生物学和定量指标。</span>
  </article>
  <article>
    <strong>前处理不一致</strong>
    <span>论文建议拼接数据后统一做 PCA，避免先对各批次做批次敏感的预处理再整合。</span>
  </article>
</div>

## 参考文献

[1] Korsunsky, I. et al. Fast, sensitive and accurate integration of single-cell data with Harmony. *Nature Methods* 16, 1289-1296 (2019). [Nature Methods](https://www.nature.com/articles/s41592-019-0619-0)

[2] Harmony GitHub repository. [immunogenomics/harmony](https://github.com/immunogenomics/harmony)

[3] LISI GitHub repository. [immunogenomics/LISI](https://github.com/immunogenomics/LISI)
