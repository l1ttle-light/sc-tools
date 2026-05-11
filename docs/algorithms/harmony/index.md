# Harmony

Harmony 是一个用于整合单细胞数据的无监督算法。它的核心思想很明确：不直接修改基因表达矩阵，而是在 PCA 等低维 embedding 上学习 batch/covariate correction，让细胞在低维空间中更多按生物状态聚集，而不是按实验批次、供体、测序平台或组织来源分开 [1]。

这篇页面基于论文 *Fast, sensitive and accurate integration of single-cell data with Harmony* 和官方 GitHub 仓库代码整理。

## 1. 算法基本信息

| 项目 | 内容 |
|---|---|
| 算法名称 | Harmony |
| 论文标题 | Fast, sensitive and accurate integration of single-cell data with Harmony |
| 发表信息 | *Nature Methods*, 2019 |
| DOI | `10.1038/s41592-019-0619-0` |
| GitHub 仓库 | `https://github.com/immunogenomics/harmony` |
| 任务类型 | batch integration / multi-dataset integration / covariate correction |
| 适用数据 | scRNA-seq low-dimensional embeddings; 论文也展示了跨模态整合场景 |
| 主要输出 | corrected embedding, usually stored as `harmony`, `X_harmony`, or `reducedDim(..., "HARMONY")` |

## 2. 算法作用

Harmony 解决的是“多个单细胞数据集放在一起时，低维空间被 batch/covariate 主导”的问题。它把输入的 PCA embedding 和细胞 metadata 作为输入，输出一个校正后的 embedding。后续的 nearest neighbors、UMAP、clustering、trajectory analysis 都应基于这个校正 embedding 运行。

它不输出 corrected counts，也不应该把 Harmony embedding 当作新的表达矩阵去做 gene-level differential expression。论文讨论里明确建议：差异表达这类问题应使用能显式处理 batch 的统计模型，例如包含 batch/covariate 的线性模型或混合效应模型 [1]。

<div class="doc-callout important">
  <strong>一句话理解</strong>
  <p>Harmony 做的是 embedding correction，不是 expression imputation。它让低维空间更适合联合聚类和可视化，但不创造新的基因表达值。</p>
</div>

## 3. 输入与输出

### 输入文件

| 输入 | 格式 | 形状/字段 | 必需 | 说明 |
|---|---|---|---|---|
| expression matrix | `.h5ad`, `.rds`, `.mtx`, `.loom`, `.csv`, `.tsv` | cells x genes | upstream | Harmony 通常不直接从 raw counts 开始，而是先归一化、找 HVG、PCA。 |
| PCA/cell embedding | matrix, `adata.obsm["X_pca"]`, Seurat `pca`, SCE `PCA` | cells x PCs | yes | 论文记作 `Z`，实现内部转成 `d x N`。 |
| cell metadata | `.csv`, `.tsv`, `adata.obs`, Seurat `meta.data`, SCE `colData` | cells x covariates | yes | 必须包含要校正的分类变量，例如 `batch`, `donor`, `platform`, `chemistry`。 |
| covariate list | string/list | column names | yes | R 接口为 `group.by.vars` 或 `vars_use`。 |

### 输出文件

| 输出 | 格式 | 形状/字段 | 用途 |
|---|---|---|---|
| corrected embedding | matrix, `adata.obsm["X_harmony"]`, Seurat reduction, SCE reducedDim | cells x PCs | downstream neighbors/UMAP/clustering |
| convergence trace | plot/data in object | objective values | 检查优化是否稳定。 |
| soft cluster assignment | R6 object field `R` when `return_object=TRUE` | clusters x cells | 解释每个细胞属于多个 cluster 的权重。 |
| co-occurrence statistics | R6 object fields `O`, `E` | clusters x batches | 理解 diversity penalty 的 observed/expected batch composition。 |

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
| `Z` | `Z_orig` | `d x N` | 原始 PCA/cell embedding。 |
| `Z_hat`, `Z_corr` | `Z_corr` | `d x N` | 当前校正后的 embedding。 |
| `Phi` | `Phi` | `B x N` | batch/covariate one-hot design matrix。 |
| `R` | `R` | `K x N` | soft cluster assignment，每个细胞可同时属于多个 cluster。 |
| `Y` | `Y` | `d x K` | cluster centroids。 |
| `O` | `O` | `K x B` | observed cluster-batch co-occurrence。 |
| `E` | `E` | `K x B` | expected co-occurrence under independence。 |
| `theta` | `theta` | per covariate level | 控制 batch diversity penalty 强度。 |
| `sigma` | `sigma` | per cluster | 控制 soft k-means 的软硬程度。 |
| `lambda` | `lambda` | per covariate level | ridge penalty，越大越保守，越不容易 over-correct。 |

### 5.2 第一步：maximum diversity clustering

Harmony 先在当前 embedding 上做 soft k-means。与普通 k-means 不同，`R` 是概率分配矩阵，而不是每个细胞只有一个硬标签。这样做的好处是保留连续状态，例如 differentiation trajectory 或 activation gradient。

论文在 soft k-means 的距离项之外加入 diversity penalty。直观上，如果某个 cluster 里某个 batch 明显过多，Harmony 会降低这个 batch 的细胞继续进入该 cluster 的概率；如果某个 batch 在该 cluster 中不足，则会提高它进入的机会。代码中对应：

