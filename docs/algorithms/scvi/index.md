# scVI

scVI，全称 single-cell variational inference（单细胞变分推断），是一个面向 scRNA-seq 计数数据的深度生成模型。它用 VAE 风格的层级贝叶斯模型，把每个细胞编码到低维潜空间，同时用 ZINB 或 NB 这类计数似然显式描述测序深度、过度离散、掉落事件和批次效应 [1]。

## 1. 算法基本信息

| 项目 | 内容 |
|---|---|
| 算法名称 | scVI |
| 论文标题 | Deep generative modeling for single-cell transcriptomics |
| 发表信息 | *Nature Methods*, 2018 |
| DOI | `10.1038/s41592-018-0229-2` |
| 论文原始仓库 | `https://github.com/YosefLab/scVI` |
| 当前主流实现 | `https://github.com/scverse/scvi-tools` |
| 任务类型 | 深度生成模型 / 降维 / 批次整合 / 差异表达 |
| 适用数据 | 基于 UMI 的 scRNA-seq 计数矩阵；AnnData/Scanpy 生态最常见 |
| 主要输出 | 潜在表示、归一化表达、后验预测样本、差异表达结果 |

## 2. 算法作用

scVI 的目标不是只做一个 UMAP 前的降维工具，而是用同一个概率模型服务多个任务：批次校正、可视化、聚类、归一化、表达插补和差异表达。论文的核心动机是：scRNA-seq 的技术噪声、文库大小差异、批次效应和掉落事件都会影响下游解释，因此最好把这些不确定性放进模型里，而不是每个任务换一套互不一致的经验方法 [1]。

与 Harmony 不同，scVI 直接以原始计数数据为主要输入，并学习一个生成模型；与普通自编码器不同，scVI 输出的是分布参数和后验不确定性，而不仅是一个确定性的低维表示。

<div class="doc-callout important">
  <strong>一句话理解</strong>
  <p>scVI 是“带计数似然的 VAE”：编码器把细胞压到潜空间，解码器从潜空间和批次信息生成每个基因的计数分布。</p>
</div>

## 3. 输入与输出

### 输入文件

| 输入 | 格式 | 形状/字段 | 必需 | 说明 |
|---|---|---|---|---|
| 计数矩阵 | `.h5ad`, `.loom`, `.mtx`, `.csv`, `.tsv` | 细胞 x 基因 | 是 | 推荐使用原始 UMI 计数。当前 `scvi-tools` 通常从 `adata.X` 或指定 `layer` 读取。 |
| 批次元数据 | `adata.obs` 列, `.csv`, `.tsv` | 细胞 x 1 | 可选 | 例如 `batch`, `donor`, `sample`, `chemistry`。 |
| 标签 | `adata.obs` 列 | 细胞 x 1 | 可选 | 可用于某些扩展模型或离散度设置。 |
| 分类协变量 | `adata.obs` 列 | 细胞 x 协变量 | 可选 | 当前实现支持额外分类协变量。 |
| 连续协变量 | `adata.obs` 列 | 细胞 x 协变量 | 可选 | 当前实现支持连续协变量。 |

### 输出文件

| 输出 | 格式 | 形状/字段 | 用途 |
|---|---|---|---|
| 潜在表示 | `adata.obsm["X_scVI"]`, `.npy`, `.csv` | 细胞 x 潜空间维度 | 邻居图、UMAP、聚类、批次整合 |
| 归一化表达 | DataFrame、矩阵、`.csv`、layer | 细胞 x 基因 | 去噪、归一化丰度、可视化 |
| 后验预测样本 | 张量/矩阵 | 细胞 x 基因 x 样本数 | 模型检查、模拟、不确定性分析 |
| 差异表达 | DataFrame、`.csv` | 基因 x 统计量 | 贝叶斯因子、概率、效应量 |
| 训练后的模型 | 目录/checkpoint | 模型权重 + 注册信息 | 复用、迁移学习、查询映射 |

## 4. 算法流程图

![scVI algorithm flow](/algorithms/scvi-flow.svg)

## 5. 模型结构详解

scVI 的核心是一个变分自编码器，但它的解码器不是普通均方误差重构，而是输出计数分布的参数。论文版本默认使用 ZINB，当前 `scvi-tools` 也支持 NB、Poisson 和实验性的正态似然。

### 5.1 生成模型

对细胞 `n` 和基因 `g`，scVI 假设观测计数 `x_ng` 来自一个由潜变量控制的计数分布：

```text
z_n ~ Normal(0, I)
l_n ~ LogNormal(batch-specific mean, batch-specific variance)
rho_n = decoder_expression(z_n, s_n)
pi_ng = decoder_dropout(z_n, s_n)
x_ng ~ ZINB(mean = l_n * rho_ng, dispersion = theta_g, dropout = pi_ng)
```

这里 `z_n` 是低维细胞状态，`l_n` 是文库大小或细胞特异性缩放因子，`s_n` 是批次/协变量。`rho_n` 可以理解为考虑批次后的归一化表达谱；`theta_g` 是基因特异性逆离散度；`pi_ng` 描述零膨胀/掉落事件。

