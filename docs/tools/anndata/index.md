# AnnData 教程

AnnData 是 Python/scverse 生态里的核心数据容器。Scanpy、scvi-tools、Squidpy、Muon 等工具能顺畅协作，很大程度上是因为它们围绕 AnnData 或 AnnData-like 对象组织数据。

官方入门教程强调两个事实：AnnData 本质上是一个带注释的矩阵，行通常是观测对象/细胞，列通常是变量/基因；表达矩阵和元数据、降维结果、图结构、非结构化结果会被放在固定字段里。实践中，先学 AnnData 会比直接背 Scanpy 函数更稳。

<div class="scanpy-panel">
  <div>
    <span class="eyebrow">先学 AnnData</span>
    <h2>先理解容器，再理解流程</h2>
    <p>单细胞分析里很多“结果去哪了”的问题，本质都是 AnnData 字段问题。QC 指标通常进 obs，基因统计进 var，UMAP 坐标进 obsm，标志基因排名进 uns，原始计数可存 layers。</p>
  </div>
  <div class="metrics">
    <span>主矩阵 <strong>adata.X</strong></span>
    <span>细胞表 <strong>adata.obs</strong></span>
    <span>基因表 <strong>adata.var</strong></span>
    <span>多矩阵 <strong>adata.layers</strong></span>
    <span>低维坐标 <strong>adata.obsm</strong></span>
  </div>
</div>

## 推荐阅读顺序

<div class="path-grid">
  <a href="/tools/anndata/object-structure-io">
    <strong>对象结构与读写</strong>
    <span>理解 X、obs、var、layers、raw、obsm、varm、obsp 和 uns，并学会保存 h5ad。</span>
  </a>
  <a href="/tools/scanpy/">
    <strong>Scanpy 教程</strong>
    <span>把 AnnData 放入真实分析流程，看每一步结果写入哪些字段。</span>
  </a>
  <a href="/tools/scvi-tools/">
    <strong>scvi-tools 教程</strong>
    <span>理解 scvi-tools 为什么要求保留原始计数和批次/协变量元数据。</span>
  </a>
  <a href="/practice/raw-matrix-to-report">
    <strong>实战模板</strong>
    <span>查看本地流程如何在 layers、obs、obsm 和 uns 之间保存结果。</span>
  </a>
</div>

## 实践判断

<div class="doc-callout important">
  <strong>不要随意覆盖 counts</strong>
  <p>许多统计模型和整合方法需要原始计数。常见做法是把计数矩阵存在 <code>adata.layers["counts"]</code>，把归一化/对数转换后的矩阵用于常规可视化。</p>
</div>

## 资料来源

- [AnnData official documentation](https://anndata.readthedocs.io/)
- [AnnData getting started tutorial](https://anndata.readthedocs.io/en/stable/tutorials/notebooks/getting-started.html)
- [scverse ecosystem](https://scverse.org/)
