# scVI

scVI, single-cell variational inference, 是一个面向 scRNA-seq count data 的深度生成模型。它用 VAE 风格的层级贝叶斯模型，把每个细胞编码到低维潜空间，同时用 ZINB 或 NB 这类 count likelihood 显式描述测序深度、过度离散、dropout 和 batch effect [1]。

## 1. 算法基本信息

| 项目 | 内容 |
|---|---|
| 算法名称 | scVI |
| 论文标题 | Deep generative modeling for single-cell transcriptomics |
| 发表信息 | *Nature Methods*, 2018 |
| DOI | `10.1038/s41592-018-0229-2` |
| 论文原始仓库 | `https://github.com/YosefLab/scVI` |
| 当前主流实现 | `https://github.com/scverse/scvi-tools` |
| 任务类型 | deep generative model / dimensionality reduction / batch integration / differential expression |
| 适用数据 | UMI-based scRNA-seq count matrix; AnnData/Scanpy 生态最常见 |
| 主要输出 | latent representation, normalized expression, posterior predictive samples, differential expression result |

## 2. 算法作用

scVI 的目标不是只做一个 UMAP 前的降维工具，而是用同一个概率模型服务多个任务：batch correction、visualization、clustering、normalization、imputation 和 differential expression。论文的核心动机是：scRNA-seq 的技术噪声、library size 差异、batch effect 和 dropout 都会影响下游解释，因此最好把这些不确定性放进模型里，而不是每个任务换一套互不一致的经验方法 [1]。

与 Harmony 不同，scVI 直接以 raw count data 为主要输入，并学习一个生成模型；与普通 autoencoder 不同，scVI 输出的是分布参数和后验不确定性，而不仅是一个 deterministic embedding。

<div class="doc-callout important">
  <strong>一句话理解</strong>
  <p>scVI 是“带 count likelihood 的 VAE”：encoder 把细胞压到 latent space，decoder 从 latent space 和 batch 信息生成每个 gene 的 count 分布。</p>
</div>

## 3. 输入与输出

### 输入文件

| 输入 | 格式 | 形状/字段 | 必需 | 说明 |
|---|---|---|---|---|
| count matrix | `.h5ad`, `.loom`, `.mtx`, `.csv`, `.tsv` | cells x genes | yes | 推荐使用 raw UMI counts。当前 `scvi-tools` 通常从 `adata.X` 或指定 `layer` 读取。 |
| batch metadata | `adata.obs` column, `.csv`, `.tsv` | cells x 1 | optional | 例如 `batch`, `donor`, `sample`, `chemistry`。 |
| labels | `adata.obs` column | cells x 1 | optional | 可用于某些扩展模型或 dispersion 设置。 |
| categorical covariates | `adata.obs` columns | cells x covariates | optional | 当前实现支持额外分类协变量。 |
| continuous covariates | `adata.obs` columns | cells x covariates | optional | 当前实现支持连续协变量。 |

### 输出文件

| 输出 | 格式 | 形状/字段 | 用途 |
|---|---|---|---|
| latent representation | `adata.obsm["X_scVI"]`, `.npy`, `.csv` | cells x latent_dim | neighbors, UMAP, clustering, batch integration |
| normalized expression | DataFrame, matrix, `.csv`, layer | cells x genes | denoising, normalized abundance, visualization |
| posterior predictive samples | tensor/matrix | cells x genes x samples | model checking, simulation, uncertainty analysis |
| differential expression | DataFrame, `.csv` | genes x statistics | Bayes factor, probability, effect size |
| trained model | directory/checkpoint | model weights + registry | reuse, transfer learning, query mapping |

## 4. 算法流程图

![scVI algorithm flow](/algorithms/scvi-flow.svg)

## 5. 模型结构详解

scVI 的核心是一个变分自编码器，但它的 decoder 不是普通均方误差重构，而是输出 count distribution 的参数。论文版本默认使用 ZINB，当前 `scvi-tools` 也支持 NB、Poisson 和 experimental Normal likelihood。

### 5.1 生成模型

对细胞 `n` 和基因 `g`，scVI 假设观测 count `x_ng` 来自一个由潜变量控制的 count 分布：