### 5.2 编码器：近似后验

真实后验 `p(z, l | x, s)` 不可直接计算，所以 scVI 用编码器网络近似：

```text
q(z_n | x_n, s_n): Gaussian with diagonal covariance
q(l_n | x_n, s_n): LogNormal / observed library size
```

论文使用变分推断和重参数化技巧，让这个采样过程可以端到端反向传播。当前 `scvi-tools` 的 `VAE._regular_inference()` 中，主要流程是：

```text
x -> log1p(x) for encoder stability
x -> z_encoder -> qz, z
x -> l_encoder -> ql, library
```

当前默认 `use_observed_lib_size=True`，也就是文库大小常常直接取观测总 UMI 的对数，而不是像论文原始形式那样总是作为潜变量学习。

### 5.3 解码器：生成计数分布

解码器接收 `z`、批次/协变量和文库大小，输出：

| 代码变量 | 概念 | 说明 |
|---|---|---|
| `px_scale` | `rho` / 归一化表达 | 每个细胞内的基因比例或非负表达尺度。 |
| `px_r` | 逆离散度 | 可设置为基因、基因-批次、基因-标签或基因-细胞级别。 |
| `px_rate` | 计数均值 | 常见形式是文库大小乘以表达尺度。 |
| `px_dropout` | 零膨胀 logit | 使用 ZINB 似然时启用。 |

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
| `n_latent` | 潜空间维度。 | 论文常用 10；更复杂数据可增大，但不应只靠 UMAP 好看来判断。 |
| `n_hidden` | 每层隐藏单元数。 | 默认 128 常够用；大数据或复杂图谱可调高。 |
| `n_layers` | 编码器/解码器层数。 | 默认 1；更深模型表达力更强但更难训练和解释。 |
| `gene_likelihood` | 计数似然。 | 论文是 ZINB；现代 UMI 数据很多场景 NB 也常用。 |
| `dispersion` | 离散度共享方式。 | `gene` 最稳；批次差异明显可考虑 `gene-batch`。 |
| `batch_key` | 批次/协变量列。 | 用于考虑批次的生成模型和整合。 |
| `use_observed_lib_size` | 是否直接用观测文库大小。 | 当前默认 `True`，和论文原始设定略有差异。 |

## 9. 结果解释与质控

scVI 的潜空间可以用于批次整合、邻居图、UMAP 和聚类；归一化表达可用于表达可视化和模型化去噪；差异表达则基于生成模型后验比较表达差异。解释时要同时检查：

1. `X_scVI` 上 UMAP 是否保留已知细胞类型和标志基因。
2. 批次是否被合理混合，而不是把真实条件效应抹平。
3. reconstruction loss 和 validation loss 是否收敛。
4. 归一化表达是否用于适合的任务，不要把去噪结果当作无噪声真实表达。
5. 差异表达结果是否与原始计数、标志基因生物学和样本设计一致。

## 10. 常见问题与风险

<div class="check-grid">
  <article>
    <strong>输入不是原始计数</strong>
    <span>scVI 的似然函数面向计数数据。把对数归一化矩阵当计数输入会破坏模型假设。</span>
  </article>
  <article>
    <strong>批次与生物学分组完全混杂</strong>
    <span>如果疾病分组和批次一一对应，模型无法凭空区分技术效应和真实生物差异。</span>
  </article>
  <article>
    <strong>潜空间不可直接解释</strong>
    <span>scVI 潜空间维度通常不像 PCA 载荷那样可解释；需要用标志基因、差异表达和模型诊断辅助解释。</span>
  </article>
  <article>
    <strong>过度相信表达插补</strong>
    <span>插补/去噪表达是模型后验估计，不是直接观测值。用于可视化可以，强结论要回到实验设计和统计检验。</span>
  </article>
</div>

## 11. 和 Harmony 的关键区别

| 维度 | scVI | Harmony |
|---|---|---|
| 输入核心 | 原始计数矩阵 | PCA/细胞低维表示 |
| 模型类型 | 深度生成模型 / VAE | 迭代式低维表示校正 |
| 是否建模计数似然 | 是，ZINB/NB/Poisson | 否 |
| 批次处理 | 放入生成模型和解码器条件中 | 在低维表示空间中做线性校正 |
| 常见输出 | 潜空间、归一化表达、差异表达 | 校正后的低维表示 |
| 训练成本 | 通常更高，GPU 更友好 | 较轻量，常规 CPU 可用 |

## 参考文献

[1] Lopez, R. et al. Deep generative modeling for single-cell transcriptomics. *Nature Methods* 15, 1053-1058 (2018). [Nature Methods](https://www.nature.com/articles/s41592-018-0229-2)

[2] scVI original repository. [YosefLab/scVI](https://github.com/YosefLab/scVI)

[3] scvi-tools repository. [scverse/scvi-tools](https://github.com/scverse/scvi-tools)

[4] scvi-tools model documentation. [scVI user guide](https://docs.scvi-tools.org/en/stable/user_guide/models/scvi.html)
