# scvi-tools 教程

scvi-tools 是 scverse 生态中的深度生成模型工具箱，常用于 batch integration、低维潜空间学习、差异表达、参考映射和多组学模型。它不是 Scanpy 的替代品，而是常接在 AnnData/Scanpy 预处理之后，用模型化方式处理批次和噪声。

官方 quick start 和 tutorials 的核心思路是：准备 AnnData，保留 raw counts，把 batch/covariate metadata 放进 obs，用 `setup_anndata()` 告诉模型数据在哪里，然后训练 `SCVI` 或其它模型。

<div class="path-grid">
  <a href="/tools/scvi-tools/integration-latent-space">
    <strong>整合与潜空间</strong>
    <span>学习 setup_anndata, SCVI model training, latent representation, neighbors, UMAP, and clustering。</span>
  </a>
  <a href="/tools/anndata/">
    <strong>AnnData 基础</strong>
    <span>理解 scvi-tools 为什么依赖 layers, obs, and raw counts。</span>
  </a>
  <a href="/tools/scanpy/">
    <strong>Scanpy 对接</strong>
    <span>用 Scanpy 做 QC 和可视化，用 scvi-tools 学 batch-corrected latent space。</span>
  </a>
  <a href="/references/">
    <strong>参考资料</strong>
    <span>查看 scvi-tools 官方文档、模型论文和实践教程。</span>
  </a>
</div>

## 什么时候使用

<div class="check-grid">
  <article>
    <strong>多样本整合</strong>
    <span>多个 donor, batch, chemistry, or condition 混在一起时，用潜变量模型学习共享空间。</span>
  </article>
  <article>
    <strong>参考映射</strong>
    <span>把新数据映射到已有 reference，减少每次从头注释的成本。</span>
  </article>
  <article>
    <strong>概率差异表达</strong>
    <span>用模型不确定性辅助 DE 判断，但仍需结合实验设计。</span>
  </article>
  <article>
    <strong>多组学模型</strong>
    <span>TOTALVI, MULTIVI 等模型可用于 RNA + protein 或 RNA + ATAC 数据。</span>
  </article>
</div>

## 资料来源

- [scvi-tools documentation](https://docs.scvi-tools.org/)
- [scvi-tools quick start](https://docs.scvi-tools.org/en/stable/tutorials/notebooks/quick_start/api_overview.html)
- [Single Cell Best Practices](https://www.sc-best-practices.org/)