```text
z_n ~ Normal(0, I)
l_n ~ LogNormal(batch-specific mean, batch-specific variance)
rho_n = decoder_expression(z_n, s_n)
pi_ng = decoder_dropout(z_n, s_n)
x_ng ~ ZINB(mean = l_n * rho_ng, dispersion = theta_g, dropout = pi_ng)
```

这里 `z_n` 是低维细胞状态，`l_n` 是 library size 或 cell-specific scaling factor，`s_n` 是 batch/covariate。`rho_n` 可以理解为 batch-aware 的 normalized expression profile；`theta_g` 是 gene-specific inverse dispersion；`pi_ng` 描述 zero inflation/dropout。

### 5.2 Encoder：近似后验

真实后验 `p(z, l | x, s)` 不可直接计算，所以 scVI 用 encoder 网络近似：

```text
q(z_n | x_n, s_n): Gaussian with diagonal covariance
q(l_n | x_n, s_n): LogNormal / observed library size
```

论文使用变分推断和 reparameterization trick，让这个采样过程可以端到端反向传播。当前 `scvi-tools` 的 `VAE._regular_inference()` 中，主要流程是：

```text
x -> log1p(x) for encoder stability
x -> z_encoder -> qz, z
x -> l_encoder -> ql, library
```

当前默认 `use_observed_lib_size=True`，也就是 library size 常常直接取观测总 UMI 的 log，而不是像论文原始形式那样总是作为潜变量学习。

### 5.3 Decoder：生成 count 分布

decoder 接收 `z`、batch/covariates 和 library size，输出：

| 代码变量 | 概念 | 说明 |
|---|---|---|
| `px_scale` | `rho` / normalized expression | 每个细胞内 gene proportion 或非负表达尺度。 |
| `px_r` | inverse dispersion | 可设置为 gene、gene-batch、gene-label 或 gene-cell 级别。 |
| `px_rate` | count mean | 常见形式是 library size 乘以 expression scale。 |
| `px_dropout` | zero-inflation logits | ZINB likelihood 时使用。 |

在当前代码 `VAE.generative()` 中，`gene_likelihood == "zinb"` 时会构造 `ZeroInflatedNegativeBinomial(mu=px_rate, theta=px_r, zi_logits=px_dropout)`；若设置为 `"nb"`，则构造 `NegativeBinomial(mu=px_rate, theta=px_r)`。

### 5.4 Loss：ELBO

scVI 最大化 ELBO，代码里等价地最小化：

```text
loss = reconstruction_loss + KL_z + KL_l
```

其中 reconstruction loss 是观测 count 在生成分布下的负 log likelihood；`KL_z` 约束 `q(z | x)` 不要偏离标准正态先验；`KL_l` 约束 library size posterior 不要偏离 batch-specific prior。当前 `VAE.loss()` 对应：

```text
reconst_loss = -px.log_prob(x)
kl_z = KL(qz, pz)
kl_l = KL(ql, pl)
loss = mean(reconst_loss + weighted_KL)
```

## 6. GitHub 代码阅读记录

| 模块 | 文件路径 | 作用 | 重点函数/类 |
|---|---|---|---|
| 高层模型 API | `src/scvi/model/_scvi.py` | 注册 AnnData、初始化 VAE、暴露 train/latent/DE 等接口。 | `SCVI`, `setup_anndata()` |
| VAE 核心模块 | `src/scvi/module/_vae.py` | 定义 encoder、decoder、likelihood 和 loss。 | `VAE`, `_regular_inference()`, `generative()`, `loss()` |
| Encoder/Decoder 组件 | `src/scvi/nn/_base_components.py` | MLP blocks、Encoder、DecoderSCVI。 | `Encoder`, `DecoderSCVI` |
| 训练框架 | `scvi-tools` training mixins and Lightning modules | mini-batch stochastic optimization。 | `model.train()` |
| 官方模型文档 | `docs/user_guide/models/scvi.md` | 当前 scVI 数学形式和 API 任务说明。 | generative process, inference, tasks |

## 7. 最小使用流程