```text
dist_mat = 2 * (1 - Y.t() * Z_corr)
E = sum(R, 1) * Pr_b.t()
O = R * Phi_t
Rcells = exp(-dist / sigma) * diversity_score
```

实际实现入口在 `src/harmony.cpp` 的 `cluster_cpp()` 和 `update_R()`。其中 `update_R()` 会分 block 更新细胞，先暂时移除一批细胞对 `O` 和 `E` 的贡献，再用新的 diversity score 更新这些细胞的 `R`，最后把它们加回统计量。

### 5.3 第二步：mixture-of-experts ridge correction

聚类后，Harmony 在每个 cluster 内估计 batch effect。这里可以理解为“每个 cluster 是一个 expert”，每个 expert 都学习一组 batch/covariate 的线性校正项；细胞最终的校正值是多个 experts 按 `R` 加权后的结果。

论文强调 correction step 使用原始 `Z` 估计校正，而不是持续在已经校正过的 `Z_corr` 上叠加回归。这样可以减少过度校正风险。代码中 `moe_correct_ridge_cpp()` 一开始就执行：

```text
Z_corr = Z_orig
```

随后对每个 cluster `k` 拟合 ridge regression：

```text
W_k = (Phi* diag(R_k) Phi*^T + lambda I)^-1 Phi* diag(R_k) Z_orig^T
```

其中 `Phi*` 是带 intercept 的 design matrix。实现里会保留 intercept，不从 embedding 中移除全局 cluster centroid，只移除 batch/covariate 相关项：

```text
Y.col(k) = W.row(0).t()
W.row(0).zeros()
Z_corr -= W.t() * Phi_Rk
```

### 5.4 收敛判断

Harmony 有两层收敛：clustering 内部用 k-means objective 的窗口变化判断；外层 harmonization 用 correction 前后的 objective 变化判断。R 层 `harmonize()` 每轮调用：

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
| 外层循环 | `R/utils.R` | 执行每轮 clustering 和 correction。 | `harmonize()` |
| C++ 对象定义 | `src/harmony.h` | 保存 `Z_orig`, `Z_corr`, `R`, `Y`, `O`, `E` 等核心状态。 | `class harmony` |
| 初始化与目标函数 | `src/harmony.cpp` | 初始化 centroids、计算 objective。 | `setup()`, `init_cluster_cpp()`, `compute_objective()` |
| 聚类 | `src/harmony.cpp` | soft k-means + diversity penalty。 | `cluster_cpp()`, `update_R()` |
| 校正 | `src/harmony.cpp` | mixture-of-experts ridge correction。 | `moe_correct_ridge_cpp()` |

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
| `group.by.vars` / `vars_use` | 指定要校正的 covariates。 | 可以传多个变量，例如 `donor` 和 `chemistry`。 |
| `nclust` | Harmony 内部 mixture experts 数量。 | 默认 `min(round(N / 30), 100)`；太小会接近简单线性回归。 |
| `theta` | diversity penalty。 | `theta=0` 等于不鼓励 batch mixing；过大可能过度混合。 |
| `sigma` | soft k-means width。 | 小值更接近 hard clustering；大值让细胞分配更分散。 |
| `lambda` | ridge penalty。 | 大值更保守，减少 over-correction；小值校正更强。 |
| `max_iter` | 外层 Harmony 迭代次数。 | 默认通常够用；检查 convergence plot 更稳。 |

## 9. 结果解释与质控

Harmony 的结果要同时看 batch mixing 和 biological conservation。论文提出 LISI 指标：iLISI 用于衡量局部邻域中 dataset mixing，cLISI 用于衡量 cell type 是否被错误混合 [1]。直观检查时，可以画：

1. UMAP colored by `batch`, `donor`, `platform`。
2. UMAP colored by known `cell_type` 或 canonical markers。
3. 每个 cluster 内不同 batch 的比例。
4. Harmony 前后 PCA/UMAP 对比。
5. known marker expression 是否仍符合生物学预期。

如果 batch 看起来完全混合但 marker/cell type 也被混掉了，这不是好结果；如果 cell type 很清晰但 batch 仍分层，也说明校正不足或 batch 与 biology confounded。

## 10. 常见问题与风险

<div class="check-grid">
  <article>
    <strong>把 Harmony 当 corrected expression</strong>
    <span>Harmony 输出的是 embedding。不要把它当作 gene expression matrix 做 marker gene 或 differential expression。</span>
  </article>
  <article>
    <strong>校正真实生物差异</strong>
    <span>如果 batch 与 disease group 完全混杂，任何 integration 方法都可能把真实差异当作 batch 去掉。</span>
  </article>
  <article>
    <strong>只看 UMAP</strong>
    <span>UMAP 好看不等于整合正确。需要结合 marker、cluster composition、known biology 和定量指标。</span>
  </article>
  <article>
    <strong>前处理不一致</strong>
    <span>论文建议拼接数据后统一做 PCA，避免先对各 batch 做 batch-sensitive preprocessing 再整合。</span>
  </article>
</div>

## 参考文献

[1] Korsunsky, I. et al. Fast, sensitive and accurate integration of single-cell data with Harmony. *Nature Methods* 16, 1289-1296 (2019). [Nature Methods](https://www.nature.com/articles/s41592-019-0619-0)

[2] Harmony GitHub repository. [immunogenomics/harmony](https://github.com/immunogenomics/harmony)

[3] LISI GitHub repository. [immunogenomics/LISI](https://github.com/immunogenomics/LISI)