```python
import scanpy as sc
import scvi

adata = sc.read_h5ad("data/raw/pbmc.h5ad")

scvi.model.SCVI.setup_anndata(
    adata,
    layer="counts",
    batch_key="batch"
)

model = scvi.model.SCVI(
    adata,
    n_latent=10,
    n_layers=1,
    n_hidden=128,
    gene_likelihood="zinb"
)
model.train()

adata.obsm["X_scVI"] = model.get_latent_representation()

sc.pp.neighbors(adata, use_rep="X_scVI")
sc.tl.umap(adata)
sc.tl.leiden(adata)

normalized = model.get_normalized_expression()
de = model.differential_expression(groupby="cell_type", group1="B cell")
```

## 8. 参数解释

| 参数 | 作用 | 实用建议 |
|---|---|---|
| `n_latent` | latent space 维度。 | 论文常用 10；更复杂数据可增大，但不应只靠 UMAP 好看来判断。 |
| `n_hidden` | 每层 hidden units。 | 默认 128 常够用；大数据或复杂 atlas 可调高。 |
| `n_layers` | encoder/decoder 层数。 | 默认 1；更深模型表达力更强但更难训练和解释。 |
| `gene_likelihood` | count likelihood。 | 论文是 ZINB；现代 UMI 数据很多场景 NB 也常用。 |
| `dispersion` | dispersion 共享方式。 | `gene` 最稳；batch 差异明显可考虑 `gene-batch`。 |
| `batch_key` | batch/covariate 列。 | 用于 batch-aware 生成模型和整合。 |
| `use_observed_lib_size` | 是否直接用观测 library size。 | 当前默认 `True`，和论文原始设定略有差异。 |

## 9. 结果解释与质控

scVI 的 latent space 可以用于 batch integration、neighbors、UMAP 和 clustering；normalized expression 可用于表达可视化和模型化的 denoising；differential expression 则基于生成模型后验比较表达差异。解释时要同时检查：

1. `X_scVI` 上 UMAP 是否保留已知 cell type 和 marker。
2. batch 是否被合理混合，而不是把真实 condition effect 抹平。
3. reconstruction loss 和 validation loss 是否收敛。
4. normalized expression 是否用于适合的任务，不要把 denoising 结果当作无噪声真实表达。
5. DE 结果是否与 raw counts、marker biology 和样本设计一致。

## 10. 常见问题与风险

<div class="check-grid">
  <article>
    <strong>输入不是 raw counts</strong>
    <span>scVI 的 likelihood 面向 count data。把 log-normalized matrix 当 counts 输入会破坏模型假设。</span>
  </article>
  <article>
    <strong>batch 与 biology 完全混杂</strong>
    <span>如果 disease group 和 batch 一一对应，模型无法凭空区分技术效应和真实生物差异。</span>
  </article>
  <article>
    <strong>latent space 不可直接解释</strong>
    <span>scVI latent dimensions 通常不像 PCA loading 那样可解释；需要用 marker、DE 和模型诊断辅助解释。</span>
  </article>
  <article>
    <strong>过度相信 imputation</strong>
    <span>imputed/denoised expression 是模型后验估计，不是直接观测值。用于可视化可以，强结论要回到实验设计和统计检验。</span>
  </article>
</div>

## 11. 和 Harmony 的关键区别

| 维度 | scVI | Harmony |
|---|---|---|
| 输入核心 | raw count matrix | PCA/cell embedding |
| 模型类型 | deep generative model / VAE | iterative embedding correction |
| 是否建模 count likelihood | yes, ZINB/NB/Poisson | no |
| batch 处理 | 放入生成模型和 decoder 条件中 | 在 embedding 空间中做线性校正 |
| 常见输出 | latent, normalized expression, DE | corrected embedding |
| 训练成本 | 通常更高，GPU 更友好 | 较轻量，常规 CPU 可用 |

## 参考文献

[1] Lopez, R. et al. Deep generative modeling for single-cell transcriptomics. *Nature Methods* 15, 1053-1058 (2018). [Nature Methods](https://www.nature.com/articles/s41592-018-0229-2)

[2] scVI original repository. [YosefLab/scVI](https://github.com/YosefLab/scVI)

[3] scvi-tools repository. [scverse/scvi-tools](https://github.com/scverse/scvi-tools)

[4] scvi-tools model documentation. [scVI user guide](https://docs.scvi-tools.org/en/stable/user_guide/models/scvi.html)
